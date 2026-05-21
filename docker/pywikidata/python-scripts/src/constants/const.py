URL_SCHOOLAR = "https://query-scholarly.wikidata.org/sparql"
URL_WIKIDATA = "https://query.wikidata.org/sparql"

WIKIDATA_DOI_QUERY_TEMPLATE = """
SELECT ?item ?title ?doi 
       ?date ?journalLabel ?volume ?pages 
       (GROUP_CONCAT(DISTINCT ?keywordLabel; SEPARATOR=", ") AS ?keywords)
WHERE {{
  ?item wdt:P356 "{doi}" .
  
  OPTIONAL {{ ?item wdt:P1476 ?title }}       
  OPTIONAL {{ ?item wdt:P356 ?doi }}                
  OPTIONAL {{ ?item wdt:P577 ?date }}         
  OPTIONAL {{ ?item wdt:P1433 ?journal }}     
  OPTIONAL {{ ?item wdt:P478 ?volume }}       
  OPTIONAL {{ ?item wdt:P304 ?pages }}        
  OPTIONAL {{ ?item wdt:P921 ?keyword }}      

  SERVICE wikibase:label {{ 
    bd:serviceParam wikibase:language "[AUTO_LANGUAGE],es,en". 
    ?keyword rdfs:label ?keywordLabel .
    ?journal rdfs:label ?journalLabel .
  }}
}}
GROUP BY ?item ?title ?doi ?date ?journalLabel ?volume ?pages
"""

WIKIDATA_CITAS = """
SELECT (COUNT(?citante) AS ?numeroDeCitas) WHERE {{
  ?citante wdt:P2860 <{item_uri}>. 
}}
"""

WIKIDATA_OBTENER_DOI = """
SELECT ?item ?doi WHERE {{
  ?item wdt:P31 wd:Q13442814 ;
        wdt:P1476 "{doi}"@en ;
        wdt:P356 ?doi .
}}
"""
