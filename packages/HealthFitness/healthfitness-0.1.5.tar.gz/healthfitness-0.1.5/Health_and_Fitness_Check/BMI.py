def hitung_dan_tampilkan_bmi(tinggi, berat, jenis_kelamin):
    """Fungsi untuk menghitun, menampilkan hasil BMI dan kategorinya.
    Args:
        tinggi (float) : tinggi badan dalam satuan meter.
        berat (float) : berat badan dalam satuan kg.
        jenis kelamin (str) : "1"/ "laki laki" "2" / "perempuan".
    Example:
        tampilkan_hasil_bmi(1.8, 50.9, "perempuan")"""

    bmi = berat / tinggi**2

    if jenis_kelamin == "1" or jenis_kelamin == "laki laki":
        if bmi < 18:
            kategori = "kekurangan berat badan (laki-laki)"
        elif 18 <= bmi <= 23.9:
            kategori = "normal (laki-laki)"
        elif 24 <= bmi <= 26.9:
            kategori = "kelebihan berat badan (laki-laki)"
        else:
            kategori = "obesitas (laki-laki)"
    elif jenis_kelamin == "2" or jenis_kelamin == "perempuan":
        if bmi < 19:
            kategori = "kekurangan berat badan (perempuan)"
        elif 19 <= bmi <= 24.9:
            kategori = "normal (perempuan)"
        elif 25 <= bmi <= 27.9:
            kategori = "kelebihan berat badan (perempuan)"
        else:
            kategori = "obesitas (perempuan)"
    else:
        return "Jenis kelamin tidak valid"
    
    print(f"Dengan tinggi badan {tinggi} m dan berat badan {berat} kg, nilai BMI anda adalah : {bmi:.2f}")
    print(f"Kategori BMI anda adalah : {kategori}")












