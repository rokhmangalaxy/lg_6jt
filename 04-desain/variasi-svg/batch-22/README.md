# Batch 22 — 10 master rasio manual, tanpa APK

Sumber **rasio_1 16/09 dan 17/01–09**. Nama PNG, Drive ID, SHA-256 dan lokasi SVG/JSON dicatat dalam `progress.json`. ID keluarga rasio tidak digabung dengan berisi.

## Konstruksi spesifik sumber

| Sumber rasio | Struktur |
|---|---|
| 16/09 | Rail merah bertingkat seperti I-beam, MCM navy dengan C chamfer pendek |
| 17/01 | Diamond merah, empat tip navy terpisah dan MCM putih positif |
| 17/02 | Atap merah berlekuk tengah, dua M navy berpilar, C merah rendah |
| 17/03 | Cap/alas merah, bracket samping navy terpisah, MCM navy |
| 17/04 | Tip rail navy pendek, rail merah panjang meruncing, M navy dan C merah oblique |
| 17/05 | C merah vertikal berujung runcing dengan lengan kanan pendek; dua M navy |
| 17/06 | Rail merah chamfer sederhana, MCM navy; C sedikit oblique |
| 17/07 | Atap navy, dua M navy tinggi, C merah dengan lengan kanan miring |
| 17/08 | Bingkai merah persegi berlekuk samping, jendela transparan dan MCM navy |
| 17/09 | C merah berujung bawah runcing, M navy oblique, dua V bawah merah/navy |

Sepuluh sumber dibuka satu per satu; render hasil dibandingkan kembali dalam montage. Koordinat ditulis manual per sumber, bukan auto-trace, font atau penggantian desain generik. Kurva diregularisasi sebagai chamfer pendek; tekstur diratakan menjadi merah/navy/putih solid. Huruf putih 17/01 adalah bidang positif recolorable. Jendela 17/08 memakai counter evenodd transparan, bukan bidang putih. Celah antarkomponen mengikuti latar. Hasil masih menunggu review visual pengguna; tidak diklaim pixel-perfect atau final produksi.

## Progres dan audit terbatas

- **189 master Drive unik** (+10); redraw saja **189/342 = 55,26%**.
- Alias duplikat sumber terverifikasi tetap **18**, diwariskan tanpa perubahan.
- Cakupan sumber **207/342 = 60,53%**; **135 sumber tersisa**.
- Sepuluh hash sumber baru berbeda satu sama lain dan dari sumber master terdahulu, diperiksa sebelum ekspor. Motif mirip tidak otomatis digabung.
- 342 adalah jumlah file yang sebelumnya dilaporkan, bukan jumlah desain unik terverifikasi global. Audit hanya sumber unduhan; snapshot lama tidak diubah.

## Artefak dan validasi

10 SVG path-only tanpa bitmap/font, 10 JSON native, 10 PNG preview, provenance/progress, dan `perbandingan.html` mandiri/offline dengan toggle latar putih/abu-abu. Raster hanya untuk referensi pembanding di HTML.

**109 tes lokal lulus:** 100 path-batch + 8 geometris + 1 variasi. Memeriksa SVG/JSON konsisten, path tertutup/dalam kanvas, persilangan polygon, nonkolisi ID/geometri/hash, progres/alias, huruf putih positif dan counter bingkai transparan, katalog tetap serta job APK dijeda. Tidak ada tes perangkat Android baru.

**Tidak ada build APK, workflow dispatch, integrasi Android atau rilis.** Katalog tetap 105 variasi; APK terakhir v1.0.42.

Reproduksi dengan sumber lokal dan resvg:
```sh
python scripts/build_drive_batch_22.py
python -m unittest discover -s tests -p 'test_path_batches.py'
python -m unittest discover -s tests -p 'test*geometric*.py'
python -m unittest discover -s tests -p 'test_variation_vectors.py'
```
