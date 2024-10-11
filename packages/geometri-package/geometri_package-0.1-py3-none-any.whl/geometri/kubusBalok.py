import math
#Volume Kubus
def volume_kubus ():
    sisi = int(input('Masukkan Sisi : '))

    v = sisi**3

    print (f'Volume Kubus: {v}')
volume_kubus()
#Luas Permukaan Kubus
def luas_permukaan_kubus ():
    sisi = int(input('Masukkan Sisi : '))

    LP = 6 * sisi**2

    print (f'Luas Kubus: {LP}')

luas_permukaan_kubus()

#Keliling Kubus
def keliling_kubus ():
    sisi = int(input('Masukkan Sisi : '))

    K = sisi * 12

    print (f'Keliling Kubus : {K}')

keliling_kubus()

#Panjang Diagonal Sisi Kubus
def panjang_diagonal_sisi_kubus():
    sisi = int(input('Masukkan Sisi : '))

    PDS = sisi * math.sqrt(2)

    print (f'Panjang Diagonal sisi : {PDS:.2f}')

panjang_diagonal_sisi_kubus()

#Panjang Diagonal Ruang Kubus
def panjang_diagonal_ruang_kubus ():
    sisi = int(input('Masukkan Sisi : '))

    PDR = sisi * math.sqrt(3)

    print (f'Panjang diagonal ruang : {PDR:.2f}')

#Luas Satu Sisi Kubus
def luas_satu_sisi():
    sisi = int(input('Masukkan Sisi : '))
    
    LSS = sisi**2

    print (f'Luas satu sisi : {LSS}')

#Keliling satu sisi kubus
def keliling_satu_sisi():
    sisi = int(input('Masukkan Sisi : '))
    
    KSS = 4 * sisi

    print (f'Keliling Satu sisi : {KSS}')

#Jumlah Panjang Rusuk Kubus
def jumlah_panjang_rusuk(s):
    sisi = int(input('Masukkan Sisi : '))
    
    JPR =  12 * sisi

    print (f'Jumlah Panjang Rusuk : {JPR}')


#Volume Balok
def volume_balok ():    
    p = int(input('Masukkan panjang :'))
    l = int(input('Masukkan lebar :'))
    t = int(input('Masukkan tinggi : '))

    V = p*l*t

    print (f'Volume Balok : {V}')
volume_kubus()

# Keliling Balok
def keliling_balok():

    p = int(input('Masukkan panjang :'))
    l = int(input('Masukkan lebar :'))
    t = int(input('Masukkan tinggi : '))

    K = 4 * (p+l+t)

    print (f'Keliling Balok : {K}')
keliling_balok()

#Luas Permukaan Balok
def luas_permukaan_balok ():
    p = int(input('Masukkan panjang :'))
    l = int(input('Masukkan lebar :'))
    t = int(input('Masukkan tinggi : '))

    LP = 2 * (p*l + p*t + l*t)

    print (F'luas permukaan balok : {LP}')
luas_permukaan_balok()

#Diagonal Ruang Balok
def diagonal_ruang_balok():
    p = int(input('Masukkan panjang :'))
    l = int(input('Masukkan lebar :'))
    t = int(input('Masukkan tinggi : '))

    DR = math.sqrt(p**2 + l**2 + t**2)

    print (f'Diagonal ruang : {DR:.2f}')
diagonal_ruang_balok()

#Luas Diagonal Balok
def luas_diagonal_balok():
    p = int(input('Masukkan panjang :'))
    l = int(input('Masukkan lebar :'))
    t = int(input('Masukkan tinggi : ')) 

    LD = p * math.sqrt(l**2 + t**2)
    
    print (f'Luas diagonal balok : {LD:.2f}')
luas_diagonal_balok()
