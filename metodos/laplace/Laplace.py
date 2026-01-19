import numpy as np

def validar_entradas(T, max_iter, tol, w, dx=None):
    """
    Valida las dimensiones de la matriz y los parámetros numéricos.
    """
    if not isinstance(T, np.ndarray):
        raise TypeError("La matriz T debe ser un arreglo NumPy (ndarray).")
    
    if T.ndim != 2:
        raise ValueError("La matriz debe ser bidimensional.")
    
    filas, cols = T.shape
    if filas < 3 or cols < 3:
        raise ValueError("La matriz debe ser de al menos 3x3 para tener nodos interiores.")
        
    if not (0 < w < 2):
        raise ValueError("El factor de relajación 'w' debe estar entre 0 y 2.")
        
    if dx is not None and dx <= 0:
        raise ValueError("El paso 'dx' debe ser mayor a 0.")

def resolver_laplace_general(T_inicial, dx, condiciones, max_iter=1000, tol=1e-4, w=1.5):
    """
    Resuelve la Ecuación de Laplace usando el Método de Liebmann con SOR.
    Soporta condiciones de Dirichlet (Valor) y Neumann (Derivada) en los 4 bordes,
    aceptando tanto valores constantes como arreglos variables.

    Parámetros:
    -----------
    T_inicial : np.ndarray
        Matriz inicial con la estimación.
    dx : float
        Paso de la malla (distancia entre nodos).
    condiciones : dict
        Diccionario con claves 'arriba', 'abajo', 'izquierda', 'derecha'.
        Cada valor: {'tipo': 'dirichlet'|'neumann', 'valor': float | list | np.array}
    max_iter : int
        Máximo de iteraciones.
    tol : float
        Tolerancia de error para convergencia.
    w : float
        Factor de sobrerrelajación (1.0 = Gauss-Seidel, 1.5 recomendado).

    Retorna:
    --------
    T : np.ndarray (Matriz resuelta)
    error : float (Error final alcanzado)
    iter : int (Iteraciones realizadas)
    """
    
    # 1. Validaciones
    validar_entradas(T_inicial, max_iter, tol, w, dx)
    T = T_inicial.copy().astype(float)
    filas, cols = T.shape
    
    # Función auxiliar para obtener el valor correcto (escalar o vector) en la posición k
    def get_val(valor_condicion, k):
        if isinstance(valor_condicion, (list, np.ndarray)):
            # Si es vector, verifica que no nos salgamos del índice
            try:
                return valor_condicion[k]
            except IndexError:
                raise IndexError(f"El array de condición de borde no coincide con el tamaño de la matriz en el índice {k}.")
        return valor_condicion  # Si es escalar, retorna el número

    # 2. Pre-aplicar condiciones DIRICHLET (Fijas)
    # Esto "pinta" los bordes fijos antes de empezar a iterar
    if condiciones['arriba']['tipo'] == 'dirichlet':
        T[0, :] = condiciones['arriba']['valor']
        
    if condiciones['abajo']['tipo'] == 'dirichlet':
        T[-1, :] = condiciones['abajo']['valor']
        
    if condiciones['izquierda']['tipo'] == 'dirichlet':
        T[:, 0] = condiciones['izquierda']['valor']
        
    if condiciones['derecha']['tipo'] == 'dirichlet':
        T[:, -1] = condiciones['derecha']['valor']

    # 3. Bucle Iterativo (Liebmann)
    for k in range(max_iter):
        T_old = T.copy()
        
        # A. Actualizar INTERIOR (Nodos 1 a N-1)
        for i in range(1, filas - 1):
            for j in range(1, cols - 1):
                # Promedio de los 4 vecinos
                T_prom = (T[i+1, j] + T[i-1, j] + T[i, j+1] + T[i, j-1]) / 4
                # Aplicar SOR
                T[i, j] = w * T_prom + (1 - w) * T[i, j]

        # B. Actualizar BORDES NEUMANN (Derivadas) usando nodos fantasma
        
        # --- IZQUIERDA (j=0) ---
        if condiciones['izquierda']['tipo'] == 'neumann':
            vals = condiciones['izquierda']['valor']
            for i in range(1, filas - 1):
                q = get_val(vals, i)
                # Fórmula: T(-1, i) = T(1, i) - 2*dx*q
                # Promedio: (2*Right + Up + Down - 2*dx*q) / 4
                T_prom = (2*T[i, 1] + T[i+1, 0] + T[i-1, 0] - 2*dx*q) / 4
                T[i, 0] = w * T_prom + (1 - w) * T[i, 0]

        # --- DERECHA (j=cols-1) ---
        if condiciones['derecha']['tipo'] == 'neumann':
            vals = condiciones['derecha']['valor']
            c = cols - 1
            for i in range(1, filas - 1):
                q = get_val(vals, i)
                # Fórmula: T(cols, i) = T(cols-2, i) + 2*dx*q
                # Promedio: (2*Left + Up + Down + 2*dx*q) / 4
                T_prom = (2*T[i, c-1] + T[i+1, c] + T[i-1, c] + 2*dx*q) / 4
                T[i, c] = w * T_prom + (1 - w) * T[i, c]

        # --- ARRIBA (i=0) ---
        if condiciones['arriba']['tipo'] == 'neumann':
            vals = condiciones['arriba']['valor']
            for j in range(1, cols - 1):
                q = get_val(vals, j)
                # Promedio: (2*Down + Left + Right - 2*dx*q) / 4
                T_prom = (2*T[1, j] + T[0, j+1] + T[0, j-1] - 2*dx*q) / 4
                T[0, j] = w * T_prom + (1 - w) * T[0, j]

        # --- ABAJO (i=filas-1) ---
        if condiciones['abajo']['tipo'] == 'neumann':
            vals = condiciones['abajo']['valor']
            f = filas - 1
            for j in range(1, cols - 1):
                q = get_val(vals, j)
                # Promedio: (2*Up + Left + Right + 2*dx*q) / 4
                T_prom = (2*T[f-1, j] + T[f, j+1] + T[f, j-1] + 2*dx*q) / 4
                T[f, j] = w * T_prom + (1 - w) * T[f, j]

        # 4. Chequeo de Convergencia
        # Usamos la norma infinita (máxima diferencia absoluta)
        diferencia = np.abs(T - T_old)
        error_actual = np.max(diferencia)
        
        if error_actual < tol:
            return T, error_actual, k + 1

    return T, error_actual, max_iter