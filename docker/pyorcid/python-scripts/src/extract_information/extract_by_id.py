import sys
import requests
import os

CLIENT_URL = os.environ.get("CLIENT_URL") # Depende de si es producción o sandbox.

def info_orcid_by_id(orcid_id, token):
    orcid_uri_id = f"{CLIENT_URL}/v3.0/{orcid_id}/record"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    response = None
    try:
        response = requests.get(orcid_uri_id, headers=headers)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP al consultar el ORCID {orcid_id}: {http_err}", file=sys.stderr)
        if response is not None:
            print(f"Detalles: {response.text}", file=sys.stderr)
        return None
    except Exception as err:
        print(f"Error inesperado al consultar el ORCID {orcid_id}: {err}", file=sys.stderr)
        return None
