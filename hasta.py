import database # Veritabanına hasta verilerini yazmak, sorgulamak ve silmek için kullanılan modül.

def hasta_ekle():
    # yeni hasta kaydeder.
    print("\n" + "="*40)
    print(          "YENİ HASTA KAYDI")
    print("\n" + "="*40)

    ad = input("Ad: ").strip() # kullanıcıdan adını alır ve başındaki/sonundaki boşlukları temizler
    ad = input("Soyad: ").strip()

    # tc no kontrolü: amaç kullanıcıdan geçerli bir tc girmesini sağlamak
    while True:
        tc_no = input("T.C No(11 Hane Olacak Şekilde): ").strip()
        
        
