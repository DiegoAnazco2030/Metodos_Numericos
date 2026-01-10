
def ingresoMatrizTerminal(nMatriz, mMatriz):
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

def multiplicacion_matrices(matrix_a, matrix_b):
    """
    Multiplica dos matrices dadas.
    Args:
        matrix_a (list of list of floats): Primera matriz.
        matrix_b (list of list of floats): Segunda matriz.
    Returns:
        list of list of floats: Matriz resultante de la multiplicación.
    """
    # Verificar si las matrices son compatibles para la multiplicación
    if len(matrix_a[0]) != len(matrix_b):
        raise ValueError("El número de columnas de la primera matriz debe ser igual al número de filas de la segunda matriz.")
    # Inicializar la matriz resultante con ceros
    result = [[0 for _ in range(len(matrix_b[0]))] for _ in range(len(matrix_a))]
    # Realizar la multiplicación de matrices
    for i in range(len(matrix_a)):
        for j in range(len(matrix_b[0])):
            for k in range(len(matrix_b)):
                result[i][j] += matrix_a[i][k] * matrix_b[k][j]
    return result

def matrizIdentidad(nMatriz):
    matrizI = [[0 for _ in range(nMatriz)] for _ in range(nMatriz)]
    for i in range(nMatriz):
        matrizI[i][i] = 1
    return matrizI

def traza_matriz(matrix):
    if len(matrix[0]) != len(matrix):
        raise ValueError("El número de columnas de la matriz debe ser igual al número de filas de la matriz.")
    sum = 0
    for i in range(len(matrix)):
        sum += matrix[i][i]
    return sum

def obtenerBr(matrix, pr):
    if len(matrix[0]) != len(matrix):
        raise ValueError("El número de columnas de la matriz debe ser igual al número de filas de la matriz.")

    resultado = [[0 for _ in range(len(matrix))] for _ in range(len(matrix))]
    identidad = matrizIdentidad(len(matrix))

    for i in range(len(matrix)):
        for j in range(len(matrix)):
            resultado[i][j] = matrix[i][j] - pr*identidad[i][j]

    return resultado
