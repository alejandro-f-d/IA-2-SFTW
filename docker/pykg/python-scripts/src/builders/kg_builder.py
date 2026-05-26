import os
import re
from typing import Optional
from rdflib import Graph, Literal, Namespace, RDF, URIRef, XSD
from rdflib.namespace import RDFS

from src.resolvers.resolution_chains import (
    resolve,
    PAPER_CHAINS, PERSON_CHAINS, ORG_CHAINS,
    _normalize_name,
)

NS   = Namespace("http://example.org/citation#")
BASE = Namespace("http://example.org/")
OA   = Namespace("https://openalex.org/")

def build_kg(papers: dict, globals_: dict, ontology_path: Optional[str] = None) -> Graph:
    g = Graph()
    g.bind("ns",   NS)
    g.bind("base", BASE)
    g.bind("oa",   OA)

    if ontology_path and os.path.exists(ontology_path):
        g.parse(ontology_path, format="turtle")
        print(f"  Ontología cargada: {ontology_path} ({len(g)} triples)")
    elif ontology_path:
        print(f"  [WARN] Ontología no encontrada en: {ontology_path}")

    ner_entities = globals_.get("ner_graph") or []
    if ner_entities:
        _build_ner(g, ner_entities)

    for paper_id, sources in papers.items():
        print(f"  Construyendo triples para: {paper_id}")
        _build_paper(g, paper_id, sources, globals_)

    _build_similarities(g, globals_.get("similarity", {}))

    return g


def save_kg(g: Graph, output_path: str) -> None:
    g.serialize(destination=output_path, format="turtle")
    print(f"KG guardado: {len(g)} triples → {output_path}")

def _build_paper(g: Graph, paper_id: str, sources: dict, globals_: dict) -> None:
    paper_uri = _paper_uri(paper_id)
    g.add((paper_uri, RDF.type, NS.Paper))

    _add_literal(g, paper_uri, NS.title,
                 resolve(PAPER_CHAINS["title"], sources), XSD.string)
    _add_literal(g, paper_uri, NS.doi,
                 resolve(PAPER_CHAINS["doi"], sources), XSD.string)
    _add_literal(g, paper_uri, NS.abstract,
                 resolve(PAPER_CHAINS["abstract"], sources), XSD.string)
    _add_literal(g, paper_uri, NS.open_alex_id,
                 resolve(PAPER_CHAINS["open_alex_id"], sources), XSD.string)

    year = resolve(PAPER_CHAINS["year"], sources)
    if year:
        g.add((paper_uri, NS.publication_year, Literal(str(year), datatype=XSD.gYear)))

    citations = resolve(PAPER_CHAINS["citation_count"], sources)
    if citations is not None:
        g.add((paper_uri, NS.citation_count, Literal(int(citations), datatype=XSD.integer)))

    keywords = resolve(PAPER_CHAINS["keywords"], sources)
    for kw in (keywords or []):
        if kw and kw.strip():
            g.add((paper_uri, NS.keyword, Literal(kw.strip(), datatype=XSD.string)))

    for person in (sources.get("people") or []):
        _build_person(g, paper_uri, sources, person)

    _build_topics(g, paper_uri, paper_id, sources, globals_)

    for cited_id in ((sources.get("openalex") or {}).get("cited_by_openalex_ids") or []):
        cited_uri = _safe_uri(str(OA), _oa_local(cited_id))
        g.add((cited_uri, RDF.type, NS.Paper))
        g.add((paper_uri, NS.cites, cited_uri))

def _build_person(g: Graph, paper_uri: URIRef, sources: dict, person: dict) -> None:
    person_uri = _person_uri(person)
    g.add((person_uri, RDF.type, NS.Person))
    g.add((paper_uri, NS.hasAuthor, person_uri))

    _add_literal(g, person_uri, NS.name,
                 resolve(PERSON_CHAINS["name"], sources, person=person), XSD.string)
    _add_literal(g, person_uri, NS.orcid,
                 resolve(PERSON_CHAINS["orcid"], sources, person=person), XSD.string)
    _add_literal(g, person_uri, NS.email,
                 resolve(PERSON_CHAINS["email"], sources, person=person), XSD.string)
    _add_literal(g, person_uri, NS.wikidata_qid,
                 resolve(PERSON_CHAINS["wikidata_qid"], sources, person=person), XSD.string)

    for afil in (person.get("afiliaciones") or []):
        _build_org(g, person_uri, sources, person, afil)


def _build_org(g: Graph, person_uri: URIRef, sources: dict,
               person: dict, org: dict) -> None:
    org_name = resolve(ORG_CHAINS["name"], sources, org=org, person=person)
    if not org_name:
        return

    org_uri = _org_uri(org_name)
    g.add((org_uri, RDF.type, NS.Organization))
    g.add((person_uri, NS.affiliated_with, org_uri))

    g.add((org_uri, RDFS.label, Literal(org_name, datatype=XSD.string)))

    _add_literal(g, org_uri, NS.country,
                 resolve(ORG_CHAINS["country"], sources, org=org, person=person), XSD.string)
    _add_literal(g, org_uri, NS.rorId,
                 resolve(ORG_CHAINS["ror_id"], sources, org=org, person=person), XSD.string)

def _build_topics(g: Graph, paper_uri: URIRef, paper_id: str,
                  sources: dict, globals_: dict) -> None:
    paper_topics = globals_.get("paper_topics", {})
    topics_info  = globals_.get("topics", {})

    topic_id = _find_paper_topic(paper_id, paper_topics)

    if topic_id is not None:
        topic_data = topics_info.get(str(topic_id), {})
        topic_uri  = URIRef(f"{BASE}topic/{topic_id}")
        g.add((topic_uri, RDF.type, NS.Topic))

        label = topic_data.get("label")
        if label:
            g.add((topic_uri, NS.topicLabel, Literal(label, datatype=XSD.string)))
        for word in (topic_data.get("keywords") or []):
            if word.strip():
                g.add((topic_uri, NS.topicWord, Literal(word.strip(), datatype=XSD.string)))

        assignment_uri = URIRef(f"{BASE}assignment/{_safe_local(paper_id)}__topic{topic_id}")
        g.add((assignment_uri, RDF.type, NS.TopicAssignment))
        g.add((assignment_uri, NS.assignedTopic, topic_uri))
        g.add((paper_uri, NS.belongs_to_topic, assignment_uri))

    if topic_id is None:
        for concept in ((sources.get("openalex") or {}).get("concepts") or []):
            cid  = concept.get("open_alex_concept_id")
            name = concept.get("display_name")
            score = concept.get("score")
            if not cid or not name:
                continue
            topic_uri = _safe_uri(str(OA), _oa_local(cid))
            g.add((topic_uri, RDF.type, NS.Topic))
            g.add((topic_uri, NS.topicLabel, Literal(name, datatype=XSD.string)))

            assignment_uri = URIRef(
                f"{BASE}assignment/{_safe_local(paper_id)}__{_oa_local(cid)}")
            g.add((assignment_uri, RDF.type, NS.TopicAssignment))
            g.add((assignment_uri, NS.assignedTopic, topic_uri))
            g.add((paper_uri, NS.belongs_to_topic, assignment_uri))
            if score is not None:
                g.add((assignment_uri, NS.probability,
                       Literal(float(score), datatype=XSD.float)))

def _build_similarities(g: Graph, similarity: dict) -> None:
    for paper_key, similar_list in similarity.items():
        paper_id  = paper_key.replace("_abstract", "")
        paper_uri = _paper_uri(paper_id)
        g.add((paper_uri, RDF.type, NS.Paper))

        for sim_entry in (similar_list or []):
            other_key   = sim_entry.get("paper", "").replace("_abstract", "")
            score       = sim_entry.get("score")
            other_uri   = _paper_uri(other_key)
            g.add((other_uri, RDF.type, NS.Paper))

            stmt_uri = URIRef(
                f"{BASE}similarity/{_safe_local(paper_id)}__{_safe_local(other_key)}")
            g.add((stmt_uri, RDF.type, NS.SimilarityStatement))
            g.add((paper_uri, NS.similar_to, stmt_uri))
            if score is not None:
                g.add((stmt_uri, NS.similarityScore,
                       Literal(float(score), datatype=XSD.float)))

def _paper_uri(paper_id: str) -> URIRef:
    return URIRef(f"{BASE}paper/{_safe_local(paper_id)}")

def _person_uri(person: dict) -> URIRef:
    orcid = person.get("orcid")
    if orcid:
        return URIRef(f"{BASE}person/{_safe_local(orcid)}")
    name = _safe_local(person.get("nombre_completo", "unknown"))
    return URIRef(f"{BASE}person/{name}")

def _org_uri(org_name: str) -> URIRef:
    return URIRef(f"{BASE}organization/{_safe_local(org_name)}")

def _safe_local(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_\-]", "_", value)

def _safe_uri(base: str, local: str) -> URIRef:
    return URIRef(f"{base}{_safe_local(local)}")

def _oa_local(oa_id: str) -> str:
    return oa_id.rstrip("/").split("/")[-1]

def _find_paper_topic(paper_id: str, paper_topics: dict):
    if paper_id in paper_topics:
        return paper_topics[paper_id]
    key_abstract = f"{paper_id}_abstract"
    if key_abstract in paper_topics:
        return paper_topics[key_abstract]
    return None

def _add_literal(g: Graph, subject: URIRef, predicate: URIRef,
                 value, datatype) -> None:
    if value is not None and value != "":
        g.add((subject, predicate, Literal(value, datatype=datatype)))

_NER_TYPE_MAP = {
    "http://ia-practica-2.org/Paper":        NS.Paper,
    "http://ia-practica-2.org/Person":       NS.Person,
    "http://ia-practica-2.org/Organization": NS.Organization,
    "http://ia-practica-2.org/Project":      NS.Project,
    "http://ia-practica-2.org/Location":     None,  
}

_NER_PROP_MAP = {
    "http://ia-practica-2.org/acknowledges": NS.acknowledges,
    "http://ia-practica-2.org/hasProject":   NS.isFundedBy,
    "http://www.w3.org/2000/01/rdf-schema#label": RDFS.label,
}


def _build_ner(g: Graph, entities: list) -> None:
    for entity in entities:
        entity_id  = entity.get("@id")
        entity_types = entity.get("@type") or []
        if not entity_id:
            continue

        subject = URIRef(entity_id)

        for t in entity_types:
            ns_class = _NER_TYPE_MAP.get(t)
            if ns_class:
                g.add((subject, RDF.type, ns_class))

        for json_prop, values in entity.items():
            if json_prop in ("@id", "@type"):
                continue
            onto_prop = _NER_PROP_MAP.get(json_prop)
            if not onto_prop:
                continue
            for val in (values or []):
                if "@id" in val:
                    g.add((subject, onto_prop, URIRef(val["@id"])))
                elif "@value" in val:
                    g.add((subject, onto_prop, Literal(val["@value"], datatype=XSD.string)))