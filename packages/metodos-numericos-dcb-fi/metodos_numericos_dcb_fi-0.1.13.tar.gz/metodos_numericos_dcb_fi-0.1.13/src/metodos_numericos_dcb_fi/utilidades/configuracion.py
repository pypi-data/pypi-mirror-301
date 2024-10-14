# ------------------- Importar bibliotecas -------------------
import string

# -------------------  Definir constantes -------------------
colores = ['blue', 'red', 'green', 'orange', 'purple', 'magenta', 'yellow', 'black']
letras_latinas = list(string.ascii_letters)
letras_griegas = [chr(i) for i in range(0x3b1, 0x3ca)] + [chr(i) for i in range(0x3ca, 0x3d6)] + [chr(i) for i in range(0x391, 0x3a2)] + [chr(i) for i in range(0x3a3, 0x3aa)] + [chr(i) for i in range(0x3aa, 0x3b1)]
maxIteraciones = 20
idioma = 'es'
text = {}
