# Batch 30 — 10 master manual, tanpa APK

Sumber rasio_1 **7/08–09 + 8/01–08**. Nama PNG, Drive ID, SHA-256 dan lokasi master ada di `progress.json`. Semua sumber dibuka individual sebelum polygon ditulis manual per sumber, tanpa auto-trace, font atau substitusi generik. Render diperiksa dalam montage; M kanan 7/09 dicerminkan agar kaki luar tidak menyentuh alas merah.

## Konstruksi spesifik sumber

| Sumber | Struktur |
|---|---|
| 7/08 | Enam panel atap terpisah merah/navy, MCM navy dan baseline merah |
| 7/09 | Cap navy, dua facet alas merah terbelah dan MCM navy |
| 8/01 | Diamond merah, empat tip navy terpisah, MCM putih positif |
| 8/02 | Atap merah dengan dua tip navy terpisah, MCM navy dan dua baseline merah/navy |
| 8/03 | Cap/alas navy terbuka, MCM merah angular |
| 8/04 | Rail merah miring bertingkat, MCM navy dengan aperture C diagonal |
| 8/05 | Cap/alas merah, C merah dan dua facet bahu navy terpisah |
| 8/06 | Dua flange merah dan dua rail navy terpisah, rail atas bergigi dua, MCM navy |
| 8/07 | C merah vertikal dengan ujung diagonal dan dua M navy berbahu bergerigi |
| 8/08 | MCM merah dan empat rail merah terpisah, dua tip diamond navy vertikal |

Celah antarkomponen mengikuti latar; huruf putih 8/01 adalah bidang positif recolorable, bukan lubang. Tekstur sumber diratakan menjadi warna solid; kurva diregularisasi menjadi chord/chamfer pendek. Menunggu persetujuan visual pengguna; tidak diklaim pixel-perfect atau final produksi.

## Progres dan audit terbatas

- **269 master Drive unik** (+10); redraw saja **269/342 = 78,65%**.
- **18 alias sumber duplikat terverifikasi**, diwariskan tanpa perubahan.
- Cakupan sumber **287/342 = 83,92%**, **55 sumber tersisa**.
- Sepuluh hash baru berbeda satu sama lain dan dari sumber master terdahulu; diperiksa sebelum ekspor. Kemiripan motif tidak otomatis dianggap duplikat.
- 342 adalah jumlah file yang dilaporkan, bukan jumlah desain unik terverifikasi global. Snapshot historis tidak diubah.

## Artefak dan validasi

10 SVG path-only, 10 JSON native, 10 PNG preview, provenance/progress dan HTML perbandingan mandiri/offline dengan sumber asli serta pilihan latar putih/abu-abu. Raster hanya referensi pembanding, bukan master.

**149 tes lokal lulus**: 140 path-batch, 8 geometris dan 1 variasi. Meliputi konsistensi SVG/JSON, penutupan/batas path, persilangan polygon, nonkolisi ID/geometri/hash, progres/alias, bidang putih positif, panel atap/rail terpisah serta katalog tetap dan jeda APK.

**Tidak ada build APK, dispatch workflow, integrasi Android atau rilis.** Katalog tetap 105 variasi; APK terakhir v1.0.42. Tidak ada tes perangkat Android baru.

Reproduksi dengan PNG sumber lokal dan resvg:
```sh
python scripts/build_drive_batch_30.py
python -m unittest discover -s tests -p 'test_path_batches.py'
python -m unittest discover -s tests -p 'test*geometric*.py'
python -m unittest discover -s tests -p 'test_variation_vectors.py'
```
