import os
def save_content(content, save_path):
    try:
        folder = os.path.dirname(save_path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Archivo guardado: {save_path}")
        return True
    except Exception as e:
        print(f"Error al salvar en {save_path}: {e}")
        return False
