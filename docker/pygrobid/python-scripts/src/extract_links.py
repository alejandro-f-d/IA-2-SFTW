from bs4 import BeautifulSoup

def extract_links(xml_path):
    """Extrae todos los link de un documento."""
    with open(xml_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'xml')
    
    links = []
   
    # Grobid lo guarda como ptr y ref cada uno de los enlaces.
    tags = soup.find_all(['ptr', 'ref'], target=True)
    
    for tag in tags:
        url = tag['target']
        if url.startswith('http') or url.startswith('www.'):
            links.append(url)
            
    return list(set(links))
