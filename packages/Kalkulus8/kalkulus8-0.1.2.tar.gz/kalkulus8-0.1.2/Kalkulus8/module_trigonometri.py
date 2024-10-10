import math

def trigonometri(sudut_derajat):
    sudut_radians = math.radians(sudut_derajat)

    sin = math.sin(sudut_radians)
    cos = math.cos(sudut_radians)
    tan = math.tan(sudut_radians)

    cot = None if tan == 0 else 1/tan
    sec = None if cos == 0 else 1/cos
    csc = None if sin == 0 else 1/sin

    return {
        "sudut (derajat)": sudut_derajat,
        "sin": sin,
        "cos": cos,
        "tan": tan,
        "cot": cot,
        "sec": sec,
        "csc": csc
    }

def penyesualian_sudut_dengan_kuadran(sudut, kuadran):
    if kuadran == 1:
        return sudut
    elif kuadran == 2:
        return 180 - sudut
    elif kuadran == 3:
        return 180 + sudut
    elif kuadran == 4:
        return 360 - sudut
    else:
        return None

def hitung_trigonometri_dengan_kuadran(sudut, kuadran):
    if kuadran not in [1, 2, 3, 4]:
        raise ValueError("Kuadran hanya bisa bernilai 1-4.")

    penyesuaian_sudut = penyesualian_sudut_dengan_kuadran(sudut, kuadran)

    if penyesuaian_sudut is None:
        raise ValueError("Sudut tidak valid.")

    result = trigonometri(penyesuaian_sudut)

    return {
        "sudut asli": sudut,
        "sudut disesuaikan": penyesuaian_sudut,
        "sin": result['sin'],
        "cos": result['cos'],
        "tan": result['tan'],
        "cot": result['cot'],
        "sec": result['sec'],
        "csc": result['csc']
    }

# contoh penggunaan 
# result = hitung_trigonometri_dengan_kuadran(30, 2)
# print(result)
