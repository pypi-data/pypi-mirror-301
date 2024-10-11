import math

# Volume Kubus
def volume_kubus(sisi):
    v = sisi**3
    print(f'Volume Kubus: {v}')

# Luas Permukaan Kubus
def luas_permukaan_kubus(sisi):
    LP = 6 * sisi**2
    print(f'Luas Permukaan Kubus: {LP}')

# Keliling Kubus
def keliling_kubus(sisi):
    K = sisi * 12
    print(f'Keliling Kubus: {K}')

# Panjang Diagonal Sisi Kubus
def panjang_diagonal_sisi_kubus(sisi):
    PDS = sisi * math.sqrt(2)
    print(f'Panjang Diagonal Sisi: {PDS:.2f}')

# Panjang Diagonal Ruang Kubus
def panjang_diagonal_ruang_kubus(sisi):
    PDR = sisi * math.sqrt(3)
    print(f'Panjang Diagonal Ruang: {PDR:.2f}')

# Luas Satu Sisi Kubus
def luas_satu_sisi(sisi):
    LSS = sisi**2
    print(f'Luas Satu Sisi Kubus: {LSS}')

# Keliling Satu Sisi Kubus
def keliling_satu_sisi(sisi):
    KSS = 4 * sisi
    print(f'Keliling Satu Sisi Kubus: {KSS}')

# Jumlah Panjang Rusuk Kubus
def jumlah_panjang_rusuk(sisi):
    JPR = 12 * sisi
    print(f'Jumlah Panjang Rusuk: {JPR}')

# Volume Balok
def volume_balok(p, l, t):
    V = p * l * t
    print(f'Volume Balok: {V}')

# Keliling Balok
def keliling_balok(p, l, t):
    K = 4 * (p + l + t)
    print(f'Keliling Balok: {K}')

# Luas Permukaan Balok
def luas_permukaan_balok(p, l, t):
    LP = 2 * (p * l + p * t + l * t)
    print(f'Luas Permukaan Balok: {LP}')

# Diagonal Ruang Balok
def diagonal_ruang_balok(p, l, t):
    DR = math.sqrt(p**2 + l**2 + t**2)
    print(f'Diagonal Ruang Balok: {DR:.2f}')

# Luas Diagonal Balok
def luas_diagonal_balok(p, l, t):
    LD = p * math.sqrt(l**2 + t**2)
    print(f'Luas Diagonal Balok: {LD:.2f}')
