import json
import pytest
import numpy as np
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock


SAMPLE_DOCS = [
    "Food waste reduction strategies in European Union supply chains and circular economy models.",
    "Hotel buffet management practices to minimize restaurant food waste and reduce operational costs.",
    "Agricultural food preservation technologies to prevent post-harvest losses in developing countries.",
    "Household food waste behaviour drivers and shopping habits affecting waste generation.",
    "Digital tracking indices and mobile apps for rescuing surplus food from businesses.",
]

SAMPLE_NAMES = [
    "paper0_abstract",
    "paper1_abstract",
    "paper2_abstract",
    "paper3_abstract",
    "paper4_abstract",
]


@pytest.fixture
def tmp_abstracts_dir(tmp_path):
    """Crea un directorio temporal con ficheros *_abstract.txt de prueba."""
    for name, doc in zip(SAMPLE_NAMES, SAMPLE_DOCS):
        (tmp_path / f"{name}.txt").write_text(doc, encoding="utf-8")
    return str(tmp_path)


@pytest.fixture
def sample_embeddings():
    """Embeddings sintéticos normalizados (L2)."""
    rng = np.random.default_rng(42)
    emb = rng.random((len(SAMPLE_DOCS), 384)).astype(np.float32)
    norms = np.linalg.norm(emb, axis=1, keepdims=True)
    return emb / norms



class TestLoadAbstracts:

    def test_returns_correct_number_of_docs(self, tmp_abstracts_dir):
        from src.clustering.clustering import load_abstracts
        names, docs = load_abstracts(tmp_abstracts_dir)
        assert len(docs) == len(SAMPLE_NAMES)
        assert len(names) == len(SAMPLE_NAMES)

    def test_names_match_stems(self, tmp_abstracts_dir):
        from src.clustering.clustering import load_abstracts
        names, _ = load_abstracts(tmp_abstracts_dir)
        for name in names:
            assert name in SAMPLE_NAMES

    def test_docs_content_is_correct(self, tmp_abstracts_dir):
        from src.clustering.clustering import load_abstracts
        names, docs = load_abstracts(tmp_abstracts_dir)
        for name, doc in zip(names, docs):
            expected_idx = SAMPLE_NAMES.index(name)
            assert docs[names.index(name)] == SAMPLE_DOCS[expected_idx]

    def test_empty_directory_returns_empty_lists(self, tmp_path):
        from src.clustering.clustering import load_abstracts
        names, docs = load_abstracts(str(tmp_path))
        assert names == []
        assert docs == []

    def test_ignores_non_abstract_files(self, tmp_path):
        """Ficheros sin el sufijo _abstract.txt no deben cargarse."""
        (tmp_path / "paper0_abstract.txt").write_text("valid doc", encoding="utf-8")
        (tmp_path / "readme.txt").write_text("ignored", encoding="utf-8")
        from src.clustering.clustering import load_abstracts
        names, docs = load_abstracts(str(tmp_path))
        assert len(docs) == 1



class TestGetEmbeddings:

    def test_output_shape(self):
        from src.clustering.clustering import get_embeddings
        embeddings = get_embeddings(SAMPLE_DOCS)
        assert embeddings.shape[0] == len(SAMPLE_DOCS)
        assert embeddings.shape[1] > 0

    def test_embeddings_are_normalized(self):
        from src.clustering.clustering import get_embeddings
        embeddings = get_embeddings(SAMPLE_DOCS)
        norms = np.linalg.norm(embeddings, axis=1)
        np.testing.assert_allclose(norms, np.ones(len(SAMPLE_DOCS)), atol=1e-5)

    def test_returns_numpy_array(self):
        from src.clustering.clustering import get_embeddings
        embeddings = get_embeddings(SAMPLE_DOCS)
        assert isinstance(embeddings, np.ndarray)



class TestComputeSimilarity:

    def test_all_papers_present_in_results(self, sample_embeddings):
        from src.clustering.clustering import compute_similarity
        results = compute_similarity(sample_embeddings, SAMPLE_NAMES)
        for name in SAMPLE_NAMES:
            assert name in results

    def test_top_k_results_count(self, sample_embeddings):
        from src.clustering.clustering import compute_similarity
        top_k = 3
        results = compute_similarity(sample_embeddings, SAMPLE_NAMES, top_k=top_k)
        for name in SAMPLE_NAMES:
            assert len(results[name]) == top_k

    def test_self_not_in_results(self, sample_embeddings):
        """Un paper no debe aparecer como similar a sí mismo."""
        from src.clustering.clustering import compute_similarity
        results = compute_similarity(sample_embeddings, SAMPLE_NAMES)
        for name in SAMPLE_NAMES:
            similar_papers = [entry["paper"] for entry in results[name]]
            assert name not in similar_papers

    def test_scores_between_minus_one_and_one(self, sample_embeddings):
        from src.clustering.clustering import compute_similarity
        results = compute_similarity(sample_embeddings, SAMPLE_NAMES)
        for name in SAMPLE_NAMES:
            for entry in results[name]:
                assert -1.0 <= entry["score"] <= 1.0

    def test_scores_are_floats(self, sample_embeddings):
        from src.clustering.clustering import compute_similarity
        results = compute_similarity(sample_embeddings, SAMPLE_NAMES)
        for name in SAMPLE_NAMES:
            for entry in results[name]:
                assert isinstance(entry["score"], float)

    def test_scores_sorted_descending(self, sample_embeddings):
        from src.clustering.clustering import compute_similarity
        results = compute_similarity(sample_embeddings, SAMPLE_NAMES)
        for name in SAMPLE_NAMES:
            scores = [entry["score"] for entry in results[name]]
            assert scores == sorted(scores, reverse=True)



class TestBuildPaperTopics:

    def test_all_papers_assigned(self):
        from src.clustering.clustering import build_paper_topics
        topics = [0, 1, 0, 2, 1]
        results = build_paper_topics(SAMPLE_NAMES, topics)
        assert set(results.keys()) == set(SAMPLE_NAMES)

    def test_topic_values_are_int(self):
        from src.clustering.clustering import build_paper_topics
        topics = [0, 1, 0, 2, 1]
        results = build_paper_topics(SAMPLE_NAMES, topics)
        for val in results.values():
            assert isinstance(val, int)

    def test_outlier_topic_preserved(self):
        """El topic -1 (outlier de BERTopic) debe conservarse tal cual."""
        from src.clustering.clustering import build_paper_topics
        topics = [-1, 0, -1, 1, 0]
        results = build_paper_topics(SAMPLE_NAMES, topics)
        assert results["paper0_abstract"] == -1
        assert results["paper2_abstract"] == -1

    def test_correct_mapping(self):
        from src.clustering.clustering import build_paper_topics
        topics = [3, 1, 2, 0, 1]
        results = build_paper_topics(SAMPLE_NAMES, topics)
        for name, expected_topic in zip(SAMPLE_NAMES, topics):
            assert results[name] == expected_topic



class TestExtractTopics:

    def _mock_topic_model(self, topic_ids):
        """Genera un topic_model mock con los topic_ids indicados."""
        import pandas as pd
        topic_model = MagicMock()
        topic_model.get_topic_info.return_value = pd.DataFrame({"Topic": topic_ids})
        topic_model.get_topic.side_effect = lambda tid: [
            ("food", 0.9), ("waste", 0.8), ("reduction", 0.7),
            ("supply", 0.6), ("chain", 0.5), ("circular", 0.4),
            ("economy", 0.3), ("model", 0.2), ("linear", 0.1), ("policy", 0.05)
        ]
        return topic_model

    def test_outlier_topic_excluded(self):
        from src.clustering.clustering import extract_topics
        topic_model = self._mock_topic_model([-1, 0, 1])
        topics = [0, 0, 1, 1, -1]
        results = extract_topics(topic_model, SAMPLE_DOCS, topics)
        assert -1 not in results

    def test_result_has_label_and_keywords(self):
        from src.clustering.clustering import extract_topics
        topic_model = self._mock_topic_model([-1, 0, 1])
        topics = [0, 0, 1, 1, -1]
        results = extract_topics(topic_model, SAMPLE_DOCS, topics)
        for topic_data in results.values():
            assert "label" in topic_data
            assert "keywords" in topic_data

    def test_keywords_is_list_of_strings(self):
        from src.clustering.clustering import extract_topics
        topic_model = self._mock_topic_model([-1, 0])
        topics = [0, 0, 0, 0, -1]
        results = extract_topics(topic_model, SAMPLE_DOCS, topics)
        for topic_data in results.values():
            assert isinstance(topic_data["keywords"], list)
            for kw in topic_data["keywords"]:
                assert isinstance(kw, str)

    def test_label_is_string(self):
        from src.clustering.clustering import extract_topics
        topic_model = self._mock_topic_model([-1, 0])
        topics = [0, 0, 0, 0, -1]
        results = extract_topics(topic_model, SAMPLE_DOCS, topics)
        for topic_data in results.values():
            assert isinstance(topic_data["label"], str)



class TestSaveJson:

    def test_file_is_created(self, tmp_path):
        from src.save.save_results import save_json
        output_file = tmp_path / "test.json"
        save_json({"key": "value"}, str(output_file))
        assert output_file.exists()

    def test_content_is_valid_json(self, tmp_path):
        from src.save.save_results import save_json
        data = {"paper0": [{"paper": "paper1", "score": 0.95}]}
        output_file = tmp_path / "similarity.json"
        save_json(data, str(output_file))
        loaded = json.loads(output_file.read_text(encoding="utf-8"))
        assert loaded == data

    def test_creates_parent_directories(self, tmp_path):
        from src.save.save_results import save_json
        nested_path = tmp_path / "a" / "b" / "c" / "output.json"
        save_json({"x": 1}, str(nested_path))
        assert nested_path.exists()

    def test_encoding_utf8(self, tmp_path):
        """Caracteres no ASCII deben guardarse correctamente."""
        from src.save.save_results import save_json
        data = {"label": "Reducción de residuos alimentarios"}
        output_file = tmp_path / "topics.json"
        save_json(data, str(output_file))
        loaded = json.loads(output_file.read_text(encoding="utf-8"))
        assert loaded["label"] == "Reducción de residuos alimentarios"

    def test_indentation_is_applied(self, tmp_path):
        from src.save.save_results import save_json
        output_file = tmp_path / "pretty.json"
        save_json({"a": 1}, str(output_file))
        raw = output_file.read_text(encoding="utf-8")
        assert "\n" in raw  # fichero con indentación, no en una sola línea

    def test_overwrites_existing_file(self, tmp_path):
        from src.save.save_results import save_json
        output_file = tmp_path / "overwrite.json"
        save_json({"v": 1}, str(output_file))
        save_json({"v": 2}, str(output_file))
        loaded = json.loads(output_file.read_text(encoding="utf-8"))
        assert loaded["v"] == 2

    def test_empty_dict(self, tmp_path):
        from src.save.save_results import save_json
        output_file = tmp_path / "empty.json"
        save_json({}, str(output_file))
        loaded = json.loads(output_file.read_text(encoding="utf-8"))
        assert loaded == {}