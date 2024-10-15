# Fungsi untuk mengonversi bilangan desimal ke biner
def desimal_ke_biner(desimal):
    """
    Mengonversi bilangan desimal (bilangan bulat) ke dalam format biner tanpa prefiks '0b'.

    Parameter:
    desimal (int): Bilangan bulat desimal yang akan dikonversi ke biner.

    Return:
    String: Representasi biner dari bilangan desimal yang diberikan.

    Contoh Penggunaan:
    desimal_ke_biner(10)  # Output: '1010'
    """
    return bin(desimal)[2:]  # Menghapus prefix '0b'

# Fungsi operasi AND
def operasi_and(bil1, bil2):
    """
    Melakukan operasi bitwise AND antara dua bilangan bulat, kemudian mengembalikan hasilnya dalam bentuk biner dan desimal.

    Parameter:
    bil1 (int): Bilangan bulat pertama.
    bil2 (int): Bilangan bulat kedua.

    Return:
    Tuple (String, int): Representasi biner dan desimal dari hasil operasi AND.

    Contoh Penggunaan:
    operasi_and(10, 7)  # Output: ('0010', 2) - AND 1010 & 0111 = 0010
    """
    hasil_and = bil1 & bil2
    return desimal_ke_biner(hasil_and), hasil_and

# Fungsi operasi OR
def operasi_or(bil1, bil2):
    """
    Melakukan operasi bitwise OR antara dua bilangan bulat, kemudian mengembalikan hasilnya dalam bentuk biner dan desimal.

    Parameter:
    bil1 (int): Bilangan bulat pertama.
    bil2 (int): Bilangan bulat kedua.

    Return:
    Tuple (String, int): Representasi biner dan desimal dari hasil operasi OR.

    Contoh Penggunaan:
    operasi_or(10, 7)  # Output: ('1111', 15) - OR 1010 | 0111 = 1111
    """
    hasil_or = bil1 | bil2
    return desimal_ke_biner(hasil_or), hasil_or

# Fungsi operasi XOR
def operasi_xor(bil1, bil2):
    """
    Melakukan operasi bitwise XOR antara dua bilangan bulat, kemudian mengembalikan hasilnya dalam bentuk biner dan desimal.

    Parameter:
    bil1 (int): Bilangan bulat pertama.
    bil2 (int): Bilangan bulat kedua.

    Return:
    Tuple (String, int): Representasi biner dan desimal dari hasil operasi XOR.

    Contoh Penggunaan:
    operasi_xor(10, 7)  # Output: ('1101', 13) - XOR 1010 ^ 0111 = 1101
    """
    hasil_xor = bil1 ^ bil2
    return desimal_ke_biner(hasil_xor), hasil_xor

# Fungsi operasi NOT
def operasi_not(bil):
    """
    Melakukan operasi bitwise NOT pada satu bilangan bulat. Hasil biner dipresentasikan dalam format 4-bit (padding).

    Parameter:
    bil (int): Bilangan bulat yang akan dioperasikan menggunakan bitwise NOT.

    Return:
    Tuple (String, int): Hasil operasi NOT dalam format biner 4-bit dan desimal. Biner dikemas dalam format 4 bit menggunakan padding.

    Contoh Penggunaan:
    operasi_not(10)  # Output: ('0101', -11) - NOT 1010 menghasilkan 0101 (4-bit), hasil desimalnya -11
    """
    hasil_not = ~bil
    # Menambahkan padding hanya di sini
    biner_hasil = format(hasil_not & 0b1111, '04b')  # 4 bit padding
    return biner_hasil, hasil_not
