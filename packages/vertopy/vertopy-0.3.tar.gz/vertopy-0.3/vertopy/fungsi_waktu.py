# Kamus konversi waktu berdasarkan detik
konversi_waktu = {
    "detik": {"nama": "Detik", "nilai": 1},
    "menit": {"nama": "Menit", "nilai": 60},
    "jam": {"nama": "Jam", "nilai": 3600},
    "hari": {"nama": "Hari", "nilai": 86400}
}

# Fungsi untuk mengkonversi satuan waktu
def konversi_waktu_satuan(satuan1: str, satuan2: str, nilai: float):
    try:
        # Hitung hasil konversi dengan mengalikan nilai awal dengan nilai satuan1 kemudian dibagi nilai satuan2
        hasil = nilai * konversi_waktu[satuan1]["nilai"] / konversi_waktu[satuan2]["nilai"]
        return f"{hasil:.2f}"
    except KeyError:
        # Jika input tidak valid, cetak pesan kesalahan
        return "Input tidak valid"