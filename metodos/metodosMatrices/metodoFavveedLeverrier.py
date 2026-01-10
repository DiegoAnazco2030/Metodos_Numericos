from metodos.usoGeneralFunicones.usoMatrices import ingresoMatrizTerminal, matrizIdentidad, traza_matriz, obtenerBr, multiplicacion_matrices

def favveedLeberrier():
    print("Ingrese las dimensiones de la matriz")
    nMatriz = int(input("Ingrese el numero de filas de la matriz: "))
    mMatriz = int(input("Ingrese el numero de columnas de la matriz: "))

    if nMatriz != mMatriz:
        raise ValueError("ERROR: La matriz debe ser cuadrada")

    A = ingresoMatrizTerminal(nMatriz, mMatriz)
    if A is None:
        return None

    Ar = A
    Br = None
    coeficientes_p = []

    for r in range(1, nMatriz + 1):
        pr = (1 / r) * traza_matriz(Ar)
        coeficientes_p.append(pr)
        if r == nMatriz:
            break
        Br = obtenerBr(Ar, pr)
        Ar = multiplicacion_matrices(A, Br)

    print(coeficientes_p)

if __name__ == "__main__":
    favveedLeberrier()
