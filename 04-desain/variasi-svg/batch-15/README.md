# Batch 15 — 10 master manual, tanpa APK

Melanjutkan instruksi redraw-only. Tidak menjalankan Gradle atau workflow dispatch, tidak mengubah katalog Android, tidak membuat APK/rilis. Seluruh job APK tetap dijeda; katalog aplikasi tetap 105 variasi.

## Master baru
Sembilan sumber **berisi 15/01–09**, ditambah **rasio_1 14/02** dengan ID terpisah `exp-rasio-014-02`. Koordinat diukur manual dari referensi, bukan auto-trace, klasifikasi raster atau glyph font. Tekstur warna diratakan menjadi merah/navy/putih solid; proporsi dan sudut dirapikan secara geometris, bukan klaim pixel-perfect.

| Sumber | Struktur sumber yang dipertahankan |
|---|---|
| berisi 15/01 | Diamond merah solid dengan huruf MCM putih positif; bukan ring ganda 13/01 |
| berisi 15/02 | Rail hexagon navy atas/bawah terpisah, M navy, C merah |
| berisi 15/03 | MCM merah dan tiga bar navy pada setiap sisi; celah wing/letter tetap terbuka |
| berisi 15/04 | Atap navy terbuka di bawah; MCM merah dengan kaki M oblique |
| berisi 15/05 | Dua rail horizontal navy berujung chamfer, M blok dan C merah runcing |
| berisi 15/06 | C merah sangat tinggi, M merah membentuk diamond, dua sidebar navy terpisah |
| berisi 15/07 | Atap dan sidebar navy; M merah bertangkai luar tipis dan C merah |
| berisi 15/08 | Bingkai diamond empat bagian merah/navy dan MCM navy tinggi |
| berisi 15/09 | Bingkai chevron navy turun, M merah miring dan C merah tengah membuka kanan |
| rasio_1 14/02 | Atap merah, alas navy, MCM navy mendatar dengan C ber-chamfer pendek |

Sumber/renders dibuka dan dibandingkan visual. Draft 15/03 diperbaiki posisi puncak C dan celah sayapnya; draft 15/07 diperbaiki M luar yang tipis dan jarak C–M agar tidak saling menumpuk. Hasil masih menunggu review visual pengguna. Huruf putih pada 15/01 adalah layer warna positif yang bisa di-recolor, bukan lubang. Semua SVG master hanya path tanpa bitmap/font; PNG hanya preview.

## Audit duplikat dan progres
**berisi 14/02–09 identik byte/SHA-256 dengan berisi 13/02–09.** Dengan 14/01 yang sudah diperiksa batch sebelumnya, seluruh kelompok berisi 14 terpetakan sebagai alias kelompok 13. Tidak dibuat geometri/entri baru untuk duplikat. Identitas Drive dan hash dicatat dalam `progress.json`.

- Master unik baru: **10**; kumulatif **119**.
- Alias duplikat baru: **8**; kumulatif **18**.
- Total sumber tercakup: **137/342 = 40,06%**.
- Belum diproses: **205**.
- Redraw unik dibagi jumlah file: **119/342 = 34,80%**.

342 tetap jumlah file yang sebelumnya dilaporkan, bukan total desain unik yang sudah diaudit. Audit hash hanya mencakup PNG yang sudah diunduh, bukan seluruh folder. Tidak menganggap file dengan nomor sama lintas keluarga otomatis duplikat. Snapshot batch lama tidak ditulis ulang.

## Artefak dan validasi
- `perbandingan.html`: mandiri/offline, raster sumber sebagai pembanding dan SVG master sebagai hasil; toggle latar putih/abu-abu.
- 10 SVG, 10 JSON koordinat native, 10 PNG preview.
- `progress.json`: sumber/Drive ID/SHA-256, alias, progres, dan status menunggu persetujuan.
- **77 tes lokal lulus**: 68 tes batch path + 8 geometris + 1 variasi. Memeriksa kesamaan SVG/JSON, kontur tertutup, batas koordinat, persilangan proper polygon, ID/hash master berbeda dari batch sebelumnya, alias sumber bila tersedia, progres, katalog aplikasi tetap dan guard APK dijeda.
- Tidak mengklaim pengujian perangkat Android untuk batch desain ini.

Reproduksi dengan sumber lokal dan resvg yang sudah tersedia:
```sh
python scripts/build_drive_batch_15.py
python -m unittest discover -s tests -p 'test_path_batches.py'
python -m unittest discover -s tests -p 'test*geometric*.py'
python -m unittest discover -s tests -p 'test_variation_vectors.py'
```
