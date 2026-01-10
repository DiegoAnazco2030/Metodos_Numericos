import sympy as sp


def parse_function(expr: str):
    x = sp.symbols('x')
    return sp.sympify(expr)
