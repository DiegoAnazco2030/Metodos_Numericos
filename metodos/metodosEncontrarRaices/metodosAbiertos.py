import sympy as sp
import math
from typing import Callable
#Llamo mi funcion que transforma strings a funciones evaluables
from metodos.usoGeneralFunicones import usoVariablesSympy as uv


#*--------------------------------------------------------------------------------------------------------*

# Iteracion simple de punto fijo

def encontrarGOptima(f_simbolica: sp.Expr, x0: float) -> tuple[Callable[[float], float], sp.Expr] | tuple[None, None]:
    """
    Intenta encontrar una función de iteración g(x) tal que |g'(x0)| < 1 
    para garantizar convergencia local.
    """
    x = sp.symbols('x')
    f_prima = sp.diff(f_simbolica, x)
    
    try:
        # 1. Evaluar simbólicamente
        f_prima_x0_sym = f_prima.evalf(subs={x: x0})
        
        # 2. Convertir a un float de Python INMEDIATAMENTE.
        #    Pylance puede quejarse de ESTA línea, pero es la correcta.
        f_prima_x0_float = float(f_prima_x0_sym)
        
        # 3. Ahora, usar SIEMPRE el float de Python para las funciones de 'math' y 'abs'
        if not math.isfinite(f_prima_x0_float): # <-- Usa el float
            print(f"[ERROR] No se pudo evaluar f'({x0}). Resultado no finito.")
            return None, None
            
    except Exception as e:
        print(f"[ERROR] No se pudo evaluar la derivada f'({x0}): {e}")
        return None, None # No se pudo evaluar la derivada
        
    # Usa el float para la comparación
    if abs(f_prima_x0_float) < 1e-10:
        C_optimo = -1.0
    else:
        # Usa el float para la división
        C_optimo = -1.0 / f_prima_x0_float

    # 4. Al crear la g_simbolica, usamos el C_optimo (float)
    #    SymPy es lo suficientemente inteligente para convertirlo.
    #    Mi sugerencia anterior de sp.Float() confundió más a Pylance.
    g_simbolica = x + C_optimo * f_simbolica
    
    # Verificar el criterio de convergencia
    g_prima_simbolica = sp.diff(g_simbolica, x)
    try:
        # --- Aplicamos la misma lógica aquí ---
        g_prima_x0_sym = g_prima_simbolica.evalf(subs={x: x0})
        g_prima_x0_float = float(g_prima_x0_sym) # Convertir a float
        
        if not math.isfinite(g_prima_x0_float): # Usar float
            pass # No podemos verificar, pero continuamos
        else:
            g_prima_x0_abs = abs(g_prima_x0_float) # Usar float
            print(f"\n[INFO] g(x) generada. |g'({x0})| = {g_prima_x0_abs:.4e}")
            
            # Ahora es una simple comparación float >= int
            if g_prima_x0_abs >= 1:
                print("[ALERTA] La g(x) generada tiene |g'(x0)| >= 1. Es posible que diverja.")
                
    except:
        pass # No se pudo calcular |g'(x0)|, continuamos con la g generada
    g_evaluable = sp.lambdify(x, g_simbolica, "math")
    return g_evaluable, g_simbolica

def puntoFijo(g: Callable[[float], float], x0: float, tol: float = 1e-6, max_iter: int = 50) -> float | None:
    """
    Método de Iteración Simple de Punto Fijo, con chequeo de divergencia.
    Busca una raíz r tal que g(r) = r.
    """
    x_prev = x0
    error_prev = float('inf')  # Inicializamos el error anterior
    divergence_count = 0       # Contador para detectar crecimiento de error
    
    print(f"\n{'Iteración':<12} {'x':<20} {'Error':<20}")
    print("-" * 52)
    print(f"{0:<12} {x0:<20.10f} {'---':<20}")
    
    for i in range(1, max_iter + 1):
        try:
            x_new = g(x_prev)
        except Exception as e:
            print(f"\n¡Error! Falló la evaluación de g(x) en x={x_prev:.8f}: {e}")
            return x_prev

        # 1. CHEQUEO DE DIVERGENCIA (Valores inválidos)
        if not math.isfinite(x_new): # Chequea si es NaN, inf, -inf
            print(f"\n¡Divergencia detectada! x_new es un valor no finito ({x_new}).")
            return x_prev
        
        error = abs(x_new - x_prev)
        
        print(f"{i:<12} {x_new:<20.10f} {error:<20.10e}")
        
        # 2. CRITERIO DE CONVERGENCIA (Parada)
        if error < tol:
            print(f"\n¡Convergencia alcanzada en {i} iteraciones!")
            return x_new
            
        # 3. CHEQUEO DE DIVERGENCIA (Error creciente)
        if error > error_prev:
            divergence_count += 1
        else:
            divergence_count = 0 # Reiniciar si el error disminuye
        
        if divergence_count >= 5 and error > 10 * tol:
            # Si el error crece consistentemente durante 5 iteraciones y aún es grande
            print(f"\n¡Divergencia detectada! Error creciente durante 5 iteraciones consecutivas.")
            return x_new
        
        x_prev = x_new
        error_prev = error
        
    print(f"\n¡Advertencia! El método no convergió después de {max_iter} iteraciones.")
    return None

def puntoFijoTerminal():
    print("\n--- Método de Iteración Simple de Punto Fijo ---")
    try:
        # Pedimos f(x) para poder comprobar la raíz al final
        f_input = input("Ingrese la función f(x) (para f(x)=0): ")
        f_eval = uv.deStringAFuncionEvaluable(f_input)
        f_simbolica = uv.deStringAFuncionSimbolica(f_input)

        opcion = input("¿Desea ingresar g(x) manualmente? (s/n): ").lower()
        
        x0 = float(input("Ingresa la estimación inicial (x0): "))
        tol = float(input("Ingrese la tolerancia (ej: 1e-7): "))
        max_iter = int(input("Ingrese el máximo de iteraciones: "))
        
        g_eval = None
        
        if opcion == 's':
            g_input = input("Ingrese la función g(x): ")
            g_eval = uv.deStringAFuncionEvaluable(g_input)
        else:
            print("\nGenerando g(x) óptima a partir de f(x)...")
            g_eval, g_simbolica = encontrarGOptima(f_simbolica, x0)
            
            if g_eval is None:
                print("[FALLO] No se pudo generar una g(x) automáticamente.")
                return
            
            print(f"Función g(x) generada: {g_simbolica}")

        # Ejecutar el método
        raiz_pf = puntoFijo(g_eval, x0, tol, max_iter)
        
        if raiz_pf is not None:
            print(f"\nRaíz aproximada con Punto Fijo: {raiz_pf:.10f}")
            print(f"Valor de f(raíz): {f_eval(raiz_pf):.2e}")
        
        print("-" * 50)

    except ValueError:
        print("\nError: Asegúrate de ingresar números válidos.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

"""
#*--------------------------------------------------------------------------------------------------------*

# Metodo newtonRaphson
NOTE: Este es la version original por asi decirlo, la de abajo es la mejorada, si da algun error usar esta
def newtonRaphson(funcion_input, xi, n):
    x = sp.symbols('x')
    funcion_simbolica = uv.deStringAFuncionSimbolica(funcion_input)
    funcion_diff = sp.diff(funcion_simbolica, x)
    funcion_eval = uv.deStringAFuncionEvaluable(funcion_input)
    funcion_diff_eval = uv.deStringAFuncionEvaluable(str(funcion_diff))

    xi_anterior = xi

    print(f"{'Iteración':<10} {'xi':<20} {'Error relativo':<20}")
    print("-" * 50)

    for i in range(n):
        xi_actual = xi_anterior - funcion_eval(xi_anterior)/funcion_diff_eval(xi_anterior)
        error = abs(xi_actual - xi_anterior)
        print(f"{i:<10} {xi_actual:<20.10f} {error:<20.10f}")
        xi_anterior = xi_actual

    return xi_actual

def newtonRaphsonTerminal():
    
    funcion_input = input("Ingrese la función: ")
    xi = float(input("Ingresa el valor de xi inicial: "))
    numIteracion = int(input("Ingrese el numero de iteraciones a evaluar: "))
    
    resultado = newtonRaphson(funcion_input, xi, numIteracion)
    print("El valor de 0 es: ", resultado)

#*--------------------------------------------------------------------------------------------------------*
"""

#*--------------------------------------------------------------------------------------------------------*

# Metodo newtonRaphson

# En metodos/metodosAbiertos.py

# Nueva versión para la GUI en metodos/metodosAbiertos.py

def NewtonRaphson(funcion_input, xi, max_iter, tol=1e-7):
    """Versión para GUI: Retorna (raiz, historial_lista)"""
    x = sp.symbols('x')
    # Usamos tus utilidades para procesar la función
    funcion_simbolica = uv.deStringAFuncionSimbolica(funcion_input)
    funcion_diff = sp.diff(funcion_simbolica, x)

    funcion_eval = uv.deStringAFuncionEvaluable(funcion_input)
    funcion_diff_eval = uv.deStringAFuncionEvaluable(str(funcion_diff))

    xi_anterior = xi
    historial_iteraciones = []

    # Iteración 0
    f_0 = funcion_eval(xi_anterior)
    historial_iteraciones.append((0, f"{xi_anterior:.10f}", f"{f_0:.10e}", "---"))

    for i in range(1, max_iter + 1):
        f_val = f_0  # Reutilizamos el valor calculado
        f_derivada_val = funcion_diff_eval(xi_anterior)

        if abs(f_derivada_val) < 1e-15:
            return xi_anterior, historial_iteraciones

        xi_actual = xi_anterior - f_val / f_derivada_val
        error = abs(xi_actual - xi_anterior)

        f_actual = funcion_eval(xi_actual)
        historial_iteraciones.append((i, f"{xi_actual:.10f}", f"{f_actual:.10e}", f"{error:.10e}"))

        if error < tol:
            return xi_actual, historial_iteraciones

        xi_anterior = xi_actual
        f_0 = f_actual  # Actualizamos para la siguiente iteración

    return xi_anterior, historial_iteraciones

def newtonRaphson(funcion_input, xi, max_iter, tol=1e-7): 
    
    x = sp.symbols('x')
    funcion_simbolica = uv.deStringAFuncionSimbolica(funcion_input)
    funcion_diff = sp.diff(funcion_simbolica, x)
    
    funcion_eval = uv.deStringAFuncionEvaluable(funcion_input)
    funcion_diff_eval = uv.deStringAFuncionEvaluable(str(funcion_diff))

    xi_anterior = xi

    print(f"\n{'Iteración':<10} {'xi':<20} {'Error Absoluto':<20}") 
    print("-" * 50)
    print(f"{0:<10} {xi_anterior:<20.10f} {'---':<20}")

    for i in range(1, max_iter + 1): 
        
        f_val = funcion_eval(xi_anterior)
        f_derivada_val = funcion_diff_eval(xi_anterior)
        
        if abs(f_derivada_val) < 1e-15:
            print(f"\n¡Error! La derivada es cero en la iteración {i}. No se puede continuar.")
            return xi_anterior
            
        xi_actual = xi_anterior - f_val / f_derivada_val
        error = abs(xi_actual - xi_anterior) 

        print(f"{i:<10} {xi_actual:<20.10f} {error:<20.10e}")
        
        
        if error < tol:
            print(f"\n¡Convergencia alcanzada en {i} iteraciones!")
            return xi_actual
            
        xi_anterior = xi_actual

    print(f"\n¡Advertencia! El método no convergió tras {max_iter} iteraciones.")
    return xi_actual

def newtonRaphsonTerminal():
    
    funcion_input = input("Ingrese la función: ")
    xi = float(input("Ingresa el valor de xi inicial: "))
    max_iter = int(input("Ingrese el numero MAXIMO de iteraciones: "))
    tol = float(input("Ingrese la tolerancia (ej: 1e-7): ")) 
    
    resultado = newtonRaphson(funcion_input, xi, max_iter, tol) 
    print("\nEl valor de la raíz es: ", resultado)

#*--------------------------------------------------------------------------------------------------------*

# El metodo de la secante

def secante(f: Callable[[float], float], x_prev: float, x_curr: float, tol: float = 1e-6, max_iter: int = 50) -> float | None:
    
    print(f"{'Iteración':<12} {'x':<15} {'Error':<15}")
    print("-" * 50)
    for i in range(1, max_iter + 1):
        f_prev = f(x_prev)
        f_curr = f(x_curr)
        
        if abs(f_curr) < tol:
            print(f"\n¡Convergencia de f(x) alcanzada en {i-1} iteraciones!")
            return x_curr
            
        if abs(f_curr - f_prev) < 1e-15:  # Evitar división por cero
            print(f"\n¡Advertencia! El denominador es casi cero en la iteración {i}. No se pudo continuar.")
            return x_curr # Devuelve la mejor estimación hasta el momento

        x_next = x_curr - f_curr * (x_curr - x_prev) / (f_curr - f_prev)
        error = abs(x_next - x_curr)

        print(f"Iteración {i:<3}| x = {x_next:<12.8f}| Error = {error:<12.8e}")
        

        if error < tol:
            print(f"\n¡Convergencia alcanzada en {i} iteraciones!")
            return x_next
            
        x_prev = x_curr
        x_curr = x_next
        
    print(f"\n¡Advertencia! El método no convergió después de {max_iter} iteraciones.")
    return None

def metodoSecanteTerminal():
    # --- Ejecución del Método de la Secante ---
    try:
        funcion_input = input("Ingrese la función: ")
        f_eval = uv.deStringAFuncionEvaluable(funcion_input)
        x_a = float(input("Ingresa el primer punto inicial (x_0): "))
        x_b = float(input("Ingresa el segundo punto inicial (x_1): "))
        raiz_secante = secante(f_eval, x_a, x_b)
        if raiz_secante is not None:
            print(f"\nRaíz aproximada con Secante: {raiz_secante:.10f}")
            print(f"Valor de f(raíz): {f_eval(raiz_secante):.2e}")
        print("-" * 50)
    except ValueError:
        print("\nError: Asegúrate de ingresar números válidos para los puntos iniciales.")
    except Exception as e:
        print(f"Ocurrió un error durante la Secante: {e}")

#*--------------------------------------------------------------------------------------------------------*


