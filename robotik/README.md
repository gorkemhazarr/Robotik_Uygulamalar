# 1. Proje Başlığı

## Ultrasonik Sensör ve Motor Aktüatörleri ile Engelden Kaçan Mobil Robot Simülasyonu

**Ders:** Robotik Uygulamalarda Sensör ve Aktüatörler

# 2. Proje Açıklaması

Bu projede, çevresindeki engelleri sanal ultrasonik sensörlerle algılayan ve
motor hızlarını değiştirerek engellerden kaçan iki tekerlekli bir mobil robot
modellenmiştir. Simülasyon, Python ve Pygame kullanılarak iki boyutlu ortamda
gerçekleştirilmiştir.

Robotun sensör ölçümleri, motor hızları ve anlık hareket durumu ekrandaki bilgi
panelinden izlenebilir. Proje; sensör verisinin alınması, kontrol algoritmasıyla
değerlendirilmesi ve aktüatör komutuna dönüştürülmesi sürecini göstermektedir.

Projede kullanılacak simülasyon ekran görüntüleri ve videosu
`assets/screenshots/` klasöründedir.

# 3. Kullanılan Sensörler

Robot üzerinde üç sanal ultrasonik mesafe sensörü bulunmaktadır:

- **Ön sensör:** Robotun hareket yönündeki engelleri algılar.
- **Sol çapraz sensör:** Robot yönüne göre yaklaşık `-45°` açıyla ölçüm yapar.
- **Sağ çapraz sensör:** Robot yönüne göre yaklaşık `+45°` açıyla ölçüm yapar.

Sensörler en fazla `170 piksel` mesafeye ışın gönderir. Işının bir engel veya
dünya sınırıyla ilk kesiştiği nokta hesaplanarak mesafe ölçümü elde edilir.
Yeşil ışın açık alanı, kırmızı ışın ise algılanan engeli gösterir.

# 4. Kullanılan Aktüatörler

Robotun hareketi, sağ ve sol tekerleği temsil eden iki sanal motor aktüatörüyle
sağlanır. Diferansiyel sürüş modeline göre:

- Motor hızları eşitse robot düz hareket eder.
- Sağ motor daha hızlıysa robot sola döner.
- Sol motor daha hızlıysa robot sağa döner.
- İki motor da negatif hız alırsa robot geri gider.

# 5. Kullanılan Teknolojiler

- Python 3.10 veya üzeri
- Pygame 2.5.2 veya üzeri
- Python standart kütüphaneleri
- Nesne yönelimli ve modüler programlama

ROS, Gazebo, Webots veya benzeri ağır robotik simülasyon araçları
kullanılmamıştır.

# 6. Kurulum

Proje klasöründe bir terminal açın ve aşağıdaki komutları sırasıyla çalıştırın:

```bat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
```

# 7. Çalıştırma

Bağımlılıklar kurulduktan sonra simülasyon, proje kök dizininde şu komutla
başlatılır:

```bash
python src/main.py
```

# 8. Simülasyon Kontrolleri

| Kontrol | İşlev |
| --- | --- |
| `R` | Robotu başlangıç konumuna ve yönüne döndürür. |
| `ESC` | Simülasyonu kapatır. |
| Pencere kapatma düğmesi | Simülasyonu güvenli biçimde sonlandırır. |

# 9. Proje Klasör Yapısı

```text
robotik_sensor_aktor_projesi/
├── src/
│   ├── main.py
│   ├── config.py
│   ├── robot.py
│   ├── sensors.py
│   ├── actuators.py
│   ├── controller.py
│   ├── world.py
│   └── utils.py
├── docs/
│   ├── proje_plani.md
│   ├── algoritma_aciklamasi.md
│   └── rapor_notlari.md
├── assets/
│   └── screenshots/
├── requirements.txt
├── README.md
└── .gitignore
```

# 10. Kontrol Algoritması

Kontrol algoritması basit eşik ve karşılaştırma kurallarına dayanır:

1. Ön sensör mesafesi `75 piksel` değerinden büyükse robot ileri gider.
2. Ön tarafta engel varsa sol ve sağ sensör mesafeleri karşılaştırılır.
3. Sol taraf daha açıksa robot sola, sağ taraf daha açıksa sağa döner.
4. Ön mesafe `25 piksel` veya daha azsa robot `0,45 saniye` geri manevra yapar.
5. Her döngüde sensör ölçümü, kontrol kararı ve robot hareketi sırasıyla
   gerçekleştirilir.

Bu yaklaşım PID, haritalama, yapay zeka veya rota planlama içermez. Amaç,
sensör-kontrol-aktüatör ilişkisini açık ve anlaşılır biçimde göstermektir.

# 11. Ders Bağlamında Değerlendirme

Bu proje, **Robotik Uygulamalarda Sensör ve Aktüatörler** dersi kapsamında
sensörlerin çevreden bilgi toplama, kontrol sisteminin karar üretme ve
aktüatörlerin bu kararı harekete dönüştürme görevlerini birlikte göstermektedir.

Sanal ultrasonik sensörler engel mesafelerini ölçmekte, kontrolcü bu ölçümleri
güvenli ve kritik mesafe eşikleriyle değerlendirmekte, sağ-sol motor
aktüatörleri ise robotun ileri, geri ve dönüş hareketlerini oluşturmaktadır.
Simülasyon bu temel robotik zinciri düşük maliyetli, gözlemlenebilir ve
tekrarlanabilir bir eğitim ortamında sunmaktadır.
