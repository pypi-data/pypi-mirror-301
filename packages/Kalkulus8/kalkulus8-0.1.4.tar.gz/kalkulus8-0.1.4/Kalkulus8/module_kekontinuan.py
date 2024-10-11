def is_continuous(f, x, epsilon=1e-7):
    from sympy import limit, Symbol  
    x_sym = Symbol('x')
    
    try:
        limit_left = limit(f(x_sym), x_sym, x, dir='-')
        limit_right = limit(f(x_sym), x_sym, x, dir='+')
        f_value = f(x)
        
        return abs(limit_left - limit_right) < epsilon and abs(limit_left - f_value) < epsilon
    except:
        return False

def check_continuity_interval(f, start, end, step=0.1, epsilon=1e-7):
    discontinuities = []
    x = start
    while x <= end:
        if not is_continuous(f, x, epsilon):
            discontinuities.append(x)
        x += step
    return discontinuities

def check_continuity_at_points(f, points, epsilon=1e-7):
    results = []
    for x in points:
        is_cont = is_continuous(f, x, epsilon)
        results.append((x, is_cont))
    return results

def is_continuous_everywhere(f, domain, epsilon=1e-7, step=0.1):
    start, end = domain
    x = start
    while x <= end:
        if not is_continuous(f, x, epsilon):
            return False
        x += step
    return True
