def suhu(satuan1, satuan2, nilai):
    # Fungsi untuk mengkonversi suhu dari satuan1 ke satuan2
    
    # Konversi dari Celcius ke Fahrenheit
    if satuan1 == 'c' and satuan2 == 'f':
        return (nilai * 9/5) + 32
    
    # Konversi dari Celcius ke Kelvin
    elif satuan1 == 'c' and satuan2 == 'k':
        return (nilai + 273.15)
    
    # Konversi dari Celcius ke Reamur
    elif satuan1 == 'c' and satuan2 == 'r':
        return (nilai * 4/5)
    
    # Konversi dari Fahrenheit ke Celcius
    elif satuan1 == 'f' and satuan2 == 'c':
        return ((nilai * 5/9) + 32)
    
    # Konversi dari Fahrenheit ke Kelvin
    elif satuan1 == 'f' and satuan2 == 'k':
        return (nilai - 32) * 5/9 + 273.15
    
    # Konversi dari Fahrenheit ke Reamur
    elif satuan1 == 'f' and satuan2 == 'r':
        return (nilai * 4/9 - 32)
    
    # Konversi dari Kelvin ke Celcius
    elif satuan1 == 'k' and satuan2 == 'c':
        return (nilai - 273.15)
    
    # Konversi dari Kelvin ke Fahrenheit
    elif satuan1 == 'k' and satuan2 == 'f':
        return ((nilai - 273.15) * 9/5 + 32)
    
    # Konversi dari Kelvin ke Reamur
    elif satuan1 == 'k' and satuan2 == 'r':
        return (nilai * 4/5 - 273.15)
    
     # Konversi dari Reamur ke Celcius
    elif satuan1 == 'r' and satuan2 == 'c':
        return (nilai * 5/4)
    
    # Konversi dari Reamur ke Fahrenheit
    elif satuan1 == 'r' and satuan2 == 'f':
        return (nilai * 9/4 + 32)
    
    # Konversi dari Reamur ke Kelvin
    elif satuan1 == 'r' and satuan2 == 'k':
        return (nilai * 5/4 + 273.15)
    
     # Jika tidak ada konversi yang sesuai, maka return nilai asli dengan 2 desimal
    return round(nilai, 2)