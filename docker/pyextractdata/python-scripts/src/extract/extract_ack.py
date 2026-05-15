import re
from bs4 import BeautifulSoup
def extract_ack(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'xml') 
        ack_tag = soup.find('div', attrs={'type': 'acknowledgement'})
        if ack_tag:
            return ack_tag.get_text(separator=" ", strip=True)
        return None 
    except Exception as e:
        print(f"Error leyendo el XML en extract_ack: {e}")
        return None
