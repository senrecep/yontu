Listeyi ters çevirmenin iki yaygın yolu var. Listenin kendisini değiştirmek istiyorsan `liste.reverse()` kullan, yeni bir liste istiyorsan `liste[::-1]` yaz.

İkisi arasındaki fark şu: `reverse()` yeni bir liste döndürmez, yerinde değiştirir ve `None` döner. Bu yüzden `yeni = liste.reverse()` yazarsan `yeni` boş kalır. Bu hatayı sık görüyorum.

Liste çok büyükse ve yalnızca tersten dolaşman gerekiyorsa `reversed(liste)` daha az bellek kullanır, çünkü kopya oluşturmaz.
