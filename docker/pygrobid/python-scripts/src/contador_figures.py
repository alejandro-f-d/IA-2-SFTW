from bs4 import BeautifulSoup
def count_figures(xml_path):
    """Contador de la cantidad de figuras en un paper en concreto."""
    with open(xml_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'xml')
        figures = soup.find_all('figure')
    only_pictures = [fig for fig in figures if fig.get('type') != 'table'] 
    return len(only_pictures)
