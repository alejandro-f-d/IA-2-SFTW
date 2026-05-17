from src.execute_query.executor import atacar_wikidata
import os 
OUTPUT_DIR = os.getenv('OUTPUT_DIR', '/output')

def main():    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    query = """
    SELECT ?cityLabel ?population WHERE {
    ?city wdt:P31 wd:Q515;       # Instancia de: Ciudad
            wdt:P17 wd:Q29;        # País: España
            wdt:P1082 ?population. # Propiedad: Población
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],es,en". }
    }
    ORDER BY DESC(?population)
    LIMIT 5
    """
    resultado = atacar_wikidata(query)
    print(resultado)
if __name__ == "__main__":
    main()

