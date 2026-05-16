from src.login.login import login
import os
from src.extract_information.extract_by_id import info_orcid_by_id 
from src.process_output.processator import  get_employment_information, get_publication_information, get_researcher_information
import json

INPUT_DIR = os.getenv('INPUT_DIR', '/input') 
OUTPUT_DIR = os.getenv('OUTPUT_DIR', '/output')

def main():    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    token = login()
    if token:
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)

        # Lo primero es ir iterando sobre los ficheros y los json.
        files = [f for f in os.listdir(INPUT_DIR) if f.endswith('_people.txt')] # Obtenemos la lista de ficheros que sean de personas. 
        if not files:
            print("No se encontraron ficheros.")
            return
        for filename in files: 
            file_path = os.path.join(INPUT_DIR, filename)
            print(f"Se empieza a analizar {file_path}")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    personas = json.load(f)
                    for persona in personas:
                        orcid = persona.get('orcid')
                        nombre_autor = persona.get('nombre_completo', 'Desconocido')
                        if orcid:
                            print(f"Autor: {nombre_autor} -> ORCID: {orcid}")
                            json_info_completa = info_orcid_by_id(orcid, token)
                            if json_info_completa is not None:  
                                informacion_researcher = get_researcher_information(json_info_completa)
                                informacion_empresa = get_employment_information(json_info_completa)
                                informacion_publicaciones = get_publication_information(json_info_completa)
                                # Diccionario para contener el resultado.
                                resultado_investigador = {
                                    "investigador": informacion_researcher,
                                    "empleo": informacion_empresa,
                                    "publicaciones": informacion_publicaciones
                                }
                                output_filename = filename.replace('_people.txt', '_processed_orcid.json')
                                output_path = os.path.join(OUTPUT_DIR, output_filename)
                                with open(output_path, 'w', encoding='utf-8') as f_out:
                                    json.dump(resultado_investigador, f_out, indent=4, ensure_ascii=False)
                                print(f"Información procesada para {nombre_autor}, {filename}")
                        else: 
                            print(f"No se ha encontrado orcid para: {nombre_autor}")
                            
            except json.JSONDecodeError:
                print(f"Error: El archivo {filename} no tiene un formato JSON válido.")
            except Exception as e:
                print(f"Error al procesar {filename}: {e}")
            
    else:
        print("No se pudo iniciar sesión en ORCID. Abortando pipeline.")

if __name__ == "__main__":
    main()
