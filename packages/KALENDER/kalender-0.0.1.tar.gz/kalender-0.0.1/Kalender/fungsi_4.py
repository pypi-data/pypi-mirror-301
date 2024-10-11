import holidays
import calendar

def ambil_hari_libur(tahun, bulan):
    
    id_holidays = holidays.Indonesia(years=tahun)
    
    hari_libur_bulanan = {
        tanggal: nama for tanggal, nama in id_holidays.items() if tanggal.month == bulan
    }

    return hari_libur_bulanan

def tampilkan_hari_libur(tahun, bulan):
    hari_libur_dalam_bulan = ambil_hari_libur(tahun, bulan)
    hasil = []

    if hari_libur_dalam_bulan:
        hasil.append(f"Hari libur nasional di bulan {calendar.month_name[bulan]} {tahun}:")
        for tanggal, nama in hari_libur_dalam_bulan.items():
            hasil.append(f"{tanggal.day} {calendar.month_name[tanggal.month]} - {nama}")
    else:
        hasil.append(f"Tidak ada hari libur nasional di bulan {calendar.month_name[bulan]} {tahun}.")

    return hasil

tahun = 2024  # Ganti dengan tahun yang diinginkan
bulan = 10    # Ganti dengan bulan yang diinginkan

hasil_hari_libur = tampilkan_hari_libur(tahun, bulan)

hasil_hari_libur


