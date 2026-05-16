import os
import sys
import json

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from src.extract.extract_abstract import extract_abstract
from src.extract.extract_ack import extract_ack
from src.extract.extract_people import extract_people

TEST_XML = "./test_txt.txt" 

def test_extract_abstract_success():
    resultado = extract_abstract(TEST_XML)
    print(f"Contenido del abstract: {resultado}") 
    assert resultado is not None
    assert "ABSTRACT_START" in resultado
    assert "ABSTRACT_END" in resultado

def test_extract_ack_success():
    resultado = extract_ack(TEST_XML)
    
    assert resultado is not None
    assert "ACK_START" in resultado
    assert "ACK_END" in resultado

def test_extract_none_if_file_missing():
    resultado = extract_abstract("archivo_fantasma.xml")
    assert resultado is None

def test_extract_authors_success():

    resultado_json = extract_people(TEST_XML)

    assert resultado_json is not None

    autores = json.loads(resultado_json)

    assert isinstance(autores, list)
    assert len(autores) > 0

    autor_test = next(
        (a for a in autores if a["nombre_completo"] == "JULIO CÉSAR"), None
    )

    assert autor_test is not None, "No se encontró a JULIO CÉSAR en el resultado"
    assert autor_test["nombre"] == "JULIO"
    assert autor_test["apellido"] == "CÉSAR"
    assert autor_test["orcid"] == "0000-0000-0000-0000"

    afiliaciones = autor_test["afiliaciones"]
    assert len(afiliaciones) == 2

    assert afiliaciones[0]["departamento"] == "Department of Lorem Studies"
    assert afiliaciones[0]["institucion"] == "University of Ipsum"
    assert afiliaciones[0]["pais"] == "ROMULO Y REMO"

    assert afiliaciones[1]["departamento"] == ""
    assert afiliaciones[1]["institucion"] == "Elit Research Lab, Eiusmod University"
    assert afiliaciones[1]["pais"] == "Australia"
