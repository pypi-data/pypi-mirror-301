def ganti_bit(angka: int, posisi: int, nilai: int) -> int:
    """
    Mengganti bit pada posisi tertentu di angka dengan nilai (0 atau 1).
    
    Args:
    angka (int): Angka target
    posisi (int): Posisi bit yang ingin diganti (dimulai dari 0)
    nilai (int): Nilai bit yang baru (0 atau 1)
    
    Returns:
    int: Angka baru setelah bit diganti
    """
    mask = 1 << posisi
    if nilai == 1:
        # return angka | mask  # Set bit to 1
        hasil = angka | mask  # Set bit to 1
        return bin(hasil)
    else:
        # return angka & ~mask  # Set bit to 0
        hasil = angka & ~mask  # Set bit to 0
        return bin(hasil)
     
def cari_bit(angka: int, posisi: int) -> int:
    """
    Mencari nilai bit pada posisi tertentu di angka.
    
    Args:
    angka (int): Angka target
    posisi (int): Posisi bit yang ingin dicari (dimulai dari 0)
    
    Returns:
    int: Nilai bit (0 atau 1) pada posisi yang dimaksud
    """
    return (angka >> posisi) & 1

