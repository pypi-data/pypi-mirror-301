def vLimasST(T, P, Ta):
    """
    Menghitung volume limas segitiga.

    Parameters:
    T (float): Tinggi limas.
    P (float): Panjang alas segitiga.
    Ta (float): Tinggi alas segitiga.

    Returns:
    float: Volume limas segitiga.
    """
    La = 0.5 * P * Ta
    V = (1/3) * La * T
    return V

def LPLimasST(T, P, Ta):
    """
    Menghitung luas permukaan limas segitiga.

    Parameters:
    T (float): Tinggi limas.
    P (float): Panjang alas segitiga.
    Ta (float): Tinggi alas segitiga.

    Returns:
    float: Luas permukaan limas segitiga.
    """
    La = 0.5 * P * Ta
    Lst = 3 * (0.5 * P * T)
    L = La + Lst
    return L

def KaLimasST(Sa, Sb, Sc):
    """
    Menghitung keliling alas limas segitiga.

    Parameters:
    Sa (float): Sisi a dari segitiga.
    Sb (float): Sisi b dari segitiga.
    Sc (float): Sisi c dari segitiga.

    Returns:
    float: Keliling alas limas segitiga.
    """
    K = Sa + Sb + Sc
    return K

def TlimasST(V, La):
    """
    Menghitung tinggi limas segitiga berdasarkan volume dan luas alas.

    Parameters:
    V (float): Volume limas.
    La (float): Luas alas segitiga.

    Returns:
    float: Tinggi limas segitiga.
    """
    T = (3 * V) / La
    return T

def LPSLimasST(S, T):
    """
    Menghitung luas permukaan samping limas segitiga.

    Parameters:
    S (float): Panjang sisi segitiga.
    T (float): Tinggi limas.

    Returns:
    float: Luas permukaan samping limas segitiga.
    """
    Lps = 3 * (0.5 * S * T)
    return Lps


def vLimasSE(T, P, L):
    """
    Menghitung volume limas segi empat.

    Parameters:
    T (float): Tinggi limas.
    P (float): Panjang alas segi empat.
    L (float): Lebar alas segi empat.

    Returns:
    float: Volume limas segi empat.
    """
    A = P * L
    V = (1/3) * A * T
    return V

def LPLimasSE(T, S):
    """
    Menghitung luas permukaan limas segi empat.

    Parameters:
    T (float): Tinggi limas.
    S (float): Panjang sisi alas segi empat.

    Returns:
    float: Luas permukaan limas segi empat.
    """
    A = S * S
    L = A + 4 * (0.5 * S * T)
    return L

def KaLimasSTE(S):
    """
    Menghitung keliling alas limas segi empat.

    Parameters:
    S (float): Panjang sisi alas segi empat.

    Returns:
    float: Keliling alas limas segi empat.
    """
    K = 4 * S
    return K

def TlimasSE(V, La):
    """
    Menghitung tinggi limas segi empat berdasarkan volume dan luas alas.

    Parameters:
    V (float): Volume limas.
    La (float): Luas alas segi empat.

    Returns:
    float: Tinggi limas segi empat.
    """
    T = (3 * V) / La
    return T

def LPSLimasSE(S, T):
    """
    Menghitung luas permukaan samping limas segi empat.

    Parameters:
    S (float): Panjang sisi alas segi empat.
    T (float): Tinggi limas.

    Returns:
    float: Luas permukaan samping limas segi empat.
    """
    Lps = 4 * (0.5 * S * T)
    return Lps



def vLimasSL(T, P, L):
    """
    Menghitung volume limas segi lima.

    Parameters:
    T (float): Tinggi limas.
    P (float): Panjang alas segi lima.
    L (float): Lebar alas segi lima.

    Returns:
    float: Volume limas segi lima.
    """
    A = P * L
    V = (1/3) * A * T
    return V

def LPLimasSL(T, S):
    """
    Menghitung luas permukaan limas segi lima.

    Parameters:
    T (float): Tinggi limas.
    S (float): Panjang sisi alas segi lima.

    Returns:
    float: Luas permukaan limas segi lima.
    """
    import math
    A = (5/4) * S**2 * (1 / math.tan(math.pi / 5))
    L = A + 5 * (0.5 * S * T)
    return L

def KaLimasSL(S):
    """
    Menghitung keliling alas limas segi lima.

    Parameters:
    S (float): Panjang sisi alas segi lima.

    Returns:
    float: Keliling alas limas segi lima.
    """
    K = 5 * S
    return K

def TlimasSL(V, La):
    """
    Menghitung tinggi limas segi lima berdasarkan volume dan luas alas.

    Parameters:
    V (float): Volume limas.
    La (float): Luas alas segi lima.

    Returns:
    float: Tinggi limas segi lima.
    """
    T = (3 * V) / La
    return T

def LPSLimasSL(S, T):
    """
    Menghitung luas permukaan samping limas segi lima.

    Parameters:
    S (float): Panjang sisi alas segi lima.
    T (float): Tinggi limas.

    Returns:
    float: Luas permukaan samping limas segi lima.
    """
    Lps = 5 * (0.5 * S * T)
    return Lps



def vLimasSEn(T, P, L):
    """
    Menghitung volume limas segi enam.

    Parameters:
    T (float): Tinggi limas.
    P (float): Panjang alas segi enam.
    L (float): Lebar alas segi enam.

    Returns:
    float: Volume limas segi enam.
    """
    A = P * L
    V = (1/3) * A * T
    return V

def LPLimasSEn(T, S):
    """
    Menghitung luas permukaan limas segi enam.

    Parameters:
    T (float): Tinggi limas.
    S (float): Panjang sisi alas segi enam.

    Returns:
    float: Luas permukaan limas segi enam.
    """
    import math
    A = (3 * math.sqrt(3) / 2) * S**2
    L = A + 6 * (0.5 * S * T)
    return L

def KaLimasSTEn(S):
    """
    Menghitung keliling alas limas segi enam.

    Parameters:
    S (float): Panjang sisi alas segi enam.

    Returns:
    float: Keliling alas limas segi enam.
    """
    K = 6 * S
    return K

def TlimasSEn(V, La):
    """
    Menghitung tinggi limas segi enam berdasarkan volume dan luas alas.

    Parameters:
    V (float): Volume limas.
    La (float): Luas alas segi enam.

    Returns:
    float: Tinggi limas segi enam.
    """
    T = (3 * V) / La
    return T

def LPSLimasSEn(S, T):
    """
    Menghitung luas permukaan samping limas segi enam.

    Parameters:
    S (float): Panjang sisi alas segi enam.
    T (float): Tinggi limas.

    Returns:
    float: Luas permukaan samping limas segi enam.
    """
    Lps = 6 * (0.5 * S * T)
    return Lps
