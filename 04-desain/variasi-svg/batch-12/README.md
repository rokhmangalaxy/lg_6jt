# Batch 12 — 10 master path manual

## Progres kumulatif
| Status | Jumlah |
|---|---:|
| Sudah redraw / memiliki master path | **98 dari 342 sumber** |
| Sisa belum diproses | **244 sumber** |
| Progres | **28,65%** |
| Penambahan batch ini | **10 sumber** |

Rumus `98 / 342 × 100 = 28,654...%`, dibulatkan dua desimal. Penyebut 342 adalah jumlah file Drive yang sebelumnya dilaporkan, **bukan total desain unik terverifikasi**. Persentase menghitung sumber dengan master path, bukan persetujuan visual/produksi. Dua studi tambahan aplikasi tidak dihitung sebagai sumber Drive.

- Kelompok 1–10: masing-masing **9/9** sumber memiliki master.
- Kelompok 11: **01–08** memiliki master; **09** sudah terdaftar tetapi belum diunduh/redraw.
- Batch ini: kelompok 10/08–09 dan 11/01–08.
- Semua master baru **menunggu review visual pengguna**.

## Review bentuk per sumber
| Sumber | Ciri spesifik yang dipertahankan |
|---|---|
| 10/08 | Sayap atas merah, dua strip navy di bawah; M navy dan C merah |
| 10/09 | Atap segitiga merah sangat tinggi, M navy, C/kaki merah |
| 11/01 | Seluruh MCM merah, C lebar dengan aperture besar |
| 11/02 | MCM navy di antara cap dan rel bawah merah lebar |
| 11/03 | MCM navy, wing/tab atas merah serta dua rel diagonal merah bawah |
| 11/04 | MCM navy oblique dengan cap merah atas/kiri dan stripe bawah; M tidak dicerminkan |
| 11/05 | V navy bawah dengan ujung tersapu naik, MCM merah |
| 11/06 | C navy dengan terminal miring, M merah dengan lekukan V atas sempit |
| 11/07 | Diamond navy, MCM merah positif dan segitiga tip merah terpisah |
| 11/08 | MCM navy horizontal bersudut, C chamfer dan cap/footer merah |

Semua sumber dibuka dan hasil render seluruh master ditinjau visual terhadap sumber. Master 11/07 dikoreksi setelah render pertama: MCM adalah **huruf merah positif**, bukan counter pada bidang merah penuh. Setelah koreksi render dibuka ulang; celah tip, antarahuruf, dan aperture C diperiksa.

Koordinat ditulis manual per sumber, bukan auto-trace, raster atau font di SVG. Tekstur/gradasi diratakan ke merah #DC2626 / navy #173257. Simetri M dirapikan bila sesuai konsep. Desain 11/04 tetap oblique dan asimetris sesuai sumber, tidak dipaksa menjadi desain tegak. Ini bukan klaim salinan identik piksel atau persetujuan produksi.

## Audit dan validasi
- SHA-256 **98 PNG unduhan**: tidak ditemukan file byte-identik pada subset tersebut. Audit visual seluruh folder Drive belum selesai.
- Motif mirip tidak otomatis digabung. Contoh 10/08 berbeda urutan warna sayap dari 10/04; 11/07 memakai huruf positif berbeda dari diamond berbidang merah dengan counter.
- ID dan hash SVG baru diperiksa agar tidak bertabrakan dengan master sebelumnya.
- Tes kesamaan koordinat SVG–JSON, warna, fill-rule evenodd, kontur tertutup, luas bukan nol, batas koordinat, dan kontur menyilang secara proper.
- Sampel tambahan memeriksa huruf positif 11/07, celah tip dan antarahuruf, gap wing, aperture C pada bentuk blok dan miring.
- Hash sumber, progres/persentase, serta penahanan APK juga diperiksa. Tes tidak membuktikan kemiripan visual sempurna atau kelayakan cetak/bordir.

## Artefak
`perbandingan.html` mandiri/offline: sumber vs SVG, jumlah/sisa/persentase, tombol latar putih/abu-abu. Setiap logo memiliki master `.svg`, native `.json`, dan `-preview.png` hasil render. `progress.json` merekam ID Drive, hash sumber, cakupan audit dan progres.

Tidak ada build APK atau perubahan aset/katalog Android. ID/favorit lama tetap utuh. Job APK tetap ditahan `if: false`.

## Reproduksi
```sh
npm install --prefix .cache/mcm-redraw @resvg/resvg-js
python scripts/build_drive_batch_12.py
python -m unittest discover -s tests -p 'test_path_batches.py'
python -m unittest discover -s tests -p 'test*geometric*.py'
python -m unittest discover -s tests -p 'test_variation_vectors.py'
```
Generator memerlukan sumber lokal `google_drive/` dan resvg. Unduhan mentah tidak dimasukkan Git; HTML membawa sumber untuk review offline. Progres batch terdahulu adalah snapshot historis.
