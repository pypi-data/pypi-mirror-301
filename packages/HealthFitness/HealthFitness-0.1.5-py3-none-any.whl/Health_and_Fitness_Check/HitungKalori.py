def hitung_kalori(berat_badan, durasi, aktivitas):
    """Menghitung jumlah kalori yang dibakar berdasarkan berat badan, durasi aktivitas, dan jenis aktivitas.
    Args:
        berat_badan (float): Berat badan dalam kilogram.
        durasi (float): Durasi aktivitas dalam menit.
        aktivitas (str): Jenis aktivitas yang dilakukan.
    Example:
        hitung_kalori(70, 60, jogging)
    Aktifitas Tersedia:
        "duduk di meja"
        "berjalan santai"
        "bersepeda ringan"
        "jogging" 
        "berenang" 
        "lari cepat"
        
    """
    try:
        met_values = {
            "duduk di meja": 1,
            "berjalan santai": 2.5,
            "bersepeda ringan": 4.5,
            "jogging": 7.5,
            "berenang": 7.5,
            "lari cepat": 11
        }

        if aktivitas not in met_values:
            return "Aktivitas tidak dikenali. Harap masukkan aktivitas yang valid."
        
    
        if berat_badan <= 0 :
            return "Berat badan kurang dari 0, mohon isi ulang"
        elif durasi <= 0 :
            return "durasi kurang dari 0, mohon isi ulang"
        
            
        met = met_values[aktivitas]
        kalori_per_menit = (met * 3.5 * berat_badan) / 200
        total_kalori = kalori_per_menit * durasi
        return total_kalori
    except:
        return "Input tidak valid"
    


print(hitung_kalori(70, 60, "jogging"))
