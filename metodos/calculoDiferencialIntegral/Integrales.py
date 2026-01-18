def regla_trapecio(f, a, b, n):
    """Integración numérica usando la Regla del Trapecio compuesta."""
    h = (b - a) / n
    suma = f(a) + f(b)  # Primer y último término [cite: 57]
    
    for i in range(1, n):
        suma += 2 * f(a + i * h)  # Los términos intermedios se multiplican por 2
        
    return (h / 2) * suma

def simpson_1_3(f, a, b, n):
    """Integración numérica usando la Regla de Simpson 1/3 compuesta."""
    if n % 2 != 0:
        raise ValueError("Para Simpson 1/3, n debe ser par[cite: 85].")
        
    h = (b - a) / n
    suma = f(a) + f(b)
    
    for i in range(1, n):
        x_i = a + i * h
        if i % 2 == 0:
            suma += 2 * f(x_i)  # Pares por 2
        else:
            suma += 4 * f(x_i)  # Impares por 4 [cite: 82, 87]
            
    return (h / 3) * suma

def simpson_3_8(f, a, b, n):
    """Integración numérica usando la Regla de Simpson 3/8 compuesta."""
    if n % 3 != 0:
        raise ValueError("Para Simpson 3/8, n debe ser múltiplo de 3.")
        
    h = (b - a) / n
    suma = f(a) + f(b)
    
    for i in range(1, n):
        x_i = a + i * h
        if i % 3 == 0:
            suma += 2 * f(x_i)  # Múltiplos de 3 por 2
        else:
            suma += 3 * f(x_i)  # El resto por 3 [cite: 91]
            
    return (3 * h / 8) * suma