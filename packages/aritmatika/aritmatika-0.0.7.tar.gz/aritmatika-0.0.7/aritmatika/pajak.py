def ppn(transaksi: float, tarif_ppn: float = 0.11) -> float:
    """Menghitung pajak pertambahan nilai atau PPN."""
    return transaksi * tarif_ppn

def total_bayar(transaksi: float, tarif_ppn: float = 0.11) -> float:
    """Menghitung total yang harus dibayar setelah PPN."""
    return transaksi + ppn(transaksi, tarif_ppn)

def njkp(njop: float) -> float:
    """Menghitung NJKP untuk dipakai menghitung PBB."""
    if njop <= 1000000000:
        persen_njkp = 20
    else:
        persen_njkp = 40
    return njop * (persen_njkp / 100)

def pbb(njop: float, persen_pbb: float = 0.5) -> float:
    """Menghitung Pajak Bumi dan Bangunan (PBB)."""
    return njkp(njop) * (persen_pbb / 100)

def hitung_pph(penghasilan: float, status_pernikahan: str, jumlah_tanggungan: int) -> float:
    """Menghitung PPH (Pajak Penghasilan)."""
    if status_pernikahan == 'lajang':
        ptkp = 54000000  
    else:  # Menikah
        ptkp = 58500000 + (4500000 * min(jumlah_tanggungan, 3))

    pkp = penghasilan - ptkp

    if pkp <= 0:
        return 0

    if pkp <= 50000000:
        return pkp * 0.05
    elif pkp <= 250000000:
        return (50000000 * 0.05) + ((pkp - 50000000) * 0.15)
    elif pkp <= 500000000:
        return (50000000 * 0.05) + (200000000 * 0.15) + ((pkp - 250000000) * 0.25)
    else:
        return (50000000 * 0.05) + (200000000 * 0.15) + (250000000 * 0.25) + ((pkp - 500000000) * 0.30)
