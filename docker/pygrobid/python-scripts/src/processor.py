import re
from bs4 import BeautifulSoup

# Baneamos estas palabras que son conectores y no vienen a cuento mostrarlas.
STOPWORDS = {
    'the', 'and', 'that', 'for', 'from', 'with', 'this', 'these', 'those',
    'been', 'have', 'has', 'were', 'was', 'are', 'their', 'such', 'into',
    'which', 'also', 'than', 'they', 'our', 'some', 'could', 'should'
}

def get_clean_words(xml_path):
    """Devuelve del abstract las palabras encontradas."""
    with open(xml_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'xml') # Leer el XML.
    
    abs_tag = soup.find('abstract') # Va a una parte específica del XML.
    if not abs_tag: 
        return []

    text = abs_tag.get_text().lower() # Lo parafrraseamos a un formato común de datos.
    words = re.findall(r'\b[a-z]{3,}\b', text) # Expresión regular para que sea una palabra con sentido y no salga como palabra más encontrada a, an, ... 
    clean_words = [w for w in words if w not in STOPWORDS]
    return clean_words
