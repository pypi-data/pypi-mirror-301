import sympy as sp
import re

def validasi_input(expression):
    pattern = r'^[\d\+\-\/\^\(\)\.\,\sxyzt\w\s]*(?:[+\-*/^]|sqrt|sin|cos|tan|log|exp|abs|pi|E)[\d\+\-\/\^\(\)\.\,\sxyzt\w\s]*$'
    functions = r'(sqrt|sin|cos|tan|log|exp|abs|pi|E)'

    if re.match(pattern, expression):
        cleaned_expr = expression.replace(" ", "")
        if re.search(functions, cleaned_expr):
            return True
        elif re.fullmatch(r'\d+', cleaned_expr):
            return False  
        return True
    
    return False

def temukan_domain_dan_range(expression):
    x = sp.Symbol('x')
    
    if expression.is_constant():
        domain = sp.S.Reals
        f_range = sp.simplify(expression)
        return domain, {f_range}
    else:
        domain = sp.calculus.util.continuous_domain(expression, x, sp.S.Reals)
        f_range = sp.calculus.util.function_range(expression, x, domain)
    
    return domain, f_range

def analisis_fungsi(expression):
    if not validasi_input(expression):
        return "Ekspresi yang dimasukkan tidak valid."

    try:
        expr = sp.sympify(expression)
        domain, f_range = temukan_domain_dan_range(expr)

        if domain == sp.S.Reals:
            return f"Domain: Semua bilangan real, Range: {f_range}"
        else:
            return f"Domain: {domain}, Range: {f_range}"

    except Exception as e:
        return f"Terjadi kesalahan: {e}"

