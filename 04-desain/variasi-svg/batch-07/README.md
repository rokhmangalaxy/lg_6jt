# Batch 07 — 10 master path manual

## Progres kumulatif
| Status | Jumlah |
|---|---:|
| Sudah redraw / memiliki master path | **48 dari 342 sumber** |
| Belum diproses | **294 sumber** |
| Progres | **14,04%** |
| Penambahan batch ini | **10 sumber** |

Rumus: `48 / 342 × 100 = 14,035...%`, dibulatkan dua desimal. Penyebut 342 adalah jumlah file Drive yang sebelumnya dilaporkan, **bukan jumlah desain unik terverifikasi**. Persentase mengukur ketersediaan master path, bukan persetujuan desain/produksi. Dua studi tambahan aplikasi tidak dihitung sebagai sumber Drive.

- Kelompok 1–5: masing-masing **9/9** sumber memiliki master.
- Kelompok 6: **01–03** memiliki master. Sisa isi kelompok belum dilisting; pending kosong di JSON tidak berarti kelompok 6 selesai.
- Batch ini: kelompok 5/03–09 dan 6/01–03.
- Semua hasil baru berstatus **menunggu review visual pengguna**.

## Pemeriksaan bentuk per sumber
| Sumber | Ciri spesifik yang dipertahankan |
|---|---|
| 5/03 | Hexagon navy, bidang merah, counter MCM; C dan M berbeda proporsi dari 4/03 |
| 5/04 | Nameplate hexagon landai, bidang navy dengan counter MCM, cap/footer merah |
| 5/05 | Wing wedge navy, MCM merah, dasar segitiga terbuka |
| 5/06 | Nameplate miring, perimeter/bar merah, bidang navy; M tidak dicerminkan karena komposisi oblique |
| 5/07 | Bingkai segitiga merah terbalik, MCM navy tanpa bidang isi |
| 5/08 | Hexagon ganda merah dengan celah vertikal bawah dan counter MCM transparan |
| 5/09 | Diamond navy lebar, MCM navy dan chevron merah terpisah di kedua sisi |
| 6/01 | Diamond navy, inset merah dengan counter MCM, tanpa perimeter merah ganda |
| 6/02 | M merah mengapit C navy yang lebih lebar, tidak menyamakan dengan desain warna terbalik |
| 6/03 | Hexagon landai navy, dua strip dalam merah, MCM navy |

Semua sumber telah dibuka, kemudian hasil render seluruh sepuluh master ditinjau berdampingan terhadap sumber. Celah 5/08 diperiksa ulang agar tidak bertabrakan dengan counter C. Warna tekstur/gradasi diratakan ke merah #DC2626 dan navy #173257. Geometri ditulis manual per sumber, bukan auto-trace, font, atau raster dalam SVG. Sisi M disimetriskan bila sesuai konsep; 5/06 tetap miring/asimetris. Bukan klaim salinan piksel atau persetujuan produksi.

## Validasi
- Audit SHA-256 **48 PNG unduhan**: tidak ada duplikat byte-identik pada subset tersebut. Audit visual seluruh Drive belum selesai.
- ID baru dan hash SVG tidak bertabrakan dengan master sebelumnya.
- Tes kesamaan koordinat SVG–JSON, fill-rule, warna, kontur tertutup, luas bukan nol, batas koordinat, kontur menyilang secara proper, provenance/progres, persentase, dan penahanan build APK.
- Sampel transparansi meliputi celah hexagon, counter bidang miring, ruang kosong segitiga, dan aperture C. Tes bukan pembuktian otomatis kemiripan visual sempurna atau kesiapan cetak/bordir.

## Artefak
`perbandingan.html` mandiri/offline menampilkan sumber vs SVG dan ringkasan jumlah/sisa/persentase, dengan tombol latar putih/abu-abu untuk memeriksa transparansi. Setiap logo memiliki `.svg`, `.json`, dan `-preview.png` hasil render. `progress.json` memuat ID Drive, hash sumber, cakupan audit, serta angka progres.

Tidak ada build APK atau perubahan katalog/aset Android. Semua ID/favorit lama utuh. Job APK tetap ditahan `if: false`.

## Reproduksi
```sh
npm install --prefix .cache/mcm-redraw @resvg/resvg-js
python scripts/build_drive_batch_07.py
python -m unittest discover -s tests -p 'test_path_batches.py'
python -m unittest discover -s tests -p 'test*geometric*.py'
python -m unittest discover -s tests -p 'test_variation_vectors.py'
```
Generator membutuhkan sumber lokal pada `google_drive/` dan resvg. Unduhan mentah tidak dimasukkan Git; HTML perbandingan membawa sumber untuk review offline. Catatan batch lama tetap snapshot historis.
