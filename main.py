import utils
import hasta
import database

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