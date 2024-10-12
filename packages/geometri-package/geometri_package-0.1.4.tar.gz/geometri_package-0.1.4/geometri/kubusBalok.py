import math

# Volume Kubus
def volume_kubus(sisi):
    """
    Menghitung volume kubus berdasarkan panjang sisi.
    
    Parameter:
    - sisi (float): Panjang sisi kubus.
    
    Keluaran:
    - Volume kubus (float).
    """
    volume = sisi**3
    return volume

# Luas Permukaan Kubus
def luas_permukaan_kubus(sisi):
    """
    Menghitung luas permukaan kubus berdasarkan panjang sisi.
    
    Parameter:
    - sisi (float): Panjang sisi kubus.
    
    Keluaran:
    - Luas permukaan kubus (float).
    """
    luas_permukaan = 6 * sisi**2
    return luas_permukaan

# Keliling Kubus
def keliling_kubus(sisi):
    """
    Menghitung keliling kubus berdasarkan panjang sisi.
    
    Parameter:
    - sisi (float): Panjang sisi kubus.
    
    Keluaran:
    - Keliling kubus (float).
    """
    keliling = sisi * 12
    return keliling

# Panjang Diagonal Sisi Kubus
def panjang_diagonal_sisi_kubus(sisi):
    """
    Menghitung panjang diagonal sisi kubus berdasarkan panjang sisi.
    
    Parameter:
    - sisi (float): Panjang sisi kubus.
    
    Keluaran:
    - Panjang diagonal sisi kubus (float).
    """
    diagonal_sisi = sisi * math.sqrt(2)
    return diagonal_sisi

# Panjang Diagonal Ruang Kubus
def panjang_diagonal_ruang_kubus(sisi):
    """
    Menghitung panjang diagonal ruang kubus berdasarkan panjang sisi.
    
    Parameter:
    - sisi (float): Panjang sisi kubus.
    
    Keluaran:
    - Panjang diagonal ruang kubus (float).
    """
    diagonal_ruang = sisi * math.sqrt(3)
    return diagonal_ruang

# Luas Satu Sisi Kubus
def luas_satu_sisi(sisi):
    """
    Menghitung luas satu sisi kubus berdasarkan panjang sisi.
    
    Parameter:
    - sisi (float): Panjang sisi kubus.
    
    Keluaran:
    - Luas satu sisi kubus (float).
    """
    luas_sisi = sisi**2
    return luas_sisi

# Keliling Satu Sisi Kubus
def keliling_satu_sisi(sisi):
    """
    Menghitung keliling satu sisi kubus berdasarkan panjang sisi.
    
    Parameter:
    - sisi (float): Panjang sisi kubus.
    
    Keluaran:
    - Keliling satu sisi kubus (float).
    """
    keliling_sisi = 4 * sisi
    return keliling_sisi

# Jumlah Panjang Rusuk Kubus
def jumlah_panjang_rusuk(sisi):
    """
    Menghitung jumlah panjang rusuk kubus berdasarkan panjang sisi.
    
    Parameter:
    - sisi (float): Panjang sisi kubus.
    
    Keluaran:
    - Jumlah panjang rusuk kubus (float).
    """
    panjang_rusuk = 12 * sisi
    return panjang_rusuk

# Volume Balok
def volume_balok(p, l, t):
    """
    Menghitung volume balok berdasarkan panjang, lebar, dan tinggi.
    
    Parameter:
    - p (float): Panjang balok.
    - l (float): Lebar balok.
    - t (float): Tinggi balok.
    
    Keluaran:
    - Volume balok (float).
    """
    volume = p * l * t
    return volume

# Keliling Balok
def keliling_balok(p, l, t):
    """
    Menghitung keliling balok berdasarkan panjang, lebar, dan tinggi.
    
    Parameter:
    - p (float): Panjang balok.
    - l (float): Lebar balok.
    - t (float): Tinggi balok.
    
    Keluaran:
    - Keliling balok (float).
    """
    keliling = 4 * (p + l + t)
    return keliling

# Luas Permukaan Balok
def luas_permukaan_balok(p, l, t):
    """
    Menghitung luas permukaan balok berdasarkan panjang, lebar, dan tinggi.
    
    Parameter:
    - p (float): Panjang balok.
    - l (float): Lebar balok.
    - t (float): Tinggi balok.
    
    Keluaran:
    - Luas permukaan balok (float).
    """
    luas_permukaan = 2 * (p * l + p * t + l * t)
    return luas_permukaan

# Diagonal Ruang Balok
def diagonal_ruang_balok(p, l, t):
    """
    Menghitung diagonal ruang balok berdasarkan panjang, lebar, dan tinggi.
    
    Parameter:
    - p (float): Panjang balok.
    - l (float): Lebar balok.
    - t (float): Tinggi balok.
    
    Keluaran:
    - Diagonal ruang balok (float).
    """
    diagonal_ruang = math.sqrt(p**2 + l**2 + t**2)
    return diagonal_ruang

# Luas Diagonal Balok
def luas_diagonal_balok(p, l, t):
    """
    Menghitung luas diagonal balok berdasarkan panjang, lebar, dan tinggi.
    
    Parameter:
    - p (float): Panjang balok.
    - l (float): Lebar balok.
    - t (float): Tinggi balok.
    
    Keluaran:
    - Luas diagonal balok (float).
    """
    luas_diagonal = p * math.sqrt(l**2 + t**2)
    return luas_diagonal
