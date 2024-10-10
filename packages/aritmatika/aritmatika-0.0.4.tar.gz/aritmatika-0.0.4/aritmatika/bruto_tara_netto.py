def hitung_bruto(netto, tara):
    """Hitung bruto dari netto dan tara.

    Args:
      netto: Berat bersih suatu barang.
      tara: Berat dari suatu kemasan.

    Returns:
      Bruto dari barang tersebut.
    """
    return netto + tara

def hitung_tara(bruto, netto):
    """Hitung tara dari bruto dan netto.

    Args:
      bruto: Berat kotor suatu barang.
      netto: Berat bersih suatu barang.

    Returns:
      Tara atau berat kemasan dari barang tersebut.
    """
    return bruto - netto

def hitung_netto(bruto, tara):
    """Hitung netto dari bruto dan tara.

    Args:
      bruto: Berat kotor suatu barang.
      tara: Berat dari suatu kemasan.

    Returns:
      Netto dari barang tersebut.
    """
    return bruto - tara
