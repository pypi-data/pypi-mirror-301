"""Menghitung kebutuhan kalori harian berdasarkan statistik tubuh dan tingkat aktivitas."""

def kebutuhan_kalori_harian(berat, tinggi, usia, jenis_kelamin, tingkat_aktivitas):
    try:
        # Hitung BMR
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
        
        return kalori_harian
    except:
        return "Inputan invalid"

# while True:
#     try:
#         # Input pengguna
#         berat = int(input('Masukkan berat badan (kg) : ')) 
#         tinggi = int(input('Masukkan tinggi badan (cm) : '))  
#         usia = int(input('Masukkan usia (tahun) : '))   
#         jenis_kelamin = (input('Masukkan jenis kelamin (L/P) : ')).upper()  
#         tingkat_aktivitas = (input('Masukkan tingkat aktivitas (rendah/sedang/tinggi) : ')).lower()  

#         # kebutuhan kalori
#         kebutuhan_kalori = kebutuhan_kalori_harian(berat, tinggi, usia, jenis_kelamin, tingkat_aktivitas)
#         print(f"Kebutuhan kalori harian: {kebutuhan_kalori:.2f} kalori")

#     except ValueError:
#         print(f"Kesalahan: Input tidak valid")
    
#     # apakah pengguna ingin menghitung lagi
#     ulang = input("Ingin menghitung lagi? (ya/tidak): ").lower()
#     if ulang == 'tidak':
#         print("Terima kasih! Program selesai.")
#         break


