def jarak_langkah(jenis_kelamin, tinggi_badan, banyak_langkah): 
    """
    Menghitung jarak dari banyak langkah yang ditempuh berdasarkan jenis kelamin dan tinggi badan.
    Args:
        jenis_kelamin (str): untuk laki-laki disimbolkan "L", sedangkan perempuan "P"
        tinggi_badan (float): tinggi badan dalam satuan meter
        banyak_langkah (int): jumlah langkah yang ditempuh
    Example:
        jarak_langkah("L", 1.7, 2000)
    """ 
    try:
        if tinggi_badan <= 0 or banyak_langkah <= 0:
            raise ValueError("Tinggi badan dan banyak langkah harus angka positif dan tidak nol.")
        
        if jenis_kelamin.upper() == "L":  
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
            raise ValueError("Jenis kelamin yang dipilih tidak valid. Gunakan 'L' untuk laki-laki atau 'P' untuk perempuan.")
        
        jarak = banyak_langkah * panjang
        return f"Jarak yang ditempuh: {jarak:,} meter"
    
    except ValueError as error:
        return f"Error: {error}"



    


