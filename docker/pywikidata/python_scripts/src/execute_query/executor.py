import requests
import os
URL_WIKI = os.getenv('URL_WIKI', 'https://query.wikidata.org/sparql')

def atacar_wikidata(query):
    headers = {
        "User-Agent": "WikidataExtractInformation",
        "Accept": "application/json"
    }
    response = requests.get(URL_WIKI, params={'query': query}, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")

