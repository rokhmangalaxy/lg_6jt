# Batch 03 — 10 redraw manual, tanpa build APK

## Cakupan
- Kelompok 1: 05, 06, 07, 09 → kelompok 1 selesai **9/9**.
- Kelompok 2: 01–06 → kelompok 2 selesai **6/9**, tersisa 07–09.
- Total sumber Drive dengan master: **15/342** file yang sebelumnya dilaporkan. **327 belum diproses**; bukan klaim 327 desain unik.
- Dua studi baru di aplikasi (geo-007/008) tidak dihitung sebagai sumber Drive yang selesai.

## Artefak
- `perbandingan.html`: offline, sumber Drive versus master SVG untuk seluruh sepuluh logo.
- `exp-GGG-NN.svg`: master transparan dengan path M/L/Z, tanpa raster/font tertanam.
- `exp-GGG-NN.json`: path native dan peran warna dari koordinat identik.
- `*-preview.png`: hasil render master pada putih untuk pemeriksaan, bukan sumber path.
- `progress.json`: pemetaan ID, sumber Drive, hash, progres, dan status review.

Semua koordinat dikonstruksi manual. Dua M disimetriskan kecuali desain miring 2/05 yang memang tidak bercermin. Warna bertekstur sumber diratakan ke palet kerja merah/navy/putih. Sisi dan ruang negatif dirapikan; bukan salinan piksel atau persetujuan produksi. Kandidat memerlukan review pengguna untuk kemiripan bentuk.

## Audit duplikat
SHA-256 dibandingkan untuk **15 file PNG yang sudah diunduh**, tidak ditemukan duplikat byte-identik pada subset tersebut. Sepuluh sumber baru ditinjau visual dan dibangun sebagai master berbeda. Desain mirip (contoh hexagon 2/06 dan 1/03) tidak disamakan otomatis karena susunan warna dan ruang negatif berbeda. Belum ada audit folder penuh atau jaminan tidak ada duplikat visual di file yang belum dibuka.

## Build ditahan
Tidak ada perubahan katalog atau aset Android pada batch ini. Sebelas logo dan semua ID favorit lama tetap utuh. Job Android di `.github/workflows/android-apk.yml` dinonaktifkan secara eksplisit; validasi PR hanya menjalankan pemeriksaan data desain tanpa Gradle/SDK/APK. Jangan membangun APK sampai seluruh koleksi path selesai dan penahanan dicabut setelah konfirmasi pengguna.

## Reproduksi
```sh
npm install --prefix .cache/mcm-redraw @resvg/resvg-js
python scripts/build_drive_batch_03.py
python -m unittest discover -s tests -p 'test_path_batches.py'
```
Generator membutuhkan sepuluh sumber di `google_drive/` (unduhan lokal tidak dimasukkan Git). Tes dapat berjalan tanpa unduhan sumber, memverifikasi SVG/JSON, kontur tertutup, luas bukan nol, batas koordinat, progres, dan penahanan build. Saat sumber tersedia, tes juga memeriksa SHA-256.
