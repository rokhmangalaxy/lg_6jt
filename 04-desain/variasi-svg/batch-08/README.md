# Batch 08 — 10 master path manual

## Progres kumulatif
| Status | Jumlah |
|---|---:|
| Sudah redraw / memiliki master path | **58 dari 342 sumber** |
| Sisa belum diproses | **284 sumber** |
| Progres | **16,96%** |
| Penambahan batch ini | **10 sumber** |

Rumus: `58 / 342 × 100 = 16,959...%`, dibulatkan dua desimal. Penyebut 342 adalah jumlah file Drive yang sebelumnya dilaporkan, **bukan jumlah desain unik terverifikasi**. Progres menghitung sumber dengan master path, bukan persetujuan visual/produksi. Dua studi tambahan aplikasi tidak dihitung sebagai sumber Drive.

- Kelompok 1–6: masing-masing **9/9** sumber memiliki master.
- Kelompok 7: **01–04** memiliki master. Sisa kelompok belum dilisting; pending kosong di JSON tidak berarti kelompok selesai.
- Batch ini: kelompok 6/04–09 dan 7/01–04.
- Semua hasil baru masih **menunggu review visual pengguna**.

## Review bentuk per sumber
| Sumber | Ciri spesifik yang dipertahankan |
|---|---|
| 6/04 | MCM merah dengan cap/footer navy melebar, bukan bingkai tertutup |
| 6/05 | Bidang tengah merah dengan counter C transparan, bahu M navy bersudut |
| 6/06 | Diamond pecah empat elemen: dua arah navy samping, atap/kaki merah |
| 6/07 | M merah sangat tinggi dengan lekukan tengah bersudut, footer navy tunggal |
| 6/08 | Hexagon navy tegak, inset merah dan counter MCM; proporsi diukur tersendiri, bukan SVG 5/03 yang dipakai ulang |
| 6/09 | M merah, C navy, chevron navy bawah dan stripe merah bawah terpisah |
| 7/01 | MCM seluruhnya merah tanpa bingkai; C tinggi dengan terminal diagonal |
| 7/02 | Hexagon navy padat dengan MCM sebagai lubang transparan |
| 7/03 | Diamond merah terbuka dengan bar horizontal samping independen |
| 7/04 | Shield merah dengan dinding dalam bertingkat di samping MCM navy |

Sepuluh sumber asli telah dibuka. Render semua master ditinjau visual terhadap sumber untuk proporsi, urutan warna, bukaan huruf, dan pemisahan elemen. Koordinat ditulis manual per sumber, bukan auto-trace atau font. Tekstur/gradasi diratakan ke merah #DC2626 / navy #173257. M kiri/kanan disimetriskan sesuai konsep; perbedaan kecil raster dirapikan, bukan klaim salinan identik piksel atau persetujuan produksi.

## Duplikat dan validasi
- Audit SHA-256 pada **58 PNG unduhan** tidak menemukan file byte-identik. Audit visual seluruh Drive belum selesai.
- Geometri SVG dan ID baru diperiksa agar tidak bertabrakan dengan master sebelumnya.
- Tes SVG–JSON memeriksa koordinat sama, warna, fill-rule, kontur tertutup, luas bukan nol, batas koordinat dan kontur menyilang secara proper.
- Sampel negatif/positif tambahan memeriksa counter C bidang tengah, counter hexagon, gap bar diamond terbuka, gap diamond pecah, serta pemisahan chevron navy dan stripe merah.
- Progres, persentase, hash sumber dan penahanan APK juga diperiksa. Tes bukan pembuktian kemiripan visual sempurna atau kesiapan bordir/cetak.

## Artefak
`perbandingan.html` mandiri/offline menampilkan sumber asli dan redraw SVG berdampingan, jumlah/sisa/persentase, serta tombol latar putih/abu-abu untuk memeriksa transparansi. Setiap logo mempunyai `.svg`, native `.json`, dan `-preview.png` hasil render. `progress.json` merekam ID Drive, SHA-256 dan cakupan audit.

Tidak ada build APK atau perubahan katalog/aset Android. ID/favorit lama tetap utuh. Job APK tetap ditahan `if: false`.

## Reproduksi
```sh
npm install --prefix .cache/mcm-redraw @resvg/resvg-js
python scripts/build_drive_batch_08.py
python -m unittest discover -s tests -p 'test_path_batches.py'
python -m unittest discover -s tests -p 'test*geometric*.py'
python -m unittest discover -s tests -p 'test_variation_vectors.py'
```
Generator memerlukan sumber lokal di `google_drive/` dan resvg. Unduhan mentah tidak dimasukkan Git; HTML perbandingan memuat sumber untuk review offline. Progres batch terdahulu merupakan snapshot historis.
