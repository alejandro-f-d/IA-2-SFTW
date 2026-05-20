import os
import json
from dataclasses import asdict
from src.extract_information.extract_by_doi import fetch_work_by_doi
from src.extract_information.extract_by_title import fetch_work_by_title
from src.process_output.processator import (
    get_paper_information,
    get_authors_information,
    get_concepts_information,
    get_citations_information,
)

INPUT_DIR = os.getenv("INPUT_DIR", "/input")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/output")

# E-mail polite pool para OpenAlex (https://docs.openalex.org/how-to-use-the-api/rate-limits-and-authentication)
OPENALEX_EMAIL = os.getenv("OPENALEX_EMAIL", "")


def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Buscamos ficheros _doi.txt generados por el pipeline anterior
    files = [f for f in os.listdir(INPUT_DIR) if f.endswith("_doi.txt")]
    if not files:
        print("No se encontraron ficheros _doi.txt.")
        return

    for filename in files:
        file_path = os.path.join(INPUT_DIR, filename)
        print(f"Procesando: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                doi_data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            print(f"Error leyendo {filename}: {e}")
            continue

        doi = doi_data.get("doi")
        title = doi_data.get("title")

        raw = None
        if doi:
            print(f"  → Buscando por DOI: {doi}")
            raw = fetch_work_by_doi(doi, email=OPENALEX_EMAIL)
        if raw is None and title:
            print(f"  → DOI no disponible, buscando por título: {title[:80]}")
            raw = fetch_work_by_title(title, email=OPENALEX_EMAIL)

        if raw is None:
            print(f"  → No se pudo recuperar información de OpenAlex para {filename}")
            continue

        paper = get_paper_information(raw)
        authors = get_authors_information(raw)
        concepts = get_concepts_information(raw)
        cited_by_ids = get_citations_information(raw)

        result = {
            "paper": asdict(paper),
            "authors": [asdict(a) for a in authors],
            "concepts": [asdict(c) for c in concepts],
            "cited_by_openalex_ids": cited_by_ids,
        }

        output_filename = filename.replace("_doi.txt", "_openalex.json")
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        with open(output_path, "w", encoding="utf-8") as f_out:
            json.dump(result, f_out, indent=4, ensure_ascii=False)
        print(f"  → Guardado: {output_filename}")


if __name__ == "__main__":
    main()
