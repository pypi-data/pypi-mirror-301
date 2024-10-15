def shift_bit(a):

	# a = int(input("Masukkan bilangan bulat: "))

	biner_a = bin(a)[2: ]
	print(f'Konversi ke biner: {biner_a}')

	# pada bagian ini, bilangan bulat akan diubah ke bilangan biner terlebih dahulu. Jika
	# bilangannya sudah menjadi biner, maka bilangan tersebut langsung keluar

	hasil_shift_left = a << 2 # Hasil: 0b101000 (40)
	# pada bagian ini, bilangan biner tadi akan digeser sebanyak 2 kali ke kiri atau mengkalikan bulat dengan 4
	hasil_shift_right = a >> 2 # Hasil: 0b10 (2)
	# kebalikan dari shift kiri, yaitu membagi bilangan bulat dengan 4

	print(f"Shift kiri: {bin(hasil_shift_left)}")   # Output: '0b101000'
	print(f"Shift kanan: {bin(hasil_shift_right)}") # Output: '0b10'
	# mengeluarkan hasil pergeseran biner. bin berfungsi mengubah kembali bilangan bulat ke biner

def inverse_bit(a):
	biner_a = bin(a)[2: ]
	print(f'Konversi ke biner: {biner_a}')
	# pada bagian ini, bilangan bulat akan diubah ke bilangan biner terlebih dahulu. Jika
	# bilangannya sudah menjadi biner, maka bilangan tersebut langsung keluar
	bits = biner_a
	# variabel baru untuk membalikkan bilangan biner
	inverse = ''
	# Sengaja dikasi string kosong agar dapat menyimpan hasil inverse biner tadi

	for i in bits:
	# melakukan perulangan tergantung dari jumlah bilangan binernya

		if i == '0':
			inverse += '1'
		# kalau bilangan binernya adalah 0, maka yang disimpan di variabel inverse adalah 1
			
		else:
			inverse += '0'
		# kalau bilangan binernya adalah 1, maka yang disimpan di variabel inverse adalah 1
			
	print(f"Inverse-nya: {inverse}")

# untuk memanggil fungsinya, dalam tanda kurung itu harus di isi bilangan bulat. kalau ingin memasukkan bilangan biner maka harus
# berawalan 0b. dan pada baris ke-6 dan ke-22 cukup hapus saja kalau inputannya bilangan biner
