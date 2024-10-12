import math

def keliling_alas_prisma(sisi):
    """
    Menghitung keliling alas segi lima beraturan.
    Rumus: Keliling = 5 * sisi
    """
    keliling = 5 * sisi
    return keliling

def luas_alas_segi_lima(sisi):
    """
    Menghitung luas alas segi lima beraturan.
    Rumus: Luas Alas = (1/4) * sqrt(5(5 + 2sqrt(5))) * s^2
    """
    luas_alas = (1/4) * math.sqrt(5 * (5 + 2 * math.sqrt(5))) * sisi**2
    return luas_alas

def luas_permukaan_prisma(sisi, tinggi):
    """
    Menghitung luas permukaan prisma segi lima.
    Rumus: Luas Permukaan = 2 * Luas Alas + Keliling Alas * Tinggi
    """
    luas_alas = luas_alas_segi_lima(sisi)  
    keliling = keliling_alas_prisma(sisi)  
    luas_permukaan = 2 * luas_alas + keliling * tinggi
    return luas_permukaan

def volume_prisma(sisi, tinggi):
    """
    Menghitung volume prisma segi lima.
    Rumus: Volume = Luas Alas * Tinggi
    """
    luas_alas = luas_alas_segi_lima(sisi)  # Luas alas segi lima
    volume = luas_alas * tinggi
    return volume

def hitung_prisma_segi_lima(sisi, tinggi):
    """
    Fungsi untuk menghitung keliling, luas alas, luas permukaan, dan volume prisma segi lima
    berdasarkan panjang sisi alas segi lima dan tinggi prisma.
    """
    keliling = keliling_alas_prisma(sisi)
    luas_alas = luas_alas_segi_lima(sisi)
    luas_permukaan = luas_permukaan_prisma(sisi, tinggi)
    volume = volume_prisma(sisi, tinggi)
    
    print(f"Keliling alas segi lima: {keliling:.2f} cm")
    print(f"Luas alas segi lima: {luas_alas:.2f} cm²")
    print(f"Luas permukaan prisma segi lima: {luas_permukaan:.2f} cm²")
    print(f"Volume prisma segi lima: {volume:.2f} cm³")

