Aritamtika

Aritmatika adalah package Python yang berfungsi untuk menyelesaikan masalah aritmatika sosial seperti untung dan rugi, bunga, pajak, diskon dan rabat, serta bruto, netto, dan tara.

Aritmatika is a Python Package for dealing with social arithmetic problems such as profit and loss, interest, tax, discount and rebate, and also gross, net, and tare

`bash
pip install aritmatika
`

Penggunaan
1. Fungsi Gaji

`python
from aritmatika import gaji

# Menghitung gaji pokok
gaji_pokok = gaji.hitung_gaji_pokok(50000, 40)
print(f"Gaji pokok: {gaji_pokok}")

# Menghitung gaji bersih
gaji_bersih = gaji.hitung_gaji_bersih(gaji_pokok, 500000, 300000)
print(f"Gaji bersih: {gaji_bersih}")

# Menghitung gaji lembur
gaji_lembur = gaji.hitung_gaji_lembur(5, 75000)
print(f"Gaji lembur: {gaji_lembur}")
`