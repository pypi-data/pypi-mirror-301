# Function 1 : Body Mass Index (BMI)
def hitung_bmi(tinggi_badan, berat_badan):
    """Menghitung BMI berdasarkan tinggi badan (meter) dan berat badan (kg)."""
    bmi = berat_badan / tinggi_badan**2
    return bmi

def kategori_bmi(jenis_kelamin, bmi):
    """Menentukan kategori BMI berdasarkan jenis kelamin dan nilai BMI."""
    if jenis_kelamin == "1" or jenis_kelamin == "laki laki":
        if bmi < 18:
            return "Underweight (Laki-laki)"
        elif 18 <= bmi <= 23.9:
            return "Normal (Laki-laki)"
        elif 24 <= bmi <= 26.9:
            return "Overweight (Laki-laki)"
        else:
            return "Obese (Laki-laki)"
    elif jenis_kelamin == "2" or jenis_kelamin == "perempuan":
        if bmi < 19:
            return "Underweight (Perempuan)"
        elif 19 <= bmi <= 24.9:
            return "Normal (Perempuan)"
        elif 25 <= bmi <= 27.9:
            return "Overweight (Perempuan)"
        else:
            return "Obese (Perempuan)"
    else:
        return "Jenis kelamin tidak valid"

# Fungsi untuk menampilkan hasil BMI dan kategorinya
def tampilkan_hasil_bmi(tinggi, berat, jenis_kelamin):
    """Fungsi untuk menghitung dan menampilkan hasil BMI dan kategori."""
    bmi_result = hitung_bmi(tinggi, berat)
    kategori = kategori_bmi(jenis_kelamin, bmi_result)
    print(f"Dengan tinggi badan {tinggi} m dan berat badan {berat} kg, nilai BMI Anda adalah: {bmi_result:.2f}")
    print(f"Kategori BMI Anda adalah: {kategori}")

