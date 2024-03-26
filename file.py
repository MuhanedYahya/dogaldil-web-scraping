import requests
from bs4 import BeautifulSoup
import csv

def haberleri_getir(url, num_pages=None):
    haberler = []
    page_count = 0
    
    while url and (not num_pages or page_count < num_pages):
        # Web sayfasını getir
        response = requests.get(url)
        # HTML içeriğini analiz et
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tüm haber başlıklarını ve linklerini bul
        haber_etiketleri = soup.find_all('h2', class_='entry-title')
        for haber_etiketi in haber_etiketleri:
            haber = {}
            haber['link'] = haber_etiketi.a['href']
            
            # Her bir haberin içeriğini al
            haber_icerigi = haber_icerigini_getir(haber['link'])
            haberler.append(haber_icerigi)
        
        page_count += 1
        print("Sayfa Sayısı:", page_count)
        
        # Next page link
        next_page_link = soup.find('div', class_='herald-next')
        if next_page_link and next_page_link.a:
            url = next_page_link.a['href']
        else:
            url = None
    
    return haberler

def haber_icerigini_getir(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Haber içeriğini bul
    icerik_div = soup.find('div', class_='entry-content')
    
    # Paragrafları topla ve birleştirerek içerik oluştur
    paragraflar = icerik_div.find_all('p')[2:]
    icerik = " ".join([p.text.strip() for p in paragraflar])
    
    return icerik

if __name__ == "__main__":
    url = 'https://www.dunyahalleri.com/category/kultur-sanat/'
    num_pages = 5  # Specify the number of pages here
    haberler = haberleri_getir(url, num_pages)
    
    with open('haberler.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for haber in haberler:
            writer.writerow([haber])
