import os
import json
from bs4 import BeautifulSoup


def extract_people(xml_data):
    if isinstance(xml_data, str) and os.path.exists(xml_data):
        with open(xml_data, "r", encoding="utf-8") as f:
            contenido_xml = f.read()
    else:
        contenido_xml = xml_data

    soup = BeautifulSoup(contenido_xml, "xml")
    
    autores_elementos = soup.find_all("author") 
    lista_autores = []

    for autor in autores_elementos:
        if autor.find_parent("back"):
            continue

        # Estructura que busca en el paper: <persName><forename type="first">Nombre</forename><surname>Apellido</surname></persName>
        forename_el = autor.find("forename", type="first") 
        surname_el = autor.find("surname")
        
        nombre = forename_el.get_text(strip=True) if forename_el else "" 
        apellido = surname_el.get_text(strip=True) if surname_el else "" 
        
        # La estructura que contiene el orcid es: <idno type="ORCID">0000-0000-0000-0000</idno>
        orcid_el = autor.find("idno", type="ORCID") 
        orcid = orcid_el.get_text(strip=True) if orcid_el else None
        
        afiliaciones = []
        # Las organizaciones vienen dentro de las afiliaciones
        afiliaciones_el = autor.find_all("affiliation") 

        for aff in afiliaciones_el:
            org_data = {"departamento": "", "institucion": ""}
            org_names = aff.find_all("orgName")

            for org in org_names:
                tipo_org = org.get("type")
                texto_org = org.get_text(strip=True)

                if tipo_org == "department":
                    org_data["departamento"] = (
                        f"{org_data['departamento']}, {texto_org}"
                        if org_data["departamento"]
                        else texto_org
                    )
                elif tipo_org == "institution":
                    org_data["institucion"] = (
                        f"{org_data['institucion']}, {texto_org}"
                        if org_data["institucion"]
                        else texto_org
                    )

            country_el = aff.find("country")
            pais = country_el.get_text(strip=True) if country_el else None

            # Guardamos la afiliación si contiene al menos algún dato organizativo
            if org_data["departamento"] or org_data["institucion"]:
                afiliaciones.append(
                    {
                        "institucion": org_data["institucion"],
                        "departamento": org_data["departamento"],
                        "pais": pais,
                    }
                )
                
        # Establecemos la información en formato JSON más práctico para trabajar con ello. 
        autor_json = {
            "nombre_completo": f"{nombre} {apellido}".strip(),
            "nombre": nombre,
            "apellido": apellido,
            "orcid": orcid,
            "afiliaciones": afiliaciones,
        }
        lista_autores.append(autor_json)
        
    # Devolvemos el json con la librería de json.
    return json.dumps(lista_autores, ensure_ascii=False, indent=4)
