# FUNGSI 1
def setbits(n:int) -> int:
    """
    Menghitung jumlah bit yang disetel (1) dalam representasi bilangan biner.

    Input:
        angka (int): Bilangan (bulat/biner) yang akan dihitung jumlah bit yang disetelnya.
    Returns:
        int: Jumlah bit '1' dalam representasi biner bilangan tersebut.

    Contoh:
        >>> setbits(13)
        3  # Karena 13 dalam biner adalah '1101' yang memiliki 3 bit '1'.
        
        >>> setbits(0b1101)
        3  # Karena dalam biner '1101' yang memiliki 3 bit '1'.
    """ 
    try:
        if n < 0:
            raise ValueError("Input harus bilangan positif : setbits(bilangan positif)")
        return bin(n).count("1")
    except ValueError as e:
        print(e)
        return 


# FUNGSI 2
def unsetbits(n:int) -> int:
    """
    Menghitung jumlah bit yang tidak disetel (0) dalam representasi bilangan biner.

    Input:
        angka (int): Bilangan (bulat/biner) yang akan dihitung jumlah bit yang tidak disetelnya.
    Returns:
        int: Jumlah bit '0' dalam representasi biner bilangan tersebut.

    Contoh:
        >>> unsetbits(13)
        1  # Karena 13 dalam biner adalah '1101' yang memiliki 1 bit '0'.
        
        >>> unsetbits(0b1101)
        1  # Karena dalam biner '1101' yang memiliki 1 bit '0'.
    """
    try:
        if n < 0:
            raise ValueError("Input harus bilangan positif : unsetbits(bilangan positif)")
        return bin(n)[2:].count("0")  # Ambil setelah '0b'
    except ValueError as e:
        print(e)
        return


# FUNGSI 3
def bitlength(n:int) -> int:
    """
    Menghitung jumlah bit yang diperlukan untuk merepresentasikan bilangan dalam bentuk biner.

    Input:
        n (int): Bilangan yang panjang biner-nya akan dihitung.

    Returns:
        int: Jumlah bit yang diperlukan untuk merepresentasikan bilangan dalam bentuk biner.

    Contoh:
        >>> bitlength(8)
        4 (biner 8 = 1000)
        >>> bitlength(15)
        4 (biner 15 = 1111)
    """
    try:
        if n < 0:
            raise ValueError("Input harus bilangan positif : bitlength(bilangan positif)")
        return len(bin(n)[2:])  # Ambil setelah '0b'
    except ValueError as e:
        print(e)
        return


# FUNGSI 4
def parity(n:int) -> str:
    """
    Menghitung paritas dari bilangan input.

    Fungsi ini bertujuan untuk menentukan paritas dari bilangan biner, yaitu apakah jumlah bit yang disetel (bit 1) dalam representasi biner adalah genap atau ganjil.

    Input:
        n (int): Bilangan bulat yang paritasnya akan dihitung.

    Returns:
        str: "even" jika jumlah bit 1 adalah genap.
            "odd" jika jumlah bit 1 adalah ganjil.

    Contoh:
        >>> parity(6)
        "even"
        >>> parity(7)
        "odd"
    """
    try:
        if n < 0:
            raise ValueError("Input harus bilangan positif : parity(bilangan positif)")
        paritas = setbits(n)
        return "even" if paritas % 2 == 0 else "odd"
    except ValueError as e:
        print(e)
        return


# FUNGSI 5
def hamming(n:int, m:int) -> int:
    """
    Menghitung Hamming Distance antara dua bilangan non-negatif.

    Hamming Distance adalah jumlah posisi di mana dua bilangan biner berbeda.

    Input:
        n (int): Bilangan bulat non-negatif pertama.
        m (int): Bilangan bulat non-negatif kedua.

    Returns:
        int: Jumlah perbedaan bit antara dua bilangan biner (Hamming Distance).
    """
    try:
        if n < 0 or m < 0:
            raise ValueError("Input harus bilangan positif : hamming(bilangan positif, bilangan positif)")
        
        # Ambil representasi biner tanpa '0b'
        biner_1 = bin(n)[2:]
        biner_2 = bin(m)[2:]
        
        # Samakan panjang dengan menambahkan nol di depan yang lebih pendek
        panjang = max(len(biner_1), len(biner_2))
        biner_1 = biner_1.zfill(panjang)
        biner_2 = biner_2.zfill(panjang)
        
        # Hitung perbedaan bit
        beda = sum(bit1 != bit2 for bit1, bit2 in zip(biner_1, biner_2))
        
        return beda
    except ValueError as e:
        print(e)
        return


