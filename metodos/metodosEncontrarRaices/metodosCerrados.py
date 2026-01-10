import math
#Llamo mi funcion que transforma strings a funciones evaluables
from usoGeneralFunicones import usoVariablesSympy as uv


#*--------------------------------------------------------------------------------------------------------*

# Metodo de biseccion

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