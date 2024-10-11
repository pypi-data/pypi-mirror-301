import math

#Volume Kubus
def volume_kubus():
    """
    Menghitung volume kubus berdasarkan panjang sisi yang dimasukkan pengguna.
    
    Returns:
    None
    """
    sisi = int(input('Masukkan Sisi : '))
    v = sisi**3

#Luas Permukaan Kubus
def luas_permukaan_kubus():
    """
    Menghitung luas permukaan kubus berdasarkan panjang sisi yang dimasukkan pengguna.
    
    Returns:
    None
    """
    sisi = int(input('Masukkan Sisi : '))
    LP = 6 * sisi**2

#Keliling Kubus
def keliling_kubus():
    """
    Menghitung keliling kubus berdasarkan panjang sisi yang dimasukkan pengguna.
    
    Returns:
    None
    """
    sisi = int(input('Masukkan Sisi : '))
    K = sisi * 12

#Panjang Diagonal Sisi Kubus
def panjang_diagonal_sisi_kubus():
    """
    Menghitung panjang diagonal sisi kubus berdasarkan panjang sisi yang dimasukkan pengguna.
    
    Returns:
    None
    """
    sisi = int(input('Masukkan Sisi : '))
    PDS = sisi * math.sqrt(2)

#Panjang Diagonal Ruang Kubus
def panjang_diagonal_ruang_kubus():
    """
    Menghitung panjang diagonal ruang kubus berdasarkan panjang sisi yang dimasukkan pengguna.
    
    Returns:
    None
    """
    sisi = int(input('Masukkan Sisi : '))
    PDR = sisi * math.sqrt(3)

#Luas Satu Sisi Kubus
def luas_satu_sisi():
    """
    Menghitung luas satu sisi kubus berdasarkan panjang sisi yang dimasukkan pengguna.
    
    Returns:
    None
    """
    sisi = int(input('Masukkan Sisi : '))
    LSS = sisi**2

#Keliling satu sisi kubus
def keliling_satu_sisi():
    """
    Menghitung keliling satu sisi kubus berdasarkan panjang sisi yang dimasukkan pengguna.
    
    Returns:
    None
    """
    sisi = int(input('Masukkan Sisi : '))
    KSS = 4 * sisi

#Jumlah Panjang Rusuk Kubus
def jumlah_panjang_rusuk():
    """
    Menghitung jumlah panjang rusuk kubus berdasarkan panjang sisi yang dimasukkan pengguna.
    
    Returns:
    None
    """
    sisi = int(input('Masukkan Sisi : '))
    JPR =  12 * sisi

#Volume Balok
def volume_balok():
    """
    Menghitung volume balok berdasarkan panjang, lebar, dan tinggi yang dimasukkan pengguna.
    
    Returns:
    None
    """
    p = int(input('Masukkan panjang :'))
    l = int(input('Masukkan lebar :'))
    t = int(input('Masukkan tinggi : '))
    V = p*l*t

# Keliling Balok
def keliling_balok():
    """
    Menghitung keliling balok berdasarkan panjang, lebar, dan tinggi yang dimasukkan pengguna.
    
    Returns:
    None
    """
    p = int(input('Masukkan panjang :'))
    l = int(input('Masukkan lebar :'))
    t = int(input('Masukkan tinggi : '))
    K = 4 * (p+l+t)

#Luas Permukaan Balok
def luas_permukaan_balok():
    """
    Menghitung luas permukaan balok berdasarkan panjang, lebar, dan tinggi yang dimasukkan pengguna.
    
    Returns:
    None
    """
    p = int(input('Masukkan panjang :'))
    l = int(input('Masukkan lebar :'))
    t = int(input('Masukkan tinggi : '))
    LP = 2 * (p*l + p*t + l*t)

#Diagonal Ruang Balok
def diagonal_ruang_balok():
    """
    Menghitung diagonal ruang balok berdasarkan panjang, lebar, dan tinggi yang dimasukkan pengguna.
    
    Returns:
    None
    """
    p = int(input('Masukkan panjang :'))
    l = int(input('Masukkan lebar :'))
    t = int(input('Masukkan tinggi : '))
    DR = math.sqrt(p**2 + l**2 + t**2)

#Luas Diagonal Balok
def luas_diagonal_balok():
    """
    Menghitung luas diagonal balok berdasarkan panjang, lebar, dan tinggi yang dimasukkan pengguna.
    
    Returns:
    None
    """
    p = int(input('Masukkan panjang :'))
    l = int(input('Masukkan lebar :'))
    t = int(input('Masukkan tinggi : ')) 
    LD = p * math.sqrt(l**2 + t**2)
