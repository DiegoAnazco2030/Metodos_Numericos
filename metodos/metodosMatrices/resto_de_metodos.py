from usoGeneralFunicones.usoMatrices import *
import math

# ---------- VALIDACIONES PARA METODOS NUMERICOS ----------

def es_simetrica(A, tol=1e-9):
    for i in range(1, len(A)):
        for j in range(i):
            if abs(A[i][j] - A[j][i]) > tol:
                return False
    return True

def es_definida_positiva(A):
    n = len(A)
    diag = [0.0] * n
    for i in range(n):
        s = sum(diag[k]**2 for k in range(i))
        val = A[i][i] - s
        if val <= 0:
            return False
        diag[i] = math.sqrt(val)
    return True

def es_diagonal_dominante(A):
    for i in range(len(A)):
        if abs(A[i][i]) < sum(abs(A[i][j]) for j in range(len(A)) if j != i):
            return False
    return True

# ================================
# MÉTODO DE JACOBI
# ================================
def metodoJacobi():
    print("\n=== MÉTODO DE JACOBI ===")
    n = int(input("Ingrese el número de ecuaciones (n): "))
    print("Ingrese la matriz de coeficientes A:")
    A = ingresoMatrizTerminal(n, n)

    if(not(es_diagonal_dominante(A) or (es_simetrica(A) and es_definida_positiva(A)))):
        print("No cumple las condiciones para aplicar el metodo de Jacobi")
        return None;

    print("Ingrese el vector b (separado por comas, ej: 5,2,3):")
    b = [float(x.strip()) for x in input("b: ").split(',')]

    x = [0.0] * n
    tol = float(input("Ingrese la tolerancia (ej: 1e-6): ") or 1e-6)
    max_iter = int(input("Ingrese el número máximo de iteraciones: ") or 100)

    for _ in range(max_iter):
        x_new = x.copy()
        for i in range(n):
            suma = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - suma) / A[i][i]
        if max(abs(x_new[i] - x[i]) for i in range(n)) < tol:
            print("Solución encontrada:", x_new)
            return x_new
        x = x_new
    print("Iteraciones máximas alcanzadas. Solución aproximada:", x)
    return x


# ================================
# MÉTODO DE ELIMINACIÓN GAUSSIANA
# ================================
def eliminacionGaussiana():
    print("\n=== MÉTODO DE ELIMINACIÓN GAUSSIANA ===")
    n = int(input("Ingrese el número de ecuaciones (n): "))
    print("Ingrese la matriz de coeficientes A:")
    A = ingresoMatrizTerminal(n, n)
    print("Ingrese el vector b (separado por comas):")
    b = [float(x.strip()) for x in input("b: ").split(',')]

    for i in range(n):
        A[i].append(b[i])

    for i in range(n):
        max_fila = max(range(i, n), key=lambda k: abs(A[k][i]))
        if i != max_fila:
            A[i], A[max_fila] = A[max_fila], A[i]

        pivote = A[i][i]
        if abs(pivote) < 1e-12:
            raise ValueError("La matriz es singular o casi singular.")
        for j in range(i, n + 1):
            A[i][j] /= pivote
        for k in range(i + 1, n):
            factor = A[k][i]
            for j in range(i, n + 1):
                A[k][j] -= factor * A[i][j]

    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = A[i][n] - sum(A[i][j] * x[j] for j in range(i + 1, n))

    print("Solución del sistema:", x)
    return x


# ================================
# MÉTODO DE GAUSS-SEIDEL
# ================================
def metodoGaussSeidel():
    print("\n=== MÉTODO DE GAUSS-SEIDEL ===")
    n = int(input("Ingrese el número de ecuaciones (n): "))
    print("Ingrese la matriz de coeficientes A:")
    A = ingresoMatrizTerminal(n, n)
    if(not(es_diagonal_dominante(A) or (es_simetrica(A) and es_definida_positiva(A)))):
        print("No cumple las condiciones para aplicar el metodo de Gauss-Seidel")
        return None;

    print("Ingrese el vector b (separado por comas):")
    b = [float(x.strip()) for x in input("b: ").split(',')]

    x = [0.0] * n
    tol = float(input("Ingrese la tolerancia (ej: 1e-6): ") or 1e-6)
    max_iter = int(input("Ingrese el número máximo de iteraciones: ") or 100)

    for _ in range(max_iter):
        x_old = x.copy()
        for i in range(n):
            suma = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x[i] = (b[i] - suma) / A[i][i]
        if max(abs(x[i] - x_old[i]) for i in range(n)) < tol:
            print("Solución encontrada:", x)
            return x
    print("Iteraciones máximas alcanzadas. Solución aproximada:", x)
    return x


# ================================
# DESCOMPOSICIÓN DE CHOLESKY
# ================================
def metodoCholesky():
    print("\n=== MÉTODO DE CHOLESKY ===")
    n = int(input("Ingrese el tamaño de la matriz (n): "))
    print("Ingrese la matriz A (debe ser simétrica y definida positiva):")
    A = ingresoMatrizTerminal(n, n)
    if(not(es_simetrica(A) and es_definida_positiva(A))):
        print("No cumple las condiciones para aplicar el metodo de Cholesky")
        return None;

    print("Ingrese el vector b (separado por comas):")
    b = [float(x.strip()) for x in input("b: ").split(',')]

    L = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            suma = sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                val = A[i][i] - suma
                if val <= 0:
                    raise ValueError("La matriz no es definida positiva.")
                L[i][j] = math.sqrt(val)
            else:
                L[i][j] = (A[i][j] - suma) / L[j][j]

    y = [0.0] * n
    for i in range(n):
        y[i] = (b[i] - sum(L[i][k] * y[k] for k in range(i))) / L[i][i]

    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(L[k][i] * x[k] for k in range(i + 1, n))) / L[i][i]

    print("Matriz L:")
    for fila in L:
        print(fila)
    print("Solución del sistema:", x)
    return x


# ================================
# MÉTODO DE LA POTENCIA
# ================================
def metodoPotencia():
    print("\n=== MÉTODO DE LA POTENCIA ===")
    print("Nota: Este método calcula el autovalor dominante y su autovector.")
    print("No resuelve sistemas de ecuaciones Ax = b.")
    confirmar = input("¿Deseas continuar con el método de la potencia? (y/n): ").strip().lower()
    if confirmar != 'y':
        print("Operación cancelada por el usuario.")
        return None
    n = int(input("Ingrese el tamaño de la matriz (n): "))
    print("Ingrese la matriz A:")
    A = ingresoMatrizTerminal(n, n)

    x = [1.0] * n
    tol = float(input("Ingrese la tolerancia (ej: 1e-6): ") or 1e-6)
    max_iter = int(input("Ingrese el número máximo de iteraciones: ") or 100)
    lambda_old = 0.0

    for _ in range(max_iter):
        y = [sum(A[i][j] * x[j] for j in range(n)) for i in range(n)]
        norma = math.sqrt(sum(y_i ** 2 for y_i in y))
        y = [y_i / norma for y_i in y]
        lambda_new = sum(y[i] * sum(A[i][j] * y[j] for j in range(n)) for i in range(n))
        if abs(lambda_new - lambda_old) < tol:
            print(f"Autovalor dominante ≈ {lambda_new}")
            print(f"Autovector asociado ≈ {y}")
            return lambda_new, y
        x = y
        lambda_old = lambda_new

    print("Máximas iteraciones alcanzadas.")
    print(f"Autovalor aproximado ≈ {lambda_old}")
    print(f"Autovector ≈ {x}")
    return lambda_old, x


# ================================
# PRUEBA GENERAL
# ================================
if __name__ == "__main__":
    while True:
        print("\nSeleccione el método numérico que desea usar:")
        print("0. Salir")
        print("1. Jacobi")
        print("2. Eliminación Gaussiana")
        print("3. Gauss-Seidel")
        print("4. Cholesky")
        print("5. Potencia")
        opcion = input("Opción: ").strip()

        if opcion == "0":
            print("Saliendo...")
            break
        elif opcion == "1":
            metodoJacobi()
        elif opcion == "2":
            eliminacionGaussiana()
        elif opcion == "3":
            metodoGaussSeidel()
        elif opcion == "4":
            metodoCholesky()
        elif opcion == "5":
            metodoPotencia()
        else:
            print("Opción no válida. Intente de nuevo.")
