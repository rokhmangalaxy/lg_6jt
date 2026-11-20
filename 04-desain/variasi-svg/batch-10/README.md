# Batch 10 — 10 master path manual

## Progres kumulatif
| Status | Jumlah |
|---|---:|
| Sudah redraw / memiliki master path | **78 dari 342 sumber** |
| Sisa belum diproses | **264 sumber** |
| Progres | **22,81%** |
| Penambahan batch ini | **10 sumber** |

Rumus `78 / 342 × 100 = 22,807...%`, dibulatkan dua desimal. Penyebut 342 adalah jumlah file Drive yang sebelumnya dilaporkan, **bukan total desain unik terverifikasi**. Progres mengukur sumber dengan master path, bukan persetujuan visual/produksi. Dua studi tambahan aplikasi tidak dihitung sebagai sumber Drive.

- Kelompok 1–8: masing-masing **9/9** sumber memiliki master.
- Kelompok 9: **01–06** memiliki master. Sisa kelompok belum dilisting; pending kosong di JSON tidak berarti kelompok selesai.
- Batch ini: kelompok 8/06–09 dan 9/01–06.
- Semua master baru **menunggu review visual pengguna**.

## Review bentuk per sumber
| Sumber | Ciri spesifik yang dipertahankan |
|---|---|
| 8/06 | Bingkai persegi panjang navy, M navy dan C merah chamfer |
| 8/07 | MCM merah tinggi dengan chevron navy terpisah di samping |
| 8/08 | Shield merah bertaper, inset navy dan counter MCM |
| 8/09 | Roof/footer navy pendek, MCM merah melebar |
| 9/01 | Diamond merah padat, counter MCM dengan ujung C lunak |
| 9/02 | Hexagon navy, MCM merah; rasio huruf diukur tersendiri, bukan memakai ulang 3/02 |
| 9/03 | MCM miring dengan C terbuka, bar merah horizontal terpisah |
| 9/04 | M navy terintegrasi sayap tengah, strip atas dan tab bawah, C merah |
| 9/05 | Roof diagonal navy pendek dan terpisah, M navy dan C merah tinggi |
| 9/06 | Diamond navy, bidang tengah merah dengan counter MCM, aksen segitiga merah terpisah di tip kiri/kanan |

Semua sumber dibuka dan hasil render sepuluh master ditinjau terhadap sumber. Aksen segitiga 9/06 dikoreksi setelah render pertama: berupa bidang merah terpisah dengan celah transparan, bukan lubang segitiga pada bidang merah penuh. Render koreksi dibuka dan diperiksa ulang.

Koordinat ditulis manual per sumber, bukan auto-trace, font atau raster dalam SVG. Tekstur/gradasi sumber diratakan ke merah #DC2626 dan navy #173257. Ujung lunak C 9/01 didekati segmen chamfer pendek; bukan kurva atau salinan piksel identik. M kiri/kanan disimetriskan bila sesuai konsep, sedangkan M miring 9/03 ditulis terpisah. Ini bukan persetujuan produksi.

## Duplikat dan validasi
- Audit SHA-256 **78 PNG unduhan** tidak menemukan file byte-identik pada subset tersebut. Audit visual seluruh folder Drive belum selesai.
- Motif serupa tidak otomatis digabung: 9/03 berbeda dari 2/05 pada bentuk C dan batang M; 9/06 memiliki aksen tip positif terpisah, bukan diamond merah utuh dengan counter tip.
- ID dan hash SVG baru diperiksa agar tidak bertabrakan dengan master sebelumnya.
- Tes kesamaan koordinat SVG–JSON, warna, fill-rule, kontur tertutup, luas bukan nol, batas koordinat dan kontur menyilang secara proper.
- Sampel tambahan memeriksa aksen merah positif, celah antaraksen dan bidang tengah, counter shield/diamond, aperture C, gap bingkai dan sayap.
- Progres/persentase, hash sumber dan penahanan APK juga diperiksa. Tes tidak membuktikan kemiripan visual sempurna atau kelayakan cetak/bordir.

## Artefak
`perbandingan.html` mandiri/offline: sumber vs SVG, jumlah/sisa/persentase dan tombol latar putih/abu-abu. Masing-masing logo memiliki master `.svg`, native `.json`, serta `-preview.png` hasil render. `progress.json` menyimpan ID Drive, hash sumber, cakupan audit dan progres.

Tidak ada build APK atau perubahan katalog/aset Android. ID/favorit lama tetap utuh. Job APK tetap ditahan `if: false`.

## Reproduksi
```sh
npm install --prefix .cache/mcm-redraw @resvg/resvg-js
python scripts/build_drive_batch_10.py
python -m unittest discover -s tests -p 'test_path_batches.py'
python -m unittest discover -s tests -p 'test*geometric*.py'
python -m unittest discover -s tests -p 'test_variation_vectors.py'
```
Generator membutuhkan sumber lokal `google_drive/` dan resvg. Unduhan mentah tidak dimasukkan Git; HTML membawa sumber untuk review offline. Progres batch terdahulu adalah snapshot historis.
