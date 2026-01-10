"""
Modulo principal para la ejecución de métodos para encontrar raices.
"""

import sys
from typing import Callable, Dict

# -------------------------------------------------------------------
# Funciones imprtados
from metodosMatrices import resto_de_metodos as rdm, Leverrier_Faddeev as lf1, metodoFavveedLeverrier as lf2


# -------------------------------------------------------------------

# --- Implementaciones Simuladas (para demostración) ---

def metodo_jacobi() -> None:
    print("\n[Iniciando Método de Jacobi...]")
    rdm.metodoJacobi()
    print("[...Método de Jacobi finalizado.]")


def metodo_eliminacion_gaussiana() -> None:
    print("\n[Iniciando Método de eliminacion Gaussiana...]")
    rdm.eliminacionGaussiana()
    print("[...Método de eliminacion Gaussiana finalizado.]")


def metodo_gauss_seidel() -> None:
    print("\n[Iniciando Método de Gauss-Seidel...]")
    rdm.metodoGaussSeidel()
    print("[...Método de Gauss-Seidel finalizado.]")


def metodo_descomposicion_cholesky() -> None:
    print("\n[Iniciando Método de Cholesky...]")
    rdm.metodoCholesky()
    print("[...Método de Cholesky finalizado.]")


def metodo_de_la_potencia() -> None:
    print("\n[Iniciando Método de la Potencia...]")
    rdm.metodoPotencia()
    print("[...Método de la Potencia finalizado.]")


def metodo_Leverrier_Faddeev_1() -> None:
    print("\n[Iniciando Método de Leverrier-Faddeev(1)...]")
    lf1.metodo_leverrier_faddeev()
    print("[...Método de Leverrier-Faddeev(1) finalizado.]")


def metodo_Leverrier_Faddeev_2() -> None:
    print("\n[Iniciando Método de Leverrier-Faddeev(2)...]")
    lf2.favveedLeberrier()
    print("[...Método de Leverrier-Faddeev(2) finalizado.]")


# -------------------------------------------------------------------

# El 'dispatch table' mapea la entrada a la función correspondiente.
# Esta es la "buena práctica" en lugar de un switch o if/elif.
METODOS_DISPONIBLES: Dict[int, Callable[[], None]] = {
    1: metodo_jacobi,
    2: metodo_eliminacion_gaussiana,
    3: metodo_gauss_seidel,
    4: metodo_descomposicion_cholesky,
    5: metodo_de_la_potencia,
    6: metodo_Leverrier_Faddeev_1,
    7: metodo_Leverrier_Faddeev_2
}


def mostrar_menu() -> None:
    """Imprime el menú principal de opciones en la consola."""
    print("\n" + "=" * 30)
    print("  Menú de Métodos Numéricos")
    print("=" * 30)
    print("1. Método de Jacobi")
    print("2. Método de eliminacion Gaussiana")
    print("3. Método de Gauss-Seidel")
    print("4. Método de Cholesky")
    print("5. Método de la Potencia")
    print("6. Método de Leverrier-Faddeev(1)")
    print("7. Método de Leverrier-Faddeev(2)")
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


def menu_metodos_matrices() -> None:
    """
    Función principal que ejecuta el bucle del menú interactivo.
    """

    while True:
        mostrar_menu()
        opcion = obtener_opcion_valida()

        if opcion == 0:
            print("Regresando...")
            return None


        metodo_a_ejecutar = METODOS_DISPONIBLES[opcion]

        try:
            # Ejecuta el método seleccionado
            metodo_a_ejecutar()
        except Exception as e:
            # Captura cualquier error inesperado DURANTE la ejecución del método
            print(f"\n¡ERROR! Ocurrió un problema al ejecutar el método: {e}")
            print("Volviendo al menú principal.")


if __name__ == "__main__":
    menu_metodos_matrices()