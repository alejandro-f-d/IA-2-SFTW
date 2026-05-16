from src.login.login import login
import os

INPUT_DIR = os.getenv('INPUT_DIR', '/input') 
OUTPUT_DIR = os.getenv('OUTPUT_DIR', '/output')

def main():    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    token = login()
    if token:
        print("Listo para consultar perfiles de ORCID.")
    else:
        print("No se pudo iniciar sesión en ORCID. Abortando pipeline.")

if __name__ == "__main__":
    main()
