def rekomendasi_asupan_air(berat_badan):
    """Menghitung Kebutuhan Air dalam sehari
    Args:
        berat_badan (int) : Berat Badan dalam kilogram
    Example:
        rekomendasi_asupan_air(70)
    
    """
    if isinstance(berat_badan, int):
        return f"{berat_badan * 35 / 1000} liter"
    else:
        return "Masukkan dalam bentuk angka"
