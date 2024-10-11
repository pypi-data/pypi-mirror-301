import math

def luas_tabung(r, t):
    """
    Menghitung luas permukaan tabung.

    Parameters:
    r (float): Jari-jari alas tabung.
    t (float): Tinggi tabung.

    Returns:
    float: Luas permukaan tabung.
    """
    return 2 * math.pi * r * (r + t)

def keliling_alas_tabung(r, t):
    """
    Menghitung keliling alas tabung.

    Parameters:
    r (float): Jari-jari alas tabung.

    Returns:
    float: Keliling alas tabung.
    """
    return 2 * math.pi * r

def volume_tabung(r, t):
    """
    Menghitung volume tabung.

    Parameters:
    r (float): Jari-jari alas tabung.
    t (float): Tinggi tabung.

    Returns:
    float: Volume tabung.
    """
    return math.pi * (r**2) * t

def selimut_tabung(r, t):
    """
    Menghitung luas selimut tabung.

    Parameters:
    r (float): Jari-jari alas tabung.
    t (float): Tinggi tabung.

    Returns:
    float: Luas selimut tabung.
    """
    return 2 * math.pi * r * t

def diameter_tabung(r):
    """
    Menghitung diameter tabung berdasarkan jari-jari.

    Parameters:
    r (float): Jari-jari alas tabung.

    Returns:
    float: Diameter tabung.
    """
    return 2 * r

def mencari_jarijari_dengan_volume(volume, t):
    """
    Menghitung jari-jari alas tabung berdasarkan volume dan tinggi.

    Parameters:
    volume (float): Volume tabung.
    t (float): Tinggi tabung.

    Returns:
    float: Jari-jari alas tabung.
    """
    return math.sqrt(volume / (math.pi * t))

def mencari_tinggi_dengan_volume(volume, r):
    """
    Menghitung tinggi tabung berdasarkan volume dan jari-jari alas.

    Parameters:
    volume (float): Volume tabung.
    r (float): Jari-jari alas tabung.

    Returns:
    float: Tinggi tabung.
    """
    return volume / (math.pi * r**2)

def perbandingan_dua_tabung(tabung1, tabung2, parameter='volume'):
    """
    Membandingkan dua tabung berdasarkan parameter tertentu.

    Parameters:
    tabung1 (dict): Data tabung pertama dengan key 'volume' dan 'luas'.
    tabung2 (dict): Data tabung kedua dengan key 'volume' dan 'luas'.
    parameter (str): Parameter yang akan dibandingkan ('volume' atau 'luas'). Default adalah 'volume'.

    Returns:
    float: Perbandingan antara tabung pertama dan tabung kedua berdasarkan parameter yang dipilih.

    Raises:
    ValueError: Jika parameter yang diberikan tidak valid.
    """
    if parameter == 'volume':
        return tabung1['volume'] / tabung2['volume']
    elif parameter == 'luas':
        return tabung1['luas'] / tabung2['luas']
    else:
        raise ValueError("Parameter tidak dikenali. Gunakan 'volume' atau 'luas'.")

def luas_alas_tabung(r):
    """
    Menghitung luas alas tabung.

    Parameters:
    r (float): Jari-jari alas tabung.

    Returns:
    float: Luas alas tabung.
    """
    return math.pi * r**2

def luas_permukaan_tanpa_tutup(r, t):
    """
    Menghitung luas permukaan tabung tanpa tutup (hanya alas dan selimut).

    Parameters:
    r (float): Jari-jari alas tabung.
    t (float): Tinggi tabung.

    Returns:
    float: Luas permukaan tabung tanpa tutup.
    """
    return math.pi * r * (2 * t + r)

def luas_permukaan_tanpa_alas(r, t):
    """
    Menghitung luas permukaan tabung tanpa alas (hanya tutup dan selimut).

    Parameters:
    r (float): Jari-jari alas tabung.
    t (float): Tinggi tabung.

    Returns:
    float: Luas permukaan tabung tanpa alas.
    """
    return math.pi * r * (2 * t + r)

def mencari_tinggi_dengan_selimut(luas_selimut, r):
    """
    Menghitung tinggi tabung berdasarkan luas selimut dan jari-jari alas.

    Parameters:
    luas_selimut (float): Luas selimut tabung.
    r (float): Jari-jari alas tabung.

    Returns:
    float: Tinggi tabung.
    """
    return luas_selimut / (2 * math.pi * r)

def rasio_volume_luas_permukaan(r, t):
    """
    Menghitung rasio volume terhadap luas permukaan tabung.

    Parameters:
    r (float): Jari-jari alas tabung.
    t (float): Tinggi tabung.

    Returns:
    float: Rasio antara volume dan luas permukaan tabung.
    """
    volume = volume_tabung(r, t)
    luas = luas_tabung(r, t)
    return volume / luas

def panjang_kawat_bingkai_tabung(r, t):
    """
    Menghitung total panjang kawat yang dibutuhkan untuk membuat bingkai tabung
    (keliling alas atas + keliling alas bawah + tinggi tabung x 2).

    Parameters:
    r (float): Jari-jari alas tabung.
    t (float): Tinggi tabung.

    Returns:
    float: Total panjang kawat yang dibutuhkan.
    """
    keliling = 2 * math.pi * r
    return 2 * keliling + 2 * t

def biaya_pembuatan_tabung(r, t, harga_per_satuan_luas, include_tutup=True):
    """
    Menghitung biaya pembuatan tabung berdasarkan luas permukaan dan harga material.

    Parameters:
    r (float): Jari-jari alas tabung.
    t (float): Tinggi tabung.
    harga_per_satuan_luas (float): Harga per satuan luas material (misal per meter persegi).
    include_tutup (bool): Menentukan apakah biaya termasuk tutup tabung (default: True).

    Returns:
    float: Biaya total pembuatan tabung.
    """
    if include_tutup:
        luas_total = luas_tabung(r, t)
    else:
        luas_total = luas_permukaan_tanpa_tutup(r, t)
    
    return luas_total * harga_per_satuan_luas

def optimasi_volume_dengan_luas_terbatas(luas_material, r):
    """
    Menghitung tinggi maksimal yang menghasilkan volume terbesar dengan luas material terbatas.

    Parameters:
    luas_material (float): Luas total material yang tersedia.
    r (float): Jari-jari alas tabung.

    Returns:
    float: Tinggi optimal untuk volume maksimal.
    """
    # Luas permukaan tabung = 2 * pi * r * (r + t)
    # Kita memaksimalkan t untuk volume terbesar
    t = (luas_material / (2 * math.pi * r)) - r
    return t

def cek_kapasitas_tabung(r, t, kapasitas_minimal):
    """
    Memeriksa apakah volume tabung memenuhi kapasitas minimal.

    Parameters:
    r (float): Jari-jari alas tabung.
    t (float): Tinggi tabung.
    kapasitas_minimal (float): Kapasitas volume minimal yang diinginkan.

    Returns:
    bool: True jika volume tabung lebih besar atau sama dengan kapasitas minimal, False jika tidak.
    """
    volume = volume_tabung(r, t)
    return volume >= kapasitas_minimal

def konversi_volume_ke_liter(volume_meter_kubik):
    """
    Mengkonversi volume dari meter kubik ke liter.

    Parameters:
    volume_meter_kubik (float): Volume dalam meter kubik.

    Returns:
    float: Volume dalam liter.
    """
    return volume_meter_kubik * 1000  # 1 meter kubik = 1000 liter

def validasi_dimensi_tabung(r, t):
    """
    Memeriksa apakah jari-jari dan tinggi tabung valid (tidak negatif atau nol).

    Parameters:
    r (float): Jari-jari alas tabung.
    t (float): Tinggi tabung.

    Returns:
    bool: True jika dimensi valid, False jika tidak.
    """
    return r > 0 and t > 0


