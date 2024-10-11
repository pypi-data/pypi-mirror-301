import sympy as sp
import re

def hitung_limit_kanan_kiri(fungsi_str, titik):
    try:
        try:
            x = sp.Symbol('x')
            fungsi_kondisi_list = fungsi_str.split(',')
            for fungsi_kondisi in fungsi_kondisi_list:
                if "jika" in fungsi_kondisi:
                    fungsi_part, kondisi_part = fungsi_kondisi.split("jika")
                    fungsi = sp.sympify(fungsi_part.strip())
                    kondisi = sp.sympify(kondisi_part.strip())
                else:
                    fungsi = sp.sympify(fungsi_kondisi.strip())
                    kondisi = True
        except (SyntaxError, ValueError) as e:
            return "Fungsi yang dimasukkan tidak valid."

        if not isinstance(titik, (int, float)):
            return "Titik yang dimasukkan tidak valid."

        if re.search(r'[a-zA-Z]', str(titik)):
            return "Titik yang dimasukkan tidak valid."

        kondisi_pieces = []
        for fungsi_kondisi in fungsi_kondisi_list:
            try:
                if "jika" in fungsi_kondisi:
                    fungsi_part, kondisi_part = fungsi_kondisi.split("jika")
                    fungsi = sp.sympify(fungsi_part.strip())
                    kondisi = sp.sympify(kondisi_part.strip())
                else:
                    fungsi = sp.sympify(fungsi_kondisi.strip())
                    kondisi = True
                kondisi_pieces.append((fungsi, kondisi))
            except (SyntaxError, ValueError) as e:
                raise ValueError(f"Terjadi kesalahan sintaksis atau tipe data dalam fungsi: {e}")
            except NameError as e:
                raise ValueError(f"Variabel tidak terdefinisi: {e}")
            except ZeroDivisionError:
                raise ValueError("Fungsi tidak terdefinisi pada titik tersebut.")
            except Exception as e:
                raise ValueError(f"Terjadi kesalahan tak terduga: {e}")

        if not kondisi_pieces:
            raise ValueError("Fungsi piecewise tidak dapat dibentuk.")

        fungsi_piecewise = sp.Piecewise(*kondisi_pieces)
        print(f"Fungsi piecewise yang terbentuk: {fungsi_piecewise}")  

        limit_kanan = sp.limit(fungsi_piecewise, x, titik, dir='+')
        limit_kiri = sp.limit(fungsi_piecewise, x, titik, dir='-')

        return f"Limit kanan: {limit_kanan}\nLimit kiri: {limit_kiri}"

    except Exception as e:
        return f"Terjadi kesalahan: {e}"

