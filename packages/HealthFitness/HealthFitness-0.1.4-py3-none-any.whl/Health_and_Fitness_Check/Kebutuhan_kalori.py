def kebutuhan_kalori_harian(berat, tinggi, usia, jenis_kelamin, tingkat_aktivitas):
    """Menghitung kebutuhan kalori harian berdasarkan statistik tubuh dan tingkat aktivitas
    Args:
        berat (float): Berat badan dalam kilogram
        tinggi (float) : tinggi dalam centimeter
        usia (int): Umur dalam angka
        jenis_kelamin (str): untuk laki-laki di simbolkan "L", sedangkan perempuan "P"
        tingkat_aktifitas (str): rendah, sedang dan tinggi
    Example:
        kebutuhan_kalori_harian(70, 170, 18, "L", "sedang")
    """
    try:      
        if jenis_kelamin.upper() == 'L':
            bmr = 10 * berat + 6.25 * tinggi - 5 * usia + 5
        elif jenis_kelamin.upper() == 'P':
            bmr = 10 * berat + 6.25 * tinggi - 5 * usia - 161
        else:
            raise ValueError("Jenis kelamin tidak valid. Gunakan 'L' untuk laki-laki atau 'P' untuk perempuan.")
        if tingkat_aktivitas.lower() == 'rendah':
            kalori_harian = bmr * 1.2
        elif tingkat_aktivitas.lower() == 'sedang':
            kalori_harian = bmr * 1.55
        elif tingkat_aktivitas.lower() == 'tinggi':
            kalori_harian = bmr * 1.9
        else:
            raise ValueError("Tingkat aktivitas tidak valid. Gunakan 'rendah', 'sedang', atau 'tinggi'.")  
        return f"{kalori_harian:,} kalori"
    except:
        return "Inputan invalid"


