import sympy as sp
from typing import Callable
#Llamo mi funcion que transforma strings a funciones evaluables
from metodos.usoGeneralFunicones import usoVariablesSympy as uv


#*--------------------------------------------------------------------------------------------------------*

# Metodo de Muller

def muller(f: Callable[[float], float], x0: float, x1: float, x2: float, tol: float = 1e-6, max_iter: int = 50) -> float | None:

    for i in range(1, max_iter + 1):
        f0, f1, f2 = f(x0), f(x1), f(x2)

        # Calcular h0, h1, delta0, delta1
        h0 = x1 - x0
        h1 = x2 - x1
        d0 = (f1 - f0) / h0
        d1 = (f2 - f1) / h1
        
        # Calcular a, b, c (coeficientes de la parábola)
        a = (d1 - d0) / (h1 + h0)
        b = a * h1 + d1
        c = f2
        
        # Elige el signo que da el denominador más grande (para estabilidad)
        denominador = b + (sp.sqrt(b**2 - 4 * a * c) if b >= 0 else -sp.sqrt(b**2 - 4 * a * c))
        """
        # Este cdigo de aqui es por si el discriminante se vuelve complejo, usa esto de aqui 
        discriminante = cmath.sqrt(b**2 - 4 * a * c) # <-- USA CMATH
        denominador = b + discriminante if abs(b + discriminante) > abs(b - discriminante) else b - discriminante
        """
        
        if abs(denominador) < 1e-15:
            print(f"\n¡Advertencia! El denominador es casi cero en la iteración {i}. No se pudo continuar.")
            return x2

        # Calcular la siguiente aproximación de la raíz
        x_new = x2 - 2 * c / denominador
        error = abs(x_new - x2)

        print(f"Iteración {i} | x = {x_new:.8f} | Error = {error:.8e}")

        if error < tol:
            print(f"\n¡Convergencia alcanzada en {i} iteraciones!")
            return x_new
            
        # Preparar para la siguiente iteración
        x0 = x1
        x1 = x2
        x2 = x_new
        
    print(f"\n¡Advertencia! El método no convergió después de {max_iter} iteraciones.")
    return None

def mullerTerminal():
    funcion_input = input("\nIngresa la función f(x) para Secante y Müller: ")
    funcion_evaluable = uv.deStringAFuncionEvaluable(funcion_input)
    
    # --- Ejecución del Método de Müller ---
    try:
        print("\n*** Prueba con el Método de Müller ***")
        x0 = float(input("Ingresa el primer punto inicial (x_0): "))
        x1 = float(input("Ingresa el segundo punto inicial (x_1): "))
        x2 = float(input("Ingresa el tercer punto inicial (x_2): "))

        #Cabezera de resultados
        print(f"\n{'Iteración':<10} | {'x (aprox)':<15} | {'Error':<15}")
        print("-" * 50)

        raiz_muller = muller(funcion_evaluable, x0, x1, x2)
        if raiz_muller is not None:
            print(f"\nRaíz aproximada con Müller: {raiz_muller:.10f}")
            print(f"Valor de f(raíz): {funcion_evaluable(raiz_muller):.2e}")
        print("-" * 50)
    except ValueError:
        print("\nError: Asegúrate de ingresar números válidos para los puntos iniciales.")
    except Exception as e:
        print(f"Ocurrió un error durante Müller: {e}")

#*--------------------------------------------------------------------------------------------------------*