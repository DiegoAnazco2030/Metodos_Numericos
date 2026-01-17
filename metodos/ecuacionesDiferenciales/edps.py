import numpy as np

def resolverLaplace(nx, ny, iteraciones=100, tol=1e-4, te=0, td=0, ta=0, tb=0):
    """
    Resuelve la Ecuación de Laplace (Elíptica) usando Diferencias Finitas.
    Placa rectangular.
    nx, ny: Puntos en malla x e y
    te, td, ta, tb: Temperaturas fronteras (Izq, Der, Arr, Abajo)
    """
    # Inicializamos la malla con ceros
    T = np.zeros((ny, nx))
    
    # Condiciones de frontera (Dirichlet)
    # Izquierda y Derecha
    T[:, 0] = te
    T[:, -1] = td
    # Arriba y Abajo
    T[0, :] = ta
    T[-1, :] = tb
    
    # Promedio inicial para acelerar convergencia (opcional pero util)
    promedio = (te + td + ta + tb) / 4
    T[1:-1, 1:-1] = promedio
    
    error_history = []
    
    for k in range(iteraciones):
        T_viejo = T.copy()
        
        # Metodo de Gauss-Seidel: iteramos sobre puntos interiores
        # T(i,j) = (T(i+1,j) + T(i-1,j) + T(i,j+1) + T(i,j-1)) / 4
        
        for i in range(1, ny - 1):
            for j in range(1, nx - 1):
                T[i, j] = 0.25 * (T[i+1, j] + T[i-1, j] + T[i, j+1] + T[i, j-1])
                
        # Calculamos error relativo maximo
        error = np.max(np.abs(T - T_viejo))
        error_history.append(error)
        
        if error < tol:
            break
            
    return T, error_history

def resolverCalorExplicito(c_inicial_str, long_barra, tiempo_total, nx, nt, alpha):
    """
    Ecuacion Calor 1D (Parabolica): u_t = alpha * u_xx
    Metodo Explicito.
    """
    # Discretizacion
    dx = long_barra / (nx - 1)
    dt = tiempo_total / (nt - 1)
    
    lambda_val = alpha * dt / (dx**2)
    
    # Estabilidad (condicion CFL)
    # Si lambda > 0.5, el metodo explicito es inestable
    msg_alerta = ""
    if lambda_val > 0.5:
        msg_alerta = "¡Alerta! Lambda > 0.5. La solución puede ser inestable."
    
    x = np.linspace(0, long_barra, nx)
    u = np.zeros((nt, nx))
    
    # Evaluamos condicion inicial u(x,0) = f(x)
    # Usamos eval simple de numpy si es posible, o lambda simulado
    # Importante: c_inicial_str debe ser compatible con python, ej "np.sin(x)"
    # Para simplificar "Student Mode", asumimos un ambiente seguro o funcion fija
    try:
        # Reemplazamos x simbolico por array numpy
        # Esto es un truco rapido para evaluar string con numpy
        contexto = {"x": x, "np": np, "sin": np.sin, "cos": np.cos, "exp": np.exp}
        u[0, :] = eval(c_inicial_str, contexto)
    except:
        # Fallback simple
        u[0, :] = 0
        
    # Condiciones de frontera fijas en 0 (pueden ser parametros luego)
    u[:, 0] = 0
    u[:, -1] = 0
    
    # Iteracion en tiempo
    for n in range(0, nt - 1):
        for i in range(1, nx - 1):
            u[n+1, i] = u[n, i] + lambda_val * (u[n, i+1] - 2*u[n, i] + u[n, i-1])
            
    return u, x, msg_alerta

def resolverOnda(c_inicial_str, long_cuerda, tiempo_total, nx, nt, c_velocidad):
    """
    Ecuacion Onda 1D (Hiperbolica): u_tt = c^2 * u_xx
    """
    dx = long_cuerda / (nx - 1)
    dt = tiempo_total / (nt - 1)
    
    C = c_velocidad * dt / dx # Numero de Courant
    
    # Condicion CFL para onda: C <= 1
    msg_alerta = ""
    if C > 1:
        msg_alerta = "¡Alerta! Courant > 1. Solución inestable."
        
    x = np.linspace(0, long_cuerda, nx)
    u = np.zeros((nt, nx))
    
    # Condicion inicial: Posicion inicial u(x,0)
    try:
        contexto = {"x": x, "np": np, "sin": np.sin, "cos": np.cos, "pi": np.pi}
        u[0, :] = eval(c_inicial_str, contexto)
    except:
        u[0, :] = np.sin(np.pi * x) # Default
        
    # Condicion inicial derivada: u_t(x,0) = 0 (velocidad inicial cero para simplificar)
    # Primer paso especial usando diferencia centrada en tiempo
    # u(x, dt) approx u(x,0) + 0.5*C^2 * (uxx)
    for i in range(1, nx - 1):
        u[1, i] = u[0, i] + 0.5 * (C**2) * (u[0, i+1] - 2*u[0, i] + u[0, i-1])
        
    # Resto de pasos
    for n in range(1, nt - 1):
        for i in range(1, nx - 1):
            u[n+1, i] = 2*u[n, i] - u[n-1, i] + (C**2) * (u[n, i+1] - 2*u[n, i] + u[n, i-1])
            
    return u, x, msg_alerta
