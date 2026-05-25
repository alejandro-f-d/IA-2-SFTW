from src.login.login import login
import os
from src.extract_information.extract_by_id import info_orcid_by_id 
from src.process_output.processator import get_employment_information, get_publication_information, get_researcher_information
import json
from dataclasses import asdict

INPUT_DIR = os.getenv('INPUT_DIR', '/input') 
OUTPUT_DIR = os.getenv('OUTPUT_DIR', '/output')

def main():    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    token = login()
    if not token:
        print("No se pudo iniciar sesión en ORCID. Abortando pipeline.")
        return

    files = [f for f in os.listdir(INPUT_DIR) if f.endswith('_people.txt')]
    if not files:
        print("No se encontraron ficheros.")
        return

    for filename in files:
        file_path = os.path.join(INPUT_DIR, filename)
        print(f"Se empieza a analizar {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                personas = json.load(f)
        except json.JSONDecodeError:
            print(f"Error: El archivo {filename} no tiene un formato JSON válido.")
            continue
        except Exception as e:
            print(f"Error al procesar {filename}: {e}")
            continue

        autores = []

        for persona in personas:
            orcid = persona.get('orcid')
            nombre_autor = persona.get('nombre_completo', 'Desconocido')

            if not orcid:
                print(f"No se ha encontrado orcid para: {nombre_autor}, se omite.")
                continue

            print(f"Autor: {nombre_autor} -> ORCID: {orcid}")
            json_info_completa = info_orcid_by_id(orcid, token)

            if json_info_completa is None:
                print(f"ORCID no devolvió datos para: {nombre_autor}, se omite.")
                continue

            informacion_researcher = get_researcher_information(json_info_completa)
            informacion_empresa = get_employment_information(json_info_completa)
            informacion_publicaciones = get_publication_information(json_info_completa)

            autores.append({
                "nombre_completo": nombre_autor,
                "orcid": orcid,
                "investigador": asdict(informacion_researcher) if informacion_researcher else None,
                "empleo": [asdict(emp) for emp in informacion_empresa],
                "publicaciones": [asdict(pub) for pub in informacion_publicaciones]
            })
            print(f"Información procesada para {nombre_autor}")

        if not autores:
            print(f"No se encontraron autores con datos para {filename}, se omite el fichero de salida.")
            continue

        resultado_paper = {"autores": autores}
        output_filename = filename.replace('_people.txt', '_processed_orcid.json')
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        with open(output_path, 'w', encoding='utf-8') as f_out:
            json.dump(resultado_paper, f_out, indent=4, ensure_ascii=False)

        print(f"Paper procesado: {output_filename} ({len(autores)} autores)")

if __name__ == "__main__":
    main()
