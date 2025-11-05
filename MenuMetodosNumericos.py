"""
Modulo principal para la ejecución de métodos para encontrar raices.
"""

import sys
from typing import Callable, Dict

# -------------------------------------------------------------------
# Funciones imprtados
from metodosEncontrarRaices.MenuEncontrarRaices import *
from metodosMatrices.MenuMetodosMatrices import *
# -------------------------------------------------------------------

# --- Implementaciones Simuladas (para demostración) ---

def menu_raices() -> None:
    print("\n[Iniciando Menu De Encontrar Raices...]")
    menu_encontrar_raices()
    print("[...Menu de Encontrar Raices finalozado.]")


def menu_matrices() -> None:
    print("\n[Iniciando Menu de Matrices...]")
    menu_metodos_matrices()
    print("[...Menu de Matrices finalizado.]")

# -------------------------------------------------------------------

# El 'dispatch table' mapea la entrada a la función correspondiente.
# Esta es la "buena práctica" en lugar de un switch o if/elif.
METODOS_DISPONIBLES: Dict[int, Callable[[], None]] = {
    1: menu_raices,
    2: menu_matrices,
}


def mostrar_menu() -> None:
    """Imprime el menú principal de opciones en la consola."""
    print("\n" + "=" * 30)
    print("  Menú de Métodos Numéricos")
    print("=" * 30)
    print("1. Menu de los metodos para encontrar raices")
    print("2. Menu de los metodos de Matrices")
    print("\n0. Salir")
    print("-" * 30)


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


def menu_metodos_numericos() -> None:
    """
    Función principal que ejecuta el bucle del menú interactivo.
    """
    print("Bienvenido al programa de Métodos Numéricos.")

    while True:
        mostrar_menu()
        opcion = obtener_opcion_valida()

        if opcion == 0:
            print("Saliendo del programa. ¡Adiós!")
            sys.exit(0)

        metodo_a_ejecutar = METODOS_DISPONIBLES[opcion]

        try:
            # Ejecuta el metodo seleccionado
            metodo_a_ejecutar()
        except Exception as e:
            # Captura cualquier error inesperado DURANTE la ejecución del metodo
            print(f"\n¡ERROR! Ocurrió un problema al ejecutar el método: {e}")
            print("Volviendo al menú principal.")


if __name__ == "__main__":
    menu_metodos_numericos()