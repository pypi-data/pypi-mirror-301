def panjang(dari_satuan, ke_satuan, nilai):
    # Tabel konversi untuk setiap satuan
    konversi_faktor = {
    
    "km" : {"mm" : 1000000, "cm" : 100000,"dam": 10000, "m" : 1000,   "hm"  : 10},
    "hm" : {"mm" : 10000,   "cm" : 1000,  "dam":  10,   "m" : 100,    "km"  : 0.1},
    "dam": {"mm" : 100,     "cm" : 10,    "m"  : 0.1, "km"  : 0.001,  "hm"  : 0.01},
    "m"  : {"mm" : 1000,    "cm" : 100,   "dam": 10, "km"   : 0.001,  "hm"  : 0.1},
    "dm" : {"mm" : 100,     "cm" : 10,    "m"  : 0.1, "km"  : 0.00001,"hm"  : 0.001, "dam": 0.1},
    "cm" : {"mm" : 10,      "dam": 0.1,   "m"  : 0.01, "km" : 0.00001,"hm"  : 0.001},
    "mm" : {"cm" : 0.1,     "dam": 0.01,  "m"  : 0.001, "km": 0.000001,"hm" : 0.00001}
    }
    try:
        hasil =  nilai * konversi_faktor[dari_satuan][ke_satuan]
        return f"{hasil:.2f}"
    except:
        return "Satuan tidak ditemukan"  # Tambahkan pesan error jika sat

