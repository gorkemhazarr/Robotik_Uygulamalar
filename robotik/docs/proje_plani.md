# Proje Planı

## Proje Adı

**Ultrasonik Sensör ve Motor Aktüatörleri ile Engelden Kaçan Mobil Robot
Simülasyonu**

## Projenin Amacı

Bu projenin amacı, çevresindeki engelleri sanal ultrasonik sensörlerle algılayan
ve sağ-sol motor hızlarını değiştirerek engellerden kaçan iki tekerlekli bir
mobil robotu iki boyutlu ortamda modellemektir. Böylece sensör verisinin kontrol
kararına ve aktüatör komutuna dönüşme süreci görsel olarak incelenmektedir.

## Projenin Kapsamı

Proje; dikdörtgen engellerin bulunduğu bir simülasyon dünyasını, dairesel mobil
robotu, ön-sol-sağ mesafe sensörlerini, diferansiyel sürüş modelini ve basit
engelden kaçma algoritmasını kapsar. Bilgi panelinde sensör ölçümleri, motor
hızları ve robotun anlık durumu gösterilir. Haritalama, rota planlama, PID,
yapay zeka ve gerçek donanım haberleşmesi kapsam dışındadır.

## Kullanılan Teknolojiler

- Python 3.10 ve üzeri
- Pygame
- Python standart kütüphaneleri
- Modüler ve nesne yönelimli programlama yaklaşımı

## Simülasyon Yaklaşımı

Simülasyon 900x600 piksel boyutunda iki boyutlu bir Pygame penceresinde
çalışmaktadır. Engeller `pygame.Rect`, robot ise daire olarak temsil edilir.
Robotun üç sensörü kendi yön açısına bağlı ışınlar göndererek en yakın engelle
olan kesişim mesafesini hesaplar. Kontrolcü bu değerleri eşiklerle karşılaştırır
ve diferansiyel sürüş için sağ ve sol motor hızlarını belirler. Konum ve yön,
geçen kare süresine (`dt`) göre her döngüde güncellenir.
