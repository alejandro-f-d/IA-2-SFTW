import requests
from src.constants.const import URL_WIKIDATA, URL_SCHOOLAR, WIKIDATA_DOI_QUERY_TEMPLATE, WIKIDATA_CITAS

def atacar_wikidata(query, url):
    url_exec = None
    if url == 1:
        url_exec = URL_WIKIDATA
    else: 
        url_exec = URL_SCHOOLAR

    headers = {
        "User-Agent": "WikidataExtractInformation",
        "Accept": "application/json"
    }
    response = requests.get(url_exec, params={'query': query}, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")

def obtener_citas_por_uri(item_uri):

    query_citas = WIKIDATA_CITAS.format(item_uri=item_uri)
    resultado = atacar_wikidata(query_citas, url=2) 
    
    if resultado:
        bindings = resultado.get('results', {}).get('bindings', [])
        if bindings:
            return bindings[0].get('numeroDeCitas', {}).get('value', '0')
    return '0'


def atacar_wikidata_doi(doi_buscar):

    query_wikidata_ejecutar_doi = WIKIDATA_DOI_QUERY_TEMPLATE.format(doi=doi_buscar) 
    resultado_query_info_general_doi = atacar_wikidata(query_wikidata_ejecutar_doi, url=2)
    
    if not resultado_query_info_general_doi:
        return {}

    bindings = resultado_query_info_general_doi.get('results', {}).get('bindings', [])
    
    if not bindings:
        print(f"No se encontraron resultados para el DOI: {doi_buscar}")
        return {}

    coincidencia = bindings[0]
    
    item_uri = coincidencia.get('item', {}).get('value', 'No disponible')
    titulo   = coincidencia.get('title', {}).get('value', 'No disponible')
    doi      = coincidencia.get('doi', {}).get('value', 'No disponible')
    fecha    = coincidencia.get('date', {}).get('value', 'No disponible')
    volumen  = coincidencia.get('volume', {}).get('value', 'No disponible')
    revista  = coincidencia.get('journalLabel', {}).get('value', 'No disponible')
    pages    = coincidencia.get('pages', {}).get('value', 'No disponible')
    keywords = coincidencia.get('keywords', {}).get('value', 'No disponible')
    
    numero_citas = "0"
    if item_uri != 'No disponible':
        numero_citas = obtener_citas_por_uri(item_uri)

    resultado_final = {
        "item_uri": item_uri,
        "titulo": titulo,
        "doi": doi,
        "fecha": fecha,
        "volumen": volumen,
        "paginas": pages,
        "revista": revista,
        "keywords": [k.strip() for k in keywords.split(",")] if keywords != 'No disponible' else [],
        "numero_de_citas": int(numero_citas)
    }

    print(f"El resultado final {resultado_final}")
    return resultado_final
