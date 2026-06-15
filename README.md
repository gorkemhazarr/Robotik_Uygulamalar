# Ultrasonik Sensör ve Motor Aktüatörleri ile Engelden Kaçan Mobil Robot Simülasyonu

## Projenin İncelenmesi Hakkında

Bu proje, **`robotik/`** klasörü içerisinde yer almaktadır. Projeye ait tüm kaynak kodlar, dokümantasyon dosyaları, ekran görüntüleri ve simülasyon çıktıları bu klasörün içindedir.

Projeyi incelemek için öncelikle ana dizinde bulunan **`robotik/`** klasörüne girilmelidir.

```text
robotik/
├── src/
├── docs/
├── assets/
├── requirements.txt
├── README.md
└── .gitignore
```

Simülasyonu çalıştırmak, kaynak kodları incelemek, proje açıklamalarına ulaşmak ve ekran görüntüsü/video gibi çıktıları görmek için **`robotik/`** klasörü kullanılmalıdır.

Simülasyon ekran görüntüleri ve varsa video kayıtları şu klasörde yer almaktadır:

```text
robotik/assets/screenshots/
```

Projenin ayrıntılı açıklaması, algoritma yapısı ve rapor notları ise şu klasördedir:

```text
robotik/docs/
```

---

# 1. Proje Başlığı

## Ultrasonik Sensör ve Motor Aktüatörleri ile Engelden Kaçan Mobil Robot Simülasyonu

**Ders:** Robotik Uygulamalarda Sensör ve Aktüatörler

---

# 2. Proje Açıklaması

Bu projede, çevresindeki engelleri sanal ultrasonik sensörlerle algılayan ve motor hızlarını değiştirerek engellerden kaçan iki tekerlekli bir mobil robot modellenmiştir.

Simülasyon, **Python** ve **Pygame** kullanılarak iki boyutlu ortamda gerçekleştirilmiştir. Robotun sensör ölçümleri, motor hızları ve anlık hareket durumu ekrandaki bilgi panelinden izlenebilmektedir.

Proje; sensör verisinin alınması, kontrol algoritmasıyla değerlendirilmesi ve aktüatör komutuna dönüştürülmesi sürecini göstermektedir.

Projeyi incelemek için:

* Kaynak kodlar için: `robotik/src/`
* Dokümantasyon için: `robotik/docs/`
* Ekran görüntüsü ve video için: `robotik/assets/screenshots/`
* Kurulum ve çalıştırma bilgisi için: `robotik/README.md`

klasörleri incelenebilir.

---

# 3. Kullanılan Sensörler

Robot üzerinde üç sanal ultrasonik mesafe sensörü bulunmaktadır:

* **Ön sensör:** Robotun hareket yönündeki engelleri algılar.
* **Sol çapraz sensör:** Robot yönüne göre yaklaşık `-45°` açıyla ölçüm yapar.
* **Sağ çapraz sensör:** Robot yönüne göre yaklaşık `+45°` açıyla ölçüm yapar.

Sensörler en fazla `170 piksel` mesafeye ışın gönderir. Işının bir engel veya dünya sınırıyla ilk kesiştiği nokta hesaplanarak mesafe ölçümü elde edilir.

Simülasyonda:

* **Yeşil ışın:** Açık alanı,
* **Kırmızı ışın:** Algılanan engeli

göstermektedir.

---

# 4. Kullanılan Aktüatörler

Robotun hareketi, sağ ve sol tekerleği temsil eden iki sanal motor aktüatörüyle sağlanır.

Diferansiyel sürüş modeline göre:

* Motor hızları eşitse robot düz hareket eder.
* Sağ motor daha hızlıysa robot sola döner.
* Sol motor daha hızlıysa robot sağa döner.
* İki motor da negatif hız alırsa robot geri gider.

Bu yapı sayesinde robot, sensörlerden gelen mesafe bilgisine göre motor hızlarını değiştirerek engellerden kaçabilmektedir.

---

# 5. Kullanılan Teknolojiler

Projede kullanılan temel teknolojiler şunlardır:

* Python 3.10 veya üzeri
* Pygame 2.5.2 veya üzeri
* Python standart kütüphaneleri
* Nesne yönelimli programlama
* Modüler yazılım mimarisi

Projede **ROS, Gazebo, Webots** veya benzeri ağır robotik simülasyon araçları kullanılmamıştır. Amaç, sensör-kontrol-aktüatör ilişkisini sade ve anlaşılır bir simülasyon üzerinden göstermektir.

---

# 6. Kurulum

Projeyi çalıştırmak için öncelikle ana dizinde bulunan **`robotik/`** klasörüne girilmelidir.

```bash
cd robotik
```

Ardından aşağıdaki komutlar sırasıyla çalıştırılmalıdır:

```bat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
```

---

# 7. Çalıştırma

Bağımlılıklar kurulduktan sonra simülasyon, **`robotik/`** klasörü içerisindeyken şu komutla başlatılır:

```bash
python src/main.py
```

Program çalıştırıldığında Pygame penceresi açılır ve robotun engellerden kaçma davranışı simülasyon ortamında gözlemlenebilir.

---

# 8. Simülasyon Kontrolleri

| Kontrol                 | İşlev                                         |
| ----------------------- | --------------------------------------------- |
| `R`                     | Robotu başlangıç konumuna ve yönüne döndürür. |
| `ESC`                   | Simülasyonu kapatır.                          |
| Pencere kapatma düğmesi | Simülasyonu güvenli biçimde sonlandırır.      |

---

# 9. Proje Klasör Yapısı

Projenin ana dosyaları **`robotik/`** klasörü içerisinde yer almaktadır.

```text
robotik/
├── src/
│   ├── main.py
│   ├── config.py
│   ├── robot.py
│   ├── sensors.py
│   ├── actuators.py
│   ├── controller.py
│   ├── world.py
│   └── utils.py
│
├── docs/
│   ├── proje_plani.md
│   ├── algoritma_aciklamasi.md
│   └── rapor_notlari.md
│
├── assets/
│   └── screenshots/
│
├── requirements.txt
├── README.md
└── .gitignore
```

Dosyaların görevleri kısaca şöyledir:

| Dosya/Klasör          | Açıklama                                           |
| --------------------- | -------------------------------------------------- |
| `src/main.py`         | Pygame başlangıcı, ana döngü ve olay yönetimi      |
| `src/config.py`       | Ekran, renk, hız ve eşik değerleri                 |
| `src/robot.py`        | Robotun konumu, hareketi ve çizimi                 |
| `src/sensors.py`      | Sanal ultrasonik sensör ölçümleri                  |
| `src/actuators.py`    | Sağ-sol motor aktüatörleri                         |
| `src/controller.py`   | Engelden ve duvardan kaçma algoritması             |
| `src/world.py`        | Simülasyon alanı, engeller ve sınırlar             |
| `src/utils.py`        | Bilgi paneli ve yardımcı arayüz bileşenleri        |
| `docs/`               | Proje planı, algoritma açıklaması ve rapor notları |
| `assets/screenshots/` | Simülasyon ekran görüntüleri ve video çıktıları    |

---

# 10. Kontrol Algoritması

Kontrol algoritması basit eşik ve karşılaştırma kurallarına dayanır.

Temel çalışma mantığı şöyledir:

1. Ön sensör mesafesi `75 piksel` değerinden büyükse robot ileri gider.
2. Ön tarafta engel varsa sol ve sağ sensör mesafeleri karşılaştırılır.
3. Sol taraf daha açıksa robot sola döner.
4. Sağ taraf daha açıksa robot sağa döner.
5. Ön mesafe `25 piksel` veya daha azsa robot `0,45 saniye` geri manevra yapar.
6. Robot duvarlara veya köşelere yaklaşırsa aktif simülasyon alanının içine doğru yönelir.
7. Her döngüde sırasıyla sensör ölçümü, kontrol kararı ve robot hareketi gerçekleştirilir.

Basitleştirilmiş algoritma:

```text
DÖNGÜ simülasyon açık olduğu sürece

    sensör mesafelerini ölç

    EĞER robot duvara çok yakınsa
        duvardan uzaklaş

    DEĞİLSE EĞER ön engel kritik mesafedeyse
        geri manevra yap

    DEĞİLSE EĞER ön engel güvenli mesafe içindeyse
        sol ve sağ boşluğu karşılaştır
        daha açık tarafa dön

    DEĞİLSE
        ileri git

    robotun konumunu güncelle
    ekranı çiz

SON
```

Bu yaklaşım PID, haritalama, yapay zeka veya rota planlama içermez. Amaç, sensör-kontrol-aktüatör ilişkisini açık ve anlaşılır biçimde göstermektir.

---

# 11. Ders Bağlamında Değerlendirme

Bu proje, **Robotik Uygulamalarda Sensör ve Aktüatörler** dersi kapsamında sensörlerin çevreden bilgi toplama, kontrol sisteminin karar üretme ve aktüatörlerin bu kararı harekete dönüştürme görevlerini birlikte göstermektedir.

Sanal ultrasonik sensörler engel mesafelerini ölçmekte, kontrolcü bu ölçümleri güvenli ve kritik mesafe eşikleriyle değerlendirmekte, sağ-sol motor aktüatörleri ise robotun ileri, geri ve dönüş hareketlerini oluşturmaktadır.

Simülasyon bu temel robotik zinciri düşük maliyetli, gözlemlenebilir ve tekrarlanabilir bir eğitim ortamında sunmaktadır.

---

# 12. Proje Çıktıları

Projeye ait ekran görüntüsü ve video çıktıları aşağıdaki klasörde bulunmaktadır:

```text
robotik/assets/screenshots/
```

Bu klasörde simülasyonun çalışma anına ait görseller ve varsa video kayıtları incelenebilir. Bu çıktılar, robotun sensörlerle engelleri algıladığını ve motor hızlarını değiştirerek engellerden kaçtığını göstermektedir.
