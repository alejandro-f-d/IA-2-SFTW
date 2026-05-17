from transformers import pipeline
import re

# Cargamos el modelo NER de HuggingFace
ner_pipeline = pipeline(
    "ner",
    model="Jean-Baptiste/roberta-large-ner-english",
    aggregation_strategy="simple"
)

def extract_project_ids(text):
    """
    Extrae IDs de proyectos usando expresiones regulares.
    Detecta patrones comunes como #41871214, BK20200113, N00014-21-1-2437
    """
    patrones = [
        r'#\s*\d+',                      # #41871214
        r'\b[A-Z]{2,}\d{6,}\b',          # BK20200113
        r'\b\w+\-\d+\-\d+\-\d+\-\d+\b'   # N00014-21-1-2437
    ]
    
    ids = []
    for patron in patrones:
        encontrados = re.findall(patron, text)
        ids.extend(encontrados)
    
    # Eliminamos duplicados
    return list(set(ids))




def fusionar_entidades(organizaciones, texto):
    
    """
    Elimina acrónimos duplicados de la lista de organizaciones.
    Un acrónimo se detecta cuando aparece entre paréntesis
    o seguido de un guión en el texto original.
    """
    
    resultado = []
    vistas = []
    for org in organizaciones:
        # Patrón 1: aparece entre paréntesis 
        es_acronimo_parentesis = f"({org})" in texto
        # Patrón 2: aparece seguido de guión 
        es_acronimo_guion = f"{org} -" in texto and any(len(otra) > len(org) for otra in organizaciones)
        
         # Comprobamos si ya hemos visto esta entidad antes
        es_duplicado = org in vistas
        
        
        # Solo añadimos si no es acrónimo ni duplicado
        if not es_acronimo_parentesis and not es_acronimo_guion and not es_duplicado:
            resultado.append(org)
            vistas.append(org)
    
    return resultado


def extract_entities(text):
    
    """
    Extrae personas y organizaciones de un texto usando el modelo NER.
    Devuelve dos listas: personas, organizaciones, lugares y project_ids
    """
    
    if not text:
        return [], [], [],[]
    
    # Aplicamos el modelo NER sobre el texto
    resultados = ner_pipeline(text)
    
    personas = []
    organizaciones = []
    lugares = []
    
    for entidad in resultados:
        nombre = entidad["word"].strip()
        confianza = entidad["score"]
        tipo = entidad["entity_group"]
        
        # Filtramos entidades con confianza menor al 85%
        if confianza < 0.85:
            continue
        
        if tipo == "PER":
            personas.append(nombre)
        elif tipo == "ORG":
            organizaciones.append(nombre)
        elif tipo == "LOC":  
            lugares.append(nombre)
            
    organizaciones = fusionar_entidades(organizaciones, text)
    project_ids = extract_project_ids(text)
    
    
    return personas, organizaciones, lugares, project_ids