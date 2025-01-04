Proje Hakkında

Bu proje, Binance API kullanarak (2 yıllık 15 dakikalık periyotta) kapanış verilerini analiz eder. Amaç, 0.85'in üzerinde korelasyona sahip coin çiftlerini ve son 30 gün boyunca korelasyonlarının 0'ın altına düşen çiftleri tespit etmektir. Aralarındaki getiri farkı %30 veya üzerinde olan çiftler ayrıca analiz edilir.

Bu analiz, kullanıcıların korele coin çiftleri arasındaki arbitraj farkından faydalanarak biri long, diğeri short pozisyon açmasıyla avantaj sağlamasına yardımcı olabilir.

Özellikler

Binance API kullanılarak tarihsel kapanış fiyatlarının analizi.

Yüksek korelasyona ve büyük getiri farkına sahip coin çiftlerinin tespiti.

Arbitraj potansiyeli taşıyan çiftlerin otomatik filtrelenmesi.

Analiz sonuçlarının Excel'e aktarılması.

Korelasyonların ısı haritası ile görsel olarak sunumu.

Kurulum

Bu depoyu klonlayın:

git clone <depo_adresi>

Proje dizinine geçiş yapın:

cd <proje_dizini>

Bağımlılıkları yükleyin:

pip install -r requirements.txt

Gereksinimler

Proje aşağıdaki Python kütüphanelerine bağlıdır:

 pandas==2.0.3
 numpy==1.25.2
 matplotlib==3.5.1
 seaborn==0.11.2
 requests==2.26.0

Binance API Yapılandırması

Binance hesabınızdan API anahtarı ve şifresini alın.

main.py dosyasındaki aşağıdaki değişkenleri kendi bilgilerinizle değiştirin:

API_KEY = "api_anahtarınız"
API_SECRET = "api_sifreniz"

Alternatif olarak, bilgilerinizi bir .env dosyasında saklayabilirsiniz.

Kullanım

Analizi başlatmak için ana dosyayı çalıştırın:

python main.py

Önemli Notlar

Binance API ağırlık sınırlarına uyulması gerekmektedir.

API anahtarı ve şifrenizin gizli kalmasını sağlayın.

Binance'den alınan verilerin doğruluğu ve yorumlanması kullanıcının sorumluluğundadır.

Bu yazılımı kullanarak oluşan kazanç veya kayıplar tamamen kullanıcıya aittir.

Katkı Sağlama

Katkılarınızı bekliyoruz! Katkıda bulunmak için:

Bu depoyu fork edin.

Yeni bir branch oluşturun:

git checkout -b ozellik-adi

Değişikliklerinizi commit edin:

git commit -m "Özellik/Düzeltme açıklaması"

Fork'unuza push edin ve bir pull request oluşturun.

