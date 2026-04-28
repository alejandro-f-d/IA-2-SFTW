# Use Case
Este proyecto sirve para explorar un conjunto de papers y hacerse una idea rápida de qué autores aparecen como más influyentes dentro de ese grupo.
A partir de los artículos, se extraen las referencias y se observa quién cita a quién para detectar qué nombres se repiten más o tienen mayor peso.
Para sacar la información de los PDFs se usa GROBID, y luego se mejoran los datos enlazando autores con identificadores externos cuando es posible.
Para eso se tiran consultas a Wikidata y ORCID.
Con todo eso se acaba construyendo una red de citaciones entre autores que permite ver patrones interesantes sin necesidad de entrar en análisis demasiado complejos.

# Licencia
MIT
