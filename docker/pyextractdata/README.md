TODO: Poner la parte del name entity recognition.

# PyExtractData

Este módulo recibe como input los XML generados por `pygrobid` y extrae la información de cada paper. Adicionalmente, ejecuta un proceso de Named Entity Recognition .... 


## Flujo de ejecución:

![flujo-ejecucion](./flujo-ejecucion.png)

Cada extracción es autónoma e independiente: si una falla para un documento concreto, se notifica por consola y el proceso continúa con las demás extracciones del mismo fichero.



## Variables de entorno:

| Variable | Descripción | Valor por defecto |
|---|---|---|
| `INPUT_DIR` | Directorio con los XML de entrada | `/input` |
| `OUTPUT_DIR` | Directorio donde se guardan los ficheros de salida | `/output` |


## Volúmenes:

| Ruta en el contenedor | Descripción |
|---|---|
| `/input` | XML generados por `pygrobid` |
| `/output` | Ficheros extraídos y grafo de conocimiento |


## Ficheros de salida:

Por cada XML de entrada se generan hasta cuatro ficheros de texto y, al finalizar el loop, un fichero JSON global:

| Fichero | Contenido |
|---|---|
| `<paper>_abstract.txt` | Texto del abstract |
| `<paper>_ack.txt` | Texto de los agradecimientos |
| `<paper>_people.txt` | Autores y personas del documento en formato JSON |
| `<paper>_doi.txt` | Título y DOI en formato JSON |


## Ejecución en nativo y test:

### Ejecución nativa:
En caso de querer la ejecución en nativo se deben establecer diferentes variables de entorno (p.e. con un export). Además de instalar los requirements presentes en `./requirements.txt`.
```bash
# Creación del entorno:
python -m venv .venv
# Activación del entorno:
source .venv/bin/activate
# Instalación de los requirements:
pip install -r requirements.txt
# Movimiento a la carpeta del main
cd ./python-scripts/
# Creación de variables de entorno:
export INPUT_DIR=../../pygrobid/output
export OUTPUT_DIR=../output
python main.py
# En caso de tener error de CUDA OUT OF MEMORY:
CUDA_VISIBLE_DEVICES="" python main.py
```
| Ruta en el contenedor | Descripción |
|---|---|
| `INPUT_DIR` | Directorio con los XML a procesar |
| `OUTPUT_DIR` | Directorio donde se guardan los output generados |
### Ejecución test:
Una vez se tenga el entorno con las dependencias iremos a la carpeta `./python-scripts/tests/` y ejecutaremos:
```bash
cd ./python-scripts/tests/
pytest .
```
