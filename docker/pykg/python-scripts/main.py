import os
from src.loaders.input_loader import load_all, load_globals
from src.builders.kg_builder import build_kg, save_kg

INPUT_DIR     = os.getenv("INPUT_DIR",     "/input")
OUTPUT_DIR    = os.getenv("OUTPUT_DIR",    "/output")
ONTOLOGY_PATH = os.getenv("ONTOLOGY_PATH", "/ontology/citation_ontology.ttl")


def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print(f"Cargando ficheros desde: {INPUT_DIR}")
    papers   = load_all(INPUT_DIR)
    globals_ = load_globals(INPUT_DIR)

    if not papers:
        print("No se encontraron papers. Abortando.")
        return

    print(f"\nPapers encontrados: {len(papers)}")
    for pid in papers:
        sources = papers[pid]
        present = [k for k, v in sources.items() if v]
        print(f"  {pid}: {present}")

    print("\nConstruyendo Knowledge Graph...")
    g = build_kg(papers, globals_, ontology_path=ONTOLOGY_PATH)

    output_path = os.path.join(OUTPUT_DIR, "knowledge_graph_final.ttl")
    save_kg(g, output_path)


if __name__ == "__main__":
    main()
