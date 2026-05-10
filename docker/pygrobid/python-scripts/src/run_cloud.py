import os
from pathlib import Path
from collections import Counter
from src.processor import get_clean_words
from src.visualizer import generate_word_cloud


def run_cloud(XML_DIR, path_save, cantidadPalabras=10):
    master_counter = Counter() 
    xml_files = list(XML_DIR.glob("*.xml")) # Sacamos la información de ese directorio de los ficheros XML.
    for file_path in xml_files:
        words = get_clean_words(file_path)
        master_counter.update(words) # Contador global de todos los pdf, para no sacar el wordCloud de solo una parte.
    
    print(f"\n--- TOP {cantidadPalabras} MOST COMMON KEYWORDS ---")
    top_words = master_counter.most_common(cantidadPalabras) # Solo las n que más aparezcan, pero esto es de diseño TODO: Añadirlo a variable de entorno.
    
    for word, count in top_words:
        print(f"{word}: {count} ocurrencias")

    generate_word_cloud(master_counter, path_save, cantidadPalabras)

