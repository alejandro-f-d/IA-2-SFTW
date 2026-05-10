import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_URL= os.getenv("GROBID_URL")

def send_to_grobid(pdf_path):
    """Generación del XML del pdf."""
    try:
        with open(pdf_path, 'rb') as f:
            files = {
                'input': (os.path.basename(pdf_path), f, 'application/pdf') # No vale una petición normal porque da un error de java. 
            }
            response = requests.post(
                API_URL, 
                files=files, 
                timeout=300
            )
            
        if response.status_code == 200:
            return response.text
        else:
            print(f"Error en el servidor: {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"Connection failed: {e}")
        return None
