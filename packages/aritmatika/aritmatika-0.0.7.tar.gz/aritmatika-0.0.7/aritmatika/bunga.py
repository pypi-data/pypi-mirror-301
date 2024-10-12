def bunga_tunggal(p, r, t):
    """
    Menghitung bunga tunggal.
    
    Parameter:
    P (float): Pokok pinjaman (modal awal)
    r (float): Suku bunga per periode (dalam desimal, contoh 5% menjadi 0.05)
    t (float): Waktu (periode dalam tahun atau bulan)

    Returns:
    float: Nilai bunga yang dihasilkan
    """
    bunga =  p * r * t
    return bunga

def bunga_majemuk(p, r, n, t):
    """
    Menghitung bunga majemuk.

    Parameter:
    P (float): Pokok pinjaman (modal awal)
    r (float): Suku bunga per periode (dalam desimal)
    n (int): Frekuensi penggabungan bunga per periode (contoh: tahunan, bulanan)
    t (float): Waktu dalam tahun atau periode lainnya

    Returns:
    float: Nilai total (pokok + bunga) yang dihasilkan
    """
    total = p * (1 + r / n) ** (n * t)
    return total

