# ------------------- Importar módulos -------------------
from metodos_numericos_dcb_fi.utilidades.validacion import validarTipo
from metodos_numericos_dcb_fi.utilidades.configuracion import letras_griegas, letras_latinas

# ------------------- Importar bibliotecas -------------------
import sympy as sp
from sympy.abc import x
import numpy as np

# ------------------- Crear la clase funcion -------------------
class funcion:
    """
    Clase 'funcion'

    Esta clase representa una función matemática. Permite almacenar los valores de x e y de la función, así como también realizar operaciones y cálculos relacionados con la función.

    Atributos:
    - valores_x (list): Lista que almacena los valores de x de la función.
    - valores_y (list): Lista que almacena los valores de y de la función.
    - f_text (str): Texto de la función.
    - f (function): Función simbólica de sympy.
    - f_ (function): Función lambda de numpy.
    """
    def __init__(self) -> None:
        """
    Inicializa una instancia de la clase 'funcion'.

    Parámetros:
    - metodo (str): El método para el cual se va a utilizar la función.

    Atributos:
    - valores_x (list): Lista que almacena los valores de x de la función.
    - valores_y (list): Lista que almacena los valores de y de la función.
    - f_text (str): Texto de la función.
    - f (function): Función simbólica de sympy.
    - f_ (function): Función lambda de numpy.
    """ 
        self.valores_x = []
        self.valores_y = []
        self.limites = []
        self.f_text = None # Texto
        self.f = None # Lambdify
        self.f_ = None # Sympify
    
    def setFuncion(self, f:str, var:str='x'):
        '''
    Establece la función de la instancia actual con la función especificada.

    Parámetros:
        - f (str): La función matemática especificada como una cadena de texto.

    Excepciones:
        - Exception: Si ocurre un error al establecer la función.

    Retorno:
        - None

    Ejemplo:
        setFuncion("x**2 + 3*x - 2")
    '''
        validarTipo(f, str)
        f = f.replace('^', '**').replace('sen', 'sin').replace('tg', 'tan').replace('ctg', 'cot')
        self.f_text = f
        try:
            self.f_ = sp.sympify(self.f_text)
        except:
            raise Exception(f'La funcion ingresada no cumple con las reglas y no se puede procesar.\nFuncion ingresada: {self.f_text}.')
        for _ in var:
            if _ not in letras_latinas and _ not in letras_griegas:
                raise Exception(f'Las variables deben ser letras latinas o griegas.\nVariable ingresada: {_}.')
        self.f = sp.lambdify(var, self.f_, 'numpy')

    def agregarLimites(self, x_i:float, x_f:float):
        validarTipo(x_i, (int, float))
        validarTipo(x_f, (int, float))
        self.limites = [(x_i, x_f)]
# ------------------- Funciones -------------------
def convertirFuncion(f:str, var:str='x')->funcion:
    '''
    Convierte una función matemática especificada como una cadena de texto en una instancia de la clase 'funcion'.

    Parámetros:
        f (str): La función matemática especificada como una cadena de texto.
        var (str): La variable de la función. Por defecto es 'x'.

    Excepciones:
        No se generan excepciones.

    Retorno:
        Una instancia de la clase 'funcion' con la función especificada.

    Ejemplo:
        f = convertirFuncion("x**2 + 3*x - 2")
    '''
    f_ = funcion()
    f_.setFuncion(f, var)
    return f_

def leerFuncion()->funcion:
    '''
    Lee una función matemática ingresada por el usuario y la asigna a una instancia de la clase 'funcion'.

    Parámetros:
        f (str): la funcion en forma de scadena que se va a asignar a la instancia de la clase 'funcion'. Por defecto es una cadena vacía.

    Excepciones:
        No se generan excepciones.

    Retorno:
        Una instancia de la clase 'funcion' con la función asignada.

    Ejemplo:
        f = leerFuncion()
    '''
    f_ = funcion()
    print('Reglas para ingresar funciones:\n1.- La funcion debe de depender solo de una variable\n2.- Para ingresar seno escriba sin(argumento)\n3.- Para ingresar el numero de Euler escriba exp(1)\n4.- Para ingresar el numero pi escriba pi\n5.- La funcion se va a construir en funcion de x.')
    f = input('Ingrese la función: ')
    f_.setFuncion(f)
    return f_
    
def leerTolerancia(t:str='')->float:
    '''
    Lee la tolerancia ingresada por el usuario y la devuelve como un número de punto flotante.

    Parámetros:
        No recibe ningún parámetro.

    Excepciones:
        ValueError: Si la tolerancia ingresada es menor o igual a cero.

    Retorno:
        float: La tolerancia ingresada por el usuario.

    Ejemplo:
        leerTolerancia()
    '''
    if t != '':
        return float(t)
    print('La tolerancia debe ser un número real mayor que cero.')
    tol = float(input('Ingrese la tolerancia: '))
    if tol <= 0:
        raise ValueError(f'La tolerancia debe ser un número mayor que cero.\nTolerancia ingresada: {tol}')
    return tol

def leerPolinomio(c:list=[]):
    '''
    Función: leerPolinomio

    Descripción:
    Esta función se utiliza para leer un polinomio desde la entrada estándar. Solicita al usuario el grado del polinomio y los coeficientes correspondientes, validando que los valores ingresados sean del tipo correcto.

    Parámetros:
        No recibe ningún parámetro.

    Excepciones:
        ValueError: se lanza una excepción si el grado del polinomio es menor o igual a cero.
        Exception: se lanza una excepción si ocurre un error al validar el tipo de los valores ingresados.

    Retorno:
        Una lista de coeficientes del polinomio.

    Ejemplo de uso:
        leerPolinomio()
    '''
    if len(c) > 0:
        return c
    print('Reglas para ingresar polinomios:\n1.- EL grado del polinomio debe ser un numero entero mayor a 0.\n2.- Los coeficientes deben ser números reales.\n3.- Al menos 1 de los coeficientes debe ser distinto de cero.')
    grado = int(input('Ingrese el grado del polinomio: '))
    if grado <= 0:
        raise ValueError(f'El grado del polinomio debe ser un número entero mayor a 0.\nGrado ingresado: {grado}')
    coeficientes = []
    contador = 0
    for i in range(grado + 1):
        coeficiente = float(input(f'Ingrese los coeficientes del grado {str(grado-i)}: '))
        if i == contador and coeficiente == 0:
            contador += 1
        else:
            coeficientes.append(coeficiente)
    if len(coeficientes) < 2:
        raise ValueError('El grado del polinomio debe ser al menos 1.\nGrado ingresado: 0.')
    return coeficientes

def leerMatriznxn()->np.array:
    """
    Lee una matriz cuadrada de tamaño nxn y la devuelve como un array de numpy.

    Parámetros:
        No recibe ningún parámetro.

    Excepciones:
        ValueError: Si el valor de n es menor o igual a cero.
        Exception: Si ocurre un error al validar el tipo de los valores ingresados.

    Retorno:
        np.array: La matriz cuadrada de tamaño nxn.

    Ejemplo:
        matriz = leerMatriznxn()
    """
    print('Reglas para ingresar una matriz:\n1.- La matriz debe ser cuadrada.\n2.- Los elementos deben ser números reales.')
    n = input('Ingrese el tamaño de la matriz cuadrada (debe ser un numero entero mayor que 0): ')
    validarTipo(n, int)
    if n <= 0:
        raise ValueError(f'El tamaño de la matriz debe ser un número entero mayor que 0.\nTamaño ingresado: {n}.')
    matriz = []
    for i in range(n):
        fila = []
        for j in range(n):
            elemento = input(f'Ingrese el elemento {i+1},{j+1}: ')
            validarTipo(elemento, (int, float))
            fila.append(elemento)
        matriz.append(fila)
    return np.array(matriz)

def leerVector(n:int, reglas:str='')->np.array:
    """
    Lee un vector de números ingresados por el usuario.

    Parámetros:
    - n: int, la longitud del vector.
    - reglas: str opcional, reglas adicionales para ingresar los elementos del vector.

    Excepciones:
    - Exception: Si ocurre un error al validar el tipo de los valores ingresados.

    Retorno:
    - np.array, un arreglo numpy que contiene los elementos ingresados por el usuario.

    Ejemplo de uso:
    leerVector(5, 'Ingrese números enteros o decimales: ')
    """
    print('Reglas para ingresar un vector:\n1.- Los elementos deben ser números reales.')
    vector = []
    for i in range(n):
        elemento = input(f'Ingrese el elemento {i+1}: ')
        validarTipo(elemento, (int, float))
        vector.append(elemento)
    return np.array(vector)

def leerVectorKrilov(n:int)->np.array:
    """
    Función: leerVectorKrilov

    Descripción:
    Esta función se utiliza para leer un vector de números ingresados por el usuario para el metodo de Krilov.

    Parámetros:
    - n: int, la longitud del vector.

    Excepciones:
    - Exception: Si ocurre un error al validar el tipo de los valores ingresados.

    Retorno:
    - np.array, un arreglo numpy que contiene los elementos ingresados por el usuario.

    Ejemplo de uso:
    leerVectorKrilov(5)
    """
    print('Si desea utilizar el vector de Krilov por defecto ingrese 0. En caso contrario ingrese 1.')
    opcion = input('Ingrese la opción deseada: ')
    if opcion == '0':
        vector = np.zeros(n) # Vector de ceros de tamaño n
        vector[0] = 1 # Primer elemento igual a 1
    else:
        vector = leerVector(n, 'n2.- Al menos un elemento debe ser distinto de cero.')
        # si todos los elementos son cero
        if np.all(vector == 0):
            print('Al menos un elemento debe ser distinto de cero.')
            vector = leerVectorKrilov(n)
    return vector

def leerDatosLU()->tuple[np.array, np.array]:
    '''
    Lee los datos necesarios para realizar la factorización LU de una matriz y su vector de términos independientes.

    Parámetros:
        No recibe ningún parámetro.

    Excepciones:
        ValueError: Si el valor de n es menor o igual a cero.
        Exception: Si ocurre un error al validar el tipo de los valores ingresados.

    Retorno:
        tuple: Una tupla que contiene la matriz y el vector ingresados por el usuario.

    Ejemplo:
        matriz, vector = leerDatosLU()
    '''
    print('Matriz de coeficientes:')
    matriz = leerMatriznxn()
    print('Vector de terminos independientes:')
    vector = leerVector(len(matriz))
    return matriz, vector
