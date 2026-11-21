# Batch 17 — 10 master vektor manual, tanpa APK

Redraw-only berlanjut. Tidak menjalankan Gradle, dispatch workflow, integrasi Android atau rilis APK. Guard build tetap `if: false`; katalog aplikasi tetap 105 variasi.

## Sumber baru dan struktur

Sembilan sumber **berisi 17/01–09** ditambah **rasio_1 14/04**, memakai ID terpisah `exp-rasio-014-04`. Nama sumber, Drive ID, SHA-256 dan lokasi master tersimpan di `progress.json`.

| Sumber | Struktur yang dipertahankan |
|---|---|
| berisi 17/01 | Diamond merah, empat ujung navy terpisah, MCM navy dengan outline putih positif |
| berisi 17/02 | Rail merah atas/bawah berujung tipis, M navy, C merah membulat/chamfer |
| berisi 17/03 | MCM navy miring kanan, strip merah horizontal atas/bawah tidak simetris |
| berisi 17/04 | Atap dan dua tiang navy panjang, M merah berlekuk sempit serta C merah |
| berisi 17/05 | Dua bracket merah terpisah mengapit MCM navy horizontal |
| berisi 17/06 | Tiga parallelogram merah menaik dan satu taper panjang, MCM navy, dua baseline merah/navy |
| berisi 17/07 | Rail navy mengikuti chevron turun, M dan C merah mengikuti kemiringan bidang |
| berisi 17/08 | Ring hexagon navy, celah transparan, bidang merah dan MCM putih positif |
| berisi 17/09 | Cap/alas merah terpisah, M navy bertakik dalam, C merah tengah |
| rasio_1 14/04 | MCM navy miring dengan C ber-chamfer pendek, cap merah dan alas navy |

Semua sumber dan render dibuka untuk perbandingan visual. M kanan 17/06 diukur tersendiri agar tidak mewarisi tepi miring dari M kiri. Bentuk C membulat ditulis sebagai segmen chamfer pendek yang diukur manual, bukan font. Outline putih 17/01 memakai layer bentuk putih di bawah huruf navy, bukan stroke atau raster; huruf/outline putih tetap bisa di-recolor. Pada 17/08, ring gap tetap transparan, bukan field putih yang menutup background.

Ini rekonstruksi geometris manual dari masing-masing sumber, bukan auto-trace atau substitusi template generik. Tekstur diratakan menjadi merah/navy/putih solid; sudut dan proporsi disederhanakan/dirapikan. Tidak diklaim pixel-perfect, produksi final, atau sudah disetujui pengguna. Hasil masih menunggu review visual.

## Progres dan audit terbatas

- **10 master baru**, kumulatif **139 master Drive unik**.
- Hash sepuluh sumber baru berbeda satu sama lain dan dari sumber master sebelumnya; **tidak ada alias baru** pada batch ini. Kesamaan motif tidak otomatis digabung.
- Kumulatif alias duplikat terverifikasi tetap **18**, diwariskan tanpa perubahan dari batch 16.
- Total sumber tercakup: **157/342 = 45,91%**; sisa **185**.
- Redraw unik saja dibagi jumlah file: **139/342 = 40,64%**.
- 342 adalah jumlah file yang sebelumnya dilaporkan, bukan jumlah desain unik yang sudah diaudit global. Audit hash dibatasi PNG yang diunduh; snapshot terdahulu tidak ditulis ulang.

## Artefak dan pemeriksaan

`perbandingan.html` mandiri/offline menyandingkan raster sumber pembanding dengan SVG master. Tombol latar putih/abu-abu membantu review transparansi. Disertakan 10 SVG path-only (tanpa bitmap/font), 10 JSON koordinat native, 10 PNG preview, serta progress/provenance.

**85 tes lokal lulus:** 76 batch-path + 8 geometris + 1 variasi. Tes memeriksa kesamaan SVG/JSON, kontur tertutup, batas kanvas, persilangan proper polygon, ID/geometri/hash sumber berbeda dari batch sebelumnya, jumlah dan progres, alias tidak berubah, katalog tetap, serta APK dijeda. Tidak ada klaim uji perangkat Android untuk batch desain ini.

Reproduksi dengan sumber lokal dan resvg:
```sh
python scripts/build_drive_batch_17.py
python -m unittest discover -s tests -p 'test_path_batches.py'
python -m unittest discover -s tests -p 'test*geometric*.py'
python -m unittest discover -s tests -p 'test_variation_vectors.py'
```
