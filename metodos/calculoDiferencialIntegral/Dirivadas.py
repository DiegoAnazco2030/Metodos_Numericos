def validar_datos(f, x, h):
    """
    Verifica que los tipos de datos sean correctos y evita la división por cero.
    """
    if not callable(f):
        raise TypeError("El parámetro 'f' debe ser una función ejecutable (callable).")
    
    if not isinstance(x, (int, float)) or not isinstance(h, (int, float)):
        raise TypeError("Los parámetros 'x' y 'h' deben ser números (int o float).")
    
    if h < 0:
        raise ValueError("El tamaño del paso 'h' no puede ser negativo.")

    if h == 0:
        raise ValueError("El tamaño del paso 'h' no puede ser 0, ya que provocaría una división por cero.")

def diferencia_adelante(f, x, h):
    """Calcula la derivada usando diferencias finitas hacia adelante."""
    validar_datos(f, x, h)
    # Fórmula: (f(xi+1) - f(xi)) / h
    return (f(x + h) - f(x)) / h  # [cite: 64, 69]

def diferencia_atras(f, x, h):
    """Calcula la derivada usando diferencias finitas hacia atrás."""
    validar_datos(f, x, h)
    # Fórmula: (f(xi) - f(xi-1)) / h
    return (f(x) - f(x - h)) / h  # [cite: 65, 70]

def diferencia_centrada(f, x, h):
    """Calcula la derivada usando diferencias centradas (mayor precisión)."""
    validar_datos(f, x, h)
    # Fórmula: (f(xi+1) - f(xi-1)) / 2h
    return (f(x + h) - f(x - h)) / (2 * h)  # [cite: 66, 71]