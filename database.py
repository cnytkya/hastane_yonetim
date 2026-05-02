import sqlite3
from datetime import datetime

def baglan():
    """Veritabanına bağlantı oluşturur"""
    return sqlite3.connect('db.sqlite3')

def tablolari_olustur():
    """Gerekli tabloları oluşturur"""
    conn = baglan()
    cursor = conn.cursor()
    
    # Hastalar tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hastalar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tc_no TEXT UNIQUE NOT NULL,
            ad TEXT NOT NULL,
            soyad TEXT NOT NULL,
            telefon TEXT NOT NULL,
            dogum_tarihi TEXT
        )
    ''')
    
    # Randevular tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS randevular (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hasta_id INTEGER NOT NULL,
            randevu_tarihi TEXT NOT NULL,
            randevu_saati TEXT NOT NULL,
            doktor TEXT NOT NULL,
            aciklama TEXT,
            durum TEXT DEFAULT 'aktif',
            FOREIGN KEY (hasta_id) REFERENCES hastalar(id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()

# ============ HASTA İŞLEMLERİ ============

def hasta_kaydet(ad, soyad, tc_no, telefon, dogum_tarihi):
    """Yeni hasta kaydeder"""
    conn = baglan()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO hastalar (ad, soyad, tc_no, telefon, dogum_tarihi)
            VALUES (?, ?, ?, ?, ?)
        ''', (ad, soyad, tc_no, telefon, dogum_tarihi))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def tum_hastalari_getir():
    """Tüm hastaları listeler"""
    conn = baglan()
    cursor = conn.cursor()
    cursor.execute('SELECT id, ad, soyad, tc_no, telefon, dogum_tarihi FROM hastalar ORDER BY ad')
    sonuc = cursor.fetchall()
    conn.close()
    return sonuc

def hasta_ara(anahtar):
    """Hasta arar (ad, soyad veya TC'ye göre)"""
    conn = baglan()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, ad, soyad, tc_no, telefon, dogum_tarihi 
        FROM hastalar 
        WHERE ad LIKE ? OR soyad LIKE ? OR tc_no LIKE ?
        ORDER BY ad
    ''', (f'%{anahtar}%', f'%{anahtar}%', f'%{anahtar}%'))
    sonuc = cursor.fetchall()
    conn.close()
    return sonuc

def hasta_getir(hasta_id):
    """ID'ye göre hasta bilgilerini getirir"""
    conn = baglan()
    cursor = conn.cursor()
    cursor.execute('SELECT id, ad, soyad, tc_no, telefon, dogum_tarihi FROM hastalar WHERE id = ?', (hasta_id,))
    sonuc = cursor.fetchone()
    conn.close()
    return sonuc

def hasta_guncelle(hasta_id, ad, soyad, tc_no, telefon, dogum_tarihi):
    """Hasta bilgilerini günceller"""
    conn = baglan()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE hastalar 
        SET ad = ?, soyad = ?, tc_no = ?, telefon = ?, dogum_tarihi = ?
        WHERE id = ?
    ''', (ad, soyad, tc_no, telefon, dogum_tarihi, hasta_id))
    conn.commit()
    conn.close()

def hasta_sil(hasta_id):
    """Hasta siler"""
    conn = baglan()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM hastalar WHERE id = ?', (hasta_id,))
    conn.commit()
    conn.close()

def hasta_randevu_var_mi(hasta_id):
    """Hastanın aktif randevusu var mı kontrol eder"""
    conn = baglan()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM randevular WHERE hasta_id = ? AND durum = "aktif"', (hasta_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

# ============ RANDEVU İŞLEMLERİ ============

def randevu_kaydet(hasta_id, tarih, saat, doktor, aciklama):
    """Yeni randevu kaydeder"""
    conn = baglan()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO randevular (hasta_id, randevu_tarihi, randevu_saati, doktor, aciklama)
        VALUES (?, ?, ?, ?, ?)
    ''', (hasta_id, tarih, saat, doktor, aciklama))
    conn.commit()
    conn.close()

def randevu_musait_mi(tarih, saat, doktor):
    """Randevu saati müsait mi kontrol eder"""
    conn = baglan()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT COUNT(*) FROM randevular 
        WHERE randevu_tarihi = ? AND randevu_saati = ? AND doktor = ? AND durum = 'aktif'
    ''', (tarih, saat, doktor))
    count = cursor.fetchone()[0]
    conn.close()
    return count == 0

def tum_randevulari_getir():
    """Tüm randevuları getirir"""
    conn = baglan()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT r.id, h.ad, h.soyad, r.randevu_tarihi, r.randevu_saati, r.doktor, r.durum, r.aciklama
        FROM randevular r
        JOIN hastalar h ON r.hasta_id = h.id
        ORDER BY r.randevu_tarihi, r.randevu_saati
    ''')
    sonuc = cursor.fetchall()
    conn.close()
    return sonuc

def bugunun_randevulari():
    """Bugünün randevularını getirir"""
    bugun = datetime.now().strftime('%Y-%m-%d')
    conn = baglan()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT r.id, h.ad, h.soyad, r.randevu_tarihi, r.randevu_saati, r.doktor, r.durum, r.aciklama
        FROM randevular r
        JOIN hastalar h ON r.hasta_id = h.id
        WHERE r.randevu_tarihi = ? AND r.durum = 'aktif'
        ORDER BY r.randevu_saati
    ''', (bugun,))
    sonuc = cursor.fetchall()
    conn.close()
    return sonuc

def haftalik_randevular():
    """Bu haftanın randevularını getirir"""
    bugun = datetime.now()
    hafta_basi = bugun.strftime('%Y-%m-%d')
    # 7 gün sonrası
    yedi_gun_sonra = datetime(bugun.year, bugun.month, bugun.day + 7).strftime('%Y-%m-%d')
    
    conn = baglan()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT r.id, h.ad, h.soyad, r.randevu_tarihi, r.randevu_saati, r.doktor, r.durum, r.aciklama
        FROM randevular r
        JOIN hastalar h ON r.hasta_id = h.id
        WHERE r.randevu_tarihi BETWEEN ? AND ? AND r.durum = 'aktif'
        ORDER BY r.randevu_tarihi, r.randevu_saati
    ''', (hafta_basi, yedi_gun_sonra))
    sonuc = cursor.fetchall()
    conn.close()
    return sonuc

def hasta_randevulari_getir(hasta_id):
    """Belirli bir hastanın randevularını getirir"""
    conn = baglan()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT r.id, h.ad, h.soyad, r.randevu_tarihi, r.randevu_saati, r.doktor, r.durum, r.aciklama
        FROM randevular r
        JOIN hastalar h ON r.hasta_id = h.id
        WHERE r.hasta_id = ?
        ORDER BY r.randevu_tarihi DESC, r.randevu_saati DESC
    ''', (hasta_id,))
    sonuc = cursor.fetchall()
    conn.close()
    return sonuc

def randevu_durum_guncelle(randevu_id, yeni_durum):
    """Randevu durumunu günceller (aktif/iptal/tamamlandı)"""
    conn = baglan()
    cursor = conn.cursor()
    cursor.execute('UPDATE randevular SET durum = ? WHERE id = ?', (yeni_durum, randevu_id))
    conn.commit()
    conn.close()

def randevu_var_mi(randevu_id):
    """Randevu var mı kontrol eder"""
    conn = baglan()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM randevular WHERE id = ?', (randevu_id,))
    sonuc = cursor.fetchone()
    conn.close()
    return sonuc is not None

def randevu_sil(randevu_id):
    """Randevu siler (hard delete)"""
    conn = baglan()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM randevular WHERE id = ?', (randevu_id,))
    conn.commit()
    conn.close()

# ============ RAPORLAR ============

def randevu_istatistikleri():
    """Randevu istatistiklerini getirir"""
    conn = baglan()
    cursor = conn.cursor()
    
    # Toplam randevu sayısı
    cursor.execute('SELECT COUNT(*) FROM randevular')
    toplam = cursor.fetchone()[0]
    
    # Aktif randevu sayısı
    cursor.execute('SELECT COUNT(*) FROM randevular WHERE durum = "aktif"')
    aktif = cursor.fetchone()[0]
    
    # İptal edilen randevu sayısı
    cursor.execute('SELECT COUNT(*) FROM randevular WHERE durum = "iptal"')
    iptal = cursor.fetchone()[0]
    
    # Tamamlanan randevu sayısı
    cursor.execute('SELECT COUNT(*) FROM randevular WHERE durum = "tamamlandi"')
    tamamlandi = cursor.fetchone()[0]
    
    conn.close()
    return {'toplam': toplam, 'aktif': aktif, 'iptal': iptal, 'tamamlandi': tamamlandi}

def doktor_randevu_sayilari():
    """Doktorlara göre randevu sayılarını getirir"""
    conn = baglan()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT doktor, COUNT(*) as sayi 
        FROM randevular 
        WHERE durum = 'aktif'
        GROUP BY doktor
        ORDER BY sayi DESC
    ''')
    sonuc = cursor.fetchall()
    conn.close()
    return sonuc