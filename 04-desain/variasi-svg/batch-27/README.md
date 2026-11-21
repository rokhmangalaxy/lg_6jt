# Batch 27 — 10 master manual, tanpa APK

Sumber rasio_1 **4/05–09 + 5/01–05**. Nama PNG asli, Drive ID, SHA-256 dan lokasi master tercatat dalam `progress.json`. Semua sumber dibuka individual, lalu koordinat polygon ditulis manual per sumber tanpa auto-trace, font atau penggantian desain generik. Render diperiksa kembali dalam montage.

## Struktur spesifik sumber

| Sumber | Struktur |
|---|---|
| 4/05 | Empat facet hexagon terpisah merah/navy, M navy dan C merah panjang chamfer |
| 4/06 | Empat segmen rail merah zigzag terpisah dan MCM navy |
| 4/07 | Slab merah atas/bawah dengan chamfer sisi, MCM navy |
| 4/08 | Atap navy terbuka, flag segitiga samping merah, alas merah dan MCM navy |
| 4/09 | Emblem lipatan besar merah/navy, dua pier merah dalam dan MCM navy kompak di bawah |
| 5/01 | Diamond merah dengan empat tip navy terpisah dan MCM navy positif |
| 5/02 | C merah vertikal panjang dengan ujung diagonal, M navy diukur independen |
| 5/03 | Rail merah berujung datar dengan elevasi tengah, MCM navy dan C ber-chord pendek |
| 5/04 | Dua slab merah oblique, MCM navy miring |
| 5/05 | Empat facet frame terpisah merah/navy dan MCM navy angular |

Celah mengikuti latar; MCM navy 5/01 adalah bidang positif recolorable, bukan lubang. Batch ini tidak memakai bidang putih. Tekstur diratakan merah/navy solid, kurva diregularisasi dengan chamfer/chord pendek. Menunggu persetujuan visual pengguna; tidak diklaim pixel-perfect atau final produksi.

## Progres dan audit terbatas

- **239 master Drive unik** (+10); redraw saja **239/342 = 69,88%**.
- **18 alias sumber duplikat terverifikasi**, diwariskan tanpa perubahan.
- Cakupan sumber **257/342 = 75,15%**; **85 sumber tersisa**.
- Sepuluh hash baru berbeda satu sama lain dan dari sumber master terdahulu, diperiksa sebelum ekspor. Kemiripan motif tidak otomatis dianggap duplikat.
- 342 adalah jumlah file yang dilaporkan, bukan jumlah desain unik terverifikasi global. Snapshot historis tidak diubah.

## Artefak dan validasi

10 SVG path-only, 10 JSON native, 10 PNG preview, provenance/progress dan `perbandingan.html` mandiri/offline dengan referensi asli dan pilihan latar putih/abu-abu. Raster hanya referensi pembanding, bukan master.

**134 tes lokal lulus**: 125 path-batch, 8 geometris dan 1 variasi. Mencakup konsistensi SVG/JSON, penutupan/batas path, persilangan polygon, nonkolisi ID/geometri/hash, progres/alias, huruf navy positif, rail terpisah, katalog tetap dan jeda APK.

**Tidak ada build APK, dispatch workflow, integrasi Android atau rilis.** Katalog tetap 105 variasi, APK terakhir v1.0.42. Tidak ada tes perangkat Android baru.

Reproduksi dengan PNG sumber lokal dan resvg:
```sh
python scripts/build_drive_batch_27.py
python -m unittest discover -s tests -p 'test_path_batches.py'
python -m unittest discover -s tests -p 'test*geometric*.py'
python -m unittest discover -s tests -p 'test_variation_vectors.py'
```
