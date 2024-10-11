def binertointerger(Biner):
    """
    Mengonversi bilangan bulat menjadi string biner.

    Parameter:
    - Biner (int): Bilangan bulat yang akan dikonversi ke biner.

    Mengembalikan:
    - str: Representasi biner dari bilangan bulat tanpa prefiks '0b'.
    """
    return bin(Biner).replace("0b", "")


def bulat_ke_biner(angka):
    """
    Membulatkan angka desimal ke bilangan bulat terdekat dan
    mengonversinya menjadi string biner.

    Parameter:
    - angka (float): Bilangan desimal yang akan dibulatkan dan
      dikonversi.

    Mengembalikan:
    - str: Representasi biner dari bilangan bulat hasil pembulatan
      tanpa prefiks '0b'.
    """
    bulat = round(angka)
    biner = bin(bulat)
    return biner[2:]

