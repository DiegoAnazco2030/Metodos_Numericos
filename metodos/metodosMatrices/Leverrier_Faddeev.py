def ingreso_matriz_terminal(nMatriz, mMatriz):
    matrizIngresada = []

    i=1
    while i<=nMatriz:
        print(f"Ingrese los digitos de la fila {i} separados por comas: 1,5,3,2")
        entrada = input(f"Fila {i}: ")
        elementos_fila = entrada.split(',')
        try:
            ingresarFila = [float(e.strip()) for e in elementos_fila]
            if(len(ingresarFila) != mMatriz):
                print("ERROR: Se ingreso un tamanio incorrecto en la fila")
                continue
            matrizIngresada.append(ingresarFila)
            i+=1
        except ValueError:
            print("ERROR: Asegurese que los valores ingresados son correctos")

    return matrizIngresada

def ingreso_vector_b(n):
    while True:
        print(f"Ingrese los {n} elementos del vector b, separados por comas (por ejemplo: 1, 2, 3, ...):")
        entrada = input(f"Vector b: ")
        elementos = entrada.split(',')

        try:
            vector_b = [float(e.strip()) for e in elementos]

            if len(vector_b) != n:
                print(f"ERROR: El vector debe tener exactamente {n} elementos.")
                continue

            return vector_b
        except ValueError:
            print("ERROR: Asegúrese de que los valores ingresados son números válidos.")



def multiplicacion_matrices(matrix_a, matrix_b):
    if len(matrix_a[0]) != len(matrix_b):
        raise ValueError("El número de columnas de la primera matriz debe ser igual al número de filas de la segunda matriz.")

    result = [[0 for _ in range(len(matrix_b[0]))] for _ in range(len(matrix_a))]

    for i in range(len(matrix_a)):
        for j in range(len(matrix_b[0])):
            for k in range(len(matrix_b)):
                result[i][j] += matrix_a[i][k] * matrix_b[k][j]

    return result

def multiplicacion_matriz_escalar(A, c):
    result = [[0 for _ in range(len(A[0]))] for _ in range(len(A))]

    for i in range(len(A)):
        for j in range(len(A[0])):
            result[i][j] = c*A[i][j]

    return result

def multiplicacion_matriz_vector(A, x):
    if len(A[0]) != len(x):
        raise ValueError("El número de columnas de la primera matriz debe ser igual al número de filas del vector.")

    result = [0 for _ in range(len(A))]

    for i in range(len(A)):
        for j in range(len(x)):
            result[i] += A[i][j] * x[j]

    return result

def traza_matriz(matrix):
    if len(matrix[0]) != len(matrix):
        raise ValueError("El número de columnas de la matriz debe ser igual al número de filas de la matriz.")

    suma_diagonal = 0
    for i in range(len(matrix)):
        suma_diagonal += matrix[i][i]

    return suma_diagonal

def matriz_identidad(n):
    matrizI = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        matrizI[i][i] = 1

    return matrizI

def obtener_Bk(matrix, ck):
    if len(matrix[0]) != len(matrix):
        raise ValueError("El número de columnas de la matriz debe ser igual al número de filas de la matriz.")

    resultado = [[0 for _ in range(len(matrix))] for _ in range(len(matrix))]
    identidad = matriz_identidad(len(matrix))

    for i in range(len(matrix)):
        for j in range(len(matrix)):
            resultado[i][j] = matrix[i][j] + ck*identidad[i][j]

    return resultado

def favveed_Leberrier(A):
    c = [1]
    B = matriz_identidad(len(A))

    for k in range(1, len(A)):
        c.append(-1*traza_matriz(multiplicacion_matrices(A,B))/k)
        B = obtener_Bk(multiplicacion_matrices(A,B),c[k])

    c.append(-1*traza_matriz(multiplicacion_matrices(A,B))/len(A))
    det = ((-1)**len(A))*c[len(A)]

    inversa = multiplicacion_matriz_escalar(B, (-1)/c[len(A)])

    return c, det, inversa

def metodo_leverrier_faddeev():
    while True:
        print("-----Metodo de Favveed-Leberrier-----")
        print("Ingrese las dimensiones de la matriz:")
        nMatriz = int(input("Ingrese el numero de filas de la matriz: "))
        mMatriz = int(input("Ingrese el numero de columnas de la matriz: "))
        if(nMatriz != mMatriz):
            raise ValueError("ERROR: La matriz debe ser cuadrada")
        else:
            break
    
    matriz = ingreso_matriz_terminal(nMatriz, mMatriz)

    b = ingreso_vector_b(nMatriz)

    matriz_ck, det, inversa = favveed_Leberrier(matriz)

    x = multiplicacion_matriz_vector(inversa, b)

    print(f"\ndeterminate: {det}")

    print("\nPolinomio caracteristico:")

    for i in range(nMatriz + 1):
        coef = matriz_ck[i]
        exponente = nMatriz - i
        
        if coef.is_integer():
            termino = f"{int(coef)}x^{exponente}"
        else:
            termino = f"{coef:.6f}x^{exponente}"

        if i < nMatriz:
            print(termino, end=" + ")
        else:
            print(termino)
    
    print("\nMatriz Inversa:")

    for i in range(nMatriz):
        for j in range(nMatriz):
            print(f"{inversa[i][j]:.6f}", end=" ")
        print()

    print("\nSolucion del sistema de ecuaciones Ax = b:")

    for i in range(nMatriz):
        print(f"x_{i + 1} = {x[i]:.6}")
