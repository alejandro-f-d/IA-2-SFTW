from bs4 import BeautifulSoup

def extract_title(xml_path):
    """
    Extrae el título del paper desde el XML generado por Grobid.
    """
    with open(xml_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "xml")
    
    title = soup.find("titleStmt").find("title")
    if title:
        return title.get_text(separator=" ").strip()
    
    return None