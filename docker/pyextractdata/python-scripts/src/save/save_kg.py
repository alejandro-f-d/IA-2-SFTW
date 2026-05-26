from rdflib import Graph, Literal, URIRef, Namespace
from rdflib.namespace import RDF, RDFS

# Namespace base para todas las URIs del proyecto
EX = Namespace("http://ia-practica-2.org/")

def build_kg(papers_data, topics_info):
    """
    Construye un grafo RDF con los datos extraídos de los papers.
    Incluye entidades NER, topics y similitud entre papers.
    """
    g = Graph()
    g.bind("ex", EX)

    # Añadimos los topics como entidades
    for topic_id, topic_data in topics_info.items():
        topic_uri = URIRef(EX + f"topic/{topic_id}")
        g.add((topic_uri, RDF.type, EX.Topic))
        g.add((topic_uri, RDFS.label, Literal(topic_data["label"])))

    for paper in papers_data:
        print(f"Paper: {paper['paper_id']} - Topic: {paper.get('topic')} - Similar: {paper.get('similar_to')}")
        paper_uri = URIRef(EX + f"paper/{paper['paper_id']}")
        # Declaramos que es un Paper
        g.add((paper_uri, RDF.type, EX.Paper))

        # Añadimos el título del paper
        if paper.get("title"):
            g.add((paper_uri, EX.title, Literal(paper["title"])))

        # Añadimos belongs_to_topic
        topic_id = paper.get("topic", -1)
        if topic_id != -1:
            topic_uri = URIRef(EX + f"topic/{topic_id}")
            g.add((paper_uri, EX.belongs_to_topic, topic_uri))

        # Añadimos similar_to con umbral de 0.6
        for sim in paper.get("similar_to", []):
            if sim["score"] >= 0.6:
                other_paper_id = sim["paper"].replace("_abstract", "")
                other_uri = URIRef(EX + f"paper/{other_paper_id}")
                g.add((paper_uri, EX.similar_to, other_uri))
                g.add((paper_uri, EX.similarity_score, Literal(round(sim["score"], 2))))

        # Añadimos las personas detectadas
        for nombre in paper["personas"]:
            uri = URIRef(EX + f"person/{nombre.replace(' ', '_')}")
            g.add((uri, RDF.type, EX.Person))
            g.add((uri, RDFS.label, Literal(nombre)))
            g.add((uri, EX.name, Literal(nombre)))
            g.add((paper_uri, EX.acknowledges, uri))

        # Añadimos las organizaciones detectadas
        for nombre in paper["organizaciones"]:
            uri = URIRef(EX + f"organization/{nombre.replace(' ', '_')}")
            g.add((uri, RDF.type, EX.Organization))
            g.add((uri, RDFS.label, Literal(nombre)))
            g.add((uri, EX.name, Literal(nombre)))
            g.add((paper_uri, EX.acknowledges, uri))

        # Añadimos los lugares detectados
        for nombre in paper["lugares"]:
            uri = URIRef(EX + f"location/{nombre.replace(' ', '_')}")
            g.add((uri, RDF.type, EX.Location))
            g.add((uri, RDFS.label, Literal(nombre)))
            g.add((paper_uri, EX.acknowledges, uri))

        # Añadimos los IDs de proyectos detectados
        for pid in paper["project_ids"]:
            uri = URIRef(EX + f"project/{pid.replace(' ', '_').replace('#', '')}")
            g.add((uri, RDF.type, EX.Project))
            g.add((uri, RDFS.label, Literal(pid)))
            g.add((paper_uri, EX.hasProject, uri))

    return g


def save_kg(g, output_path):
   
    g.serialize(output_path, format="json-ld")
    print(f"KG guardado en: {output_path}")
