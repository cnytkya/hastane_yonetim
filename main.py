def ana_menu():
    pass

def main():
    """ana program"""
    print("\n" + "="*40)
    print("  HASTA RANDEVU SİSTEMİ BAŞLATILIYOR...")
    print("\n" + "="*40)
    
    while True:
        devam = ana_menu()
        if not devam:
            break

if __name__ == "__main__":
    main()