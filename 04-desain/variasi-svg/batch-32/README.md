# Batch 32 — 10 master manual, tanpa APK

Sumber rasio_1 **10/01–09 + 11/01**. Provenance nama PNG, Drive ID, SHA-256 dan lokasi master tercatat dalam `progress.json`. Sumber dibuka individual dan polygon diukur manual per sumber; bukan auto-trace, font, atau substitusi generik. Render diperiksa ulang.

## Konstruksi spesifik sumber

| Sumber | Struktur |
|---|---|
| 10/01 | Diamond merah lebar, empat tip navy terpisah, MCM navy positif |
| 10/02 | Gable navy dengan kaki vertikal, lipatan tengah merah, MCM merah |
| 10/03 | Ring persegi navy berlubang, dua trapezoid merah, MCM navy |
| 10/04 | Dua bar merah oblique terpisah, MCM navy miring |
| 10/05 | Konstruksi perspektif I/M/I navy, cap dan dua alas merah, MCM navy terpisah di bawah |
| 10/06 | Ring hexagon navy berlubang, bidang merah, MCM dan dua garis putih positif |
| 10/07 | Dua cap hexagon navy, empat flange merah terpisah dan MCM merah |
| 10/08 | MCM navy angular, dua insert segitiga merah positif |
| 10/09 | Dua bar merah, empat stub diagonal navy terpisah, MCM navy kompak |
| 11/01 | Diamond merah lebih dangkal, empat tip navy, MCM navy dengan C chamfer; diukur terpisah dari 10/01 |

Celah antarkomponen transparan mengikuti latar. Putih 10/06 adalah bidang positif recolorable, bukan lubang. Ring 10/03 dan 10/06 memakai evenodd. Tekstur diratakan menjadi warna solid; kurva diregularisasi dengan chord/chamfer pendek. Menunggu review visual pengguna; tidak diklaim pixel-perfect atau final produksi.

## Progres dan audit terbatas

- **289 master Drive unik** (+10); redraw saja **289/342 = 84,50%**.
- **18 alias sumber duplikat terverifikasi**, diwariskan tanpa perubahan.
- Cakupan **307/342 = 89,77%**, **35 sumber tersisa**.
- Sepuluh hash baru berbeda satu sama lain dan dari sumber master terdahulu; diperiksa sebelum ekspor. Motif mirip tidak otomatis disamakan.
- 342 adalah jumlah file yang dilaporkan, bukan total desain unik yang telah diaudit global. Snapshot historis tetap.

## Artefak dan validasi

10 SVG path-only, 10 JSON native, 10 PNG preview, progress/provenance serta HTML mandiri/offline berisi referensi asli dan toggle latar putih/abu-abu. Raster hanya referensi, bukan master.

**159 tes lokal lulus:** 150 path-batch, 8 geometris, 1 variasi. Mencakup konsistensi SVG/JSON, batas/penutupan path, persilangan polygon, nonkolisi ID/geometri/hash, progres/alias, huruf putih positif, ring transparan, katalog tetap serta jeda APK.

**Tidak ada build APK, dispatch workflow, integrasi Android atau rilis.** Katalog tetap 105 variasi; APK terakhir v1.0.42. Tidak ada pengujian perangkat Android baru.

Reproduksi dengan sumber PNG lokal dan resvg:
```sh
python scripts/build_drive_batch_32.py
python -m unittest discover -s tests -p 'test_path_batches.py'
python -m unittest discover -s tests -p 'test*geometric*.py'
python -m unittest discover -s tests -p 'test_variation_vectors.py'
```
