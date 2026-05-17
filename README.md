# IA-2-SFTW
Proyecto 2 de IA y Software Abierto.
Herramienta de descubrimiento de citación y autores (provisional)

Para el apartado de NER, si se quiere usar sin Docker:
Crear carpeta `input`y `output` en `IA-2-SFTW\docker\pygrobid`. En `input`, colocar papers. 
`INPUT_DIR = os.getenv('INPUT_DIR', '../../pygrobid/output')`
`OUTPUT_DIR = os.getenv('OUTPUT_DIR', '../output')`
Y ejecutamos en la dirección: `\IA-2-SFTW\docker\pyextractdata\python-scripts` con el comando `python main.py`.

Para usar con Docker: 
`INPUT_DIR = os.getenv('INPUT_DIR', '/input')`
`OUTPUT_DIR = os.getenv('OUTPUT_DIR', '/output')`


Formado por los siguientes integrantes:
Janele Ángeles Sandonas Feliz,
Alejandro Fisac Delgado,
Juan Sebastian Torres Alvarez,
Andrés Voronovskyy Knyshayid
