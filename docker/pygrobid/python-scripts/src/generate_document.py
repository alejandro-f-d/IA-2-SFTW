def generate_links_report(diccionario_links, report_path):
    """
    Crear reporte markdown con la información de los documentos.
    """
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Reporte de los documentos\n")
        f.write(f"Total: {len(diccionario_links)}\n\n")
        f.write("---\n\n")

        for doc_name, links in diccionario_links.items():
            f.write(f"## Documento: {doc_name}\n")
            
            if not links:
                f.write("*No se han encontrado enlaces.*\n\n")
            else:
                f.write(f"**Enlaces: {len(links)}:**\n")
                for link in links:
                    f.write(f"- [{link}]({link})\n")
                f.write("\n")
            
            f.write("---\n") 

    print(f"Reporte de links generado con éxito")
