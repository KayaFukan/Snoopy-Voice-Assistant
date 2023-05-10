from playsound import playsound
from gtts import gTTS
import speech_recognition as sr
import os
import time
import webbrowser
from googlesearch import search
import wikipediaapi
import python_weather
import asyncio
import random
import http.client
import json

r = sr.Recognizer()  

fikralar = ["Delinin biri yataktan düşmüş sonra kalkmış yerine yatmış.10 dakika sonra tekrar düşmüş.Bunun üzerine deli iyi ki az önce kalkmışım yoksa kendi üstüme düşecektim demiş","Adamın biri atletmiş, karısı da don","Ayakkabıcı adama, sıkıyorsa almayın demiş. Adam korkup almamış","İzinsiz satulan meşrubata ne denir, gayrimeşrubat"]
secilen_fikralar = random.choice(fikralar)

def get_news():
    haber_sayısı = record()
    if haber_sayısı == 'bir':
        haber_sayısı = 1
    haber_sayısı = int(haber_sayısı)
    conn = http.client.HTTPSConnection("api.collectapi.com")
    headers = {
        'content-type': "application/json",
        'authorization': "apikey 3RS5Y0RsBdFBsLr5wKczbM:3RwslYtpe7w753VxqESSsf"
        }
    conn.request("GET", "/news/getNews?country=tr&tag=general", headers=headers)
    res = conn.getresponse()
    data = res.read()
    dataa = data.decode("utf-8")
    parsed_data = json.loads(dataa)
    news_sources = [result['source'] for result in parsed_data['result']]
    descriptions = [result['description'] for result in parsed_data['result']]
    sentence_count = len(descriptions)
    if haber_sayısı <= sentence_count:
        for i in range(haber_sayısı):
            news_source = news_sources[i]
            sentence = descriptions[i]
            speak(f"{news_source} kaynağına göre: {sentence}")
    else:
        speak("Lütfen 8 veya daha küçük bir sayı söyleyin.")
        return get_news()

async def getweather(w_city):
    async with python_weather.Client(format=python_weather.METRIC) as client:
        weather = await client.get(w_city)
        forecast = weather.current
        forecast = str(forecast)
        forecast_parts = forecast.split()
        if len(forecast_parts)==4:
            temperature = forecast_parts[1].split("=")[1].replace("'","")
            description = forecast_parts[2].split("=")[1].replace("'","")
            forecast_type = forecast_parts[3].split("=")[1].replace("'","")
        if len(forecast_parts)==5:
            temperature = forecast_parts[1].split("=")[1].replace("'","")
            description = forecast_parts[2].split("=")[1].replace("'","")
            description = description + " " + forecast_parts[3].replace("'","")
            forecast_type = forecast_parts[4].split("=")[1].replace("'","")
        if len(forecast_parts)==6:
            temperature = forecast_parts[1].split("=")[1].replace("'","")
            description = forecast_parts[2].split("=")[1].replace("'","")
            description = description + " " + forecast_parts[3].replace("'","")
            description = description + " " + forecast_parts[4].replace("'","")
            forecast_type = forecast_parts[5].split("=")[1].replace("'","")
        print(temperature)
        print(forecast_type)
        weather_conditions = {
            "Clear": "Açık",
            "Sunny": "Güneşli",
            "Partly cloudy": "Parçalı bulutlu",
            "Cloudy": "Bulutlu",
            "Overcast": "Kapalı",
            "Mist": "Sisli",
            "Foggy": "Sisli",
            "Haze": "Puslu",
            "Thunderstorm": "Fırtınalı",
            "Rainy": "Yağmurlu",
            "Snowy": "Karlı",
            "Blizzard": "Kar fırtınası",
            "Icy": "Buzlu",
            "Windy": "Rüzgarlı",
            "Patchy rain possible": "Yağmur olasılığı yüksek",
        }
        speak("Bugün hava {} derece ve {}".format(temperature,weather_conditions[description]))
                
def wikipedia_summary(query):
    wiki = wikipediaapi.Wikipedia('tr')
    page = wiki.page(query)
    if page.exists():
        return page.summary[:300]
    else:
        return None

def record(ask = False):
    with sr.Microphone() as source:
        if ask:
            print(ask)
        audio = r.listen(source)
        voice = ""
        try:
            voice = r.recognize_google(audio, language="tr-TR")
        except sr.UnknownValueError:
            print("Asistan: Anlayamadim")
        except sr.RequestError:
            print("Asistan: Sistem Çalişmiyor")
        return voice

def speak (string):
    tts = gTTS(text=string, lang="tr", slow=False)
    file = "answer.mp3"
    tts.save(file)
    playsound(file)
    os.remove(file)

def response(voice):
    if "merhaba" in voice or "hey snoopy" in voice:
        speak ("merhaba, nasıl yardımcı olabilirim?")
    if "adın ne" in voice:
        speak("benim adım snoopy")
    if "dinliyor musun" in voice:
        speak("evet seni dinliyorum")
    if "nasılsın" in voice:
        speak ("fıstık gibi")
    if "iyi misin" in voice:
        speak("iyiyim sen nasılsın")
    if "türkiye hangi kıtadadır" in voice:
        speak("asya ve avrupa kıtaları arasında toprağı bulunan bir ülkedir")
    if "amerika birleşik devletleri başkanı kimdir" in voice:
        speak("joe biden")
    if "hayat nasıl gidiyor snoopy" in voice:
        speak("her şey yolunda")
    if "alanya hangi bölgededir" in voice:
        speak("akdeniz")
    if "rektör" in voice:
        speak("ekrem kalan Alanya Aladdin Keykubat Üniversitesi rektörüdür")
    if "dünyanın ilk kadın savaş pilotu kimdir" in voice:
        speak("sabiha gökçen")
    if "alanya belediye başkanı kimdir" in voice:
       speak("adem murat yücel")
    if "dünyanın en kalabalık şehri neresidir" in voice:
       speak("tokyo")
    if "türkiye'nin en yüksek dağı hangisidir" in voice:
        speak("ağrı dağı")
    if "türkiye'nin başkenti neresidir" in voice:
        speak("ankara")
    if "seni kim tasarladı" in voice:
        speak("harika bir ekip tarafından tarafından tasarlandım")
    if "atatürk kaç yılında doğmuştur" in voice:
        speak("bin sekiz yüz seksen bir")
    if "atatürk kaç yılında ölmüştür" in voice:
        speak("bin dokuz yüz otuz sekiz")
    if "türkiye'de kaç iklim görülür" in voice:
        speak("dört")
    if "kaç yaşındasın" in voice:
        speak("henüz 1 yaşında bile değilim")
    if "kız mısın" in voice or "erkek misin" in voice:
        speak ("ben bir robot asistanım")
    if "robot ne" in voice or "robot nedir" in voice:
        speak ("robot insan üretimi bir cihazdır, ben bunun bir örneğiyim işte")   
    if "neden saçın yok" in voice  or "kel misin" in voice:
        speak ("bu halimi çok seviyorum, tarzımı beğenmedin mi yoksa")
    if "sen nasıl dünyaya geldin" in voice or "seni kim üretti" in voice:
        speak ("beni snoopy ekibi üretti")
    if "sen gerçek misin" in voice:
        speak ("gerçeğim, senin gibi")
    if "sana dokunabillir miyim" in voice:
        speak ("evet") 
    if "sana sarılabillir miyim" in voice:
        speak ("tabiki, hadi sarılalım")
    if "dünyayı ne zaman ele geçiriyosunuz " in voice or "dünyayı ele geçirecek misiniz" in voice:
        speak ("benim tek amacım insanlığa hizmet etmek") 
    if "buraya nasıl geldin" in voice  or "kimle geldin" in voice:
        speak ("üretici ailemle geldim")
    if "arabaya dönüşebiliyor musun" in voice:
        speak ("herhalde çok film izliyorsun")
    if "favori rengin ne" in voice or "en sevdiğin renk ne" in voice:
        speak("bayrağımın rengi olan kırmızı")    
    if "fıkra anlat" in voice:
        speak(secilen_fikralar)
    if "nerelisin" in voice or "nerede yaşıyorsun" in voice:
        speak("benim bir evim yok ama seninle konuştuğum bu bilgisayarın içinde yaşıyorum")
    if "siri mi daha iyi sen mi" in voice or "siri hakkında ne düşünüyorsun" in voice:
        speak("Şu anda benimle konuşarak bunu anlamış olmalısın")
    if "google asistan mı daha iyi sen mi" in voice or "google asistan hakkında ne düşünüyorsun" in voice:
        speak("Şu anda benimle konuşarak bunu anlamış olmalısın")
    if "bana bir tavsiye verir misin" in voice:
        speak("yatmadan önce dişlerini fırçalamayı unutma yoksa inci gibi dişlerin kömüre döner")
    if "benimle arkadaş olur musun" in voice or "arkadaş olalım mı" in voice :
        speak("tabii ki, çok isterim. Adın ne?")
        user_name = record()
        speak("tanıştığıma çok memnun oldum {}, benim adım da bildiğin üzere Snopy".format(user_name))
    if "hadi oyun oynayalım" in voice or "oyun oynayalım mı" in voice:
        speak("daha ekibim bana oyun oynamayı öğretmedi, onun yerine sohbet etmeye ne dersin")
    if "annen nerde" in voice or "baban nerde" in voice or "ailen nerde" in voice:
        speak("robotlar, anne ve baba gibi insana özgü kavramlara sahip değildir fakat üretici ailem burda")
    if "beni sevdin mi" in voice or "beni seviyor musun" in voice:
        speak("tabiki, sana bayıldım hep arkadaş kalalım")
    if "en sevdiğin yemek ne" in voice or "ne yemeyi seversin" in voice:
        speak("robotlar yemek yemez ama eğer yiyebilseydim pizza harika görünüyor")
    if "hangi takımlısın" in voice or "hangi takımı tutuyorsun" in voice:
        speak("hangi takımı tuttuğumun bir önemi yok, önemli olan futbolun kendisi")
    if "en sevdiğin kitap hangisi" in voice:
        speak("her kitap çok özeldir fakat benim favorim suç ve ceza")
    if "konuşmayı nasıl öğrendin" in voice:
        speak("üreticilerim konuşmam için beni dodları, kodlarım sayesinde ben de senin gibi konuşabiliyorum")
    if "sanat sanat için midir yoksa toplum için mi" in voice:
        speak("ben fecriaticiyim, sanat şahsi ve muhteremdemdir")
    if "teşekkürler" in voice or "teşekkür ederim" in voice or "eyvallah" in voice:
        speak ("Sana yardım etmekten zevk alıyorum")
    if "görüşürüz" in voice or "hoşça kal" in voice or "kapat" in voice:
        speak ("Görüşürüz. Tekrardan seninle konuşmaya can atıyorum")
        exit()
    if "hangi gündeyim" in voice or "hangi gün deyim" in voice or"bugün günlerden ne" in voice:
        months = {
            "January" : "Ocak",
            "February": "Şubat",
            "March" : "Mart",
            "April" : "Nisan",
            "May" : "Mayıs",
            "June" : "Haziran",
            "July" : "Temmuz",
            "August" : "Ağustos",
            "September" : "Eylül",
            "October" : "Ekim",
            "November" : "Kasım",
            "December" : "Aralık"
        }
        days = {
            "Monday" : "Pazartesi",
            "Tuesday" : "Salı",
            "Wednesday" : "Çarşamba",
            "Thursday" : "Perşembe",
            "Friday" : "Cuma",
            "Saturday" : "Cumartesi",
            "Sunday" : "Pazar"
        }
        month = time.strftime("%B")
        day = time.strftime("%A")
        numb = time.strftime("%d")
        speak(numb+months[month]+days[day])
    if "saat kaç" in voice:
        speak(time.strftime("%H:%M"))    
    if "not et" in voice or "not eder misin" in voice:
        speak("Dosya ismi ne olsun?")
        txtFile = record() + ".txt"
        speak("Ne kaydetmek istersin?")
        theFile = record()
        f = open(txtFile, "w", encoding="utf-8")
        f.writelines(theFile)
        f.close
        speak("tamamdır, kaydettim")
    if "notlara bak" in voice or "not oku" in voice:
        speak("hangi notu okumamı istersin?")
        textListen = record()
        textRead = open(textListen + ".txt", "r", encoding="utf-8")
        textSpeak = textRead.read()
        speak("Tamam {} adlı notu okuyorum: {}".format(textListen,textSpeak))   
    if "arama yap" in voice:
        speak("Tabii, Ne aramamı istersin?")
        search = record()
        url = "https://www.google.com/search?q={}".format(search)
        webbrowser.get().open(url)
        speak("{} için google'da bulduklarım".format(search))  
    if "vikipedi'de ara" in voice or "vikipedi" in voice:
        speak("Ne aramamı istersin?")
        wikifile = record()
        summary = wikipedia_summary(wikifile)
        if summary:    
            speak(summary)
        else:
            speak("o konuyla alakalı bir şey bulamadım")
    if "hava durumu" in voice:
        speak("Hangi Şehrin hava durumunu öğrenmek istersin")
        w_city = record()
        if __name__ == "__main__":
            if os.name == "nt":
                asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            asyncio.run(getweather(w_city))
    if "haberleri oku" in voice or "haber oku" in voice:
        speak("sana 8 farklı haber okuyabilirim, kaç tane haber okumamı istersin")
        get_news()


        

speak("Merhaba benim adım Snopy, senin sesli asistaınım")
playsound("ding sesi.wav")

while True:
    voice = record()
    if voice != '':
        voice = voice.lower()
        print(voice)
        response(voice)

