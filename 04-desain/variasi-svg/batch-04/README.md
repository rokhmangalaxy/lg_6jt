# Batch 04 — kelompok 2/07, 08, 09

Tiga sumber tersisa kelompok 2 direkonstruksi dengan koordinat poligon manual. Bukan auto-trace atau raster dalam SVG.

## Progres kumulatif
- Kelompok 1: master **9/9**.
- Kelompok 2: master **9/9**.
- Total: **18 sumber Drive** memiliki master. **324 file belum diproses** dari 342 file yang sebelumnya dilaporkan; angka file bukan jumlah desain unik terverifikasi.
- Progres batch terdahulu merupakan snapshot historis. Semua master baru masih membutuhkan persetujuan visual pengguna.
- Dua studi tambahan bukan sumber Drive, tidak dihitung dalam angka ini.

## Review bentuk
- 2/07: sayap merah terpisah, dua M navy, kaki C runcing. Berbeda dari 1/05 yang seluruhnya merah.
- 2/08: C dengan ujung chamfer datar, dua M navy tanpa bingkai. Berbeda dari 2/02 yang C-nya runcing dan terminal miringnya berbeda.
- 2/09: diamond melebar, bingkai navy, bidang merah, counter MCM dan aksen segitiga transparan. Tidak disamakan dengan diamond 2/01 yang seluruhnya merah serta proporsinya berbeda.
- M kiri/kanan disimetriskan. Detail sumber yang tidak rata diregularisasi; tekstur/gradasi diratakan ke merah #DC2626 dan navy #173257. Ruang putih adalah lubang transparan, bukan patch putih.
- Preview hasil render telah diperiksa terhadap sumber untuk susunan, counter, dan ruang pemisah. Ini bukan klaim identik piksel atau persetujuan produksi.

## Berkas
`perbandingan.html` mandiri/offline memuat sumber asli dan SVG berdampingan. Masing-masing logo juga memiliki master `.svg`, native `.json`, dan PNG hasil render untuk pemeriksaan. JSON/SVG berbagi koordinat; PNG tidak dipakai untuk menggambar logo.

`progress.json` menyimpan ID Drive, SHA-256 sumber, status review, dan progres. Audit byte pada 18 PNG unduhan tidak menemukan duplikat identik. Audit visual terbatas pada kelompok 1–2; folder keseluruhan belum diaudit.

Tidak ada build APK, Gradle, atau perubahan katalog Android. Penahanan job Android tetap aktif. Semua ID/favorit aplikasi tidak berubah.

## Reproduksi
Dengan sumber lokal pada `google_drive/` dan resvg terpasang:
```sh
npm install --prefix .cache/mcm-redraw @resvg/resvg-js
python scripts/build_drive_batch_04.py
python -m unittest discover -s tests -p 'test_path_batches.py'
```
