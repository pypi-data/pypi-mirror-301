# ------------------- Importar módulos -------------------

# ------------------- Funciones -------------------
def validarTipo(valor:any, tipo:type)->None:
    """
    Función: validarTipo

    Descripción:
    Esta función se utiliza para validar si un valor dado es de un tipo específico. Si el valor no es del tipo especificado, se lanza una excepción.

    Parámetros:
    - valor: cualquier valor que se desee validar.
    - tipo: el tipo específico que se desea comprobar.

    Excepciones:
    - Exception: se lanza una excepción si el valor no es del tipo especificado.

    Retorno:
    - None

    Ejemplo de uso:
    validarTipo(5, int)
    """
    if not (isinstance(valor, tipo)):
        raise Exception(f'Los valores de entrada deben ser de tipo: {tipo}.\nTipo de valor ingresado: {type(valor)}.')

def validarLista(lista:list, tipo:type)->None:
    """
    Función: validarLista

    Descripción:
    Esta función se utiliza para validar si una lista dada contiene solo valores de un tipo específico. Si algún valor en la lista no es del tipo especificado, se lanza una excepción.

    Parámetros:
    - lista: una lista que se desea validar.
    - tipo: el tipo específico que se desea comprobar.

    Excepciones:
    - Exception: se lanza una excepción si algún valor en la lista no es del tipo especificado.

    Retorno:
    - None

    Ejemplo de uso:
    validarLista([1, 2, 3], int)
    """
    if not all(isinstance(x, tipo) for x in lista):
        raise Exception(f'Todos los valores de la lista deben ser de tipo: {tipo}.')

def validarDatosBiseccion(x_i:float, x_s:float, tol:float)->tuple[float, float, float]:
    '''
    Función: validarDatosBiseccion

    Descripción:
    Esta función se utiliza para validar los datos de entrada para el método de bisección. Verifica si los valores de x_i, x_s y tol son números de tipo float. Además, comprueba si x_i es menor que x_s y si tol es mayor que cero. Si alguna de estas validaciones falla, se lanza una excepción.

    Parámetros:
    - x_i: número de tipo float que representa el límite inferior del intervalo.
    - x_s: número de tipo float que representa el límite superior del intervalo.
    - tol: número de tipo float que representa la tolerancia.

    Excepciones:
    - ValueError: se lanza una excepción si x_i es mayor o igual que x_s, o si tol es menor o igual que cero.
    - Exception: se lanza una excepción si ocurre un error al validar el tipo de los valores ingresados.

    Retorno:
    - Una tupla que contiene los valores de x_i, x_s y tol.

    Ejemplo de uso:
    validarDatosBiseccion(1.0, 2.0, 0.001)
    '''
    validarTipo(x_i, (int, float))
    validarTipo(x_s, (int, float))
    if x_i >= x_s:
        raise ValueError(f'El valor de x_i debe ser menor que el de x_s.\nValores ingresados: x_i = {x_i}, x_s = {x_s}.')
    validarTipo(tol, (int, float))
    if tol <= 0:
        raise ValueError(f'La tolerancia debe ser un número mayor que cero.\nTolerancia ingresada: {tol}.')
    return x_i, x_s, tol

def validarDatosNR(x_0:str, tol:str):
    '''
    Función: validarDatosNR

    Descripción:
    Esta función se utiliza para validar los datos de entrada para el método Newton Raphson. Verifica si los valores de x_0 y tol son de tipo int o float, y si la tolerancia es mayor que cero. Si alguno de los valores no cumple con estas condiciones, se lanza una excepción.

    Parámetros:
    - x_0: valor inicial para el método.
    - tol: tolerancia para el método.

    Excepciones:
    - ValueError: se lanza una excepción si la tolerancia es menor o igual a cero.
    - Exception: se lanza una excepción si ocurre un error al validar el tipo de los valores ingresados.

    Retorno:
    - Tuple: una tupla que contiene los valores de x_0 y tol.

    Ejemplo de uso:
    validarDatosN_R(5, 0.001)
    '''
    validarTipo(x_0, (int, float))
    validarTipo(tol, (int, float))
    if tol <= 0:
        raise ValueError(f'La tolerancia debe ser un número mayor que cero.\nTolerancia ingresada: {tol}.')
    return x_0, tol

def validarTiempo(t_0:float, t_f:float):
    '''
    Función: validarTiempo

    Descripción:
    Esta función se utiliza para validar los datos de entrada para el cálculo del tiempo de ejecución de un método numérico. Verifica si t_f es mayor que t_0. Si alguno de los valores no cumple con estas condiciones, se lanza una excepción.

    Parámetros:
    - t_0: tiempo inicial.
    - t_f: tiempo final.

    Excepciones:
    - ValueError: se lanza una excepción si t_f es menor o igual que t_0.
    - Exception: se lanza una excepción si ocurre un error al validar el tipo de los valores ingresados.

    Retorno:
    - None

    Ejemplo de uso:
    validarTiempo(0.0, 10.0)
    '''
    if t_f <= t_0:
        raise ValueError(f'El tiempo final debe ser mayor que el tiempo inicial.\nValores ingresados: t_0 = {t_0}, t_f = {t_f}.')