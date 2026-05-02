import database
import utils
from datetime import datetime

def randevu_olustur():
    """Yeni randevu oluşturur"""
    print("\n" + "="*40)
    print("          RANDEVU OLUŞTUR")
    print("="*40)
    
    # Önce hasta seçimi
    print("\n  Önce hasta seçiniz:")
    hastalar = database.tum_hastalari_getir()
    
    if not hastalar:
        print("  Kayıtlı hasta bulunmamaktadır. Önce hasta ekleyin.")
        return
    
    utils.tablo_yazdir(["ID", "Ad", "Soyad", "TC No"], 
                       [(h[0], h[1], h[2], h[3]) for h in hastalar])
    
    try:
        hasta_id = int(input("\nHasta ID: "))
    except ValueError:
        print("  Geçersiz ID!")
        return
    
    hasta = database.hasta_getir(hasta_id)
    if not hasta:
        print(f"  ID '{hasta_id}' ile kayıtlı hasta bulunamadı.")
        return
    
    print(f"\n  Hasta: {hasta[1]} {hasta[2]}")
    
    # Tarih girişi (while döngüsü ile)
    while True:
        tarih = input("\nRandevu tarihi (YYYY-MM-DD): ").strip()
        if utils.tarih_gecerli_mi(tarih):
            break
        print("  Geçersiz tarih! Bugün veya ileri bir tarih girin (YYYY-MM-DD formatında).")
    
    # Doktor seçimi
    doktor = input("Doktor adı: ").strip()
    if not doktor:
        print("  Doktor adı boş olamaz!")
        return
    
    # Saat girişi (while döngüsü ile)
    while True:
        saat = input("Randevu saati (HH:MM, 08:00-18:00 arası): ").strip()
        if not utils.saat_gecerli_mi(saat):
            print("  Geçersiz saat! 08:00-18:00 arasında HH:MM formatında girin.")
            continue
        
        if database.randevu_musait_mi(tarih, saat, doktor):
            break
        print(f"  Bu saatte {doktor} doktorunun müsaitliği dolu! Lütfen başka saat seçin.")
    
    aciklama = input("Açıklama (isteğe bağlı): ").strip()
    
    database.randevu_kaydet(hasta_id, tarih, saat, doktor, aciklama)
    print(f"\n  ✓ Randevu başarıyla oluşturuldu!")
    print(f"  Tarih: {tarih}, Saat: {saat}, Doktor: {doktor}")

def randevu_listele():
    """Randevuları listeler"""
    print("\n" + "="*40)
    print("           RANDEVU LİSTELE")
    print("="*40)
    
    print("\n  Filtre seçenekleri:")
    print("  1 - Tüm randevular")
    print("  2 - Bugünün randevuları")
    print("  3 - Bu haftanın randevuları")
    print("  4 - Belirli hastanın randevuları")
    
    filtre = input("\nSeçiminiz (1-4): ").strip()
    
    if filtre == '1':
        randevular = database.tum_randevulari_getir()
        baslik = "TÜM RANDEVULAR"
    elif filtre == '2':
        randevular = database.bugunun_randevulari()
        baslik = "BUGÜNÜN RANDEVULARI"
    elif filtre == '3':
        randevular = database.haftalik_randevular()
        baslik = "BU HAFTANIN RANDEVULARI"
    elif filtre == '4':
        try:
            hasta_id = int(input("Hasta ID: "))
        except ValueError:
            print("  Geçersiz ID!")
            return
        randevular = database.hasta_randevulari_getir(hasta_id)
        baslik = f"HASTA (ID: {hasta_id}) RANDEVULARI"
    else:
        print("  Geçersiz seçim!")
        return
    
    print("\n" + "="*60)
    print(f"           {baslik}")
    print("="*60)
    
    if not randevular:
        print("  Randevu bulunamadı.")
    else:
        basliklar = ["ID", "Hasta", "Tarih", "Saat", "Doktor", "Durum", "Açıklama"]
        # Verileri düzenle
        veriler = []
        for r in randevular:
            veriler.append((
                r[0], 
                f"{r[1]} {r[2]}", 
                r[3], 
                r[4], 
                r[5], 
                r[6],
                (r[7][:30] + '...') if r[7] and len(r[7]) > 30 else (r[7] or '-')
            ))
        utils.tablo_yazdir(basliklar, veriler)

def randevu_iptal():
    """Randevu iptal eder"""
    print("\n" + "="*40)
    print("           RANDEVU İPTAL")
    print("="*40)
    
    randevular = database.tum_randevulari_getir()
    
    if not randevular:
        print("  İptal edilecek randevu bulunamadı.")
        return
    
    print("\n  Aktif Randevular:")
    aktif_randevular = [r for r in randevular if r[6] == 'aktif']
    
    if not aktif_randevular:
        print("  Aktif randevu bulunamadı.")
        return
    
    basliklar = ["ID", "Hasta", "Tarih", "Saat", "Doktor"]
    veriler = [(r[0], f"{r[1]} {r[2]}", r[3], r[4], r[5]) for r in aktif_randevular]
    utils.tablo_yazdir(basliklar, veriler)
    
    try:
        randevu_id = int(input("\nİptal edilecek randevu ID: "))
    except ValueError:
        print("  Geçersiz ID!")
        return
    
    if not database.randevu_var_mi(randevu_id):
        print(f"  ID '{randevu_id}' ile randevu bulunamadı.")
        return
    
    onay = input(f"\n  {randevu_id} nolu randevuyu iptal etmek istediğinize emin misiniz? (E/H): ").upper()
    
    if onay == 'E':
        database.randevu_durum_guncelle(randevu_id, 'iptal')
        print(f"\n  ✓ Randevu (ID: {randevu_id}) başarıyla iptal edildi!")
    else:
        print("\n  İptal işlemi iptal edildi.")

def randevu_tamamla():
    """Randevuyu tamamlandı olarak işaretler"""
    print("\n" + "="*40)
    print("        RANDEVU TAMAMLAMA")
    print("="*40)
    
    randevular = database.tum_randevulari_getir()
    
    if not randevular:
        print("  Tamamlanacak randevu bulunamadı.")
        return
    
    print("\n  Aktif Randevular:")
    aktif_randevular = [r for r in randevular if r[6] == 'aktif']
    
    if not aktif_randevular:
        print("  Aktif randevu bulunamadı.")
        return
    
    basliklar = ["ID", "Hasta", "Tarih", "Saat", "Doktor"]
    veriler = [(r[0], f"{r[1]} {r[2]}", r[3], r[4], r[5]) for r in aktif_randevular]
    utils.tablo_yazdir(basliklar, veriler)
    
    try:
        randevu_id = int(input("\nTamamlanan randevu ID: "))
    except ValueError:
        print("  Geçersiz ID!")
        return
    
    if not database.randevu_var_mi(randevu_id):
        print(f"  ID '{randevu_id}' ile randevu bulunamadı.")
        return
    
    database.randevu_durum_guncelle(randevu_id, 'tamamlandi')
    print(f"\n  ✓ Randevu (ID: {randevu_id}) tamamlandı olarak işaretlendi!")

def randevu_menu():
    """Randevu işlemleri menüsü"""
    while True:
        utils.temizle()
        print("\n" + "="*40)
        print("        RANDEVU İŞLEMLERİ")
        print("="*40)
        print("  1 - Randevu Oluştur")
        print("  2 - Randevuları Listele")
        print("  3 - Randevu İptal Et")
        print("  4 - Randevuyu Tamamla")
        print("  0 - Ana Menüye Dön")
        print("="*40)
        
        secim = input("Seçiminiz: ").strip()
        
        if secim == '1':
            utils.temizle()
            randevu_olustur()
            utils.bekle()
        elif secim == '2':
            utils.temizle()
            randevu_listele()
            utils.bekle()
        elif secim == '3':
            utils.temizle()
            randevu_iptal()
            utils.bekle()
        elif secim == '4':
            utils.temizle()
            randevu_tamamla()
            utils.bekle()
        elif secim == '0':
            break
        else:
            print("  Geçersiz seçim! Lütfen tekrar deneyin.")
            utils.bekle()