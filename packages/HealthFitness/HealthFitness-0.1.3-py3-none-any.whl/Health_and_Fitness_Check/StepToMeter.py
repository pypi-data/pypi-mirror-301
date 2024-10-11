def panjang_langkah(jenis_kelamin, tinggi_badan, banyak_langkah):  
    if tinggi_badan <= 0 or banyak_langkah <= 0:
        return "Masukkan angka positif dan tidak nol"
    elif jenis_kelamin.upper() == "L":  
        if 1.5 <= tinggi_badan <= 1.59:
            panjang = 0.625
        elif 1.6 <= tinggi_badan <= 1.69:
            panjang = 0.675
        elif 1.7 <= tinggi_badan <= 1.79:
            panjang = 0.725
        elif 1.8 <= tinggi_badan <= 1.89:
            panjang = 0.775
        elif 1.9 <= tinggi_badan <= 2:
            panjang = 0.875
    elif jenis_kelamin.upper() == "P": 
        if 1.5 <= tinggi_badan <= 1.59:
            panjang = 0.595
        elif 1.6 <= tinggi_badan <= 1.69:
            panjang = 0.645
        elif 1.7 <= tinggi_badan <= 1.79:
            panjang = 0.695
        elif 1.8 <= tinggi_badan <= 1.89:
            panjang = 0.745
        elif 1.9 <= tinggi_badan <= 2:
            panjang = 0.795
    else:
        return "jenis kelamin yang di pilih tidak valid"
    jarak = banyak_langkah * panjang
    return f"Jarak yang ditempuh: {jarak:,} meter"

def hitung_jarak(banyak_langkah, jenis_kelamin, tinggi):
    """
    Menghitung jarak yang ditempuh berdasarkan jenis kelamin, tinggi badan, dan banyaknya langkah.
    Args:
        jenis_kelamin (str): untuk laki-laki disimbolkan "L", sedangkan perempuan "P"
        tinggi_badan (float): tinggi badan dalam satuan meter
        banyak_langkah (int): jumlah langkah yang ditempuh
    Example:
        hitung_jarak(2000, "L", 1.6)
    """
    hasil_jarak = panjang_langkah(jenis_kelamin, tinggi, banyak_langkah)
    return hasil_jarak
print(hitung_jarak(2000, "L", 1.6))
