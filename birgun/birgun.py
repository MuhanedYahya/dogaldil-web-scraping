import requests
from bs4 import BeautifulSoup

# قائمة الأرقام التي تمثل الصفحات التي تريد زيارتها2691  
page_numbers = range(293,1300)

# الجزء الثابت من عنوان الصفحة
base_url = "https://www.birgun.net/kategori/kultur-sanat-11?p="

# العثور على جميع الصفحات وطباعة محتواها
for page_number in page_numbers:
    # تكوين الرابط النهائي للصفحة باستخدام قيمة page_number
    url = base_url + str(page_number)
    
    # جلب محتوى الصفحة
    response = requests.get(url)

    # التحقق من نجاح طلب الصفحة
    if response.status_code == 200:
        # تحليل محتوى الصفحة باستخدام BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        
        # العثور على جميع الديفات التي تحمل نفس اسم الكلاس
        card_body_divs = soup.find_all("div", class_="col-6 col-lg-3")
        
        # العثور على العناوين والروابط داخل كل ديف
        for card_body_div in card_body_divs:
            # العثور على جميع العناصر h2 داخل الديف
            titles = card_body_div.find_all("h2", class_="card-title")
            
            # استخراج العناوين والروابط وطباعتها
            for title in titles:
                # العنوان
                page_title = title.text.strip()
                
                # الرابط
                page_link = title.find("a")["href"]
                
                # التحقق مما إذا كان الرابط يبدأ بـ "http" أو "https"
                if not page_link.startswith('http'):
                    # إضافة بروتوكول الى الرابط
                    page_link = 'https://www.birgun.net' + page_link

                # جلب محتوى الصفحة
                response_page = requests.get(page_link)
                soup_page = BeautifulSoup(response_page.text, "html.parser")

                # العثور على الديف الذي يحمل كلاس "ريسز"
                resz_div = soup_page.find("div", class_="resize")

                if resz_div:
                    # افتح ملف CSV للكتابة
                    with open("birgun2.csv", "a", encoding="utf-8", newline="") as csvfile:
                        # كتابة العنوان إلى الملف
                        csvfile.write(page_title + "\n")
                        
                        # طباعة مجموعة من النقاط بعد العنوان
                        #csvfile.write(dots)
                        
                        # العثور على جميع البراغرافات داخل الديف "ريسز"
                        paragraphs = resz_div.find_all("p")
                        
                        # كتابة البراغرافات الجديدة إلى الملف
                        text = ""
                        for paragraph in paragraphs:
                            text = text + paragraph.text.strip() + " "
                        text.replace("\n", " ")
                        if len(text) > 1024:
                            csvfile.write(text)
                        else:
                            print(len(text))    
                        
                        print("writing success")
                else:
                    print("div bulunamadı")
        # طباعة رقم الصفحة بعد الانتهاء من قرائتها
        print("page number: ", page_number)
    else:
        print("icerik bulunamadı")