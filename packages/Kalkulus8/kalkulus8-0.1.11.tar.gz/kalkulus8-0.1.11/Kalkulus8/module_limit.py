import sympy as sp
import re

def hitung_limit_kanan_kiri(fungsi_str, titik):
    if not isinstance(titik, (int, float)):
        return "Titik harus berupa angka (int atau float)."

    x = sp.Symbol('x')

    if not re.match(r'^[\w\s\*\+\-/\^<>=,jika]*$', fungsi_str):
        return "Fungsi mengandung karakter tidak valid."

    fungsi_kondisi_list = fungsi_str.split(',')
    kondisi_pieces = []

    for fungsi_kondisi in fungsi_kondisi_list:
        fungsi_kondisi = fungsi_kondisi.strip()
        
        if "jika" in fungsi_kondisi:
            fungsi_part, kondisi_part = fungsi_kondisi.split("jika")
            fungsi = sp.sympify(fungsi_part.strip())
            kondisi = sp.sympify(kondisi_part.strip())
        else:
            fungsi = sp.sympify(fungsi_kondisi)
            kondisi = True

        kondisi_pieces.append((fungsi, kondisi))

    fungsi_piecewise = sp.Piecewise(*kondisi_pieces)

    limit_kanan = sp.limit(fungsi_piecewise, x, titik, dir='+')
    limit_kiri = sp.limit(fungsi_piecewise, x, titik, dir='-')

    return f"Limit kanan: {limit_kanan}\nLimit kiri: {limit_kiri}"

