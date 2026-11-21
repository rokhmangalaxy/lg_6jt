# Batch 09 — 10 master path manual

## Progres kumulatif
| Status | Jumlah |
|---|---:|
| Sudah redraw / memiliki master path | **68 dari 342 sumber** |
| Sisa belum diproses | **274 sumber** |
| Progres | **19,88%** |
| Penambahan batch ini | **10 sumber** |

Rumus `68 / 342 × 100 = 19,883...%`, dibulatkan dua desimal. Penyebut 342 adalah jumlah file Drive yang sebelumnya dilaporkan, **bukan total desain unik terverifikasi**. Persentase mengukur sumber dengan master path, bukan persetujuan visual/produksi. Dua studi tambahan aplikasi tidak dihitung sebagai sumber Drive.

- Kelompok 1–7: masing-masing **9/9** sumber memiliki master.
- Kelompok 8: **01–05** memiliki master. Sisa kelompok belum dilisting; pending kosong di JSON tidak berarti kelompok selesai.
- Batch ini: kelompok 7/05–09 dan 8/01–05.
- Semua master baru berstatus **menunggu review visual pengguna**.

## Pemeriksaan bentuk
| Sumber | Ciri spesifik yang dipertahankan |
|---|---|
| 7/05 | Cap/footer navy terpisah, MCM merah; M lebih rendah dari atap |
| 7/06 | MCM navy ramping, sayap merah tiga bagian, strip tengah bertakik |
| 7/07 | Sumbu bingkai diamond navy terbelah pada atas/bawah, M merah bertip keluar |
| 7/08 | C navy tinggi dengan terminal diagonal, dua M merah ramping |
| 7/09 | Diamond merah panjang dengan counter MCM dan segitiga, band navy atas/bawah terpisah |
| 8/01 | Hexagon merah padat tanpa ring terpisah, MCM transparan |
| 8/02 | Ujung luar M navy tersapu naik, C merah runcing |
| 8/03 | Diamond navy tertutup, inset merah dan counter MCM; tidak memakai geometri 7/09 yang berband terpisah |
| 8/04 | C merah sempit diapit bidang navy dengan counter M transparan |
| 8/05 | M arsitektural merah melebar, C merah dengan kaki dalam diagonal |

Semua sumber asli dibuka; hasil render sepuluh master ditinjau terhadap sumber untuk komposisi, proporsi, counter dan pemisahan elemen. Koordinat dibuat manual per sumber, bukan auto-trace, raster atau font di SVG. Tekstur/gradasi diratakan ke merah #DC2626 / navy #173257. Simetri M dirapikan sesuai konsep. Ini bukan klaim salinan piksel identik atau persetujuan produksi.

## Duplikat dan validasi
Audit SHA-256 pada **68 PNG unduhan** tidak menemukan duplikat byte-identik pada subset tersebut. Kemiripan motif ditinjau, bukan otomatis digabung: 8/03 memiliki bingkai tertutup tanpa counter segitiga, sedangkan 7/09 berband terpisah dengan counter segitiga. Varian 7/06 tidak memakai ulang koordinat sayap 3/07. Audit visual seluruh folder Drive belum selesai.

Tes memeriksa ID/hash master unik, koordinat SVG–JSON sama, warna, fill-rule evenodd, kontur tertutup, luas bukan nol, batas koordinat, dan kontur menyilang secara proper. Sampel tambahan memeriksa celah sumbu diamond, gap sayap, counter segitiga, counter M pada sideplate, dan aperture C. Progres/persentase, hash sumber, serta penahanan APK juga diperiksa. Tes tidak membuktikan kemiripan visual sempurna atau kelayakan bordir/cetak.

## Artefak
- `perbandingan.html`: offline, sumber vs SVG, jumlah/sisa/persentase dan tombol latar putih/abu-abu.
- `exp-GGG-NN.svg`: master transparan dengan path M/L/Z tanpa font/raster.
- `exp-GGG-NN.json`: native path dari koordinat sama.
- `*-preview.png`: render master untuk review, bukan sumber pembentuk path.
- `progress.json`: ID Drive, SHA-256 sumber, cakupan audit, progres.

Tidak ada build APK atau perubahan aset/katalog Android. Semua ID favorit tetap utuh. Job APK tetap ditahan `if: false`.

## Reproduksi
```sh
npm install --prefix .cache/mcm-redraw @resvg/resvg-js
python scripts/build_drive_batch_09.py
python -m unittest discover -s tests -p 'test_path_batches.py'
python -m unittest discover -s tests -p 'test*geometric*.py'
python -m unittest discover -s tests -p 'test_variation_vectors.py'
```
Generator membutuhkan sumber lokal `google_drive/` dan resvg. Unduhan mentah tidak dimasukkan Git; HTML membawa sumber untuk review offline. Progres batch sebelumnya merupakan snapshot historis.
