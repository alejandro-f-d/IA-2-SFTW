import os

from src.clustering.clustering import *
from src.save.save_results import *


INPUT_DIR = os.getenv('INPUT_DIR', '/input')
OUTPUT_DIR = os.getenv('OUTPUT_DIR', '/output')


def main():

    names, docs = load_abstracts(INPUT_DIR)

    if len(docs) == 0:
        raise ValueError("No se encontraron abstracts en el directorio: " + INPUT_DIR)

    embeddings = get_embeddings(docs)

    similarity_results = compute_similarity(
        embeddings,
        names
    )

    topic_model, topics, probs, topic_distr = run_bertopic(docs)

    topic_results = extract_topics(topic_model, docs, topics)
    paper_topics = build_paper_topics(names, topics)
    paper_topic_distribution = build_paper_topic_distribution(names, topic_distr, topic_model)

    save_json(similarity_results,       os.path.join(OUTPUT_DIR, "similarity.json"))
    save_json(topic_results,            os.path.join(OUTPUT_DIR, "topics.json"))
    save_json(paper_topics,             os.path.join(OUTPUT_DIR, "paper_topics.json"))
    save_json(paper_topic_distribution, os.path.join(OUTPUT_DIR, "paper_topic_distribution.json"))

    print("Similarity scores generated")
    print("Topics generated")


if __name__ == "__main__":
    main()