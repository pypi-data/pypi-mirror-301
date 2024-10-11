import calendar 

bulan = {
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

# # Mengganti input dengan nilai yang sudah ditentukan
# tahun = 2024  
# bulan_awal = bulan["januari"]  # Misalnya mulai dari Januari
# bulan_akhir = bulan["maret"]  # Hingga Maret

def tampilkan_bulan_range(tahun, bulan_awal, bulan_akhir):
    hasil = ""
    for b in range(bulan_awal, bulan_akhir + 1):
        hasil += calendar.month(tahun, b) + "\n"
    return hasil

tahun = 2024
bulan_awal = 1
bulan_akhir = 4

print(tampilkan_bulan_range(tahun, bulan_awal, bulan_akhir))