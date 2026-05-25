import os
from src.api_client import send_to_grobid
from pathlib import Path
from src.run_cloud import run_cloud 
from src.contador_figures import count_figures 
from src.visualizer import generate_figure_plot
from src.extract_links import extract_links 
from src.generate_document import generate_links_report 


INPUT_DIR = os.getenv("INPUT_DIR", "/input")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/output")

CANTIDAD_PALABRAS = int(os.getenv("CANTIDAD_PALABRAS", 2))


def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    # if not os.path.exists(f"{OUTPUT_DIR}/images"):
    #     os.makedirs(f"{OUTPUT_DIR}/images")
    # if not os.path.exists(f"{OUTPUT_DIR}/reporte_links"):
    #     os.makedirs(f"{OUTPUT_DIR}/reporte_links")

    files = [f for f in os.listdir(INPUT_DIR) if f.endswith('.pdf')]
    
    if not files:
        print(f"No hay PDFs en ese directorio. {INPUT_DIR}")
        return

    print(f"Se han encontrado: {len(files)} pdfs")

    for filename in files:
        pdf_path = os.path.join(INPUT_DIR, filename)
        print(f"Empezamos a procesar: {filename}")

        xml_data = send_to_grobid(pdf_path)

        if xml_data:
            xml_filename = filename.replace(".pdf", ".xml")
            save_path = os.path.join(OUTPUT_DIR, xml_filename)
            
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(xml_data)
            
            print(f"Salvado el XML en: {save_path}")
        else:
            print(f"Fallo al generar el XML de: {filename}")
    # run_cloud(OUTPUT_DIR, f"{OUTPUT_DIR}/images", CANTIDAD_PALABRAS) 
    # # Contar las figuras: Usamos un diccionario que contine la relación entre el nombre del fichero y la cantidad de imágenes
    # diccionario_contador_figuras = {}
    # files_xml = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.xml')]
    # if not files_xml:
    #     print("Se ha producido un error, no hay ficheros xml de los que extraer información.")
    #     return
    # for filename in files_xml:
    #     # Filename contiene el nombre luego será la clave del diccionario.
    #     diccionario_contador_figuras[filename] = count_figures(os.path.join(OUTPUT_DIR, filename))
    # generate_figure_plot(diccionario_contador_figuras,  f"{OUTPUT_DIR}/images")
    # diccionario_links = {}
    # for filename in files_xml:
    #     # Filename contiene el nombre luego será la clave del diccionario.
    #     diccionario_links[filename] = extract_links(os.path.join(OUTPUT_DIR, filename)) 
    # generate_links_report(diccionario_links, f"{OUTPUT_DIR}/reporte_links/links_documentos.md")

if __name__ == "__main__":
    main()
