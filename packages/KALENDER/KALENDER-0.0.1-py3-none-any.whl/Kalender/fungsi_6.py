import calendar

hari_dalam_indonesia = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
bulan_dalam_indonesia = {
    "Januari": 1, "Februari": 2, "Maret": 3, "April": 4,
    "Mei": 5, "Juni": 6, "Juli": 7, "Agustus": 8,
    "September": 9, "Oktober": 10, "November": 11, "Desember": 12
}

def is_weekday(year, month, day):
    month = convert_month_to_int(month)
    weekday = calendar.weekday(year, month, day)
    is_weekday_result = weekday < 5
    print(f"{day}/{month}/{year} adalah {'hari kerja' if is_weekday_result else 'hari libur'}")
    return is_weekday_result

def is_weekend(year, month, day):
    month = convert_month_to_int(month)
    is_weekend_result = not is_weekday(year, month, day)
    print(f"{day}/{month}/{year} adalah {'akhir pekan' if is_weekend_result else 'hari kerja'}")
    return is_weekend_result

def get_day_name(year, month, day):
    month = convert_month_to_int(month)
    weekday = calendar.weekday(year, month, day)
    day_name = hari_dalam_indonesia[weekday]
    print(f"Nama hari: {day_name}")
    return day_name

def convert_month_to_int(month):
    if isinstance(month, int):
        return month
    elif isinstance(month, str):
        month = month.capitalize()
        if month in bulan_dalam_indonesia:
            return bulan_dalam_indonesia[month]
        else:
            raise ValueError("Nama bulan tidak valid.")
    else:
        raise TypeError("Bulan harus berupa nama atau angka.")