##Limas Segi Tiga
#Volume Limas Segi tiga
def vLimasST (T,P,Ta):
    La = 0.5 * P * Ta
    V = (1/3) * La * T
    return V

#Luas Permukaan Limas Segi tiga
def LPLimasST (T,P,Ta):
    La = 0.5 * P * Ta
    Lst = 3 * (0.5* P * T)
    L = La +Lst
    return L

#Keliling alas Limas Segi tiga
def KaLimasST (Sa,Sb,Sc):
    K = Sa + Sb + Sc
    return K

#Tinggi Limas Segi tiga
def TlimasST (V,La):
    T = (3 * V) /  La
    return T

#Luas Permukann Samping LImas Segi Tiga
def LPSLimasST (S,T):
    Lps = 3 * (0.5 * S * T)
    return Lps


##Limas Segi Empat
#Volume Limas Segi Empat
def vLimasSE (T,P,L):
    A = P * L
    V = (1/3) * A * T
    return V

#Luas Permukaan Limas Segi Empat
def LPLimasSE (T,S):
    A = S * S
    L = A + 4 * (0.5 * S * T)
    return L

#Keliling alas Limas Segi Empat
def KaLimasSTE (S):
    K = 4 * S
    return K

#Tinggi Limas Segi Empat
def TlimasSE(V,La):
    T = (3 * V) /  La
    return T

# Luas Permukann Samping Limas Segi Empat
def LPSLimasSE(S,T):
    Lps = 4 * (0.5 * S * T)
    return Lps

## Limas Segi Lima
# Volume Limas Segi Lima
def vLimasSL (T,P,L):
    A = P * L
    V = (1/3) * A * T
    return V

#Luas Permukaan Limas Segi Lima
def LPLimasSL (T,S):
    import math
    A = (5/4) * S**2 * (1 / math.tan(math.pi / 5))
    L = A + 5 * (0.5 * S * T)
    return L

#Keliling alas Limas Segi Lima
def KaLimasSL (S):
    K = 5 * S
    return K

#Tinggi Limas Segi Lima
def TlimasSL (V,La):
    T = (3 * V) /  La
    return T

#Luas Permukaan Samping Limas Segi Lima
def LPSLimasSL (S,T):
    Lps = 5 * (0.5 * S * T)
    return Lps

##Limas Segi Enam
# Volume Limas Segi Enam
def vLimasSEn (T,P,L):
    A = P * L
    V = (1/3) * A * T
    return V

#Luas Permukaan Limas Segi Enam
def LPLimasSEn (T,S):
    import math
    A = (3 * math.sqrt(3) / 2) * S**2
    L = A + 6 * (0.5 * S * T)
    return L

#Keliling alas Limas Segi Enam
def KaLimasSTEn (S):
    K = 6 * S
    return K

#Tinggi Limas Segi Enam
def TlimasSEn (V,La):
    T = (3 * V) /  La
    return T

#Luas Permukaan Samping Limas Segi Enam
def LPSLimasSEn (S,T):
    Lps = 6 * (0.5 * S * T)
    return Lps