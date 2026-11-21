# Batch 18 — 10 master manual, tanpa APK

Melanjutkan redraw-only. Tidak menjalankan Gradle, workflow dispatch, integrasi Android atau rilis APK. Semua build APK tetap dijeda (`if: false`); katalog aplikasi tetap 105 variasi.

## Sumber dan konstruksi

Sembilan sumber **berisi 18/01–09** dan satu **rasio_1 14/05**. ID rasio terpisah `exp-rasio-014-05` agar tidak bertabrakan dengan keluarga berisi. Nama file, Drive ID, hash SHA-256 dan lokasi SVG/JSON dicatat dalam `progress.json`.

| Sumber | Struktur spesifik yang dipertahankan |
|---|---|
| berisi 18/01 | Diamond merah, empat ujung navy terpisah, MCM navy sempit ber-outline putih positif |
| berisi 18/02 | Atap merah, alas navy terpisah, dua M navy lebar/rendah, C merah berujung bawah runcing |
| berisi 18/03 | Rail merah atas dan navy bawah berujung tipis, M navy, C merah chamfer |
| berisi 18/04 | Bingkai tersegmentasi: sudut atas merah, sidebar dan sudut bawah navy, M navy/C merah |
| berisi 18/05 | Atap bersegmen dengan puncak merah, tiga panel navy tiap sisi; M navy/C merah di atas baseline navy |
| berisi 18/06 | Rail merah dengan potongan diagonal terpisah di ujung kanan atas/kiri bawah, M navy/C merah |
| berisi 18/07 | Rail merah luar terpisah, ring hex navy, M navy/C merah |
| berisi 18/08 | Ring merah luar dan bidang navy, M putih positif dan C merah |
| berisi 18/09 | Bracket kiri merah/kanan navy, M navy dan C merah |
| rasio_1 14/05 | Ring navy, bidang merah, MCM putih positif bersudut |

Setiap referensi asli dan render dibuka/dibandingkan visual. Draft 18/02 dikoreksi alasnya menjadi navy sesuai sumber, bukan merah; tes khusus mengunci perbaikan warna itu. Outline putih 18/01 adalah layer putih di bawah huruf navy, bukan bitmap/stroke. C membulat diukur manual sebagai segmen chamfer pendek. Kurva dasar atap bersegmen 18/05 diregularisasi menjadi chord pendek. Celah antara ring dan bidang dalam tetap transparan. Huruf putih merupakan layer warna positif yang bisa di-recolor.

Koordinat ditulis manual per sumber, bukan auto-trace, segmentasi raster, font atau penggantian desain generik. Tekstur diratakan merah/navy/putih solid; sudut/proporsi dirapikan geometris. Tidak diklaim pixel-perfect atau produksi final. Hasil masih menunggu review visual pengguna.

## Progres dan audit terbatas

- **+10 master baru**, kumulatif **149 master Drive unik**.
- Sepuluh hash sumber baru berbeda satu sama lain dan dari sumber master sebelumnya. Motif mirip tidak otomatis digabung; tidak ada alias baru pada batch ini.
- Alias terverifikasi tetap **18**, diwariskan tanpa perubahan dari batch 17.
- Total sumber tercakup **167/342 = 48,83%**; sisa **175**.
- Redraw unik saja dibagi jumlah file **149/342 = 43,57%**.
- 342 tetap jumlah file yang sebelumnya dilaporkan, bukan jumlah desain unik yang telah diaudit global. Audit hanya PNG yang sudah diunduh. Snapshot lama tidak diubah.

## Artefak dan validasi

`perbandingan.html` mandiri/offline menyandingkan raster sumber pembanding dan SVG master dengan toggle latar putih/abu-abu. Tersedia 10 SVG path-only tanpa bitmap/font, 10 JSON koordinat native, 10 PNG preview, progress/provenance.

**90 tes lokal lulus:** 81 batch-path + 8 geometris + 1 variasi. Memeriksa SVG/JSON identik, kontur tertutup, batas kanvas, persilangan proper polygon, ID/geometri/hash sumber berbeda dari batch lain, warna alas 18/02 dan layer putih positif, progres, alias tidak berubah, katalog tetap, serta job APK dijeda. Tidak mengklaim tes perangkat Android untuk batch desain ini.

Reproduksi dengan sumber lokal dan resvg:
```sh
python scripts/build_drive_batch_18.py
python -m unittest discover -s tests -p 'test_path_batches.py'
python -m unittest discover -s tests -p 'test*geometric*.py'
python -m unittest discover -s tests -p 'test_variation_vectors.py'
```
