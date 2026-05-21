import sys
import requests
import os

OPENALEX_BASE = os.getenv("OPENALEX_BASE_URL", "https://api.openalex.org")

def fetch_work_by_title(title: str, email: str = "") -> dict | None:
    url = f"{OPENALEX_BASE}/works"
    params = {
        "filter": f"title.search:{title}",
        "per-page": 1,
        "sort": "relevance_score:desc",
    }
    if email:
        params["mailto"] = email

    response = None
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        results = data.get("results", [])
        if not results:
            print(f"No se encontraron resultados para el título: '{title[:80]}'", file=sys.stderr)
            return None

        return results[0]
    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP al buscar por título: {http_err}", file=sys.stderr)
        if response is not None:
            print(f"Detalles: {response.text[:200]}", file=sys.stderr)
        return None
    except Exception as err:
        print(f"Error inesperado al buscar por título: {err}", file=sys.stderr)
        return None
