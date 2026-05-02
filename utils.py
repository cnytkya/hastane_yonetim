import re
from datetime import datetime

def tc_gecerli_mi(tc_no):
    """TC Kimlik numarası geçerlilik kontrolü"""
    if not tc_no or len(tc_no) != 11:
        return False
    if not tc_no.isdigit():
        return False
    
    # TC Kimlik algoritması (basit kontrol)
    tekler = 0
    ciftler = 0
    for i in range(9):
        if i % 2 == 0:  # 1., 3., 5., 7., 9. haneler (0-index'te 0,2,4,6,8)
            tekler += int(tc_no[i])
        else:  # 2., 4., 6., 8. haneler
            ciftler += int(tc_no[i])
    
    hane10 = (tekler * 7 - ciftler) % 10
    hane11 = (tekler + ciftler + int(tc_no[9])) % 10
    
    return hane10 == int(tc_no[9]) and hane11 == int(tc_no[10])

def tarih_gecerli_mi(tarih_str):
    """Tarih formatı ve geçerlilik kontrolü (YYYY-MM-DD)"""
    try:
        tarih = datetime.strptime(tarih_str, '%Y-%m-%d')
        bugun = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return tarih >= bugun
    except ValueError:
        return False

def saat_gecerli_mi(saat_str):
    """Saat formatı ve geçerlilik kontrolü (HH:MM, 08:00-18:00 arası)"""
    if not re.match(r'^([0-1][0-9]|2[0-3]):[0-5][0-9]$', saat_str):
        return False
    
    saat = int(saat_str.split(':')[0])
    return 8 <= saat <= 18  # 08:00 - 18:00 arası

def tablo_yazdir(basliklar, veriler):
    """Verileri tablo formatında yazdırır"""
    if not veriler:
        print("  Kayıt bulunamadı.")
        return
    
    # Sütun genişliklerini hesapla
    genislikler = [len(str(b)) for b in basliklar]
    for veri in veriler:
        for i, hucre in enumerate(veri):
            genislikler[i] = max(genislikler[i], len(str(hucre)))
    
    # Ayırıcı çizgi
    ayrac = "+" + "+".join(["-" * (g + 2) for g in genislikler]) + "+"
    
    # Başlık satırı
    print(ayrac)
    satir = "|"
    for i, baslik in enumerate(basliklar):
        satir += f" {str(baslik).ljust(genislikler[i])} |"
    print(satir)
    print(ayrac)
    
    # Veri satırları
    for veri in veriler:
        satir = "|"
        for i, hucre in enumerate(veri):
            satir += f" {str(hucre).ljust(genislikler[i])} |"
        print(satir)
    
    print(ayrac)

def temizle():
    """Konsol ekranını temizler"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def bekle():
    """Devam etmek için enter bekler"""
    input("\nDevam etmek için Enter tuşuna basın...")