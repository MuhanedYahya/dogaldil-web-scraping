import requests
from bs4 import BeautifulSoup

def haberleri_getir(url):
    # Web sayfasını getir
    response = requests.get(url)
    # HTML içeriğini analiz et
    soup = BeautifulSoup(response.text, 'html.parser')
    
    haberler = []
    
    # Tüm haber başlıklarını ve linklerini bul
    haber_etiketleri = soup.find_all('h2', class_='entry-title')
    for haber_etiketi in haber_etiketleri:
        haber = {}
        haber['baslik'] = haber_etiketi.text.strip()
        haber['link'] = haber_etiketi.a['href']
        
        # Her bir haberin içeriğini al
        haber_icerigi = haber_icerigini_getir(haber['link'])
        haber['icerik'] = haber_icerigi
        
        haberler.append(haber)
    
    return haberler

def haber_icerigini_getir(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Haber içeriğini bul
    icerik_div = soup.find('div', class_='entry-content')
    
    # Paragrafları topla
    paragraflar = icerik_div.find_all('p')
    
    # Paragrafları birleştirerek içerik oluştur
    icerik = "\n".join([p.text.strip() for p in paragraflar])
    
    return icerik

if __name__ == "__main__":
    url = 'https://www.dunyahalleri.com/category/kultur-sanat/'
    haberler = haberleri_getir(url)
    for haber in haberler:
        print("Başlık:", haber['baslik'])
        print("Link:", haber['link'])
        print("İçerik:", haber['icerik'])
        print("\n")
