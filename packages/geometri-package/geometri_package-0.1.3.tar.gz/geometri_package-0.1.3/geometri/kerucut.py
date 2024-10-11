# Menghitung Volume Kerucut
def vkerucut(r, t):
    """
    Menghitung volume kerucut berdasarkan jari-jari alas dan tinggi.
    
    Parameter:
    - r (float): Jari-jari alas kerucut.
    - t (float): Tinggi kerucut.
    
    Keluaran:
    - Volume kerucut (float).
    
    Rumus:
    - Volume = (1/3) * π * r^2 * t
    """
    phi = 3.14
    volume = (1/3) * phi * r ** 2 * t
    return volume


# Menghitung Luas Permukaan Kerucut
def LPkerucut(r, t):
    """
    Menghitung luas permukaan kerucut berdasarkan jari-jari alas dan tinggi.
    
    Parameter:
    - r (float): Jari-jari alas kerucut.
    - t (float): Tinggi kerucut.
    
    Keluaran:
    - Luas permukaan kerucut (float).
    
    Rumus:
    - Luas permukaan = π * r * (r + s), s adalah garis pelukis.
    """
    phi = 3.14
    s = (r ** 2 + t ** 2) ** 0.5
    luas = phi * r * (r + s)
    return luas


# Menghitung Luas Alas Kerucut
def LAkerucut(r):
    """
    Menghitung luas alas kerucut.
    
    Parameter:
    - r (float): Jari-jari alas kerucut.
    
    Keluaran:
    - Luas alas kerucut (float).
    
    Rumus:
    - Luas alas = π * r^2
    """
    phi = 3.14
    luas_alas = phi * r ** 2
    return luas_alas


# Menghitung Garis Pelukis Kerucut
def GPkerucut(r, t):
    """
    Menghitung garis pelukis kerucut.
    
    Parameter:
    - r (float): Jari-jari alas.
    - t (float): Tinggi kerucut.
    
    Keluaran:
    - Garis pelukis kerucut (float).
    
    Rumus:
    - Garis pelukis (s) = sqrt(r^2 + t^2)
    """
    s = (r ** 2 + t ** 2) ** 0.5
    return s


# Menghitung Luas Selimut Kerucut
def LSkerucut(r, t):
    """
    Menghitung luas selimut kerucut.
    
    Parameter:
    - r (float): Jari-jari alas.
    - t (float): Tinggi kerucut.
    
    Keluaran:
    - Luas selimut kerucut (float).
    
    Rumus:
    - Luas selimut = π * r * s, s adalah garis pelukis.
    """
    phi = 3.14
    s = (r ** 2 + t ** 2) ** 0.5
    luas_selimut = phi * r * s
    return luas_selimut


# Menghitung Tinggi Kerucut
def Tkerucut(r, s):
    """
    Menghitung tinggi kerucut berdasarkan jari-jari alas dan garis pelukis.
    
    Parameter:
    - r (float): Jari-jari alas.
    - s (float): Garis pelukis.
    
    Keluaran:
    - Tinggi kerucut (float).
    
    Rumus:
    - Tinggi (t) = sqrt(s^2 - r^2)
    """
    if s > r:
        t = (s ** 2 - r ** 2) ** 0.5
        return t
    else:
        raise ValueError("Garis pelukis harus lebih besar dari jari-jari.")


# Menghitung Jari-Jari Alas Kerucut
def Jkerucut(t, s):
    """
    Menghitung jari-jari alas kerucut berdasarkan tinggi dan garis pelukis.
    
    Parameter:
    - t (float): Tinggi kerucut.
    - s (float): Garis pelukis.
    
    Keluaran:
    - Jari-jari alas kerucut (float).
    
    Rumus:
    - Jari-jari (r) = sqrt(s^2 - t^2)
    """
    if s > t:
        r = (s ** 2 - t ** 2) ** 0.5
        return r
    else:
        raise ValueError("Garis pelukis harus lebih besar dari tinggi kerucut.")


# Menghitung Keliling Alas Kerucut
def KAkerucut(r):
    """
    Menghitung keliling alas kerucut.
    
    Parameter:
    - r (float): Jari-jari alas.
    
    Keluaran:
    - Keliling alas kerucut (float).
    
    Rumus:
    - Keliling = 2 * π * r
    """
    phi = 3.14
    keliling = 2 * phi * r
    return keliling


# Menghitung Sudut Puncak Kerucut
def SPkerucut(r, h):
    """
    Menghitung tangensial dari sudut puncak kerucut.
    
    Parameter:
    - r (float): Jari-jari alas.
    - h (float): Tinggi kerucut.
    
    Keluaran:
    - Tan sudut puncak kerucut (float).
    
    Rumus:
    - Tan sudut puncak = r / h
    """
    sudut = r / h
    return sudut


# Menghitung Sudut Alas Kerucut
def SAkerucut(r, h):
    """
    Menghitung sudut alas kerucut dalam derajat.
    
    Parameter:
    - r (float): Jari-jari alas.
    - h (float): Tinggi kerucut.
    
    Keluaran:
    - Sudut alas kerucut dalam derajat (float).
    
    Rumus:
    - Menggunakan pendekatan tangensial dari h/r.
    """
    if r == 0:
        raise ValueError("Jari-jari tidak boleh nol.")

    tan_theta = h / r
    theta = 0
    increment = 0.0001
    
    while theta <= 90:
        if tan(theta) >= tan_theta:
            break
        theta += increment
    
    return theta


def tan(theta):
    """
    Menghitung nilai tan dari sudut dalam derajat.
    
    Parameter:
    - theta (float): Sudut dalam derajat.
    
    Keluaran:
    - Nilai tan sudut (float).
    """
    return (theta * 3.14 / 180)