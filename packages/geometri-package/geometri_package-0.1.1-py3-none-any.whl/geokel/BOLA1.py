import math
def volume_bola(jari_jari):
    """Menghitung volume bola berdasarkan jari-jari."""
    phi = 3,14
    if jari_jari < 0 :
        raise ValueError("Jari-jari tidak boleh negatif.")
    volume = (4/3) * math.pi * (jari_jari ** 3)
    return volume 


def luas_permukaan_bola(jari_jari):
    """Menghitung luas permukaan bola berdasarkan jari-jari."""
    phi = 3,14
    if jari_jari < 0:
        raise ValueError("Jari-jari tidak boleh negatif.")
    luas_permukaan = 4 * math.pi * (jari_jari ** 2)
    return luas_permukaan

def jari_jari_dari_volume(volume):
    """Menghitung jari-jari bola berdasarkan volume."""
    phi = 3.14
    if volume < 0:
        raise ValueError("Volume tidak boleh negatif.")
    jari_jari = ((3 * volume) / (4 * phi) ** (1/3))
    return jari_jari


def jari_jari_dari_luas_permukaan (luas_permukaan):
    """Menghitung jari-jari bola berdasarkan luas permukaan."""
    phi= 3.14
    if luas_permukaan < 0:
        raise ValueError("Luas permukaan tidak boleh negatif.")
    jari_jari = (luas_permukaan / (4 * phi))**0.5
    return jari_jari

def massa_bola(jari_jari, densitas):
    """Menghitung massa bola berdasarkan jari-jari dan densitas."""
    if jari_jari < 0:
        raise ValueError("Jari-jari tidak boleh negatif.")
    if densitas < 0:
        raise ValueError("Densitas tidak boleh negatif.")
    volume = (4/3) * math.pi * (jari_jari ** 3)
    massa = densitas * volume
    return massa