# Batch 35 — 10 master manual, tanpa APK

Sumber **rasio 13/04–09 + rasio_1 tanpa nomor tambahan /01–04**. Kelompok terakhir memiliki nama asli `Max_a_Gambar_kotak_rasio_1_logo-NN.png`, berbeda dari `Max_a_Gambar_kotak_rasio_1_1_logo-NN.png`. ID master memakai `exp-rasio-unnumbered-NN`; group=0 hanyalah sentinel internal, bukan nomor pada sumber. Nama, Drive ID, SHA-256 dan lokasi master ada dalam `progress.json`.

Setiap sumber dibuka individual. Polygon diukur manual per sumber, bukan auto-trace, font atau substitusi generik. Render diperiksa dalam montage.

## Konstruksi spesifik sumber

| Sumber | Struktur |
|---|---|
| 13/04 | Dua rail merah bertekuk terpisah dan MCM navy ber-chamfer |
| 13/05 | Dua M navy mengarah luar, C merah block dan dua insert merah diagonal |
| 13/06 | Dua bar merah miring naik, MCM navy mengikuti kemiringan sumber |
| 13/07 | C merah tinggi hexagonal, dua M navy bersayap |
| 13/08 | Dua rail navy dengan empat lubang mounting transparan, MCM merah positif |
| 13/09 | Dua cap hexagon merah terpisah, MCM navy tinggi |
| Tanpa nomor /01 | Diamond merah, cap/alas navy kontinu, MCM putih positif |
| Tanpa nomor /02 | Frame M navy dan merah bersarang terbuka bawah, MCM navy kecil |
| Tanpa nomor /03 | Cap/alas merah dangkal dan dua isi segitiga terpisah, MCM navy |
| Tanpa nomor /04 | Dua bar merah datar terpisah, MCM navy oblique |

Lubang 13/08 mengikuti latar, bukan diisi putih. Empat lubang kecil diregularisasi dengan polygon 16 sisi pada posisi terukur. Huruf putih tanpa nomor /01 adalah bidang positif recolorable. Warna bertekstur diratakan menjadi solid, kurva diregularisasi dengan chord/chamfer pendek. Hasil menunggu review visual pengguna; tidak diklaim pixel-perfect atau final produksi.

## Progres dan audit terbatas

- **319 master Drive unik** (+10); redraw saja **319/342 = 93,27%**.
- **18 alias sumber duplikat terverifikasi**, diwariskan tanpa perubahan.
- Cakupan **337/342 = 98,54%**, **5 sumber tersisa** terhadap jumlah file yang dilaporkan.
- Sepuluh hash baru berbeda satu sama lain dan dari sumber master terdahulu; generator memeriksa sebelum ekspor. Motif mirip tidak otomatis dianggap duplikat.
- Pencarian nama logo-01 menemukan kelompok rasio tanpa nomor tambahan yang belum diproses. Pencarian `contains` pada nama dapat mengembalikan kelompok bernomor juga; pencarian nama persis dipakai untuk /02–04.
- 342 bukan total desain unik terverifikasi global. Snapshot historis tidak diubah. Lima sumber berikutnya perlu dicari dan diverifikasi, bukan diasumsikan selesai.

## Artefak dan validasi

10 SVG path-only, 10 JSON native, 10 PNG preview, progress/provenance dan HTML mandiri/offline dengan referensi asli serta pilihan latar putih/abu-abu. Raster hanya referensi pembanding, bukan master.

**174 tes lokal lulus:** 165 path-batch, 8 geometris dan 1 variasi. Mencakup konsistensi SVG/JSON, batas/penutupan path, persilangan polygon, nonkolisi ID/geometri/hash, progres/alias, huruf putih positif, empat lubang mounting, identitas kelompok tanpa nomor, katalog tetap dan jeda APK.

**Tidak ada build APK, dispatch workflow, integrasi Android atau rilis.** Katalog tetap 105 variasi; APK terakhir v1.0.42. Tidak ada tes perangkat Android baru.

Reproduksi dengan PNG sumber lokal dan resvg:
```sh
python scripts/build_drive_batch_35.py
python -m unittest discover -s tests -p 'test_path_batches.py'
python -m unittest discover -s tests -p 'test*geometric*.py'
python -m unittest discover -s tests -p 'test_variation_vectors.py'
```
