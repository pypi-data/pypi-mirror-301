import sympy as sp

def hitung_limit_kanan_kiri(fungsi_str, titik):
    try:
        x = sp.Symbol('x')
        fungsi_kondisi_list = fungsi_str.split(',')

        kondisi_pieces = []
        for fungsi_kondisi in fungsi_kondisi_list:
            try:
                if not isinstance(titik, (int, float)):
                    return "Titik yang dimasukkan bukan bilangan."
                if "jika" in fungsi_kondisi:
                    fungsi_part, kondisi_part = fungsi_kondisi.split("jika")
                    fungsi = sp.sympify(fungsi_part.strip())
                    kondisi = sp.sympify(kondisi_part.strip())
                else:
                    fungsi = sp.sympify(fungsi_kondisi.strip())
                    kondisi = True
                kondisi_pieces.append((fungsi, kondisi))
            except (SyntaxError, ValueError) as e:
                return f"Terjadi kesalahan sintaksis atau tipe data dalam fungsi: {e}"
            except NameError as e:
                return f"Variabel tidak terdefinisi: {e}"
            except ZeroDivisionError:
                return "Fungsi tidak terdefinisi pada titik tersebut."
            except Exception as e:
                return f"Terjadi kesalahan tak terduga: {e}"

        fungsi_piecewise = sp.Piecewise(*kondisi_pieces)
        print(f"Fungsi piecewise yang terbentuk: {fungsi_piecewise}")  # Untuk debugging

        limit_kanan = sp.limit(fungsi_piecewise, x, titik, dir='+')
        limit_kiri = sp.limit(fungsi_piecewise, x, titik, dir='-')

        return f"Limit kanan: {limit_kanan}\nLimit kiri: {limit_kiri}"

    except Exception as e:
        return f"Terjadi kesalahan: {e}"

# Contoh penggunaan
# fungsi_str = '(x-2)/(x+3) jika x<1, x**2 + 3*x jika x>=1'
# titik = 2

# hasil = hitung_limit_kanan_kiri(fungsi_str, titik)
# print(hasil)