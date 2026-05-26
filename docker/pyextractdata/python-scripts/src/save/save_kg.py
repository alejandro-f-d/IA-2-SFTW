from rdflib import Graph, Literal, URIRef, Namespace
from rdflib.namespace import RDF, RDFS

# Namespace base para todas las URIs del proyecto
EX = Namespace("http://ia-practica-2.org/")

def build_kg(papers_data):
    
    """
    Construye un grafo RDF con los datos extraídos de los papers.
    Cada paper se relaciona con sus personas, organizaciones y lugares
    mediante la propiedad acknowledges.
    """
    g = Graph()
    g.bind("ex", EX)
    
    for paper in papers_data:
        paper_uri = URIRef(EX + f"paper/{paper['paper_id']}")
        # Declaramos que es un Paper
        g.add((paper_uri, RDF.type, EX.Paper))
        
        # Añadimos las personas detectadas
        for nombre in paper["personas"]:
            uri = URIRef(EX + f"person/{nombre.replace(' ', '_')}")
            g.add((uri, RDF.type, EX.Person))
            g.add((uri, RDFS.label, Literal(nombre)))
            g.add((paper_uri, EX.acknowledges, uri))
        # Añadimos las organizaciones detectadas
        for nombre in paper["organizaciones"]:
            uri = URIRef(EX + f"organization/{nombre.replace(' ', '_')}")
            g.add((uri, RDF.type, EX.Organization))
            g.add((uri, RDFS.label, Literal(nombre)))
            g.add((paper_uri, EX.acknowledges, uri))
        # Añadimos los lugares detectados
        for nombre in paper["lugares"]:
            uri = URIRef(EX + f"location/{nombre.replace(' ', '_')}")
            g.add((uri, RDF.type, EX.Location))
            g.add((uri, RDFS.label, Literal(nombre)))
            g.add((paper_uri, EX.acknowledges, uri))
        # Añadimos los IDs de proyectos detectados
        for pid in paper["project_ids"]:
            uri = URIRef(EX + f"project/{pid.replace(' ', '_').replace('#', '')}")
            g.add((uri, RDF.type, EX.Project))
            g.add((uri, RDFS.label, Literal(pid)))
            g.add((paper_uri, EX.hasProject, uri))
    
    return g

def save_kg(g, output_path):
    g.serialize(output_path, format="json-ld")
    print(f"KG guardado en: {output_path}")
