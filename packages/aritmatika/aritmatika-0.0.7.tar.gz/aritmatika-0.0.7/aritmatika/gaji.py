def hitung_gaji_pokok(gaji_per_jam: float, jam_kerja: float) -> float:
    """Menghitung gaji pokok."""
    return gaji_per_jam * jam_kerja

def hitung_gaji_bersih(gaji_pokok: float, potongan_pajak: float, potongan_bpjs: float, potongan_lain: float = 0) -> float:
    """Menghitung gaji bersih."""
    return gaji_pokok - potongan_pajak - potongan_bpjs - potongan_lain

def hitung_gaji_lembur(jam_lembur: float, tarif_lembur: float) -> float:
    """Menghitung gaji lembur."""
    return jam_lembur * tarif_lembur

def hitung_total_gaji(gaji_pokok: float, gaji_lembur: float, tunjangan: float) -> float:
    """Menghitung total gaji."""
    return gaji_pokok + gaji_lembur + tunjangan

def hitung_rata_rata_gaji(list_gaji: list) -> float:
    """Menghitung rata-rata gaji."""
    return sum(list_gaji) / len(list_gaji)
