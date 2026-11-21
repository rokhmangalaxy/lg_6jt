# Batch 14 — 10 master manual, tanpa APK

Instruksi terbaru pengguna: **“lanjut, tanpa build apk”**. Semua job APK dinonaktifkan (`if: false`), termasuk dispatch manual. Tidak menjalankan Gradle, tidak mengubah katalog Android, tidak membuat rilis. Katalog aplikasi tetap 105 variasi seperti v1.0.42.

## Sumber dan rekonstruksi

Sembilan sumber `berisi 13/01–09` dan satu sumber **keluarga `rasio_1` 14/01** diukur manual menjadi polygon SVG/native JSON. Master keluarga rasio memakai ID `exp-rasio-014-01` agar tidak bentrok dengan keluarga berisi. Nama dan Drive ID sumber yang tepat, serta SHA-256, tercatat di `progress.json`.

| Sumber | Struktur yang dipertahankan |
|---|---|
| berisi 13/01 | Dua bidang/ring diamond merah dan MCM putih positif |
| berisi 13/02 | Rail hexagon navy terpisah, M navy, C merah |
| berisi 13/03 | M navy bersudut, C merah memanjang |
| berisi 13/04 | Bingkai segitiga navy tiga bagian dan MCM merah |
| berisi 13/05 | Bidang C navy bagian atas, dua sisi M merah terpisah |
| berisi 13/06 | Shield navy dengan ring transparan, bidang merah, MCM putih positif |
| berisi 13/07 | M navy, C merah, dua pasang bar sayap merah/navy |
| berisi 13/08 | Rail merah atas/bawah, M navy dan C merah |
| berisi 13/09 | M navy tinggi dan C merah berujung runcing panjang |
| rasio_1 14/01 | Diamond merah lebar, ujung navy terbelah, MCM navy mendatar |

Koordinat disimetriskan/dirapikan secara geometris, warna tekstur diratakan. Ini bukan auto-trace, bukan glyph font, bukan klaim pixel-perfect. Preview sumber dan render telah dibuka untuk perbandingan visual. Huruf putih adalah layer warna positif yang bisa di-recolor, bukan lubang yang tidak sengaja dibuat. Area di luar shape dan celah ring tetap transparan. Seluruh hasil masih menunggu persetujuan visual pengguna.

## Audit dan progres

- **+10 master unik**, kumulatif **109** master Drive.
- `berisi 14/01` identik byte/SHA-256 dengan `berisi 13/01`: satu alias tambahan, **bukan master kesebelas**.
- Kumulatif **10 sumber duplikat terverifikasi** (9 dari batch sebelumnya + 1 baru).
- **119/342 sumber tercakup = 34,80%**; sisa **223** belum diproses.
- Redraw unik dibagi total file: **109/342 = 31,87%**. Total desain unik seluruh folder belum diketahui.
- 342 adalah jumlah file yang sebelumnya dilaporkan, bukan hasil audit global pada batch ini.
- Audit hash hanya sumber PNG yang sudah diunduh; kelompok berisi 14/02–09 belum diperiksa. Keluarga berisi dan rasio tidak dianggap sama hanya karena nama nomornya mirip.

## Artefak dan pemeriksaan

`perbandingan.html` mandiri/offline, SVG, JSON koordinat, preview PNG, dan `progress.json`. Halaman HTML menyertakan sumber raster hanya sebagai pembanding; SVG master hanya path, tanpa raster/font. Tombol latar putih/abu-abu membantu meninjau transparansi.

Tes memeriksa SVG/JSON identik, polygon tertutup/tidak bersilangan secara proper, batas kanvas, sumber/hash, ID tidak bentrok, tidak ada SVG identik dengan batch lain, progres duplicate-aware, katalog aplikasi tetap, dan job APK dijeda. Tidak mengklaim uji perangkat Android untuk master baru ini.

Reproduksi dengan sumber lokal dan dependensi resvg yang sudah tersedia:
```sh
python scripts/build_drive_batch_14.py
python -m unittest discover -s tests -p 'test_path_batches.py'
```
