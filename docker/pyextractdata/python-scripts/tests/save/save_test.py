import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.save.save import save_content

def test_save_current_dir():
    test_filename = "archivo_prueba_borrame.txt"
    test_content = "Probando guardado en el directorio actual"

    result = save_content(test_content, test_filename)

    assert result is True, "La función debería devolver True"
    assert os.path.exists(test_filename), "El archivo debería existir en el disco"
    
    with open(test_filename, "r", encoding="utf-8") as f:
        assert f.read() == test_content

    os.remove(test_filename)

