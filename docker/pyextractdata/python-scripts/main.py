import os
import json
from src.save.save import save_content
from src.extract.extract_abstract import extract_abstract
from src.extract.extract_ack import extract_ack
from src.extract.extract_people import extract_people
from src.extract.extract_title_doi import extract_title_doi

from src.save.save_kg import build_kg, save_kg
from src.ner.ner_extractor import extract_entities


INPUT_DIR = os.getenv('INPUT_DIR', '/input')
OUTPUT_DIR = os.getenv('OUTPUT_DIR', '/output')


def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    files = [f for f in os.listdir(INPUT_DIR) if f.endswith('.xml')]
    if not files:
        print(f"No hay XMLs en ese directorio. {INPUT_DIR}")
        return

    print(f"Se han encontrado: {len(files)} xmls")

    papers_data = []

    for filename in files:
        xml_path = os.path.join(INPUT_DIR, filename)
        paper_id = filename.replace('.xml', '')
        print(f"Empezamos a procesar: {filename}")

        abstract_data = extract_abstract(xml_path)
        if abstract_data:
            save_content(abstract_data,
                os.path.join(OUTPUT_DIR, filename.replace('.xml', '_abstract.txt')))
        else:
            print(f"Fallo al generar el abstract de: {filename}")

        ack_data = extract_ack(xml_path)
        if ack_data:
            save_content(ack_data,
                os.path.join(OUTPUT_DIR, filename.replace('.xml', '_ack.txt')))
        else:
            print(f"Fallo al generar el ack de: {filename}")

        people_data = extract_people(xml_path)
        if people_data:
            save_content(people_data,
                os.path.join(OUTPUT_DIR, filename.replace('.xml', '_people.txt')))
        else:
            print(f"Fallo al generar los autores de: {filename}")

        doi_data = extract_title_doi(xml_path)
        if doi_data:
            save_content(json.dumps(doi_data, ensure_ascii=False, indent=4),
                os.path.join(OUTPUT_DIR, filename.replace('.xml', '_doi.txt')))
        else:
            print(f"Fallo al obtener el doi de: {filename}")

        # Modificación: NER sobre los agradecimientos
        if ack_data:
            print(f"Procesando NER para {paper_id}...")
            personas, orgs, lugares, project_ids = extract_entities(ack_data)
            print(f"  → {len(personas)} personas, {len(orgs)} organizaciones, {len(lugares)} lugares, {len(project_ids)} proyectos")
            papers_data.append({
                "paper_id": paper_id,
                "personas": personas,
                "organizaciones": orgs,
                "lugares": lugares,
                "project_ids": project_ids
            })

    # Modificación: generar y guardar el KG
    if papers_data:
        g = build_kg(papers_data)
        save_kg(g, os.path.join(OUTPUT_DIR, "knowledge_graph.ttl"))

if __name__ == "__main__":
    main()
