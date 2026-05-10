Las fuentes externas utilizadas para enriquecer el grafo son Wikidata, ORCID y OpenAlex.
En el caso de Wikidata, se accede mediante consultas SPARQL, lo que permite recuperar información estructurada sobre los autores,
como afiliaciones, áreas de conocimiento o relaciones con otras entidades. Esto ayuda a contextualizar mejor a los autores dentro del grafo y a ampliar las conexiones más allá de las citaciones directas.
Por otro lado, ORCID se utiliza a través de su API REST, centrada en la identificación única de investigadores. A partir de ORCID se pueden obtener identificadores persistentes y, en algunos casos, metadatos adicionales como variantes de nombre o historial académico.
Finalmente, OpenAlex se utiliza como fuente de información académica para recuperar metadatos relacionados con publicaciones científicas, autores e instituciones. A través de su API REST es posible obtener información estructurada sobre artículos, palabras clave, afiliaciones y relaciones entre trabajos científicos, lo que resulta útil para calcular métricas de similitud.

