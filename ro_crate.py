from rocrate.rocrate import ROCrate
from rocrate.model.person import Person
from rocrate.model.softwareapplication import SoftwareApplication
from datetime import date
import os
import json


AUTORES = [
    {
        "orcid": "https://orcid.org/0009-0006-7735-3981",
        "name": "Juan Sebastian Torres Alvarez",
    },
    {
        "orcid": "https://orcid.org/0009-0007-0060-7856",
        "name": "Alejandro Fisac Delgado",
    },
    {
        "orcid": "https://orcid.org/0009-0006-9847-8038",
        "name": "Andrés Voronovskyy Knyshayid",
    },
    {
        "orcid": "https://orcid.org/0009-0009-5754-3026",
        "name": "Janele Ángeles Sandonas Feliz",
    },
]

OUTPUT_DIR = "./ro-crate-output"


crate = ROCrate()

crate.name = "Food Waste Paper Similarity Knowledge Graph"
crate.description = (
    "Pipeline for analyzing 30 research papers on food waste. "
    "Extracts structured data via Grobid (XML), enriches metadata "
    "with ORCID, Wikidata and OpenAlex APIs, computes semantic "
    "similarity scores and topic modeling (BERTopic + KeyBERT), "
    "and builds a Knowledge Graph in Turtle format."
)
crate.root_dataset["version"] = "1.0.0"
crate.root_dataset["license"] = "https://creativecommons.org/licenses/by/4.0/"
crate.root_dataset["datePublished"] = date.today().isoformat()
crate.root_dataset["keywords"] = "food waste, knowledge graph, topic modeling, semantic similarity, BERTopic, Grobid, ORCID, Wikidata, OpenAlex, RDF, Turtle"

upm = crate.add_jsonld({

    "@id": "https://www.upm.es",
    "@type": "Organization",
    "name": "Universidad Politécnica de Madrid",
    "url": "https://www.upm.es"
})

autores_entities = []
for autor in AUTORES:
    p = crate.add(Person(crate, autor["orcid"], properties={
        "name": autor["name"],
        "affiliation": {"@id": "https://www.upm.es"}
    }))
    autores_entities.append(p)

crate.creator = autores_entities

# DOCUMENTACIÓN DEL PROYECTO (raíz)
crate.add_file("README.md", properties={
    "name": "Project README",
    "description": "General documentation and instructions for the project",
    "encodingFormat": "text/markdown"
})

crate.add_file("ontology.png", properties={
    "name": "Citation Ontology Diagram",
    "description": "Visual diagram of the ontology used in the Knowledge Graph (ns:Paper, ns:Person, ns:Organization, ns:Topic, ns:Project, ns:SimilarityStatement)",
    "encodingFormat": "image/png"
})

crate.add_file("use_case.md", properties={
    "name": "Use Cases",
    "description": "Description of the use cases covered by the system",
    "encodingFormat": "text/markdown"
})

crate.add_file("selected_apis_sparql.md", properties={
    "name": "API and SPARQL selection rationale",
    "description": "Justification for the selected external APIs and SPARQL endpoints",
    "encodingFormat": "text/markdown"
})

# ORQUESTACIÓN: docker-compose
crate.add_file("docker/docker-compose.yml", properties={
    "name": "Docker Compose workflow",
    "description": (
        "Orchestrates the full pipeline: grobid → python-xml → python-data "
        "→ python-clustering / python-orcid → python-wikidata"
    ),
    "encodingFormat": "application/yaml"
})

# MÓDULO 1: pygrobid — PDF → XML
crate.add_dataset("docker/pygrobid/", properties={
    "name": "pygrobid module",
    "description": "Sends PDFs to Grobid API and collects structured XML output",
    "programmingLanguage": {"@id": "https://www.python.org/"},
})

crate.add_dataset("docker/pygrobid/input/", properties={
    "name": "Input PDFs",
    "description": "30 research papers on food waste in PDF format (paper0.pdf … paper29.pdf)",
    "encodingFormat": "application/pdf"
})

crate.add_dataset("docker/pygrobid/output/", properties={
    "name": "Grobid XML output",
    "description": "Structured XML files extracted from PDFs by Grobid (paper0.xml … paper29.xml)",
    "encodingFormat": "application/xml"
})

# MÓDULO 2: pyextractdata — XML → structured data
crate.add_dataset("docker/pyextractdata/", properties={
    "name": "pyextractdata module",
    "description": "Parses Grobid XML and extracts abstracts, DOIs, authors, acknowledgements and builds initial Knowledge Graph",
    "programmingLanguage": {"@id": "https://www.python.org/"},
})

crate.add_dataset("docker/pyextractdata/output/", properties={
    "name": "Extracted structured data",
    "description": (
        "Per-paper text files: *_abstract.txt, *_doi.txt, *_people.txt, *_ack.txt. "
        "Also includes knowledge_graph.ttl — the initial RDF Knowledge Graph in Turtle format."
    ),
})

crate.add_file("docker/pyextractdata/output/knowledge_graph.ttl", properties={
    "name": "Knowledge Graph (Turtle)",
    "description": "Initial RDF Knowledge Graph with paper metadata, authors and organizations in Turtle format",
    "encodingFormat": "text/turtle"
})

# MÓDULO 3: pyorcid — Author enrichment
crate.add_dataset("docker/pyorcid/", properties={
    "name": "pyorcid module",
    "description": "Queries the ORCID API to enrich author metadata for papers where ORCID IDs are available",
    "programmingLanguage": {"@id": "https://www.python.org/"},
})

crate.add_dataset("docker/pyorcid/output/", properties={
    "name": "ORCID enrichment output",
    "description": "JSON files with enriched author data from ORCID (9 papers matched: paper7, 8, 10, 23, 24, 25, 27, 28, 29)",
    "encodingFormat": "application/json"
})

# MÓDULO 4: pywikidata — Organization enrichment
crate.add_dataset("docker/pywikidata/", properties={
    "name": "pywikidata module",
    "description": "Queries Wikidata SPARQL endpoint to enrich organization metadata linked to paper authors",
    "programmingLanguage": {"@id": "https://www.python.org/"},
})

crate.add_dataset("docker/pywikidata/output/", properties={
    "name": "Wikidata enrichment output",
    "description": "JSON files with enriched organization data from Wikidata (paper17, paper19)",
    "encodingFormat": "application/json"
})

# MÓDULO 5: pyopenalex — Paper metadata enrichment
crate.add_dataset("docker/pyopenalex/", properties={
    "name": "pyopenalex module",
    "description": "Queries OpenAlex API by DOI or title to enrich paper metadata (citation count, keywords, open_alex_id)",
    "programmingLanguage": {"@id": "https://www.python.org/"},
})

crate.add_dataset("docker/pyopenalex/output/", properties={
    "name": "OpenAlex enrichment output",
    "description": "JSON files with enriched paper metadata from OpenAlex (24 papers matched)",
    "encodingFormat": "application/json"
})

# MÓDULO 6: pyclustering — Similarity + Topic Modeling
crate.add_dataset("docker/pyclustering/", properties={
    "name": "pyclustering module",
    "description": (
        "Computes semantic similarity between paper abstracts using sentence-transformers "
        "and cosine similarity. Performs topic modeling with BERTopic (UMAP + HDBSCAN) "
        "and generates human-readable topic labels with KeyBERT."
    ),
    "programmingLanguage": {"@id": "https://www.python.org/"},
})

# Resultados de clustering
for filename, description in [
    ("similarity.json",
     "Top-5 most similar papers per paper based on abstract cosine similarity (sentence-transformers all-MiniLM-L6-v2)"),
    ("topics.json",
     "BERTopic clusters with KeyBERT-generated labels and top keywords per topic"),
    ("paper_topics.json",
     "Topic assignment (cluster ID) for each of the 30 papers"),
    ("paper_topic_distribution.json",
     "Probability distribution (%) of each paper belonging to each topic cluster"),
]:
    crate.add_file(f"docker/pyclustering/output/{filename}", properties={
        "name": filename,
        "description": description,
        "encodingFormat": "application/json"
    })

# SERVICIOS EXTERNOS
crate.add_jsonld({
    "@id": "https://github.com/kermitt2/grobid",
    "@type": "SoftwareApplication",
    "name": "Grobid 0.8.2",
    "description": "Machine learning library for extracting structured data from PDF documents",
    "url": "https://github.com/kermitt2/grobid",
    "version": "0.8.2"
})

crate.add_jsonld({
    "@id": "https://orcid.org/",
    "@type": "WebAPI",
    "name": "ORCID API",
    "description": "Persistent digital identifier for researchers; used to enrich author metadata",
    "url": "https://orcid.org/"
})

crate.add_jsonld({
    "@id": "https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service",
    "@type": "WebAPI",
    "name": "Wikidata SPARQL Endpoint",
    "description": "Knowledge base queried via SPARQL to enrich organization metadata",
    "url": "https://query.wikidata.org/"
})

crate.add_jsonld({
    "@id": "https://api.openalex.org/",
    "@type": "WebAPI",
    "name": "OpenAlex API",
    "description": "Open scholarly graph queried by DOI/title for paper citation count, keywords and open_alex_id",
    "url": "https://api.openalex.org/"
})

crate.add_jsonld({
    "@id": "https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2",
    "@type": "SoftwareApplication",
    "name": "all-MiniLM-L6-v2",
    "description": "Sentence transformer model used for generating paper abstract embeddings",
    "url": "https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2"
})

crate.add_jsonld({
    "@id": "https://huggingface.co/Jean-Baptiste/roberta-large-ner-english",
    "@type": "SoftwareApplication",
    "name": "roberta-large-ner-english",
    "description": "NER model used for obtaining data from acknowledgements",
    "url": "https://huggingface.co/Jean-Baptiste/roberta-large-ner-english"
})

# GUARDAR
os.makedirs(OUTPUT_DIR, exist_ok=True)
metadata_path = os.path.join(OUTPUT_DIR, "ro-crate-metadata.json")

with open(metadata_path, "w", encoding="utf-8") as f:
    json.dump(crate.metadata.generate(), f, indent=2, ensure_ascii=False)

print(f"RO-Crate generado en: {metadata_path}")