def rekomendasi_asupan_air(berat_badan):
    """
    
    """
    if isinstance(berat_badan, int):
        return berat_badan * 35 / 1000
    else:
        return "Masukkan dalam bentuk angka"
