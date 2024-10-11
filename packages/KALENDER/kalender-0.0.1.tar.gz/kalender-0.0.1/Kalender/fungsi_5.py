def cek_tahun_kabisat(tahun):
    if (tahun % 4 == 0 and tahun % 100 != 0) or (tahun % 400 == 0):
        return f"{tahun} adalah tahun kabisat."
    else:
        return f"{tahun} bukan tahun kabisat."
