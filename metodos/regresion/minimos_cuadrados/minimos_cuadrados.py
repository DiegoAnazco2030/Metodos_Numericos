import numpy as np


def minimos_cuadrados(x, y):
    """
    Regresión lineal por mínimos cuadrados.
    Retorna m, b y un texto con el desarrollo.
    """
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)

    n = len(x)

    if n < 2:
        raise ValueError("Se requieren al menos dos puntos")

    sum_x = np.sum(x)
    sum_y = np.sum(y)
    sum_xy = np.sum(x * y)
    sum_x2 = np.sum(x ** 2)

    m = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
    b = (sum_y - m * sum_x) / n

    y_pred = m * x + b
    errores = y - y_pred
    error_relativo = errores / y

    reporte = []
    reporte.append(f"n = {n}")
    reporte.append(f"Σx = {sum_x}")
    reporte.append(f"Σy = {sum_y}")
    reporte.append(f"Σxy = {sum_xy}")
    reporte.append(f"Σx² = {sum_x2}")
    reporte.append("")
    reporte.append(f"Pendiente (m) = {m}")
    reporte.append(f"Intercepto (b) = {b}")
    reporte.append("")
    reporte.append("i\t xi\t yi\t ŷi\t error\t error relativo")

    for i in range(n):
        reporte.append(
            f"{i}\t {x[i]:.4f}\t {y[i]:.4f}\t {y_pred[i]:.4f}\t {errores[i]:.4e}\t {error_relativo[i]:.4e}"
        )

    return m, b, "\n".join(reporte), y_pred
