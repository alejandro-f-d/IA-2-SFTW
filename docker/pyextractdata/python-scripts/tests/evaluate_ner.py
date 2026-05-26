import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ner.ner_extractor import extract_entities
# ── CORPUS DE VALIDACIÓN (anotado manualmente) ──────────────
gold_standard = {
    "paper0": {
        "organizaciones": [],
        "personas": [],
        "lugares": [],
        "project_ids": []
    },
    "paper2": {
        "organizaciones": [],
        "personas": [],
        "lugares": [],
        "project_ids": []
    },
    "paper3": {
        "organizaciones": [],
        "personas": [],
        "lugares": [],
        "project_ids": []
    },
    "paper5": {
        "organizaciones": [],
        "personas": [],
        "lugares": [],
        "project_ids": []
    },
    "paper7": {
        "organizaciones": [],
        "personas": [],
        "lugares": [],
        "project_ids": []
    },
    "paper9": {
        "organizaciones": [],
        "personas": [],
        "lugares": [],
        "project_ids": []
    }
}

# ── TEXTOS DE LOS AGRADECIMIENTOS ───────────────────────────
ack_texts = {
    "paper1": "",
    "paper2": "",
    "paper3": "",
    "paper4": "",
    "paper5": "",
    "paper6": ""
}

def calculate_metrics(gold, predicted):
    """
    Calcula precisión, recall y F1 para una lista de entidades.
    Normaliza las entidades a minúsculas para comparar.
    """
    gold_set = set([e.lower() for e in gold])
    pred_set = set([e.lower() for e in predicted])

    tp = len(gold_set & pred_set)  # correctas
    fp = len(pred_set - gold_set)  # detectadas incorrectamente
    fn = len(gold_set - pred_set)  # no detectadas

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    return round(precision, 2), round(recall, 2), round(f1, 2)


def evaluate():
    print("=" * 60)
    print("EVALUACIÓN DEL MODELO NER")
    print("=" * 60)

    all_gold_orgs, all_pred_orgs = [], []
    all_gold_pers, all_pred_pers = [], []
    all_gold_locs, all_pred_locs = [], []
    all_gold_proj, all_pred_proj = [], []

    for paper_id, text in ack_texts.items():
        print(f"\nPaper: {paper_id}")
        print(f"Texto: {text[:80]}...")

        # Ejecutamos el modelo
        personas, orgs, lugares, project_ids = extract_entities(text)

        gold = gold_standard[paper_id]

        # Métricas por paper
        prec_o, rec_o, f1_o = calculate_metrics(gold["organizaciones"], orgs)
        prec_p, rec_p, f1_p = calculate_metrics(gold["personas"], personas)
        prec_l, rec_l, f1_l = calculate_metrics(gold["lugares"], lugares)
        prec_pr, rec_pr, f1_pr = calculate_metrics(gold["project_ids"], project_ids)

        print(f"  ORG  → Gold: {gold['organizaciones']}")
        print(f"         Pred: {orgs}")
        print(f"         Prec: {prec_o} | Rec: {rec_o} | F1: {f1_o}")

        print(f"  LOC  → Gold: {gold['lugares']}")
        print(f"         Pred: {lugares}")
        print(f"         Prec: {prec_l} | Rec: {rec_l} | F1: {f1_l}")

        print(f"  PROJ → Gold: {gold['project_ids']}")
        print(f"         Pred: {project_ids}")
        print(f"         Prec: {prec_pr} | Rec: {rec_pr} | F1: {f1_pr}")

        # Acumulamos para métricas globales
        all_gold_orgs.extend(gold["organizaciones"])
        all_pred_orgs.extend(orgs)
        all_gold_pers.extend(gold["personas"])
        all_pred_pers.extend(personas)
        all_gold_locs.extend(gold["lugares"])
        all_pred_locs.extend(lugares)
        all_gold_proj.extend(gold["project_ids"])
        all_pred_proj.extend(project_ids)

    # Métricas globales
    print("\n" + "=" * 60)
    print("MÉTRICAS GLOBALES")
    print("=" * 60)

    prec, rec, f1 = calculate_metrics(all_gold_orgs, all_pred_orgs)
    print(f"ORG  → Precisión: {prec} | Recall: {rec} | F1: {f1}")

    prec, rec, f1 = calculate_metrics(all_gold_pers, all_pred_pers)
    print(f"PER  → Precisión: {prec} | Recall: {rec} | F1: {f1}")

    prec, rec, f1 = calculate_metrics(all_gold_locs, all_pred_locs)
    print(f"LOC  → Precisión: {prec} | Recall: {rec} | F1: {f1}")

    prec, rec, f1 = calculate_metrics(all_gold_proj, all_pred_proj)
    print(f"PROJ → Precisión: {prec} | Recall: {rec} | F1: {f1}")


if __name__ == "__main__":
    evaluate()
