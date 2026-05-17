from src.execute_query.executor import atacar_wikidata_doi
import os 
import json

OUTPUT_DIR = os.getenv('OUTPUT_DIR', '/output')
INPUT_DIR = os.getenv('INPUT_DIR', '/input') 

def main():    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    files = [f for f in os.listdir(INPUT_DIR) if f.endswith('_doi.txt')] # Obtenemos los títulos y el doi del paper.
    if not files:
        print("No se encontraron ficheros.")
        return

    for filename in files:
        file_path = os.path.join(INPUT_DIR, filename)
        print(f"Se empieza a analizar {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error al leer el archivo {filename}: {e}")
            continue

        titulo = data.get('titulo', None)
        doi = data.get('doi', None)
        resultado = None
        if doi is not None:
            # Ejecutar la estructura de querys en base al doi.
            resultado = atacar_wikidata_doi(doi)
        elif titulo is not None:
            continue
            # Ejecutar las querys en base al título.
        else: 
            print(f"El {filename} no tiene título ni DOI.")
            continue

        output_filename = filename.replace('_doi.txt', '_processed_wikidata.json')
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        if resultado and resultado != None:
            with open(output_path, 'w', encoding='utf-8') as f_out:
                json.dump(resultado, f_out, indent=4, ensure_ascii=False)
        print(f"Información procesada para {filename}")



if __name__ == "__main__":
    main()

