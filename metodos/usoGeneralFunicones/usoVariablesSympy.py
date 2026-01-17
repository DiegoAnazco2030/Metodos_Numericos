import sympy as sp
from typing import Callable

def deStringAFuncionEvaluable(funcion_input: str) -> Callable[[float], float]:
    """Convierte una cadena de texto en una función evaluable de Python."""
    x = sp.symbols('x')
    expr = sp.sympify(funcion_input)  # convierte el string en expresion simbolica
    f = sp.lambdify(x, expr, "math")  # la convierte en función de Python evaluable
    return f

def deStringAFuncionSimbolica(funcion_input: str) -> sp.Expr:
    """Convierte una cadena de texto en una expresión simbolica de SymPy."""
    x = sp.symbols('x')
    expr = sp.sympify(funcion_input)  # convierte el string en expresion simbolica
    return expr

def deStringAFuncionEvaluableXY(funcion_input: str) -> Callable[[float, float], float]:
    """Convierte string a funcion f(x, y)."""
    x, y = sp.symbols('x y')
    expr = sp.sympify(funcion_input)
    f = sp.lambdify((x, y), expr, "math")
    return f
