import database
import utils

def hasta_ekle():
    """Yeni hasta ekler"""
    print("\n" + "="*40)
    print("         YENİ HASTA EKLE")
    print("="*40)
    
    ad = input("Ad: ").strip()
    soyad = input("Soyad: ").strip()
    
    # TC No kontrolü (while döngüsü ile)
    while True:
        tc_no = input("TC No (11 hane): ").strip()
        if utils.tc_gecerli_mi(tc_no):
            break
        print("  Geçersiz TC No! Lütfen 11 haneli geçerli bir TC girin.")
    
    telefon = input("Telefon: ").strip()
    dogum_tarihi = input("Doğum Tarihi (YYYY-MM-DD, boş bırakabilirsiniz): ").strip()
    
    sonuc = database.hasta_kaydet(ad, soyad, tc_no, telefon, dogum_tarihi if dogum_tarihi else None)
    
    if sonuc:
        print(f"\n  ✓ Hasta başarıyla eklendi! (ID: {sonuc})")
    else:
        print("\n  ✗ Hata: Bu TC No ile kayıtlı hasta zaten var!")

def hasta_listele():
    """Tüm hastaları listeler"""
    print("\n" + "="*60)
    print("              HASTA LİSTESİ")
    print("="*60)
    
    hastalar = database.tum_hastalari_getir()
    
    if not hastalar:
        print("  Kayıtlı hasta bulunmamaktadır.")
    else:
        basliklar = ["ID", "Ad", "Soyad", "TC No", "Telefon", "Doğum Tarihi"]
        utils.tablo_yazdir(basliklar, hastalar)

def hasta_ara():
    """Hasta arar"""
    print("\n" + "="*40)
    print("              HASTA ARA")
    print("="*40)
    
    anahtar = input("Aranacak kelime (ad, soyad veya TC): ").strip()
    
    if not anahtar:
        print("  Lütfen bir arama kelimesi girin.")
        return
    
    sonuclar = database.hasta_ara(anahtar)
    
    if not sonuclar:
        print(f"  '{anahtar}' ile eşleşen hasta bulunamadı.")
    else:
        print(f"\n  {len(sonuclar)} hasta bulundu:\n")
        basliklar = ["ID", "Ad", "Soyad", "TC No", "Telefon", "Doğum Tarihi"]
        utils.tablo_yazdir(basliklar, sonuclar)

def hasta_guncelle():
    """Hasta bilgilerini günceller"""
    print("\n" + "="*40)
    print("           HASTA GÜNCELLE")
    print("="*40)
    
    try:
        hasta_id = int(input("Güncellenecek hasta ID: "))
    except ValueError:
        print("  Geçersiz ID!")
        return
    
    hasta = database.hasta_getir(hasta_id)
    
    if not hasta:
        print(f"  ID '{hasta_id}' ile kayıtlı hasta bulunamadı.")
        return
    
    print(f"\n  Mevcut bilgiler:")
    print(f"  Ad: {hasta[1]}")
    print(f"  Soyad: {hasta[2]}")
    print(f"  TC No: {hasta[3]}")
    print(f"  Telefon: {hasta[4]}")
    print(f"  Doğum Tarihi: {hasta[5]}")
    
    print("\n  (Boş bırakırsanız mevcut bilgi korunur)")
    
    yeni_ad = input(f"  Yeni Ad ({hasta[1]}): ").strip()
    yeni_soyad = input(f"  Yeni Soyad ({hasta[2]}): ").strip()
    
    # TC No kontrolü
    while True:
        yeni_tc = input(f"  Yeni TC No ({hasta[3]}): ").strip()
        if not yeni_tc:
            yeni_tc = hasta[3]
            break
        if utils.tc_gecerli_mi(yeni_tc):
            break
        print("  Geçersiz TC No!")
    
    yeni_telefon = input(f"  Yeni Telefon ({hasta[4]}): ").strip()
    yeni_dogum = input(f"  Yeni Doğum Tarihi ({hasta[5] if hasta[5] else 'boş'}): ").strip()
    
    database.hasta_guncelle(
        hasta_id,
        yeni_ad if yeni_ad else hasta[1],
        yeni_soyad if yeni_soyad else hasta[2],
        yeni_tc,
        yeni_telefon if yeni_telefon else hasta[4],
        yeni_dogum if yeni_dogum else hasta[5]
    )
    
    print(f"\n  ✓ Hasta (ID: {hasta_id}) başarıyla güncellendi!")

def hasta_sil():
    """Hasta siler"""
    print("\n" + "="*40)
    print("             HASTA SİL")
    print("="*40)
    
    try:
        hasta_id = int(input("Silinecek hasta ID: "))
    except ValueError:
        print("  Geçersiz ID!")
        return
    
    hasta = database.hasta_getir(hasta_id)
    
    if not hasta:
        print(f"  ID '{hasta_id}' ile kayıtlı hasta bulunamadı.")
        return
    
    print(f"\n  Silinecek Hasta: {hasta[1]} {hasta[2]} (TC: {hasta[3]})")
    
    # Aktif randevu kontrolü
    if database.hasta_randevu_var_mi(hasta_id):
        print("\n  ✗ Bu hastanın aktif randevuları var!")
        print("  Önce randevuları iptal edin veya silin.")
        return
    
    onay = input("\n  Hastayı silmek istediğinize emin misiniz? (E/H): ").upper()
    
    if onay == 'E':
        database.hasta_sil(hasta_id)
        print(f"\n  ✓ Hasta (ID: {hasta_id}) başarıyla silindi!")
    else:
        print("\n  Silme işlemi iptal edildi.")

def hasta_menu():
    """Hasta işlemleri menüsü (do-while benzeri)"""
    while True:
        utils.temizle()
        print("\n" + "="*40)
        print("        HASTA İŞLEMLERİ")
        print("="*40)
        print("  1 - Hasta Ekle")
        print("  2 - Hasta Listele")
        print("  3 - Hasta Ara")
        print("  4 - Hasta Güncelle")
        print("  5 - Hasta Sil")
        print("  0 - Ana Menüye Dön")
        print("="*40)
        
        secim = input("Seçiminiz: ").strip()
        
        if secim == '1':
            utils.temizle()
            hasta_ekle()
            utils.bekle()
        elif secim == '2':
            utils.temizle()
            hasta_listele()
            utils.bekle()
        elif secim == '3':
            utils.temizle()
            hasta_ara()
            utils.bekle()
        elif secim == '4':
            utils.temizle()
            hasta_guncelle()
            utils.bekle()
        elif secim == '5':
            utils.temizle()
            hasta_sil()
            utils.bekle()
        elif secim == '0':
            break
        else:
            print("  Geçersiz seçim! Lütfen tekrar deneyin.")
            utils.bekle()