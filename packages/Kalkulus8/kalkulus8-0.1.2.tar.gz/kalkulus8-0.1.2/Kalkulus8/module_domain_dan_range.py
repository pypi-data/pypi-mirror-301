import sympy as sp

def temukan_domain_dan_range(expr):
    """
    Menemukan domain dan range dari suatu ekspresi matematika yang diberikan.

    Parameters:
    expr : sympy expression
        Ekspresi matematika yang akan dianalisis.

    Returns:
    domain : sympy Set
        Domain dari fungsi, yaitu nilai-nilai x yang valid.
    f_range : sympy Set
        Range dari fungsi, yaitu hasil dari fungsi terhadap domain.
    """
    x = sp.Symbol('x')
    
    if expr.is_constant():
        domain = sp.S.Reals
        f_range = sp.simplify(expr)
    else:
        domain = sp.calculus.util.continuous_domain(expr, x, sp.S.Reals)
        f_range = sp.calculus.util.function_range(expr, x, domain)
    
    return domain, f_range

def analisis_fungsi(expression):
    """
    Melakukan analisis terhadap fungsi dengan menemukan domain dan range.

    Parameters:
    expression : str
        Ekspresi matematika dalam bentuk string yang akan dianalisis.

    Returns:
    domain : sympy Set
        Domain dari fungsi, yaitu nilai-nilai x yang valid.
    f_range : sympy Set
        Range dari fungsi, yaitu hasil dari fungsi terhadap domain.

    """
    try:
        expr = sp.sympify(expression)
        domain, f_range = temukan_domain_dan_range(expr)

        return domain, f_range

    except Exception as e:
        return f"Terjadi kesalahan: {e}"

"""
Menambahkan input dari pengguna

contoh pemakaian tanpa inputan:

domain, f_range = analisis_fungsi("x**2")
print(f"Domain: {domain}")
print(f"Range: {f_range}")

contoh pemakaian menggunakan inputan:

expression = input("Masukkan fungsi yang ingin dianalisis (misal: 1/(x-2), sqrt(x), x**2 + 1, 1/(x**2 - 4) : ")

result = analisis_fungsi(expression)
print(f"Domain dan rangenya adalah: {result}")

"""