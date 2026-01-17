import math
import numpy as np
from metodos.usoGeneralFunicones import usoVariablesSympy as uv

def metodoEuler(f_str, x0, y0, h, n):
    """
    Método de Euler para EDOs.
    Retorna: (y_final, tabla_iteraciones)
    """
    f = uv.deStringAFuncionEvaluableXY(f_str)
    
    x = x0
    y = y0
    
    # Formato de tabla: is_iteracion, x, y, f(x,y), y_siguiente
    tabla = []
    
    # Agregamos condicion inicial
    tabla.append((0, f"{x:.5f}", f"{y:.5f}", "---", "---"))
    
    for i in range(1, n + 1):
        try:
            val_f = f(x, y) # Evaluamos pendiente
            y_next = y + val_f * h
            
            tabla.append((
                i, 
                f"{x:.5f}", 
                f"{y:.5f}", 
                f"{val_f:.5f}", 
                f"{y_next:.5f}"
            ))
            
            x = x + h
            y = y_next
        except Exception:
            break
            
    return y, tabla

def metodoHeun(f_str, x0, y0, h, n):
    """
    Método de Heun (Predictor-Corrector).
    Retorna: (y_final, tabla_iteraciones)
    """
    f = uv.deStringAFuncionEvaluableXY(f_str)
    x = x0
    y = y0
    tabla = []
    tabla.append((0, f"{x:.5f}", f"{y:.5f}", "---", "---", "---"))
    
    for i in range(1, n + 1):
        try:
            # Predictor (Euler)
            k1 = f(x, y)
            y_pred = y + k1 * h
            
            x_next = x + h
            
            # Corrector
            k2 = f(x_next, y_pred)
            y_prom = (k1 + k2) / 2
            
            y_next = y + y_prom * h
            
            tabla.append((
                i,
                f"{x:.5f}",
                f"{y:.5f}",
                f"{y_pred:.5f}", # Prediccion inicial
                f"{y_next:.5f}", # Valor corregido
                f"{abs(y_next - y_pred):.2e}" # Diferencia
            ))
            
            x = x_next
            y = y_next
            
        except Exception:
            break
            
    return y, tabla

def metodoRungeKutta4(f_str, x0, y0, h, n):
    """
    Método de Runge-Kutta de 4to Orden.
    """
    f = uv.deStringAFuncionEvaluableXY(f_str)
    x = x0
    y = y0
    tabla = []
    tabla.append((0, f"{x:.5f}", f"{y:.5f}", "-", "-", "-", "-", "-"))
    
    for i in range(1, n + 1):
        try:
            k1 = f(x, y)
            k2 = f(x + 0.5*h, y + 0.5*k1*h)
            k3 = f(x + 0.5*h, y + 0.5*k2*h)
            k4 = f(x + h, y + k3*h)
            
            y_next = y + (h/6.0)*(k1 + 2*k2 + 2*k3 + k4)
            
            # Formato extendido para analisis
            tabla.append((
                i,
                f"{x:.5f}",
                f"{y:.5f}",
                f"{k1:.4f}",
                f"{k2:.4f}",
                f"{k3:.4f}",
                f"{k4:.4f}",
                f"{y_next:.5f}"
            ))
            
            x = x + h
            y = y_next
            
        except Exception:
            break
            
    return y, tabla

def metodoRKFehlberg(f_str, x0, y0, h_inicial, x_final, tol=1e-6):
    """
    Método Runge-Kutta-Fehlberg (RK45) adaptativo.
    Ajusta el paso h automaticamente.
    """
    f = uv.deStringAFuncionEvaluableXY(f_str)
    x = x0
    y = y0
    h = h_inicial
    tabla = []
    
    # Coeficientes de Cash-Karp (comunes para RK45)
    c2, c3, c4, c5, c6 = 1/4, 3/8, 12/13, 1, 1/2
    a21 = 1/4
    a31, a32 = 3/32, 9/32
    a41, a42, a43 = 1932/2197, -7200/2197, 7296/2197
    a51, a52, a53, a54 = 439/216, -8, 3680/513, -845/4104
    a61, a62, a63, a64, a65 = -8/27, 2, -3544/2565, 1859/4104, -11/40
    
    # Para orden 5 (solucion)
    b1, b3, b4, b5, b6 = 16/135, 6656/12825, 28561/56430, -9/50, 2/55
    # Para orden 4 (error)
    bs1, bs3, bs4, bs5, bs6 = 25/216, 1408/2565, 2197/4104, -1/5, 0
    
    i = 0
    tabla.append((i, f"{x:.5f}", f"{y:.5f}", f"{h:.5f}", "---"))
    
    while x < x_final:
        if x + h > x_final: # Ajustar ultimo paso
            h = x_final - x
            
        k1 = f(x, y)
        k2 = f(x + c2*h, y + a21*k1*h)
        k3 = f(x + c3*h, y + a31*k1*h + a32*k2*h)
        k4 = f(x + c4*h, y + a41*k1*h + a42*k2*h + a43*k3*h)
        k5 = f(x + c5*h, y + a51*k1*h + a52*k2*h + a53*k3*h + a54*k4*h)
        k6 = f(x + c6*h, y + a61*k1*h + a62*k2*h + a63*k3*h + a64*k4*h + a65*k5*h)
        
        y_orden5 = y + h*(b1*k1 + b3*k3 + b4*k4 + b5*k5 + b6*k6)
        y_orden4 = y + h*(bs1*k1 + bs3*k3 + bs4*k4 + bs5*k5 + bs6*k6)
        
        error = abs(y_orden5 - y_orden4)
        
        if error < tol or h < 1e-9:
            # Aceptamos el paso
            x = x + h
            y = y_orden5
            i += 1
            tabla.append((i, f"{x:.5f}", f"{y:.5f}", f"{h:.6f}", f"{error:.2e}"))
        
        # Ajuste de paso basico
        if error > 0:
            delta = 0.84 * (tol / error)**0.25
        else:
            delta = 2.0 # Si error es 0 aumentamos bastante
            
        h = h * delta
        
        # Limites de seguridad para h
        h = min(h, 0.5)
        h = max(h, 1e-5)

    return y, tabla

def metodoMultipasos(f_str, x0, y0, h, n):
    """
    Método de Adams-Bashforth de 2 pasos.
    Requiere un paso inicial con RK4.
    """
    f = uv.deStringAFuncionEvaluableXY(f_str)
    x = x0
    y = y0
    tabla = []
    
    # Paso 1: Usamos RK4 para obtener el siguiente punto y1
    tabla.append((0, f"{x:.5f}", f"{y:.5f}", "Inicial"))
    
    # RK4 para el primer paso
    k1 = f(x, y)
    k2 = f(x + 0.5*h, y + 0.5*k1*h)
    k3 = f(x + 0.5*h, y + 0.5*k2*h)
    k4 = f(x + h, y + k3*h)
    y1 = y + (h/6.0)*(k1 + 2*k2 + 2*k3 + k4)
    x1 = x + h
    
    tabla.append((1, f"{x1:.5f}", f"{y1:.5f}", "RK4 (Arranque)"))
    
    # Arrays para guardar historia
    xs = [x, x1]
    ys = [y, y1]
    
    # Adams-Bashforth 2 pasos: y_{i+1} = y_i + h/2 * (3f_i - f_{i-1})
    for i in range(2, n + 1):
        x_curr = xs[-1]
        y_curr = ys[-1]
        x_prev = xs[-2]
        y_prev = ys[-2]
        
        f_curr = f(x_curr, y_curr)
        f_prev = f(x_prev, y_prev)
        
        y_next = y_curr + (h/2.0) * (3*f_curr - f_prev)
        x_next = x_curr + h
        
        xs.append(x_next)
        ys.append(y_next)
        
        tabla.append((i, f"{x_next:.5f}", f"{y_next:.5f}", "Adams-Bashforth"))
        
    return ys[-1], tabla
