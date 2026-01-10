import math
#Llamo mi funcion que transforma strings a funciones evaluables
from metodos.usoGeneralFunicones import usoVariablesSympy as uv


#*--------------------------------------------------------------------------------------------------------*

# Metodo de biseccion

# Agregar a metodos/metodosCerrados.py

def Biseccion(f_input, a, b, tol=1e-7, max_iter=50):
    """
    Versión para GUI del Método de Bisección.
    Retorna (raiz, historial_lista)
    """
    f_eval = uv.deStringAFuncionEvaluable(f_input)

    # Validación inicial de signos
    if f_eval(a) * f_eval(b) >= 0:
        raise ValueError("f(a) y f(b) deben tener signos opuestos.")

    historial_iteraciones = []
    x_anterior = a

    for i in range(1, max_iter + 1):
        x_m = (a + b) / 2
        f_m = f_eval(x_m)

        # Cálculo del error absoluto (distancia entre límites o cambio en x)
        error = abs(b - a) / 2 if i > 1 else abs(x_m - x_anterior)

        # Guardamos: It, Lim. Inf, Lim. Sup, xm, f(xm), Error
        historial_iteraciones.append((
            i,
            f"{a:.10f}",
            f"{b:.10f}",
            f"{x_m:.10f}",
            f"{f_m:.10e}",
            f"{error:.10e}" if i > 1 else "---"
        ))

        if abs(f_m) < 1e-15 or error < tol:
            return x_m, historial_iteraciones

        # Cambio de límites
        if f_eval(a) * f_m < 0:
            b = x_m
        else:
            a = x_m

        x_anterior = x_m

    return (a + b) / 2, historial_iteraciones

def biseccion(funcion, limiteInferior, limiteSuperior, numIteraciones):

    #Los limties deben ser de signos opuestos
    if funcion(limiteInferior) * funcion(limiteSuperior) > 0:
        return None
    
    #pone la media en 0
    media = 0

    #Si el numero de iteraciones es muy bajo calcula uno desente
    if numIteraciones < 10:
        numIteraciones = math.ceil(math.log2((limiteSuperior - limiteInferior) / (10**(-7))))

    #Impresion de la tabla de resultados
    print(f"\n{'Iteración':<10} | {'lim. Inf':<12} | {'lim. Sup':<12} | {'Media (x)':<15} | {'Error (%)':<12}")
    print("-" * 70)

    for i in range(numIteraciones):
        media = (limiteInferior+limiteSuperior)/2
        error = abs((limiteSuperior - limiteInferior) / media) * 100 if media != 0 else 0

        #Imprime la tabla
        print(f"{i+1:<10} | {limiteInferior:<12.7f} | {limiteSuperior:<12.7f} | {media:<15.7f} | {error:<12.7f}")

        if funcion(media) == 0:
            return media
        elif funcion(media)*funcion(limiteInferior) > 0:
            limiteInferior = media
        else:
            limiteSuperior = media
    return media

def biseccionTerminal():
    funcion_input = input("Ingrese la función: ")
    funcion_evaluable = uv.deStringAFuncionEvaluable(funcion_input)
    limiteInferiorInput = float(input("Ingrese el limite inferior: "))
    limiteSuperiorInput = float(input("Ingrese el limite superior: "))
    numIteracionesInput = int(input("Ingrese el numero de iteraciones a ejecutar: "))
    num = biseccion(funcion_evaluable, limiteInferiorInput, limiteSuperiorInput, numIteracionesInput)

    if num == None: print("No se pudo encontrar un 0 en esos limites")
    elif num != None: print("La raiz encontrada es", num)
    else: print("ERROR: Dato no esperado")

#*--------------------------------------------------------------------------------------------------------*

# Metodo de falsa posicion

# Agregar a metodos/metodosCerrados.py

def FalsaPosicion(f_input, a, b, tol=1e-7, max_iter=50):
    """
    Versión para GUI del Método de Falsa Posición.
    Retorna (raiz, historial_lista)
    """
    f_eval = uv.deStringAFuncionEvaluable(f_input)

    # Los límites deben ser de signos opuestos
    if f_eval(a) * f_eval(b) >= 0:
        raise ValueError("f(a) y f(b) deben tener signos opuestos.")

    historial_iteraciones = []

    # Cálculo inicial de Xr
    fa = f_eval(a)
    fb = f_eval(b)
    xr = (a * fb - b * fa) / (fb - fa)
    xr_anterior = xr

    for i in range(1, max_iter + 1):
        fa = f_eval(a)
        fb = f_eval(b)

        # Fórmula de Falsa Posición
        xr = (a * fb - b * fa) / (fb - fa)
        fxr = f_eval(xr)

        # Error relativo porcentual aproximado
        error = abs((xr - xr_anterior) / xr) * 100 if xr != 0 else 0

        # Guardamos: It, Lim. Inf, Lim. Sup, xr, f(xr), Error (%)
        historial_iteraciones.append((
            i,
            f"{a:.10f}",
            f"{b:.10f}",
            f"{xr:.10f}",
            f"{fxr:.10e}",
            f"{error:.7f}%" if i > 1 else "---"
        ))

        if abs(fxr) < 1e-15 or (i > 1 and error < tol):
            return xr, historial_iteraciones

        # Cambio de límites basado en el signo
        if fa * fxr > 0:
            a = xr
        else:
            b = xr

        xr_anterior = xr

    return xr, historial_iteraciones

def falsa_posicion(funcion, limiteInferior, limiteSuperior, numIteraciones):

    #Los limties deben ser de signos opuestos
    if funcion(limiteInferior) * funcion(limiteSuperior) > 0:
        return None
    
    #Si el numero de iteraciones es muy bajo calcula uno desente
    if numIteraciones < 10:
        numIteraciones = math.ceil(math.log2((limiteSuperior - limiteInferior) / (10**(-7))))

    #Variable de la falsa posicion
    Xr = (limiteInferior*funcion(limiteSuperior) - limiteSuperior*funcion(limiteInferior)) / (funcion(limiteSuperior) - funcion(limiteInferior))
    Xr_anterior = Xr;

    #Impresion de la tabla de resultados
    print(f"\n{'Iteración':<10} | {'lim. Inf':<12} | {'lim. Sup':<12} | {'Xr (x)':<15} | {'Error (%)':<12}")
    print("-" * 70)

    for i in range(numIteraciones):
        Xr = (limiteInferior*funcion(limiteSuperior) - limiteSuperior*funcion(limiteInferior)) / (funcion(limiteSuperior) - funcion(limiteInferior))
        error = abs((Xr - Xr_anterior) / Xr) * 100 if Xr != 0 else 0

        #Imprime la tabla
        print(f"{i+1:<10} | {limiteInferior:<12.7f} | {limiteSuperior:<12.7f} | {Xr:<15.7f} | {error:<12.7f}")

        if funcion(Xr) == 0:
            return Xr
        elif funcion(Xr)*funcion(limiteInferior) > 0:
            limiteInferior = Xr
        else:
            limiteSuperior = Xr
        
        Xr_anterior = Xr
    return Xr

def falsaPosicionTerminal():
    funcion_input = input("Ingrese la función: ")
    funcion_evaluable = uv.deStringAFuncionEvaluable(funcion_input)
    limiteInferiorInput = float(input("Ingrese el limite inferior: "))
    limiteSuperiorInput = float(input("Ingrese el limite superior: "))
    numIteracionesInput = int(input("Ingrese el numero de iteraciones a ejecutar: "))
    num = falsa_posicion(funcion_evaluable, limiteInferiorInput, limiteSuperiorInput, numIteracionesInput)

    if num == None: print("No se pudo encontrar un 0 en esos limites")
    elif num != None: print("La raiz encontrada es", num)
    else: print("ERROR: Dato no esperado")

#*--------------------------------------------------------------------------------------------------------*