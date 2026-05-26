# PyKG

Este módulo construye el **Knowledge Graph final** en formato Turtle (`.ttl`) combinando y enriqueciendo la información generada por todos los pipelines anteriores (`pyextractdata`, `pyclustering`, `pyorcid`, `pywikidata`, `pyopenalex`). Toma como base la ontología `citation_ontology.ttl` y aplica una cadena de prioridad por propiedad para rellenar cada campo con la fuente más fiable disponible.


## Variables de entorno

| Variable | Descripción | Valor por defecto |
|---|---|---|
| `INPUT_DIR` | Directorio raíz con los subdirectorios de entrada | `/input` |
| `OUTPUT_DIR` | Directorio donde se guarda el grafo final | `/output` |
| `ONTOLOGY_PATH` | Ruta al fichero `citation_ontology.ttl` | `/ontology/citation_ontology.ttl` |


## Volúmenes

| Ruta en el contenedor | Descripción |
|---|---|
| `/input/extract` | Ficheros `_doi.txt`, `_abstract.txt`, `_people.txt` y `knowledge_graph.json` generados por `pyextractdata` |
| `/input/clustering` | Ficheros `paper_topics.json`, `topics.json` y `similarity.json` generados por `pyclustering` |
| `/input/orcid` | JSONs `_processed_orcid.json` generados por `pyorcid` |
| `/input/wikidata` | JSONs `_processed_wikidata.json` generados por `pywikidata` |
| `/input/openalex` | JSONs `_openalex.json` generados por `pyopenalex` |
| `/output` | Knowledge Graph final generado |
| `/ontology` | Fichero `citation_ontology.ttl` |


## Ficheros de entrada y salida

| Entrada | Salida |
|---|---|
| `<paper>_doi.txt` | `knowledge_graph_final.ttl` |
| `<paper>_abstract.txt` | |
| `<paper>_people.txt` | |
| `knowledge_graph.json` | |
| `paper_topics.json` | |
| `topics.json` | |
| `similarity.json` | |
| `<paper>_processed_orcid.json` | |
| `<paper>_processed_wikidata.json` | |
| `<paper>_openalex.json` | |

Se genera un **único fichero de salida** con todos los papers procesados.


## Prioridad de fuentes por clase

El builder aplica una cadena de resolución declarativa: para cada propiedad recorre las fuentes en orden y usa el primer valor no nulo disponible.

| Clase | Prioridad |
|---|---|
| `ns:Paper` / `ns:Project` | Extracción propia → Wikidata → OpenAlex |
| `ns:Person` / `ns:Organization` | Extracción propia → ORCID → OpenAlex |
| `ns:Topic` / `ns:SimilarityStatement` | Clustering propio → OpenAlex |


## Estructura del JSON de salida

El módulo no produce JSON intermedio, directamente serializa el grafo en Turtle:

```turtle
@prefix ns: <http://example.org/citation#> .

<http://example.org/paper/s12911-024-02531-1>
    a ns:Paper ;
    ns:title "Protein sequence analysis in the context of drug repurposing" ;
    ns:doi "10.1186/s12911-024-02531-1" ;
    ns:hasAuthor <http://example.org/person/0000-0001-8801-4762> .
```


## Comportamiento ante errores

| Situación | Comportamiento |
|---|---|
| Ontología no encontrada | Log de aviso, continúa sin ontología base |
| No hay ficheros de entrada | Termina sin error, notifica por consola |
| Fichero JSON malformado | Log del error, se omite ese fichero |
| Paper sin ninguna fuente disponible | Se omite del grafo |
| Propiedad sin valor en ninguna fuente | El triple no se emite |


## Ejecución en nativo

```bash
# Creación del entorno:
python -m venv .venv
# Activación del entorno:
source .venv/bin/activate
# Instalación de los requirements:
pip install -r requirements.txt
# Movimiento a la carpeta del main:
cd ./python-scripts/
# Creación de variables de entorno:
export INPUT_DIR=../input
export OUTPUT_DIR=../output
export ONTOLOGY_PATH=../../ontology/citation_ontology.ttl
python main.py
```

| Variable | Descripción |
|---|---|
| `INPUT_DIR` | Directorio raíz con los subdirectorios `extract`, `clustering`, `orcid`, `wikidata`, `openalex` |
| `OUTPUT_DIR` | Directorio donde se guarda `knowledge_graph_final.ttl` |
| `ONTOLOGY_PATH` | Ruta local al fichero `citation_ontology.ttl` |
