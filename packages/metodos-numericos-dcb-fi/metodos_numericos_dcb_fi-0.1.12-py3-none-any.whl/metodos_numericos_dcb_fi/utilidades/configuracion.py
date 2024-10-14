# ------------------- Importar bibliotecas -------------------
from pathlib import Path
import json
import string
import subprocess
import importlib.metadata
from packaging import version

# -------------------  Definir constantes -------------------
colores = ['blue', 'red', 'green', 'orange', 'purple', 'magenta', 'yellow', 'black']
letras_latinas = list(string.ascii_letters)
letras_griegas = [chr(i) for i in range(0x3b1, 0x3ca)] + [chr(i) for i in range(0x3ca, 0x3d6)] + [chr(i) for i in range(0x391, 0x3a2)] + [chr(i) for i in range(0x3a3, 0x3aa)] + [chr(i) for i in range(0x3aa, 0x3b1)]
maxIteraciones = 20
idioma = 'es'
text = {}

# -------------------  Definir funciones -------------------
def leerTextos()->None:
    """
    Lee el archivo de texto correspondiente al idioma especificado y carga su contenido en la variable global 'text'.

    Parámetros:
        No recibe ningún parámetro.

    Excepciones:
        FileNotFoundError: Si no se encuentra el archivo de texto correspondiente al idioma especificado.
        json.JSONDecodeError: Si ocurre un error al decodificar el archivo de texto.

    Retorno:
        No retorna ningún valor.

    Ejemplo:
        leer_textos()
    """
    current_dir = Path(__file__).resolve().parent
    text_file = current_dir / '..' / 'data' / f'text_{idioma}.json'
    global text
    try:
        with open(text_file, 'r', encoding='utf-8') as file:
            text = json.load(file)
    except FileNotFoundError:
        raise Exception(f'No se puede leer el archivo text_{idioma}.json\nCan\'t read the file text_{idioma}.json')
    except json.JSONDecodeError:
        raise Exception(f'Error al decodificar el archivo text_{idioma}.json\nFailed to decode the file text_{idioma}.json')
