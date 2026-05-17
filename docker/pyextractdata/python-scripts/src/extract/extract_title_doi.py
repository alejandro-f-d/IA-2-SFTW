from bs4 import BeautifulSoup


def extract_title_doi(path):
    """
    Extrae el titulo y el DOI de un XML generado por GROBID.
    Devuelve un dict {"titulo": str | None, "doi": str | None}
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "xml")

        #Titulo
        titulo = None
        title_tag = soup.find("title", {"type": "main"})
        if title_tag:
            titulo = title_tag.get_text(strip=True)

        #DOI
        doi = None
        doi_tag = soup.find("idno", {"type": "DOI"})
        if doi_tag:
            doi = doi_tag.get_text(strip=True)

        return {"titulo": titulo, "doi": doi}

    except Exception as e:
        print(f"Error leyendo el XML en extract_title_doi: {e}")
        return {"titulo": None, "doi": None}
