from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from bertopic import BERTopic
from bertopic.vectorizers import ClassTfidfTransformer
from hdbscan import HDBSCAN
from umap import UMAP
from keybert import KeyBERT


def load_abstracts(path: str):

    files = sorted(Path(path).glob("*_abstract.txt"))

    docs = []
    names = []

    for f in files:
        names.append(f.stem)
        docs.append(f.read_text(encoding="utf-8"))

    return names, docs


def get_embeddings(docs, model_name="all-MiniLM-L6-v2"):

    model = SentenceTransformer(model_name)

    embeddings = model.encode(
        docs,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    return embeddings


def compute_similarity(embeddings, names, top_k=5):

    similarity_matrix = cosine_similarity(embeddings)

    results = {}

    for i, name in enumerate(names):

        similarities = similarity_matrix[i]

        similar_indices = similarities.argsort()[::-1]

        results[name] = []

        for idx in similar_indices[1:top_k + 1]:

            results[name].append({
                "paper": names[idx],
                "score": float(similarities[idx])
            })

    return results


def run_bertopic(docs):

    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    umap_model = UMAP(
        n_neighbors=5,        
        n_components=3,       
        min_dist=0.0,
        metric="cosine",
        random_state=42
    )

    hdbscan_model = HDBSCAN(
        min_cluster_size=2,   
        min_samples=1,        
        metric="euclidean",
        cluster_selection_method="eom",
        prediction_data=True
    )

    ctfidf_model = ClassTfidfTransformer(reduce_frequent_words=True)

    topic_model = BERTopic(
        embedding_model=embedding_model,
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        ctfidf_model=ctfidf_model,
        nr_topics="auto",
        verbose=True
    )

    topics, probs = topic_model.fit_transform(docs)

    return topic_model, topics, probs



def extract_topics(topic_model, docs, topics):
    kw_model = KeyBERT()
    topics_info = topic_model.get_topic_info()
    results = {}

    for topic_id in topics_info["Topic"]:
        if topic_id == -1:
            continue

        # Reunir todos los docs de este topic
        cluster_docs = " ".join([
            doc for doc, t in zip(docs, topics) if t == topic_id
        ])

        # Extraer keyphrase más representativa
        keyphrases = kw_model.extract_keywords(
            cluster_docs,
            keyphrase_ngram_range=(2, 4),
            stop_words="english",
            top_n=1
        )

        words = topic_model.get_topic(topic_id)
        results[int(topic_id)] = {
            "label": keyphrases[0][0] if keyphrases else "Unknown",
            "keywords": [word for word, _ in words]
        }

    return results


def build_paper_topics(names, topics):

    results = {}

    for name, topic in zip(names, topics):

        results[name] = int(topic)

    return results

