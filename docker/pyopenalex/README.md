# PyOpenAlex

Este módulo consulta la **API de OpenAlex** para obtener información enriquecida de los papers identificados en el pipeline. Toma como input los ficheros `_doi.txt` generados por `pyextractdata` e intenta recuperar cada paper primero por DOI y, si no está disponible, por título. Produce un JSON por paper con información del trabajo, sus autores, conceptos y referencias.


## Variables de entorno

| Variable | Descripción | Valor por defecto |
|---|---|---|
| `INPUT_DIR` | Directorio con los ficheros `_doi.txt` de entrada | `/input` |
| `OUTPUT_DIR` | Directorio donde se guardan los resultados | `/output` |
| `OPENALEX_EMAIL` | E-mail para el polite pool de OpenAlex (recomendado) | — |
| `OPENALEX_BASE_URL` | URL base de la API de OpenAlex | `https://api.openalex.org` |

> `OPENALEX_EMAIL` no es obligatorio pero se recomienda incluirlo para beneficiarse del polite pool de OpenAlex, que ofrece mayor rate limit y prioridad en las peticiones.


## Volúmenes

| Ruta en el contenedor | Descripción |
|---|---|
| `/input` | Ficheros `_doi.txt` generados por `pyextractdata` |
| `/output` | JSONs con la información de cada paper extraída de OpenAlex |


## Ficheros de entrada y salida

| Entrada | Salida |
|---|---|
| `<paper>_doi.txt` | `<paper>_openalex.json` |

El fichero de entrada es un JSON con los campos `doi` y `title`. Se genera **un fichero de salida por paper** siempre que OpenAlex devuelva resultados, ya sea por DOI o por título.

### Estructura del JSON de salida

```json
{
    "paper": {
        "open_alex_id": "https://openalex.org/W...",
        "title": "...",
        "doi": "https://doi.org/...",
        "publication_year": 2021,
        "citation_count": 12,
        "abstract": "...",
        "keywords": ["...", "..."]
    },
    "authors": [
        {
            "open_alex_author_id": "https://openalex.org/A...",
            "name": "...",
            "orcid": "0000-0000-0000-0000",
            "wikidata_qid": null,
            "institutions": [
                {
                    "open_alex_inst_id": "https://openalex.org/I...",
                    "name": "...",
                    "ror_id": "https://ror.org/...",
                    "country": "ES"
                }
            ]
        }
    ],
    "concepts": [
        {
            "open_alex_concept_id": "https://openalex.org/C...",
            "display_name": "...",
            "score": 0.86,
            "level": 2
        }
    ],
    "cited_by_openalex_ids": [
        "https://openalex.org/W...",
        "..."
    ]
}
```


## Comportamiento ante errores

| Situación | Comportamiento |
|---|---|
| No hay ficheros `_doi.txt` en `/input` | Termina sin error, notifica por consola |
| Fichero JSON malformado | Log del error, continúa con el siguiente fichero |
| DOI no disponible | Intenta búsqueda por título como fallback |
| OpenAlex no devuelve resultados | Log informativo, se omite el fichero de salida |
| Error HTTP en la petición | Log del error con detalles, se omite el fichero de salida |


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
export INPUT_DIR=../../pyextractdata/output
export OUTPUT_DIR=../output
export OPENALEX_EMAIL=tu@email.com
python main.py
```

| Variable | Descripción |
|---|---|
| `INPUT_DIR` | Directorio con los `_doi.txt` a procesar |
| `OUTPUT_DIR` | Directorio donde se guardan los JSONs generados |
| `OPENALEX_EMAIL` | E-mail para el polite pool de OpenAlex |
