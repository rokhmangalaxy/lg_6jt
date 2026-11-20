# Batch 11 — 10 master path manual

## Progres kumulatif
| Status | Jumlah |
|---|---:|
| Sudah redraw / memiliki master path | **88 dari 342 sumber** |
| Sisa belum diproses | **254 sumber** |
| Progres | **25,73%** |
| Penambahan batch ini | **10 sumber** |

Rumus `88 / 342 × 100 = 25,730...%`, dibulatkan dua desimal. Penyebut 342 adalah jumlah file Drive yang sebelumnya dilaporkan, **bukan total desain unik terverifikasi**. Persentase mengukur sumber dengan master path, bukan persetujuan visual/produksi. Dua studi tambahan aplikasi tidak dihitung sebagai sumber Drive.

- Kelompok 1–9: masing-masing **9/9** sumber memiliki master.
- Kelompok 10: **01–07** memiliki master; **08–09** sudah terdaftar di Drive tetapi belum diunduh/redraw.
- Batch ini: kelompok 9/07–09 dan 10/01–07.
- Semua master baru **menunggu review visual pengguna**.

## Review bentuk per sumber
| Sumber | Ciri spesifik yang dipertahankan |
|---|---|
| 9/07 | Cap/footer merah, dua M navy dengan bahu atas angular |
| 9/08 | C merah sangat tinggi, M navy bersudut tajam tanpa bingkai |
| 9/09 | M navy melebar, strip atas/bawah lurus terpisah, C merah |
| 10/01 | Diamond merah padat, counter MCM; C berujung tajam, bukan C lunak 9/01 |
| 10/02 | Roof merah, M navy, chevron bawah navy, C merah |
| 10/03 | Hexagon navy dengan bidang merah dan counter MCM; proporsi diukur tersendiri |
| 10/04 | MCM navy/merah, bar sayap navy–merah–navy terpisah |
| 10/05 | C merah lebar berterminal kotak, M navy ramping |
| 10/06 | M navy lebar/pendek, C merah kompak, roof/footer merah terpisah |
| 10/07 | Band bahu navy luar, M navy lebih kecil di dalam, cap/C merah, footer navy dan aksen ujung merah |

Semua sumber asli dibuka dan render sepuluh master ditinjau visual terhadap sumber: proporsi, bukaan huruf, sambungan dan celah antarelemen. Geometri ditulis manual per sumber, bukan auto-trace, raster atau font dalam SVG. Tekstur/gradasi diratakan ke merah #DC2626 dan navy #173257. Sisi M dirapikan secara simetris sesuai konsep sumber. Ujung aksen 10/07 yang lunak didekati segmen chamfer pendek, bukan kurva identik sumber. Ini bukan klaim salinan piksel atau persetujuan produksi.

## Audit dan validasi
- Audit SHA-256 pada **88 PNG unduhan** tidak menemukan file byte-identik pada subset tersebut. Audit visual seluruh folder belum selesai.
- Variasi bermotif serupa tidak otomatis digabung. Contoh 10/04 memiliki sayap tiga warna berbeda dari 7/06; 10/07 memiliki band luar dan counter ruang yang tidak terdapat pada 10/02.
- ID/hash SVG baru diperiksa agar tidak bertabrakan dengan master sebelumnya.
- Tes kesamaan koordinat SVG–JSON, warna, fill-rule evenodd, kontur tertutup, luas bukan nol, batas koordinat dan kontur menyilang secara proper.
- Sampel tambahan memeriksa celah band luar/inner M 10/07, celah sayap, aperture C dan counter diamond/hexagon.
- Hash sumber, progres/persentase dan penahanan APK juga diperiksa. Tes tidak membuktikan kemiripan visual sempurna atau kelayakan cetak/bordir.

## Artefak
`perbandingan.html` mandiri/offline: sumber vs SVG, jumlah/sisa/persentase dan tombol latar putih/abu-abu. Setiap logo memiliki master `.svg`, native `.json` dan `-preview.png` hasil render. `progress.json` menyimpan ID Drive, SHA-256 dan cakupan audit.

Tidak ada build APK atau perubahan aset/katalog Android. ID/favorit lama tetap utuh. Job APK tetap ditahan `if: false`.

## Reproduksi
```sh
npm install --prefix .cache/mcm-redraw @resvg/resvg-js
python scripts/build_drive_batch_11.py
python -m unittest discover -s tests -p 'test_path_batches.py'
python -m unittest discover -s tests -p 'test*geometric*.py'
python -m unittest discover -s tests -p 'test_variation_vectors.py'
```
Generator membutuhkan sumber lokal `google_drive/` dan resvg. Unduhan mentah tidak dimasukkan Git; HTML membawa sumber untuk review offline. Progres batch terdahulu adalah snapshot historis.
