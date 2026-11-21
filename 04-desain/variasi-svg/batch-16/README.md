# Batch 16 — 10 master vektor manual, tanpa APK

Melanjutkan redraw-only: tidak menjalankan Gradle, tidak dispatch build, tidak mengubah katalog Android atau merilis APK. Job APK tetap `if: false`; katalog aplikasi tetap 105 variasi.

## Sumber dan struktur

Sembilan sumber **berisi 16/01–09**, ditambah **rasio_1 14/03** (ID `exp-rasio-014-03`). Setiap sumber diunduh, dibuka dan dibandingkan dengan render. Koordinat ditulis manual sesuai struktur masing-masing, bukan auto-trace, segmentasi raster, atau substitusi font. Tekstur diratakan ke merah/navy/putih solid. Sudut dan proporsi dirapikan secara geometris; bukan klaim pixel-perfect atau produksi final. Menunggu review visual pengguna.

| Sumber | Ciri yang dipertahankan |
|---|---|
| berisi 16/01 | Diamond merah mendatar, empat ujung navy terpisah, MCM putih positif |
| berisi 16/02 | M navy tinggi dengan bahu miring; C merah bertip oblique |
| berisi 16/03 | Atap/alas merah berujung datar, MCM navy horizontal |
| berisi 16/04 | MCM navy miring kanan, cap dan alas merah memanjang |
| berisi 16/05 | Rail hexagon navy, bidang merah atas/bawah dan dua sisi; area huruf tidak diisi bidang merah |
| berisi 16/06 | C merah tengah dan cap/alas merah terpisah, M navy serta empat rail navy |
| berisi 16/07 | C merah tiga bidang lipatan dengan celah tipis; M navy bersegmen |
| berisi 16/08 | Segitiga merah atas/bawah terpisah, rail dua bagian dan MCM navy |
| berisi 16/09 | Bidang navy miring dengan MCM putih positif; rail merah atas/bawah |
| rasio_1 14/03 | Chevron merah turun, tiang navy tinggi terpisah, MCM navy horizontal |

C yang membulat pada sumber 16/01 dan rasio 14/03 direpresentasikan dengan segmen chamfer pendek yang diukur manual. Huruf putih adalah layer warna positif/recolorable, bukan lubang. Area di luar shape dan celah antarkomponen transparan. File SVG master hanya path, tanpa raster/font; PNG hanya preview.

## Progres dan audit terbatas

- **+10 master baru**, kumulatif **129 master Drive unik**.
- SHA-256 sepuluh sumber baru berbeda satu sama lain dan dari sumber master batch terdahulu; tidak ada alias baru pada batch ini. Kemiripan motif tidak otomatis dianggap duplikat.
- Alias duplikat terverifikasi tetap **18**, diwariskan tanpa perubahan dari batch 15.
- Total sumber tercakup **147/342 = 42,98%**; sisa **195** belum diproses.
- Redraw unik dibagi jumlah file **129/342 = 37,72%**.
- 342 tetap jumlah file yang sebelumnya dilaporkan, bukan jumlah desain unik terverifikasi. Audit hanya PNG yang sudah diunduh; bukan audit global Drive. Snapshot lama tidak diubah.

## Artefak dan validasi

`perbandingan.html` mandiri/offline berisi sumber raster pembanding dan SVG master; tombol latar putih/abu-abu untuk mengecek transparansi. Tersedia 10 SVG, 10 JSON koordinat native, 10 preview PNG, serta `progress.json` dengan nama sumber, Drive ID, SHA-256, progres dan alias.

**81 tes lokal lulus**: 72 batch-path, 8 geometris, 1 variasi. Pemeriksaan mencakup kesamaan SVG/JSON, kontur tertutup, batas kanvas, persilangan proper polygon, ID/geometri/hash sumber berbeda dari batch lain, progres, alias tidak berubah, katalog tetap dan build APK dijeda. Tidak menjalankan tes perangkat Android untuk batch desain-only ini.

Reproduksi memerlukan sumber lokal dan resvg yang sudah tersedia:
```sh
python scripts/build_drive_batch_16.py
python -m unittest discover -s tests -p 'test_path_batches.py'
python -m unittest discover -s tests -p 'test*geometric*.py'
python -m unittest discover -s tests -p 'test_variation_vectors.py'
```
