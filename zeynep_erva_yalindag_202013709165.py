import sqlite3 as sql

import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException



conn = sql.connect('database.db')
print("Sqlite ile bağlantı kuruldu.")
cursor = conn.cursor()
print("Cursor oluşturuldu.")
cursor.execute("""DROP TABLE IF EXISTS yorumlar""")   # Bu satırdaki kod yorumlar adlı tablo varsa siler, yoksa hata vermez.
cursor.execute("""CREATE TABLE IF NOT EXISTS "yorumlar" (
"id"	INTEGER NOT NULL,
"urun_adi" TEXT NOT NULL,
"urun_yorumlari"	TEXT,
"en_cok_yorumlanan_urunun_adi" TEXT,
"en_cok_yorumlanan_urunun_yorum_sayisi" INTEGER,
"en_yuksek_oy_alan_urunun_adi" TEXT,
"en_yuksek_oy_alan_urunun_oyu" INTEGER,
PRIMARY KEY(id AUTOINCREMENT)
);""")    # Bu satırdaki kodlar yorumlar adlı tablo yoksa oluşturur.



en_yuksek_oy_alan_urunun_oyu = 0
en_yuksek_oy_alan_urunun_adi = ""
en_cok_yorumlanan_urunun_yorum_sayisi = 0
en_cok_yorumlanan_urunun_adi = ""
for sayfaNo in range(1, 4): # 100 ile 150 arasında ürün barındırır.
    url = "https://www.ebay.com/b/Cell-Phone-Headsets/80077/bn_317525?_pgn=" + str(sayfaNo)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
    }   # Sayfayı incele>Linke tıklama>Headers>User-Agent
    driver = webdriver.Chrome()   # Bu kod Selenium'un webdriver modülünü kullanarak Chrome web tarayıcısını başlatır. (Başka bir tarayıcı da kullanabilirsiniz.)
    driver.maximize_window()   # Tarayıcı penceresini maximize etmek için
    html = requests.get(url, headers=headers).content   # Web sitesinin HTML içeriğini çekmek için
    soup = BeautifulSoup(html, "html.parser")   # Verilen HTML içeriğini bs4'ün BeautifulSoup modülünü kullanarak parse etmek için
    listem = soup.find_all("li", {"class": "s-item s-item--large"})   # Belirli bir etiket ve özellik kombinasyonuna sahip tüm öğeleri bulur.

    for li in listem:
        link = li.a.get("href")
        print(link)
        html = requests.get(link, headers=headers).content
        soup = BeautifulSoup(html, "html.parser")
        ad_2 = soup.find_all("div", {"vim x-item-title"})
        marka_degeri_2 = soup.find_all("div", {"ux-labels-values__values"})
        model_degeri_2 = soup.find_all("div", {"ux-labels-values__values"})
        marka_ismi_1 = soup.find_all("div", {"ux-labels-values__labels"})
        model_ismi_1 = soup.find_all("div", {"ux-labels-values__labels"})
        kategori_2 = soup.find_all("div", {"seo-breadcrumbs-container viexpsvc"})
        yildiz_degeri_2 = soup.find_all("div",{"fdbk-detail-seller-rating"})
        yorum_degeri_2 = soup.find_all("h2",{"fdbk-detail-list__title"})
        yildiz = 0
        i = 0
        yorum = 0
        for z in ad_2:
            ad = z.find("span", {"class": "ux-textspans ux-textspans--BOLD"}).text   # span etiketi içinde class özelliği "ux-textspans ux-textspans--BOLD" olan bir öğeyi bulur ve bulunan öğenin metin içeriğini verir.
            print("Ad: ", ad)

        try:
            for g in yildiz_degeri_2:
                yildiz_degeri=g.find("span",{"class":"fdbk-detail-seller-rating__value"}).text
                i += 1
                yildiz += float(yildiz_degeri)
            print("Yıldız: ", str(float(yildiz/i)))
            if float(yildiz / i) > en_yuksek_oy_alan_urunun_oyu:
                en_yuksek_oy_alan_urunun_oyu = float(yildiz / i)
                en_yuksek_oy_alan_urunun_adi = ad
        except ZeroDivisionError:
            print("Yıldız yok.")


        """(Ürünün yorum sayısını çekmeme izin vermiyor. This item (24) kısmını döndürüp 24
         şeklinde düzenlemem gerekirken About This Item olarak döndürüyor. Büyük ihtimal izin 
         vermiyor. Bundan dolayı Seller Feedback All items (6,603) kısmını döndürüp 6603 şeklinde
          düzenledim.)"""

        """# İlgili div etiketini ve içindeki span etiketini bulun
        ilgili_div = soup.find("div", class_="tabs__items")
        if ilgili_div:
            ilk_div = ilgili_div.find("div")
            if ilk_div:
                span_etiketi = ilk_div.find("span")
                if span_etiketi:
                    span_icindeki_span = span_etiketi.find("span")
                    if span_icindeki_span:
                        yorum_degeri = span_icindeki_span.text.strip()
                        print("Yorum Değeri:", yorum_degeri)
                    else:
                        print("İç içe geçmiş span etiketi bulunamadı.")
                else:
                    print("span etiketi bulunamadı.")
            else:
                print("İlk div etiketi bulunamadı.")
        else:
            print("tabs__items class'ına sahip div etiketi bulunamadı.")"""


        try:
            for k in yorum_degeri_2:
                yorum_degeri = k.find("span", {"class": "SECONDARY"}).text   # yorum_degeri = (5,687)
                yorum = str(yorum_degeri)
                yorum = yorum[1:-1]   # yorum = 5,687
                yorum = yorum.replace(",", "")   # yorum = 5687
                print("Yorum sayısı: {}".format(yorum))
                if int(yorum) > int(en_cok_yorumlanan_urunun_yorum_sayisi):
                    en_cok_yorumlanan_urunun_yorum_sayisi = yorum
                    en_cok_yorumlanan_urunun_adi = ad
        except ZeroDivisionError:
            print("Yorum yok.")

        for y in kategori_2:
            kategori = y.find_all("span")[-1].text   # Örneğin Electronics>Cell Phones&Accessories>Cell Phone Accessories>Headsets
            print("Kategori: ", kategori)

        index=-1
        for a in marka_ismi_1:
            marka_ismi_1 = a.find("span", {"ux-textspans"})
            index += 1
            if a.find(string="Brand") == "Brand" or a.find(string="Marke") == "Marke":   # Marka manasında yazılan Brand veya Marke yazan kısmın indexini bulup bu şekilde değerini ise listeden getiren bir kod çünkü her üründe Item specifics bölümündeki markanın konumu değişebiliyor.
                c = index

        liste = []
        for b in marka_degeri_2:
            marka_degeri_2 = b.find("span", {"ux-textspans"}).text
            liste.append(marka_degeri_2)
        try :
            print("Marka: {}".format(liste[c]))
        except:
            continue

        indexx = -1
        for d in model_ismi_1:
            model_ismi_1 = d.find("span", {"ux-textspans"})
            indexx += 1
            if d.find(string="Model") == "Model" or d.find(string="Modell") == "Modell":   # Model manasında yazılan Model ya da Modell yazan kısmın indexini bulup bu şekilde değerini ise listeden getiren bir kod çünkü her üründe Item specifics kısmındaki modelin konumu değişebiliyor.
                zz = indexx

        listee = []
        for x in model_degeri_2:
            model_degeri_2 = x.find("span", {"ux-textspans"}).text
            listee.append(model_degeri_2)
        try:
            print("Model: {}".format(listee[zz]))
        except:
            continue



        driver.get(link)   # Selenium WebDriver'ın belirli bir URL'ye gitmesini sağlar.
        time.sleep(2)   # saniye cinsinden
        try:
            dahaFazlaLink = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "a.fdbk-detail-list__tabbed-btn.fake-btn.fake-btn--large.fake-btn--secondary"))

            )   # Selenium WebDriver için belirli bir öğenin varlığını beklemeyi ifade eder.
            dahaFazlaLink.click()

            dahaFazlaLink100 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "div.itemsPerPage button.item[data-test-id='pagination-item-page-3']"))
            )   # Selenium WebDriver için belirli bir öğenin tıklanabilir olmasını beklemeyi ifade eder.
            dahaFazlaLink100.click()   # Ürünün 100'den fazla yorumu varsa 100 tanesini göstermesi için tıklanması gereken buton için.

            time.sleep(2)  # Yorumların yüklenmesini beklemeyi ifade eder.( Süreyi değiştirebilirsiniz.)

            # Şimdi tüm yorumları çekebilirsiniz
            yorum_2 = driver.find_elements(By.CSS_SELECTOR, "div.card__comment")   # Selenium'un WebDriver'ı üzerinden bir web sayfasındaki belirli bir CSS selektör ile eşleşen tüm öğeleri bulur ve liste olarak döndürür.
            tarih_2 = driver.find_elements(By.CSS_SELECTOR, "tr")
            print("Yorumlar ve Tarihler: ")

            for e in yorum_2:
                yorum_1 = e.find_element(By.TAG_NAME, "span").text   # Selenium'un WebDriver'ı üzerinden bir öğe içinde belirli bir HTML etiketini bulur ve etiketin metin içeriğini alır.
                print("Yorum: ", yorum_1)
                cursor.execute("INSERT INTO yorumlar (urun_adi,urun_yorumlari,en_cok_yorumlanan_urunun_adi,en_cok_yorumlanan_urunun_yorum_sayisi,en_yuksek_oy_alan_urunun_adi,en_yuksek_oy_alan_urunun_oyu) VALUES(?,?,?,?,?,?)", (ad, yorum_1,en_cok_yorumlanan_urunun_adi,en_cok_yorumlanan_urunun_yorum_sayisi,en_yuksek_oy_alan_urunun_adi,en_yuksek_oy_alan_urunun_oyu))
                conn.commit()   # Yapılan işlemleri kaydetmek için
            # Her tr elementi için işlemleri gerçekleştir
            for tr_element in tarih_2:
                # Her tr elementindeki 3. td elementini bul
                td_elements = tr_element.find_elements(By.CSS_SELECTOR, "td")

                # Eğer td elementleri varsa ve en az 3 tanesi varsa, 3. td elementinin içindeki div'leri bul
                if len(td_elements) >= 3:
                    third_td_element = td_elements[2]
                    div_elements = third_td_element.find_elements(By.CSS_SELECTOR, "div")

                    # Eğer div elementleri varsa ve en az 1 tanesi varsa, ilk div'in içindeki span'ı bul
                    if div_elements:
                        first_div_element = div_elements[0]
                        tarih_element = first_div_element.find_element(By.CSS_SELECTOR, "span[aria-label]")

                        # Eğer span[aria-label] elementi varsa, text değerini al ve yazdır
                        if tarih_element:
                            tarih = tarih_element.text
                            print("Tarih: ", tarih)


        except TimeoutException:
            try:
                driver.get(link)
                time.sleep(2)
                dahaFazlaLink_2 = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (
                        By.CSS_SELECTOR, "a.fdbk-detail-list__tabbed-btn.fake-btn.fake-btn--large.fake-btn--secondary"))
                )
                dahaFazlaLink_2.click()

                time.sleep(3)  # Yorumların yüklenmesini bekleyin, süreyi artırabilirsiniz
                # Şimdi tüm yorumları çekebilirsiniz
                yorum_2 = driver.find_elements(By.CSS_SELECTOR, "div.card__comment")
                tarih_2 = driver.find_elements(By.CSS_SELECTOR, "tr")
                print("Yorumlar ve Tarihler: ")
                for e in yorum_2:
                    yorum_1 = e.find_element(By.TAG_NAME, "span").text
                    print("Yorum:",yorum_1)
                    cursor.execute("INSERT INTO yorumlar (urun_adi,urun_yorumlari,en_cok_yorumlanan_urunun_adi,en_cok_yorumlanan_urunun_yorum_sayisi,en_yuksek_oy_alan_urunun_adi,en_yuksek_oy_alan_urunun_oyu) VALUES(?,?,?,?,?,?)", (ad, yorum_1,en_cok_yorumlanan_urunun_adi,en_cok_yorumlanan_urunun_yorum_sayisi,en_yuksek_oy_alan_urunun_adi,en_yuksek_oy_alan_urunun_oyu))
                    conn.commit()
                for tr_element in tarih_2:
                    # Her tr elementindeki 3. td elementini bul
                    td_elements = tr_element.find_elements(By.CSS_SELECTOR, "td")

                    # Eğer td elementleri varsa ve en az 3 tanesi varsa, 3. td elementinin içindeki div'leri bul
                    if len(td_elements) >= 3:
                        third_td_element = td_elements[2]
                        div_elements = third_td_element.find_elements(By.CSS_SELECTOR, "div")

                        # Eğer div elementleri varsa ve en az 1 tanesi varsa, ilk div'in içindeki span'ı bul
                        if div_elements:
                            first_div_element = div_elements[0]
                            tarih_element = first_div_element.find_element(By.CSS_SELECTOR, "span[aria-label]")

                            # Eğer span[aria-label] elementi varsa, text değerini al ve yazdır
                            if tarih_element:
                                tarih = tarih_element.text
                                print("Tarih: ", tarih)
            except Exception as f:
                print("Daha fazla linki bulunamadı veya yorumlar çekilemedi:", str(f))

conn.close()   # Database bağlantısını kapatmak için

print("En yüksek puan alan ürünün adı: {0} \nEn yüksek puan alan ürünün puanı: {1} ".format(en_yuksek_oy_alan_urunun_adi,en_yuksek_oy_alan_urunun_oyu))
print("O sitedeki en çok yorumlanan ürünün adı: {0} \nO sitedeki en çok yorumlanan ürünün yorum sayısı: {1} ".format(en_cok_yorumlanan_urunun_adi,en_cok_yorumlanan_urunun_yorum_sayisi))




