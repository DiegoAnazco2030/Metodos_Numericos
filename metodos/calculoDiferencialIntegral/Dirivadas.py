def diferencia_adelante(f, x, h):
    """Calcula la derivada usando diferencias finitas hacia adelante."""
    return (f(x + h) - f(x)) / h  # [cite: 64]

def diferencia_atras(f, x, h):
    """Calcula la derivada usando diferencias finitas hacia atrás."""
    return (f(x) - f(x - h)) / h  # [cite: 65]

def diferencia_centrada(f, x, h):
    """Calcula la derivada usando diferencias centradas (mayor precisión)."""
    return (f(x + h) - f(x - h)) / (2 * h)  # [cite: 71]