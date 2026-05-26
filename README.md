# Práctica 2: Inteligencia Artificial en Software Abierto

[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[[![DOI](https://zenodo.org/badge/1156519336.svg)]()](https://doi.org/10.5281/zenodo.20402705)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

El pipeline comienza con el tratamiento de artículos científicos en formato PDF, los cuales son procesados mediante GROBID para su estructuración en archivos XML. A partir de estos documentos, se realiza una extracción de metadatos y datos relevantes que posteriormente se introducen en la librería py-clustering para la agrupación por tópicos y cálculo de la similitud de papers. Una vez generados estos clústeres, los datos se enriquecen mediante consultas a las APIs de ORCID, Wikidata y OpenAlex. Con la información, se modela y construye el grafo de conocimiento utilizando pykg, el cual se despliega en Apache Jena Fuseki para habilitar un endpoint SPARQL. Finalmente, la validez del sistema se demuestra mediante el desarrollo de una aplicación web de prueba como caso de uso.
Para las instrucciones de ejecución están presentes en el [README](./docker/README.md) de la carpeta docker.

### Referencias de herramientas utilizadas:

GROBID contributors. (2008--2026). GROBID. https://github.com/kermitt2/grobid
Garijo, D., & Montero, A. RSFC: Research Software Fairness Checks (Version 0.1.2) [Computer software]. https://github.com/oeg-upm/rsfc
Grobid 0.8.2 — Machine learning library for extracting structured data from PDF documents.
ORCID API — Persistent digital identifier for researchers; used to enrich author metadata.
Wikidata SPARQL Endpoint — Knowledge base queried via SPARQL to enrich organization metadata.
OpenAlex API — Open scholarly graph queried by DOI/title for paper citation count, keywords and OpenAlex ID.
all-MiniLM-L6-v2 — Sentence transformer model used for generating paper abstract embeddings.
roberta-large-ner-english — NER model used for extracting data from acknowledgements.


### Contacto:
Cualquier problema con el software abrir una issue. 
