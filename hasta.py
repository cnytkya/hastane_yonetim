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
    
    telefon = 

        
