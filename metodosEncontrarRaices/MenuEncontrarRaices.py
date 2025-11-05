"""
Modulo principal para la ejecución de métodos para encontrar raices.
"""

import sys
from typing import Callable, Dict

# -------------------------------------------------------------------
# Funciones imprtados
from metodosEncontrarRaices import metodosAbiertos as ma, metodosCerrados as mc, raicesPolinomicas as rp
# -------------------------------------------------------------------

# --- Implementaciones Simuladas (para demostración) ---

def metodo_biseccion() -> None:
    print("\n[Iniciando Método de Bisección...]")
    mc.biseccionTerminal()
    print("[...Método de Bisección finalizado.]")

def metodo_falsa_posicion() -> None:
    print("\n[Iniciando Método de Falsa Posición...]")
    mc.falsaPosicionTerminal()
    print("[...Método de Falsa Posición finalizado.]")

def metodo_iteracion_de_punto_fijo() -> None:
    print("\n[Iniciando Método de Iteración de Punto Fijo...]")
    ma.puntoFijoTerminal()
    print("[...Método de Iteración de Punto Fijo finalizado.]")

def metodo_newton_raphson() -> None:
    print("\n[Iniciando Método de Newton-Raphson...]")
    ma.newtonRaphsonTerminal()
    print("[...Método de Newton-Raphson finalizado.]")

def metodo_de_la_secante() -> None:
    print("\n[Iniciando Método de la Secante...]")
    ma.metodoSecanteTerminal()
    print("[...Método de la Secante finalizado.]")

def metodo_muller() -> None:
    print("\n[Iniciando Método de Müller...]")
    rp.mullerTerminal()
    print("[...Método de Müller finalizado.]")

# -------------------------------------------------------------------

# El 'dispatch table' mapea la entrada a la función correspondiente.
# Esta es la "buena práctica" en lugar de un switch o if/elif.
METODOS_DISPONIBLES: Dict[int, Callable[[], None]] = {
    1: metodo_biseccion,
    2: metodo_falsa_posicion,
    3: metodo_iteracion_de_punto_fijo,
    4: metodo_newton_raphson,
    5: metodo_de_la_secante,
    6: metodo_muller,
}


def mostrar_menu() -> None:
    """Imprime el menú principal de opciones en la consola."""
    print("\n" + "="*30)
    print("  Menú de Métodos Numéricos")
    print("="*30)
    print("1. Método de Bisección")
    print("2. Método de Falsa Posición")
    print("3. Método de Iteración de Punto Fijo")
    print("4. Método de Newton-Raphson")
    print("5. Método de la Secante")
    print("6. Método de Müller")
    print("\n0. Regresar")
    print("-"*30)


def obtener_opcion_valida() -> int:
    """
    Solicita al usuario una opción y la valida.

    Asegura que la entrada sea un entero y que corresponda a una
    opción válida del menú (0 o una clave en METODOS_DISPONIBLES).

    Returns:
        int: La opción numérica validada.
    """

    opciones_validas = set(METODOS_DISPONIBLES.keys())
    
    while True:
        entrada = input("Seleccione una opción: ")
        try:
            opcion = int(entrada)
            if opcion == 0 or opcion in opciones_validas:
                return opcion
            else:
                print(f"Error: Opción '{opcion}' no válida. Intente de nuevo.")
        except ValueError:
            print(f"Error: '{entrada}' no es un número. Intente de nuevo.")


def menu_encontrar_raices() -> None:
    """
    Función principal que ejecuta el bucle del menú interactivo.
    """
    
    while True:
        mostrar_menu()
        opcion = obtener_opcion_valida()

        if opcion == 0:
            print("Regresando...")
            return None
        
        print("Sintaxis de funciones: Usa 'x' como variable, e.g., 'cos(x) - x' o 'x**2 - 2'")
        # Obtiene la función del diccionario y la ejecuta
        metodo_a_ejecutar = METODOS_DISPONIBLES[opcion]
        
        try:
            # Ejecuta el método seleccionado
            metodo_a_ejecutar()
        except Exception as e:
            # Captura cualquier error inesperado DURANTE la ejecución del método
            print(f"\n¡ERROR! Ocurrió un problema al ejecutar el método: {e}")
            print("Volviendo al menú principal.")


if __name__ == "__main__":
    menu_encontrar_raices()