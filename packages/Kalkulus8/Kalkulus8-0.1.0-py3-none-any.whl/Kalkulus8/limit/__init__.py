def hitung_limit_kanan_kiri(fungsi_str, titik):
    """
    Hitung limit kanan dan kiri dari sebuah fungsi piecewise pada titik tertentu.

    Args:
        fungsi_str (str): Representasi string dari fungsi piecewise.
            Format: "fungsi1 jika kondisi1, fungsi2 jika kondisi2, ..."
            Contoh: "(x-2)/(x+3) jika x<1, x**2 + 3*x jika x>=1"
        titik (float): Titik yang ingin dicari limitnya.

    Returns:
        tuple: Tuple berisi limit kanan dan limit kiri.

    Contoh penggunaan:
        >>> fungsi_str = '(x-2)/(x+3) jika x<1, x**2 + 3*x jika x>=1'
        >>> titik = 1
        >>> limit_kanan, limit_kiri = hitung_limit_kanan_kiri(fungsi_str, titik)
        >>> print(f"Limit kanan dari f(x) ketika x mendekati {titik} adalah {limit_kanan}")
        >>> print(f"Limit kiri dari f(x) ketika x mendekati {titik} adalah {limit_kiri}")

    Fungsi ini akan memecah fungsi piecewise menjadi beberapa bagian berdasarkan kondisi.
    Kemudian, menggunakan library SymPy, fungsi ini akan menghitung limit kanan dan kiri dari fungsi tersebut
    pada titik yang diberikan.

    **Catatan:**
    * Fungsi piecewise harus didefinisikan dalam bentuk string dengan format yang telah ditentukan.
    * Kondisi harus berupa ekspresi boolean yang valid dalam SymPy.
    * Fungsi ini akan mengembalikan nilai `nan` jika limit tidak ada.
    """
    # ... sisa kode fungsi ...