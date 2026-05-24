import os
import json
from rdflib import Graph

def load_all(input_dir: str) -> dict:
    papers = {}

    extract_dir  = os.path.join(input_dir, "extract")
    orcid_dir    = os.path.join(input_dir, "orcid")
    wikidata_dir = os.path.join(input_dir, "wikidata")
    openalex_dir = os.path.join(input_dir, "openalex")

    if os.path.exists(extract_dir):
        for f in os.listdir(extract_dir):
            path = os.path.join(extract_dir, f)
            if f.endswith("_doi.txt"):
                paper_id = f.replace("_doi.txt", "")
                _get_or_create(papers, paper_id)["doi_data"] = _load_json(path)
            elif f.endswith("_abstract.txt"):
                paper_id = f.replace("_abstract.txt", "")
                _get_or_create(papers, paper_id)["abstract"] = _load_text(path)
            elif f.endswith("_people.txt"):
                paper_id = f.replace("_people.txt", "")
                _get_or_create(papers, paper_id)["people"] = _load_json(path)

    if os.path.exists(orcid_dir):
        for f in os.listdir(orcid_dir):
            if not f.endswith("_processed_orcid.json"):
                continue
            base = f.replace("_processed_orcid.json", "")
            if len(base) > 19 and base[-19:].count("-") == 3:
                paper_id = base[:-20]
            else:
                paper_id = base
            orcid_data = _load_json(os.path.join(orcid_dir, f))
            if orcid_data:
                _get_or_create(papers, paper_id)["orcid_authors"].append(orcid_data)

    if os.path.exists(wikidata_dir):
        for f in os.listdir(wikidata_dir):
            if f.endswith("_processed_wikidata.json"):
                paper_id = f.replace("_processed_wikidata.json", "")
                _get_or_create(papers, paper_id)["wikidata"] = _load_json(
                    os.path.join(wikidata_dir, f))

    if os.path.exists(openalex_dir):
        for f in os.listdir(openalex_dir):
            if f.endswith("_openalex.json"):
                paper_id = f.replace("_openalex.json", "")
                _get_or_create(papers, paper_id)["openalex"] = _load_json(
                    os.path.join(openalex_dir, f))

    return papers


def load_globals(input_dir: str) -> dict:
    result = {
        "ner_graph":    None,
        "paper_topics": {},
        "topics":       {},
        "similarity":   {},
    }

    ttl_path = os.path.join(input_dir, "extract", "knowledge_graph.ttl")
    if os.path.exists(ttl_path):
        g = Graph()
        g.parse(ttl_path, format="turtle")
        result["ner_graph"] = g
        print(f"  knowledge_graph.ttl cargado: {len(g)} triples")

    clustering_dir = os.path.join(input_dir, "clustering")
    for key, filename in [
        ("paper_topics", "paper_topics.json"),
        ("topics",       "topics.json"),
        ("similarity",   "similarity.json"),
    ]:
        path = os.path.join(clustering_dir, filename)
        if os.path.exists(path):
            result[key] = _load_json(path) or {}

    return result

def _get_or_create(papers: dict, paper_id: str) -> dict:
    if paper_id not in papers:
        papers[paper_id] = {
            "doi_data":      None,
            "abstract":      None,
            "people":        None,
            "orcid_authors": [],
            "openalex":      None,
            "wikidata":      None,
        }
    return papers[paper_id]


def _load_json(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"  [WARN] No se pudo cargar JSON {path}: {e}")
        return None


def _load_text(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception as e:
        print(f"  [WARN] No se pudo cargar texto {path}: {e}")
        return None