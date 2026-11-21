# Batch 06 — 10 master path manual

## Cakupan
- Kelompok 4: **02–09** → kelompok 4 kini **9/9** memiliki master.
- Kelompok 5: **01–02** → **2 sumber** memiliki master; isi kelompok selebihnya belum dilisting, bukan dianggap selesai.
- Kelompok 1–3 tetap masing-masing **9/9**.
- Total kumulatif **38 sumber Drive** telah dibuat path. **304 file belum diproses** dari 342 file yang sebelumnya dilaporkan (angka file, bukan desain unik terverifikasi).
- Dua studi tambahan aplikasi tidak dihitung sebagai sumber Drive. Master baru menunggu review visual pengguna.

## Review sumber dan bentuk
| Sumber | Karakter spesifik yang dipertahankan |
|---|---|
| 4/02 | M berbentuk bahu arsitektural tanpa lekukan M klasik; C merah tinggi |
| 4/03 | Hexagon navy, bidang merah dan MCM transparan; rasio huruf berbeda dari 2/06 |
| 4/04 | Atap merah landai, MCM melebar, dasar navy terpisah |
| 4/05 | Cap merah, sayap navy tersambung M, chevron merah bawah |
| 4/06 | Sayap navy rendah dengan dua tab kecil per sisi; C merah |
| 4/07 | Kolom M bagian dalam menjulang, C merah lebih tinggi; bukan duplikat 4/02 |
| 4/08 | Badge oktagonal, perimeter merah, bidang navy dengan counter MCM dan dua lubang baut |
| 4/09 | Rel samping merah panjang yang naik ke kedua sisi, M navy dan C merah |
| 5/01 | Diamond ganda merah, counter MCM; C tajam dan proporsi berbeda dari 2/01 |
| 5/02 | M lebar dan C merah dengan terminal kotak; bukan C runcing 2/02 |

Sepuluh sumber asli telah dibuka; render seluruh master diperiksa terhadap sumber. Detail C pada 4/05 dan 4/09 dikoreksi setelah render pertama, kemudian render koreksi diperiksa ulang. Koordinat dibuat manual per sumber; tidak ada auto-trace, font, atau raster pada SVG. Tekstur/gradasi sumber diratakan menjadi merah #DC2626 / navy #173257. Counter putih pada badge/diamond adalah lubang transparan. Simetri kiri/kanan dirapikan bila sesuai konsep sumber, bukan klaim salinan identik piksel.

## Duplikat dan validasi
- Audit SHA-256 **38 PNG unduhan** tidak menemukan duplikat byte-identik.
- Layout baru ditinjau visual sebagai variasi berbeda; audit visual seluruh Drive belum selesai.
- Tidak ada ID atau SVG baru byte-identik yang bertabrakan dengan master sebelumnya.
- Tes memeriksa koordinat SVG–JSON sama, batas koordinat, kontur tertutup, luas bukan nol, kontur menyilang secara proper, provenance, progres, dan penahanan APK.
- Sampel tambahan memeriksa transparansi dua lubang baut, counter MCM badge/diamond, dan aperture C; bukan bukti otomatis bahwa seluruh gambar identik sumber atau siap bordir/cetak.

## Berkas
- `perbandingan.html`: offline, sumber asli dan redraw SVG berdampingan, tombol latar putih/abu-abu untuk memeriksa counter.
- `exp-GGG-NN.svg`: master transparan, path M/L/Z.
- `exp-GGG-NN.json`: native path dari koordinat sama.
- `*-preview.png`: render master untuk review, bukan input pembentuk path.
- `progress.json`: asal Drive, SHA-256, progres dan cakupan audit.

Tidak ada build APK atau perubahan katalog/aset Android. Semua ID favorit lama tetap utuh. Job APK tetap ditahan `if: false`.

## Reproduksi
```sh
npm install --prefix .cache/mcm-redraw @resvg/resvg-js
python scripts/build_drive_batch_06.py
python -m unittest discover -s tests -p 'test_path_batches.py'
python -m unittest discover -s tests -p 'test*geometric*.py'
python -m unittest discover -s tests -p 'test_variation_vectors.py'
```
Generator memerlukan sumber pada `google_drive/` dan resvg lokal. Unduhan mentah tidak ditambahkan Git; perbandingan HTML membawa sumber untuk review offline. Progres batch terdahulu adalah snapshot historis.
