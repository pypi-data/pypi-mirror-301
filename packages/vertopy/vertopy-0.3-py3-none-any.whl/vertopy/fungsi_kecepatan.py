# Dictionary konversi menyimpan data satuan kecepatan dan faktor konversinya
konversi = {
    "m/s" :  {"nilai" :  1},
    "km/h":  {"nilai" :  3.6},
    "mph" :  {"nilai" :  2.23694},
    "knot":  {"nilai" : 1.94384},
    "mach":  {"nilai" : 0.002915}
}
# Fungsi kecepatan menerima tiga argumen: satuan1, satuan2, dan nilai
def kecepatan(satuan1: str, satuan2: str, nilai: float):
    try:
        # Menghitung hasil konversi dengan mengalikan nilai awal dengan faktor satuan
         hasil = nilai * konversi[satuan1]["nilai"] / konversi[satuan2]["nilai"]
         return f"{hasil:.2f}"
      
         # Jika satuan yang dimasukkan tidak ditemukan dalam dictionary 'konversi', maka akan terjadi KeyError
    except KeyError:
       # Pesan kesalahan jika input satuan tidak valid
        return "Input tidak valid"