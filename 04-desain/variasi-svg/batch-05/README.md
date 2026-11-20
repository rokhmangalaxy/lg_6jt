# Batch 05 — kapasitas penuh 10 master manual

## Cakupan dan progres
- Kelompok 3: **01–09** dibuat path → kelompok 3 memiliki master **9/9**.
- Kelompok 4: **01** dibuat path. Nomor 02–09 belum dilisting; daftar pending pada JSON merupakan perkiraan dari pola nama, bukan inventaris terverifikasi.
- Kelompok 1 dan 2 tetap masing-masing **9/9**.
- Total kumulatif: **28 sumber Drive** memiliki master path. Dari **342 file yang sebelumnya dilaporkan**, **314 belum diproses**. Bukan klaim 342 desain unik.
- Dua studi tambahan di aplikasi tidak dihitung sebagai sumber Drive.
- Seluruh redraw baru berstatus **menunggu review visual pengguna**, bukan desain final produksi.

## Penilaian visual per sumber
| Sumber | Ciri yang dipertahankan | Catatan review geometris |
|---|---|---|
| 3/01 | Diamond merah padat, counter MCM transparan, C berujung lunak | Ujung lengkung sumber didekati segmen chamfer pendek; bukan kurva identik piksel |
| 3/02 | Bingkai hexagon navy, MCM merah, C lebih tinggi dari M | M kiri/kanan disimetriskan; bingkai tetap terpisah |
| 3/03 | MCM navy tanpa atap, chevron merah bawah | Celah antara huruf dan chevron tetap terbuka |
| 3/04 | Bingkai persegi panjang navy, C chamfer | Proporsi lebar bingkai dan ruang kosong dipertahankan |
| 3/05 | Diamond lebar navy, inset merah, counter MCM | Tidak menambahkan aksen segitiga 2/09; berbeda proporsi |
| 3/06 | Cap dan footer navy dengan sambungan terputus/offset | Sambungan tidak dipaksa simetris karena memang bagian dari sumber |
| 3/07 | Tiga strip sayap merah per sisi, MCM navy | Strip independen, ruang pemisah tidak tertutup |
| 3/08 | Hexagon tegak, C merah sangat tinggi, M sempit | Tidak memakai ulang geometri 3/02 walaupun konsep serupa |
| 3/09 | Diamond terbuka, tip navy, M/cap merah, C navy terbelah | Celah transparan pusat tetap terbuka pada kepala dan kaki |
| 4/01 | Diamond merah padat, C tajam dan M tinggi | Tidak disamakan dengan 3/01 yang ujung C dan proporsinya berbeda |

Sepuluh sumber asli dan hasil render master telah dibuka/diperiksa secara visual. Geometri ditulis manual per sumber; tidak ada auto-trace atau klasifikasi piksel untuk membentuk path. Warna bertekstur diratakan ke palet kerja merah #DC2626 / navy #173257. Sisi M dicerminkan bila sesuai sumber. Koreksi geometri tidak dimaksudkan sebagai redesign gaya.

## Artefak
- `perbandingan.html`: mandiri/offline, raster sumber versus SVG redraw, tombol latar putih/abu-abu untuk memeriksa transparansi.
- `exp-GGG-NN.svg`: master transparan, hanya path M/L/Z; tanpa font atau raster.
- `exp-GGG-NN.json`: native path dari koordinat yang sama dengan SVG.
- `*-preview.png`: render master untuk pemeriksaan, bukan sumber geometri.
- `progress.json`: asal Drive, SHA-256, progres dan batas cakupan audit.

Audit SHA-256 pada **28 PNG yang sudah diunduh** tidak menemukan file byte-identik. Sepuluh layout baru ditinjau sebagai bentuk berbeda; kemiripan motif bukan alasan menggabungkan otomatis. Audit visual seluruh folder masih belum selesai. Geometri SVG baru juga diperiksa agar tidak byte-identik dengan master yang sudah ada.

## Validasi dan batasan
Tes otomatis memeriksa kesamaan koordinat SVG/JSON, fill-rule evenodd, kontur tertutup, luas bukan nol, batas koordinat, warna, ID/provenance, kontur yang menyilang secara proper, serta sampel ruang negatif/celah transparan. Tes tersebut tidak membuktikan kemiripan visual sempurna atau kelayakan bordir/cetak; persetujuan visual dan sampel vendor tetap diperlukan.

Tidak ada perubahan aset/katalog Android dan tidak ada build APK. Job build tetap `if: false`. Pemicu validasi desain diperluas agar perubahan SVG/scripts/tests menjalankan tes tanpa Gradle/SDK/APK. Semua ID favorit tetap utuh.

## Reproduksi
```sh
npm install --prefix .cache/mcm-redraw @resvg/resvg-js
python scripts/build_drive_batch_05.py
python -m unittest discover -s tests -p 'test_path_batches.py'
python -m unittest discover -s tests -p 'test*geometric*.py'
python -m unittest discover -s tests -p 'test_variation_vectors.py'
```
Generator membutuhkan sumber lokal `google_drive/` dan resvg. `scripts/design_batch_io.py` mengekspor artefak/provenance saja; tidak menggambar atau men-trace sumber. Sumber unduhan lokal tidak dimasukkan ke Git; HTML perbandingan memuat salinan sumber untuk review offline.
