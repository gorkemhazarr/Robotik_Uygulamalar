# Algoritma Açıklaması

## Sensörlerden Veri Alma Süreci

Robot üzerinde ön, sol çapraz ve sağ çapraz olmak üzere üç sanal ultrasonik
sensör bulunur. Ön sensör robotun baktığı yöne, diğer sensörler bu yöne göre
yaklaşık ±45 derece açıyla bakar. Her sensör robot gövdesinin kenarından en fazla
170 piksel uzunluğunda bir ışın gönderir. Işının dünya sınırları veya
`pygame.Rect` engellerle ilk kesiştiği nokta bulunur ve bu noktaya olan uzaklık
sensör değeri olarak alınır.

## Kontrol Algoritması

Kontrolcü ön sensör değerini 75 piksellik güvenli mesafe ve 25 piksellik kritik
mesafe ile karşılaştırır. Ön taraf güvenliyse robot ileri gider. Engel güvenli
mesafe içindeyse sol ve sağ sensör değerleri karşılaştırılır; daha geniş olan
yöne dönüş yapılır. Engel kritik mesafe içindeyse robot 0,45 saniye geri
manevra yapar.

## Motor Aktüatörlerine Komut Gönderme Süreci

Kontrolcü kararına göre robotun `left_motor_speed` ve `right_motor_speed`
değerlerini doğrudan günceller. İki hız eşitse robot doğrusal hareket eder.
Sağ motor daha hızlıysa robot sola, sol motor daha hızlıysa sağa döner.
İki motorun da negatif hız alması robotun geri gitmesini sağlar. Diferansiyel
sürüş modeli bu hızlardan doğrusal ve açısal hızı hesaplar.

## Basit Sözde Kod

```text
DÖNGÜ simülasyon açık olduğu sürece
    ön, sol ve sağ sensör mesafelerini ölç

    EĞER geri manevra süresi devam ediyorsa
        iki motoru geri çalıştır
    DEĞİLSE EĞER ön mesafe kritik mesafeden küçük veya eşitse
        kısa süreli geri manevrayı başlat
    DEĞİLSE EĞER ön mesafe güvenli mesafeden büyükse
        iki motoru eşit hızla ileri çalıştır
    DEĞİLSE EĞER sol mesafe sağ mesafeden büyükse
        sola dön
    AKSİ HALDE
        sağa dön

    robotun konumunu ve yönünü güncelle
    simülasyon ekranını çiz
SON
```
