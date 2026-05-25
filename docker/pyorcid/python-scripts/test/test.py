import os
import sys
from dataclasses import asdict

# Inyección dinámica para que encuentre el paquete 'src' desde la carpeta 'test'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importamos tus funciones reales de login, extracción y procesamiento
from src.login.login import login
from src.extract_information.extract_by_id import info_orcid_by_id
from src.process_output.processator import (
    get_employment_information,
    get_publication_information,
    get_researcher_information
)

def test_pipeline_orcid_real_devuelve_datos():
    """
    Test de integración completo:
    1. Hace login real en ORCID para obtener un token.
    2. Descarga el JSON real usando el ORCID ID de Daniel Garijo.
    3. Pasa el JSON por tus tres funciones de procesamiento reales.
    4. Verifica que se extraigan datos reales y que las estructuras no vengan vacías.
    """
    orcid_test = "0000-0003-0454-7145"
    
    token = login()
    assert token is not None, "No se pudo obtener el token de ORCID. Verifica tus credenciales de entorno."
    
    json_info_completa = info_orcid_by_id(orcid_test, token)
    assert json_info_completa is not None, f"La API de ORCID no devolvió datos para el ID: {orcid_test}"
    
    informacion_researcher = get_researcher_information(json_info_completa)
    informacion_empresa = get_employment_information(json_info_completa)
    informacion_publicaciones = get_publication_information(json_info_completa)
    
    
    # Verificación del Investigador
    assert informacion_researcher is not None, "get_researcher_information devolvió None"
    dict_researcher = asdict(informacion_researcher)
    researcher_str = str(dict_researcher).lower()
    
    # Validamos que el mapeo apunte al dueño real del perfil detectado por tu método
    assert "daniel" in researcher_str or "garijo" in researcher_str
    
    # Verificación de Empleos
    assert isinstance(informacion_empresa, list), "get_employment_information debería devolver una lista"
    assert len(informacion_empresa) > 0, "La lista de empleos extraída está vacía"
    
    # Verificación de Publicaciones
    assert isinstance(informacion_publicaciones, list), "get_publication_information debería devolver una lista"
    assert len(informacion_publicaciones) > 0, "La lista de publicaciones extraída está vacía"
    
    # Comprobamos que las publicaciones se conviertan a diccionario y tengan los campos clave
    publicaciones_dict = [asdict(pub) for pub in informacion_publicaciones]
    primer_item_str = str(publicaciones_dict[0]).lower()
    assert "title" in primer_item_str or "titulo" in primer_item_str
