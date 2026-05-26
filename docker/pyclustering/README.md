# PyClustering

Este módulo calcula la **similitud semántica** entre los abstracts de los papers del corpus y realiza **topic modeling** para agruparlos por temáticas. Toma como input los ficheros `_abstract.txt` generados por `pyextractdata` y produce cuatro JSONs con los scores de similitud, los topics detectados, la asignación de cada paper a un topic y la distribución de probabilidad de pertenencia a cada cluster.


## Variables de entorno

| Variable | Descripción | Valor por defecto |
|---|---|---|
| `INPUT_DIR` | Directorio con los ficheros `_abstract.txt` de entrada | `/input` |
| `OUTPUT_DIR` | Directorio donde se guardan los resultados | `/output` |

## Volúmenes

| Ruta en el contenedor | Descripción |
|---|---|
| `/input` | Ficheros `_abstract.txt` generados por `pyextractdata` |
| `/output` | JSONs con los resultados de similitud y topic modeling |


## Ficheros de entrada y salida

| Entrada | Salida |
|---|---|
| `<paper>_abstract.txt` | `similarity.json` |
| | `topics.json` |
| | `paper_topics.json` |
| | `paper_topic_distribution.json` |

Se genera **un único conjunto de ficheros de salida** con la información agregada de todos los papers del corpus.

### Estructura de los JSONs de salida

#### `similarity.json`
Contiene los 5 papers más similares para cada paper, ordenados por score descendente. La similitud se calcula como la similitud coseno entre los embeddings de los abstracts generados con el modelo `all-MiniLM-L6-v2`.

```json
{
    "paper0_abstract": [
        {"paper": "paper5_abstract", "score": 0.91},
        {"paper": "paper12_abstract", "score": 0.87},
        {"paper": "paper3_abstract", "score": 0.84},
        {"paper": "paper19_abstract", "score": 0.81},
        {"paper": "paper7_abstract", "score": 0.78}
    ]
}
```

#### `topics.json`
Contiene los clusters detectados por BERTopic con su etiqueta generada por KeyBERT y las keywords más representativas.

```json
{
    "0": {
        "label": "food waste reduction strategies",
        "keywords": ["flw", "reducing", "circular", "model", "environmental", "chain", "linear", "use", "find", "amount"]
    },
    "1": {
        "label": "hotel restaurant management",
        "keywords": ["hotels", "buffet", "restaurants", "management", "practices", "star", "costs", "restaurant", "processes", "five"]
    }
}
```

#### `paper_topics.json`
Contiene el topic asignado a cada paper. El valor `-1` indica que el paper fue clasificado como outlier (no encaja en ningún cluster).

```json
{
    "paper0_abstract": 2,
    "paper1_abstract": 0,
    "paper2_abstract": -1
}
```

#### `paper_topic_distribution.json`
Contiene la distribución de probabilidad (en %) de pertenencia de cada paper a cada uno de los topics detectados.

```json
{
    "paper0_abstract": {
        "0": 72.34,
        "1": 15.21,
        "2": 8.10,
        "3": 4.35
    }
}
```


## Modelos utilizados

| Modelo | Uso | Fuente |
|---|---|---|
| `all-MiniLM-L6-v2` | Generación de embeddings para similitud y clustering | [HuggingFace](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) |
| `BERTopic` (UMAP + HDBSCAN) | Topic modeling | [BERTopic](https://maartengr.github.io/BERTopic/) |
| `KeyBERT` | Generación de etiquetas legibles por topic | [KeyBERT](https://maartengr.github.io/KeyBERT/) |

### Justificación de parámetros

BERTopic utiliza por defecto parámetros pensados para corpus grandes. Con 30 papers es necesario ajustarlos:

| Parámetro | Valor | Motivo |
|---|---|---|
| `n_neighbors` (UMAP) | `5` | El valor por defecto (15) requiere más documentos que los disponibles |
| `min_cluster_size` (HDBSCAN) | `2` | El valor por defecto (10) impide formar clusters con corpus pequeños |
| `min_samples` (HDBSCAN) | `1` | Reduce la restricción de outliers en corpus pequeños |
| `calculate_probabilities` | `True` | Necesario para obtener la distribución completa por topic |


## Comportamiento ante errores

| Situación | Comportamiento |
|---|---|
| No hay ficheros `_abstract.txt` en `/input` | Lanza `ValueError` y termina con código de error |
| Todos los papers clasificados como outlier (`-1`) | Log informativo, los resultados se guardan igualmente |
| Error en la generación de embeddings | Excepción propagada, termina con código de error |


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
python main.py
```

| Variable | Descripción |
|---|---|
| `INPUT_DIR` | Directorio con los `_abstract.txt` a procesar |
| `OUTPUT_DIR` | Directorio donde se guardan los JSONs generados |