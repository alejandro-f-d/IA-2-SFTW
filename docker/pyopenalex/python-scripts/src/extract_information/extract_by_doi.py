import sys
import requests
import os

OPENALEX_BASE = os.getenv("OPENALEX_BASE_URL", "https://api.openalex.org")

def fetch_work_by_doi(doi: str, email: str = "") -> dict | None:
    doi_clean = doi.strip()
    if not doi_clean.startswith("https://doi.org/"):
        doi_clean = f"https://doi.org/{doi_clean}"
    url = f"{OPENALEX_BASE}/works/{doi_clean}"
    params = {}
    if email:
        params["mailto"] = email
    response = None
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP al consultar DOI {doi}: {http_err}", file=sys.stderr)
        if response is not None:
            print(f"Detalles: {response.text[:200]}", file=sys.stderr)
        return None
    except Exception as err:
        print(f"Error inesperado al consultar DOI {doi}: {err}", file=sys.stderr)
        return None
