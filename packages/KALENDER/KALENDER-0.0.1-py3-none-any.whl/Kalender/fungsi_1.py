import calendar

nama_bulan = {
    "januari": 1,
    "februari": 2,
    "maret": 3,
    "april": 4,
    "mei": 5,
    "juni": 6,
    "juli": 7,
    "agustus": 8,
    "september": 9,
    "oktober": 10,
    "november": 11,
    "desember": 12
}

def tampilkan_kalender(tahun, inputan_bulan):
    try:
        if isinstance(inputan_bulan, int):
            bulan = inputan_bulan
            if 1 <= bulan <= 12:
                print(calendar.month(tahun, bulan))
            else:
                raise ValueError("Bulan harus antara 1 dan 12.")
        
        elif isinstance(inputan_bulan, str):
            bulan = nama_bulan[inputan_bulan.lower()]  
            print(calendar.month(tahun, bulan))
        
        else:
            raise TypeError("Input bulan harus berupa angka atau nama bulan.")

    except KeyError:
        print(f"Nama bulan '{inputan_bulan}' tidak valid. Masukkan nama bulan yang benar.")
    except ValueError as ve:
        print(ve)
    except TypeError as te:
        print(te)