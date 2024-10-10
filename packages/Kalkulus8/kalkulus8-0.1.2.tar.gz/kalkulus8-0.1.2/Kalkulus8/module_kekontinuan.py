def is_continuous(f, x, epsilon=1e-7):
    """
    Fungsi untuk memeriksa apakah fungsi f kontinu di titik x.
    
    Parameter:
    - f: fungsi matematika yang akan diuji (contoh: lambda x: x**2)
    - x: titik di mana kekontinuan akan diuji
    - epsilon: batas toleransi untuk menghitung limit (default: 1e-7)
    
    Return:
    - True jika fungsi kontinu di titik x, False jika tidak.
    """
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
    """
    Memeriksa kekontinuan fungsi f dalam interval [start, end].
    
    Parameter:
    - f: fungsi matematika yang akan diuji
    - start: titik awal interval
    - end: titik akhir interval
    - step: jarak antar titik evaluasi (default: 0.1)
    - epsilon: batas toleransi untuk menghitung limit (default: 1e-7)
    
    Return:
    - Daftar titik-titik di mana fungsi tidak kontinu.
    """
    discontinuities = []
    x = start
    while x <= end:
        if not is_continuous(f, x, epsilon):
            discontinuities.append(x)
        x += step
    return discontinuities

def check_continuity_at_points(f, points, epsilon=1e-7):
    """
    Memeriksa kekontinuan fungsi f di beberapa titik yang diberikan.
    
    Parameter:
    - f: fungsi matematika yang akan diuji
    - points: daftar titik di mana kekontinuan akan diuji
    - epsilon: batas toleransi untuk menghitung limit (default: 1e-7)
    
    Return:
    - Daftar tuple yang berisi titik-titik dan status kekontinuannya.
    """
    results = []
    for x in points:
        is_cont = is_continuous(f, x, epsilon)
        results.append((x, is_cont))
    return results

def is_continuous_everywhere(f, domain, epsilon=1e-7, step=0.1):
    """
    Memeriksa apakah fungsi f kontinu di setiap titik dalam domain.
    
    Parameter:
    - f: fungsi matematika yang akan diuji
    - domain: tuple yang mendefinisikan batas domain (contoh: (-10, 10))
    - epsilon: batas toleransi untuk menghitung limit (default: 1e-7)
    - step: jarak antar titik evaluasi dalam domain (default: 0.1)
    
    Return:
    - True jika fungsi kontinu di seluruh domain, False jika ada diskontinuitas.
    """
    start, end = domain
    x = start
    while x <= end:
        if not is_continuous(f, x, epsilon):
            return False
        x += step
    return True

# # Cek kekontinuan di satu titik
# print(is_continuous(lambda x: x**2, 1))  # True

# # Cek kekontinuan pada interval [-1, 1] untuk fungsi 1/x
# print(check_continuity_interval(lambda x: 1/x if x != 0 else None, -1, 1))

# # Cek kekontinuan di beberapa titik
# points_to_check = [-1, 0, 1, 2]
# print(check_continuity_at_points(lambda x: 1/x if x != 0 else None, points_to_check))

# # Cek kekontinuan di seluruh domain [-10, 10]
# print(is_continuous_everywhere(lambda x: x**2, (-10, 10)))  # True