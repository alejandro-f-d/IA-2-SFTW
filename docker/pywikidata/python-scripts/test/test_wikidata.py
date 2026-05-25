import os
import os
import sys
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.execute_query.executor import atacar_wikidata_doi
from src.execute_query.executor import atacar_wikidata_name

def test_atacar_wikidata_doi_devuelve_estructura_correcta():
    """
    Test unitario para validar que atacar_wikidata_doi procesa el DOI
    y devuelve exactamente la estructura JSON esperada de Wikidata.
    """
    
    doi_entrada = "10.1007/978-3-319-45174-9"
    
    output_esperado = {
        "item_uri": "http://www.wikidata.org/entity/Q56669350",
        "titulo": "Machine Learning and Interpretation in Neuroimaging",
        "doi": "10.1007/978-3-319-45174-9",
        "fecha": "2016-01-01T00:00:00Z",
        "volumen": "9444",
        "paginas": "No disponible",
        "revista": "Q924044",
        "keywords": [
            "Q2539",
            "Q551875"
        ],
        "numero_de_citas": 0
    }

    
    resultado = atacar_wikidata_doi(doi_entrada)
    
    assert resultado == output_esperado
    print("Test de atacar wikidata correcto.")


def test_atacar_wikidata_name_devuelve_estructura_correcta():
    """
    Test unitario para validar que atacar_wikidata_name procesa el título del paper
    y devuelve exactamente la misma estructura JSON esperada.
    """
    
    titulo_entrada = "Machine Learning and Interpretation in Neuroimaging"
    
    output_esperado = {
        "item_uri": "http://www.wikidata.org/entity/Q56669350",
        "titulo": "Machine Learning and Interpretation in Neuroimaging",
        "doi": "10.1007/978-3-319-45174-9",
        "fecha": "2016-01-01T00:00:00Z",
        "volumen": "9444",
        "paginas": "No disponible",
        "revista": "Q924044",
        "keywords": [
            "Q2539",
            "Q551875"
        ],
        "numero_de_citas": 0
    }
    
    resultado = atacar_wikidata_name(titulo_entrada)
    
    assert resultado == output_esperado
