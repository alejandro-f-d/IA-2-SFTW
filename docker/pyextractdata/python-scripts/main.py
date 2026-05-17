import os
from src.save.save import save_content
from src.extract.extract_abstract import extract_abstract
from src.extract.extract_ack import extract_ack
from src.extract.extract_people import extract_people
from src.extract.extract_title_doi import extract_title_doi 
import json

INPUT_DIR = os.getenv('INPUT_DIR', '/input') 
OUTPUT_DIR = os.getenv('OUTPUT_DIR', '/output')

def main():

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    files = [f for f in os.listdir(INPUT_DIR) if f.endswith('.xml')] # Obtenemos todos los ficheros xml.
    if not files:
        print(f"No hay XMLs en ese directorio. {INPUT_DIR}")
        return
    print(f"Se han encontrado: {len(files)} xmls")

    for filename in files:
        xml_path = os.path.join(INPUT_DIR, filename)
        print(f"Empezamos a procesar: {filename}")
        abstract_data = extract_abstract(xml_path)
        if abstract_data:
            abstract_file_name = filename.replace('.xml', '_abstract.txt')
            save_path = os.path.join(OUTPUT_DIR, abstract_file_name)
            save_content(abstract_data, save_path)

        else:
            print(f"Fallo al generar el abstract de: {filename}")
        ack_data = extract_ack(xml_path)
        if ack_data:
            ack_file_name = filename.replace('.xml', '_ack.txt')
            save_path = os.path.join(OUTPUT_DIR, ack_file_name)
            save_content(ack_data, save_path)
        else: 
            print(f"Fallo al generar el ack de: {filename}")
        people_data = extract_people(xml_path)
        if people_data:
            people_file_name = filename.replace('.xml', '_people.txt')
            save_path = os.path.join(OUTPUT_DIR, people_file_name)
            save_content(people_data, save_path)
        else: 
            print(f"Fallo al generar los autores de: {filename}")
        doi_data = extract_title_doi(xml_path)
        if doi_data:
            doi_file_name = filename.replace('.xml', '_doi.txt')
            save_path = os.path.join(OUTPUT_DIR, doi_file_name)
            texto_a_guardar = json.dumps(doi_data, ensure_ascii=False, indent=4)
            save_content(texto_a_guardar, save_path)
        else: 
            print(f"Fallo al obtener el doi de: {filename}")

if __name__ == "__main__":
    main()
