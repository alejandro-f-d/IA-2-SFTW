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
        print("Listo para consultar perfiles de ORCID.")
        _json_info_completa = info_orcid_by_id("0000-0003-0454-7145", token)
        if _json_info_completa is not None:
            informacion_researcher = get_researcher_information(_json_info_completa)
            informacion_empresa = get_employment_information(_json_info_completa)
            informacion_publicaciones = get_publication_information(_json_info_completa)
            print(f"Información extraida:\n Researcher: {informacion_researcher}\n Empresa: {informacion_empresa}\n Publicaciones: {informacion_publicaciones}.")
            output_file_path = os.path.join(OUTPUT_DIR, f"orcid_0000-0003-0454-7145.json")
            
            with open(output_file_path, "w", encoding="utf-8") as f:
                json.dump(_json_info_completa, f, indent=4, ensure_ascii=False)
                
            print(f"Archivo JSON original guardado correctamente en: {output_file_path}")
        else: 
            print("No se ha podido obtener información en base al id de orcid.")
    else:
        print("No se pudo iniciar sesión en ORCID. Abortando pipeline.")

if __name__ == "__main__":
    main()
