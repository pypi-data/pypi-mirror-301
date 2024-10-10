def panjang_langkah(jenis_kelamin, tinggi_badan):
    if jenis_kelamin == 1:  
        if 1.5 <= tinggi_badan <= 1.59:
            return 0.625
        elif 1.6 <= tinggi_badan <= 1.69:
            return 0.675
        elif 1.7 <= tinggi_badan <= 1.79:
            return 0.725
        elif 1.8 <= tinggi_badan <= 1.89:
            return 0.775
        elif 1.9 <= tinggi_badan <= 2:
            return 0.875
    elif jenis_kelamin == 2: 
        if 1.5 <= tinggi_badan <= 1.59:
            return 0.595
        elif 1.6 <= tinggi_badan <= 1.69:
            return 0.645
        elif 1.7 <= tinggi_badan <= 1.79:
            return 0.695
        elif 1.8 <= tinggi_badan <= 1.89:
            return 0.745
        elif 1.9 <= tinggi_badan <= 2:
            return 0.795
    return "Tinggi di luar rentang."

def hitung_jarak(banyak_langkah, panjang_langkah):
    if not isinstance(panjang_langkah, float):
        return panjang_langkah
    jarak = banyak_langkah * panjang_langkah
    return jarak


print(hitung_jarak(2000, panjang_langkah(1, 1.7)))
