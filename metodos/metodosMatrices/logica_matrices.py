import math

# ==========================================
# UTILIDADES DE VERIFICACIÓN
# ==========================================
def es_simetrica(A, tol=1e-9):
    n = len(A)
    for i in range(n):
        for j in range(i):
            if abs(A[i][j] - A[j][i]) > tol:
                return False
    return True

def es_definida_positiva(A):
    n = len(A)
    try:
        # Intento simplificado de Cholesky para verificar si es def. positiva
        temp_A = [row[:] for row in A]
        for i in range(n):
            for j in range(i + 1):
                s = sum(temp_A[i][k] * temp_A[j][k] for k in range(j))
                if i == j:
                    val = temp_A[i][i] - s
                    if val <= 0: return False
                    temp_A[i][j] = math.sqrt(val)
                else:
                    temp_A[i][j] = (temp_A[i][j] - s) / temp_A[j][j]
        return True
    except:
        return False

def es_diagonal_dominante(A):
    n = len(A)
    for i in range(n):
        diag = abs(A[i][i])
        suma_otros = sum(abs(A[i][j]) for j in range(n) if j != i)
        if diag < suma_otros:
            return False
    return True

# ==========================================
# MÉTODOS (Versiones para GUI)
# ==========================================

def MetodoJacobi(A, b, tol=1e-6, max_iter=100):
    """
    Retorna: x, historial, mensaje_advertencia
    """
    n = len(A)
    advertencia = None
    
    # 1. Validar condiciones pero NO detener
    if not es_diagonal_dominante(A):
        advertencia = "La matriz NO es diagonal dominante.\nSe recomienda reordenar las filas para asegurar la convergencia."
    elif not (es_simetrica(A) and es_definida_positiva(A)):
         # Nota: Jacobi a veces converge sin ser diag dominante, pero es raro.
         if not advertencia: 
             advertencia = "La matriz no cumple condiciones estrictas de convergencia."

    x = [0.0] * n # Vector inicial
    historial = [] 
    error_prev = float('inf')
    contador = 0

    for k in range(max_iter):
        x_new = x[:]
        # Iteración de Jacobi
        for i in range(n):
            suma = sum(A[i][j] * x[j] for j in range(n) if j != i)
            if A[i][i] == 0: 
                return x, historial, "Error Crítico: Cero en la diagonal principal. Imposible dividir."
            x_new[i] = (b[i] - suma) / A[i][i]
        
        # Calcular error
        norma = max(abs(x_new[i] - x[i]) for i in range(n))
        historial.append({'iter': k+1, 'x': x_new[:], 'error': norma})
        
        # 2. Chequeo de Convergencia
        if norma < tol:
            return x_new, historial, advertencia
            
        # 3. Chequeo de Divergencia por mas de 5 iteraciones
        # Solo verificamos después de la primera iteración para tener referencia
        if k >0 and norma > error_prev:
            contador +=1
        else:
            contador =0
        if contador >= 5:
            msg_div = "\n\n¡MÉTODO DIVERGENTE!\nEl error ha aumentado durante 5 iteraciones seguidas."
            advertencia = (advertencia or "") + msg_div
            return x_new, historial, advertencia

        x = x_new
        error_prev = norma
        
    return x, historial, (advertencia or "Se alcanzó el máximo de iteraciones sin converger.")

def MetodoGaussSeidel(A, b, tol=1e-6, max_iter=100):
    n = len(A)
    advertencia = None
    
    if not es_diagonal_dominante(A) and not (es_simetrica(A) and es_definida_positiva(A)):
        advertencia = "La matriz NO garantiza convergencia (No es Diag. Dominante ni Def. Positiva).\nIntente reordenar filas."

    x = [0.0] * n
    historial = []
    error_prev = float('inf')

    for k in range(max_iter):
        x_old = x[:]
        # Iteración de Gauss-Seidel
        for i in range(n):
            suma = sum(A[i][j] * x[j] for j in range(n) if j != i)
            if A[i][i] == 0: 
                return x, historial, "Error Crítico: Cero en la diagonal principal."
            x[i] = (b[i] - suma) / A[i][i]
        
        norma = max(abs(x[i] - x_old[i]) for i in range(n))
        historial.append({'iter': k+1, 'x': x[:], 'error': norma})

        if norma < tol:
            return x, historial, advertencia

        # Chequeo de Divergencia Explosiva
        if k >0 and norma > error_prev:
            contador +=1
        else:
            contador =0
        if contador >= 5:
            msg_div = "\n\n¡MÉTODO DIVERGENTE!\nEl error ha aumentado durante 5 iteraciones seguidas."
            advertencia = (advertencia or "") + msg_div
            return x, historial, advertencia
            
        error_prev = norma
            
    return x, historial, (advertencia or "Se alcanzó el máximo de iteraciones.")

def EliminacionGaussiana(A_in, b_in):
    n = len(A_in)
    A = [row[:] for row in A_in]
    b = b_in[:]
    
    # Matriz Aumentada
    for i in range(n):
        A[i].append(b[i])

    # Eliminación
    for i in range(n):
        # Pivoteo parcial
        max_fila = max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_fila] = A[max_fila], A[i]

        pivote = A[i][i]
        if abs(pivote) < 1e-12:
            raise ValueError("Sistema singular o infinitas soluciones.")

        for j in range(i, n + 1):
            A[i][j] /= pivote
        
        for k in range(i + 1, n):
            factor = A[k][i]
            for j in range(i, n + 1):
                A[k][j] -= factor * A[i][j]

    # Sustitución hacia atrás
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        suma = sum(A[i][j] * x[j] for j in range(i + 1, n))
        x[i] = A[i][n] - suma

    return x, [] # Gauss simple no tiene iteraciones que mostrar

def MetodoCholesky(A_in, b_in):
    n = len(A_in)
    A = [row[:] for row in A_in]
    b = b_in[:]
    
    if not (es_simetrica(A) and es_definida_positiva(A)):
        raise ValueError("La matriz debe ser simétrica y definida positiva.")

    L = [[0.0] * n for _ in range(n)]

    # Factorización
    for i in range(n):
        for j in range(i + 1):
            suma = sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                val = A[i][i] - suma
                if val <= 0: raise ValueError("Error numérico en Cholesky (raíz negativa).")
                L[i][j] = math.sqrt(val)
            else:
                L[i][j] = (A[i][j] - suma) / L[j][j]

    # Sustitución hacia adelante (Ly = b)
    y = [0.0] * n
    for i in range(n):
        y[i] = (b[i] - sum(L[i][k] * y[k] for k in range(i))) / L[i][i]

    # Sustitución hacia atrás (L_t x = y)
    x = [0.0] * n
    # Transpuesta de L se usa implícitamente intercambiando índices
    for i in range(n - 1, -1, -1):
        # L[k][i] accede a la transpuesta porque L original es triangular inferior
        x[i] = (y[i] - sum(L[k][i] * x[k] for k in range(i + 1, n))) / L[i][i]

    return x, L

# ==========================================
# HELPER DE COMPROBACIÓN
# ==========================================
def comprobar_solucion(A, x):
    """Calcula Ax para comparar con b"""
    n = len(A)
    Ax = []
    for i in range(n):
        val = sum(A[i][j] * x[j] for j in range(n))
        Ax.append(val)
    return Ax