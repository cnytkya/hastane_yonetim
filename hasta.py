import database # Veritabanına hasta verilerini yazmak, sorgulamak ve silmek için kullanılan modül.
import utils

def hasta_ekle():
    # yeni hasta kaydeder.
    print("\n" + "="*40)
    print(          "YENİ HASTA KAYDI")
    print("\n" + "="*40)

    ad = input("Ad: ").strip() # kullanıcıdan adını alır ve başındaki/sonundaki boşlukları temizler
    soyad = input("Soyad: ").strip()

    # tc no kontrolü: amaç kullanıcıdan geçerli bir tc girmesini sağlamak
    while True:
        tc_no = input("T.C No(11 Hane Olacak Şekilde): ").strip()
        if utils.tc_gecerli_mi(tc_no):
            break
        print("Geçersiz TC NO! Lütfen 11 haneli geçerli bir TC giriniz.")
    
    telefon = input("Telefon: ").strip()
    dogum_tarihi = input("Doğum tarihi (YYYY-MM-DD, boş bırakabilirsiniz): ").strip()
    result = database.hasta_kaydet(ad,soyad,tc_no,telefon,dogum_tarihi if dogum_tarihi else None)
    if result:
        print(F"\n Hasta başarıyla eklendi! (ID:{result})")
    else:
        print(F"\n Hata: Bu hasta adında TC NO zaten kayıtlı!")

def hasta_menu():
    while True:
        utils.temizle()
        print("\n" + "="*40)
        print("        HASTA İŞLEMLERİ")
        print("\n" + "="*40)
        print(" 1 - Hasta Ekle")
        print(" 2 - Hasta Listele")
        print(" 3 - Hasta Ara")
        print(" 4 - Hasta Güncelle")
        print(" 5 - Hasta Sil")
        print(" 0 - Ana Menüye dön")
        print("\n" + "="*40)

        secim = int(input("Seçimniz: "))
        if secim == 1:
            utils.temizle()
            hasta_ekle()
            utils.bekle()



        
