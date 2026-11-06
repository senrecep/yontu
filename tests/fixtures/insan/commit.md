fix(fatura): KDV oranı sıfır olan kalemlerde toplam yanlış hesaplanıyordu

Sıfır oranlı kalemler toplamdan önce filtreleniyordu. Filtre kaldırıldı, oran sıfırsa vergi tutarı doğrudan sıfır yazılıyor.

Closes #412
