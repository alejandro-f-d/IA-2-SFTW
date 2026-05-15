import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from src.extract.extract_abstract import extract_abstract
from src.extract.extract_ack import extract_ack

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

