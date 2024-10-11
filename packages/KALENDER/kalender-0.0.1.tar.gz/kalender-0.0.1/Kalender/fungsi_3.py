import calendar

def tampilkan_kalender_range(start_year, end_year):
    for year in range(start_year, end_year + 1):
        print(calendar.calendar(year))

start_year = int(input("Masukkan tahun awal: "))
end_year = int(input("Masukkan tahun akhir: "))

tampilkan_kalender_range(start_year, end_year)