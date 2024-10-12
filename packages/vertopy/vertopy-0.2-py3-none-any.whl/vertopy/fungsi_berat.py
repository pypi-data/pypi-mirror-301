# Definisikan kamus konversi satuan berat
# Kamus ini berisi pasangan key-value, di mana key adalah singkatan satuan berat
# dan value adalah dictionary yang berisi nilai dari satuan itu
konversi = {
    "mg": {"nilai": 1},
    "cg": {"nilai": 10},
    "dg": {"nilai": 100},
    "g":  {"nilai": 1000},
    "dag":{"nilai": 10000},
    "hg": {"nilai": 100000},
    "kg": {"nilai": 1000000},
    "ton":{"nilai": 1000000000}
}
# Fungsi untuk mengkonversi satuan berat
def berat(satuan1:str, satuan2:str, nilai:float):
    try:
        # Membuat variable hasil 
        # untuk menghitung hasil konversi dengan mengalikan nilai awal dari satuan berat dengan nilai satuan1 kemudian dibagi dengan nilai satuan 2
        hasil = nilai * konversi[satuan1]["nilai"] / konversi[satuan2]["nilai"]
        return f"{hasil:.2f}"
    except KeyError:
        # Jika input tidak valid, cetak pesan kesalahan
        print("input tidak valid")
