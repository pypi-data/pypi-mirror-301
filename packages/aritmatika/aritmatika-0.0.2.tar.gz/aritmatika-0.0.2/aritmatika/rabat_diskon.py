
def hitung_diskon(harga_awal, diskon_persen):
    # Menghitung jumlah diskon berdasarkan persentase yang diberikan
    diskon = harga_awal * diskon_persen / 100
    
    # Mengurangi harga awal dengan jumlah diskon untuk mendapatkan harga akhir
    harga_setelah_diskon = harga_awal - diskon
    
    # Mengembalikan harga akhir setelah diskon
    return harga_setelah_diskon

    """
    contoh pemakaian 
    harga_awal = 150000
    diskon_persen = 15

    harga_diskon = hitung_diskon(harga_awal, diskon_persen)
    print(f"Harga setelah diskon: Rp{harga_diskon}")

    """

def hitung_persen_diskon(harga_awal, harga_setelah_diskon):
    # Menghitung selisih antara harga awal dan harga setelah diskon
    diskon = harga_awal - harga_setelah_diskon
    
    # Menghitung persentase diskon
    persen_diskon = (diskon / harga_awal) * 100
    
    # Mengembalikan persentase diskon
    return persen_diskon
    """
    harga_awal = 200000
    harga_setelah_diskon = 150000

    persen_diskon = hitung_persen_diskon(harga_awal, harga_setelah_diskon)
    print(f"Persentase diskon: {persen_diskon}%")

    """

    
def hitung_rabat(harga_per_barang, jumlah_barang, rabat_persen):
    # Menghitung total harga sebelum rabat
    total_harga = harga_per_barang * jumlah_barang
    
    # Menghitung jumlah rabat berdasarkan persentase rabat
    rabat = total_harga * rabat_persen / 100
    
    # Mengurangi total harga dengan rabat untuk mendapatkan harga akhir
    total_setelah_rabat = total_harga - rabat
    
    return total_setelah_rabat

    """
    harga_per_barang = 60000
    jumlah_barang = 8
    rabat_persen = 10

    total_bayar = hitung_rabat(harga_per_barang, jumlah_barang, rabat_persen)
    print(f"Total bayar setelah rabat: Rp{total_bayar}")
    """