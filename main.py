import utils
import hasta
import database
from randevu import randevu_menu

def ana_menu():
    """ana menü"""
    while True:
        utils.temizle()
        print("\n" + "="*40)
        print("        HASTA RANDEVU SİSTEMİ")
        print("\n" + "="*40)

        print("  ╔════════════════════════════╗")
        print("  ║  1 -    Hasta İşlemleri    ║")
        print("  ║  2 -    Randevu İşlemleri  ║")
        print("  ║  3 -    Raporlar           ║")
        print("  ║  0 -    Çıkış              ║")
        print("  ╚════════════════════════════╝")
        print("\n" + "="*40)

        secim = input("Seçiminz: ")
        if secim == "1":
            hasta.hasta_menu()
        elif secim == "2":
            randevu_menu()
        elif secim == "3":
            raporlama_menu()
        elif secim == "0":
            print("\nProgram sonlanıyor...")
            print("Tekrar bekleriz...")
            return False
        else:
            print("Geçersiz seçim!")

def raporlama_menu():
    while True:
        utils.temizle()
        print("\n" + "="*40)
        print("        RAPORALAR")
        print("  ╔══════════════════════════════════╗")
        print("  ║1-Randevu İstatistikleri          ║")
        print("  ║2-Doktor Bazlı Randevu Raporu     ║")
        print("  ║0-Çıkış                           ║")
        print("  ╚══════════════════════════════════╝")
        print("\n" + "="*40)

        secim = input("Seçiminz: ")
        if secim == "1":
            utils.temizle()
            print("\n" + "="*40)
            print("        RAPORALAR İSTATİSTİKLERİ")
            print("\n" + "="*40)
            istatistik = database.randevu_istatistikleri()
            print(f"\n Toplam Randevu Sayısı: {istatistik['toplam']}")
            print(f"\n Aktif Randevular: {istatistik['aktif']}")
            print(f"\n İptal edilenler: {istatistik['iptal']}")
            print(f"\n Tamamlananlar: {istatistik['tamamlandi']}")
            utils.bekle()

        elif secim == "2":
            utils.temizle()
            print("\n" + "="*40)
            print("  DOKTOR BAZLI RANDEVULAR")
            print("\n" + "="*40)
            doktorlar = database.doktor_randevu_sayilari()
            if not doktorlar:
                print("Henüz randevu bulunmamamaktadır!")
            else:
                print("\n Doktor Adı:".ljust(25) + "Randevu sayısı")
                # print("\n Randevu Saati:")
                # print("\n" + "="*40)
                for doktor, sayi in doktorlar:
                    print(f"{doktor[:23].ljust(25)}{sayi}")
            utils.bekle()
        elif secim == "0":
            break
        else:
            print("Geçersiz Seçim!")
            utils.bekle()

        

def main():
    """ana program"""
    print("\n" + "="*40)
    print("  HASTA RANDEVU SİSTEMİ BAŞLATILIYOR...")
    print("\n" + "="*40)
    
    database.tablolari_olustur()
    print("Veriatabanı tabloları hazır...")
    utils.bekle()
    while True:
        devam = ana_menu()
        if not devam:
            break

if __name__ == "__main__":
    main()