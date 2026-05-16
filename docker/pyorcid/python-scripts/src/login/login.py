import requests
import os 
import sys
CLIENT_ID = os.environ.get("ORCID_CLIENT_ID")
CLIENT_SECRET = os.environ.get("ORCID_CLIENT_SECRET")
CLIENT_URL = os.environ.get("CLIENT_URL") # Depende de si es producción o sandbox.



def login():
    if not CLIENT_ID or not CLIENT_SECRET or not CLIENT_URL:
        print(f"Error con las variables de entorno de credenciales para ORCID. LOGS: CLIENT_ID: {CLIENT_ID}, secret: {CLIENT_SECRET}, URL: {CLIENT_URL}.")
        sys.exit(1)
    headers = {
        "Accept": "application/json"
    }
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
        "scope": "/read-public"
    }
    response = None
    try:
        response = requests.post(f"{CLIENT_URL}/oauth/token", headers=headers, data=payload)
        response.raise_for_status()
        
        data = response.json()
        access_token = data.get("access_token")
        
        print("¡Token de Producción obtenido con éxito!")
        print(f"Access Token: {access_token}") # TODO: Comentar.
        return access_token
        
    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP en Producción: {http_err}", file=sys.stderr)
        if response is not None:
            print(f"Detalles del error: {response.text}", file=sys.stderr)
    except Exception as err:
        print(f"Error inesperado: {err}", file=sys.stderr)
