def int_to_binary(num):
    """
    Mengonversi bilangan bulat menjadi representasi biner.

    Args:
        num (int): Bilangan bulat yang akan dikonversi.

    Returns:
        str: Representasi biner dari bilangan bulat, tanpa prefiks '0b'.
    
    Contoh:
        >>> int_to_binary(5)
        '101'
    """
    return bin(num)[2:]  # [2:] untuk menghilangkan prefiks '0b'


def binary_addition_from_int(a, b):
    """
    Menambahkan dua bilangan bulat dan mengembalikan hasilnya dalam bentuk biner.

    Args:
        a (int): Bilangan bulat pertama.
        b (int): Bilangan bulat kedua.

    Returns:
        str: Hasil penjumlahan a dan b dalam bentuk biner.
    
    Contoh:
        >>> binary_addition_from_int(3, 5)
        '1000'
    """
    return int_to_binary(a + b)


def binary_subtraction_from_int(a, b):
    """
    Mengurangkan dua bilangan bulat dan mengembalikan hasilnya dalam bentuk biner.

    Args:
        a (int): Bilangan bulat pertama.
        b (int): Bilangan bulat kedua.

    Returns:
        str: Hasil pengurangan a dan b dalam bentuk biner.
    
    Contoh:
        >>> binary_subtraction_from_int(5, 3)
        '10'
    """
    return int_to_binary(a - b)


def binary_multiplication_from_int(a, b):
    """
    Mengalikan dua bilangan bulat dan mengembalikan hasilnya dalam bentuk biner.

    Args:
        a (int): Bilangan bulat pertama.
        b (int): Bilangan bulat kedua.

    Returns:
        str: Hasil perkalian a dan b dalam bentuk biner.
    
    Contoh:
        >>> binary_multiplication_from_int(2, 3)
        '110'
    """
    return int_to_binary(a * b)


def binary_division_from_int(a, b):
    """
    Membagi dua bilangan bulat dan mengembalikan hasilnya dalam bentuk biner.

    Args:
        a (int): Bilangan bulat pembilang.
        b (int): Bilangan bulat penyebut.

    Returns:
        str: Hasil pembagian a dan b dalam bentuk biner.

    Catatan:
        Jika b adalah 0, fungsi ini akan menyebabkan ZeroDivisionError.

    Contoh:
        >>> binary_division_from_int(8, 2)
        '100'
    """
    return int_to_binary(a // b)
