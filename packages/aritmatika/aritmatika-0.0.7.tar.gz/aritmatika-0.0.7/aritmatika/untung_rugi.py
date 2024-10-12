def hitung_untung(harga_beli: float, harga_jual: float) -> float:
    """Hitung keuntungan dari suatu transaksi jual beli."""
    return harga_jual - harga_beli

def hitung_rugi(harga_beli: float, harga_jual: float) -> float:
    """Hitung kerugian dari suatu transaksi jual beli."""
    return harga_beli - harga_jual

def persentase_untung(harga_beli: float, harga_jual: float) -> float:
    """Menghitung persentase keuntungan."""
    if harga_jual > harga_beli:
        return ((harga_jual - harga_beli) / harga_beli) * 100
    return 0

def persentase_rugi(harga_beli: float, harga_jual: float) -> float:
    """Menghitung persentase kerugian."""
    if harga_jual < harga_beli:
        return ((harga_beli - harga_jual) / harga_beli) * 100
    return 0
