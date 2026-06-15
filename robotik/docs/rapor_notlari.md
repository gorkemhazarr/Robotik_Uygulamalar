# Rapor Notları

## Sensör Kavramı

Sensör, fiziksel ortamda veya bir simülasyonda bulunan değişkenleri algılayarak
kontrol sisteminin kullanabileceği veriye dönüştüren elemandır. Mobil
robotlarda mesafe sensörleri; engel algılama, güvenli hareket ve çevre hakkında
bilgi edinme amacıyla kullanılır.

## Aktüatör Kavramı

Aktüatör, kontrol sisteminden aldığı komutu fiziksel harekete dönüştüren
bileşendir. Elektrik motorları robotik sistemlerde en yaygın kullanılan
aktüatörlerdendir. Simülasyonda aktüatörler gerçek motor yerine sayısal hız
değerleriyle modellenmektedir.

## Projede Kullanılan Sanal Ultrasonik Sensörler

Projede robotun önünde, sol çaprazında ve sağ çaprazında üç sanal ultrasonik
sensör bulunmaktadır. Bu sensörler gerçek ultrasonik sensörlerin uçuş süresi
ölçümünü doğrudan modellemek yerine ışın-engel kesişimi yöntemini kullanır.
Ölçülen mesafeler ekrandaki renkli sensör çizgileri ve bilgi paneli üzerinden
izlenebilir.

## Projede Kullanılan Sağ-Sol Motor Aktüatörleri

Robot iki tekerlekli diferansiyel sürüş mantığıyla hareket eder. Sağ ve sol
motorlara eşit hız verildiğinde robot ileri veya geri gider. Motor hızları
arasında fark oluşturulduğunda robot daha yavaş çalışan tekerlek yönüne döner.
Zıt işaretli motor hızları, robotun bulunduğu noktaya yakın şekilde dönmesini
sağlar.

## Simülasyon Sonucunda Beklenen Davranış

Robotun önünde yeterli boşluk olduğunda ileri hareket etmesi, engel
algılandığında sol ve sağ sensörleri karşılaştırarak daha açık yöne dönmesi
beklenir. Çok yakın bir engel durumunda robot kısa süre geri giderek dönüş için
alan oluşturmalıdır. Robot ekran sınırları dışına çıkmamalı ve kararları bilgi
panelinden takip edilebilmelidir.

## Sonuç Değerlendirmesi

Geliştirilen simülasyon, sensör-algılama, kontrol-karar ve aktüatör-hareket
zincirini basit ve gözlemlenebilir bir yapıda göstermektedir. Sistem karmaşık
rota planlaması kullanmadan yerel sensör verileriyle engellerden kaçabilmektedir.
Bu yönüyle proje, robotik sensörler ve motor aktüatörleri arasındaki temel
ilişkiyi açıklamak için uygun bir eğitim uygulamasıdır.
