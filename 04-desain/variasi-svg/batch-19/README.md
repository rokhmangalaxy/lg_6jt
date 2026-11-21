# Batch 19 — 10 master manual, tanpa APK

Sembilan sumber **berisi 19/01–09** dan satu **rasio_1 14/06** digambar ulang berdasarkan pengamatan referensi, memakai koordinat polygon manual per sumber. Bukan auto-trace, font, atau substitusi desain generik. Nama sumber, Drive ID, SHA-256 dan lokasi master SVG/JSON tersedia dalam `progress.json`. ID keluarga rasio tetap terpisah: `exp-rasio-014-06`.

## Struktur spesifik sumber

| Sumber | Konstruksi |
|---|---|
| 19/01 | Diamond merah, empat ujung navy, huruf navy dengan outline putih positif |
| 19/02 | Atap/alas merah, M oblique navy, C navy dengan sisi kiri membulat |
| 19/03 | Bingkai I-beam navy dengan jendela transparan dan MCM merah |
| 19/04 | Arch merah berlubang terbuka bawah, pilar navy terpisah, MCM navy |
| 19/05 | Strip merah/navy offset berujung bertingkat, MCM navy |
| 19/06 | Cap/alas navy, bracket samping merah, MCM merah; ujung rail datar pendek |
| 19/07 | Atap naik navy lalu segmen turun merah, MCM navy oblique, baseline merah |
| 19/08 | Cap/alas navy, chevron samping merah terpisah, MCM merah; berbeda dari 19/06 |
| 19/09 | Empat rail dua warna terpisah, M merah angular, C navy membulat |
| rasio 14/06 | Tiga wing-bar merah tiap sisi, MCM navy, segitiga merah di atas alas V navy |

Semua sepuluh sumber dibuka satu per satu; render hasil dibandingkan kembali dalam montage. Kurva C diregularisasi menjadi chamfer pendek. Outline putih 19/01 merupakan bidang putih positif di bawah huruf navy. Jendela 19/03 dan celah antarbagian transparan, bukan bidang putih. Tekstur sumber diratakan menjadi merah/navy/putih solid. Hasil masih menunggu review visual pengguna, tidak diklaim pixel-perfect atau siap produksi.

## Progres dan audit terbatas

- **159 master unik** (+10); redraw saja **159/342 = 46,49%**.
- **18 alias sumber duplikat** terverifikasi diwariskan tanpa perubahan; tidak ada alias baru.
- Cakupan sumber **177/342 = 51,75%**; **165 sumber tersisa**.
- Sepuluh hash sumber baru berbeda satu sama lain dan dari hash sumber master terdahulu. Motif mirip tidak otomatis dianggap duplikat.
- 342 adalah jumlah file yang dilaporkan, bukan jumlah desain unik yang sudah diaudit global.

## Artefak dan validasi

`perbandingan.html` mandiri/offline memuat raster pembanding dan SVG master, dengan toggle putih/abu-abu. Disertakan 10 SVG, 10 JSON native, 10 PNG preview dan provenance/progress.

**94 tes lokal lulus:** 85 path-batch + 8 geometris + 1 variasi. Memeriksa kesamaan SVG/JSON, batas/penutupan path, persilangan polygon, nonkolisi ID/geometri/hash, alias/progres, katalog Android tetap, dan jeda job APK. Tidak ada tes perangkat Android baru.

**Tidak menjalankan build APK, dispatch workflow, integrasi Android atau rilis.** Katalog tetap 105 variasi; v1.0.42 tetap APK terakhir. Reproduksi (memerlukan PNG sumber lokal dan resvg):

```sh
python scripts/build_drive_batch_19.py
python -m unittest discover -s tests -p 'test_path_batches.py'
python -m unittest discover -s tests -p 'test*geometric*.py'
python -m unittest discover -s tests -p 'test_variation_vectors.py'
```
