import re
from bs4 import BeautifulSoup

def extract_abstract(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'xml') 
        abs_tag = soup.find('abstract')
        if abs_tag:
            return abs_tag.get_text(separator=" ", strip=True)
        
        return None 
    except Exception as e:
        print(f"Error leyendo el XML: {e}")
        return None
