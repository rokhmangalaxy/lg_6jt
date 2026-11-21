# Batch 33 — 10 master manual, tanpa APK

Sumber rasio_1 **11/02–09 + 12/01–02**. Nama PNG, Drive ID, SHA-256 dan lokasi master ada di `progress.json`. Setiap sumber dibuka individual; koordinat polygon ditulis manual per sumber, bukan auto-trace, font atau substitusi generik. Render diperiksa dalam montage.

## Konstruksi spesifik sumber

| Sumber | Struktur |
|---|---|
| 11/02 | Dua bidang atap merah terpisah, baseline merah, M navy dan C tinggi mengikuti ridge |
| 11/03 | Dua cap hexagon navy, dua chevron merah di dalam, MCM navy dengan sisi luar miring |
| 11/04 | Dua rail merah bertangga, dua rail navy terpisah, MCM navy |
| 11/05 | Dua M navy angular berlawanan arah, C merah angular |
| 11/06 | Rail merah atas/bawah dengan takik, MCM navy ber-chamfer |
| 11/07 | Enam facet atap merah/navy terpisah, C merah panjang, dua M navy mengikuti perspektif |
| 11/08 | Empat spear navy, dua pentagon vertikal merah, MCM navy |
| 11/09 | Strip merah atas dan navy bawah dengan bevel offset, MCM navy |
| 12/01 | Diamond merah, empat tip navy dan MCM putih positif |
| 12/02 | Atap/alas merah dangkal terpisah, MCM navy |

Celah antarkomponen transparan mengikuti latar. Putih 12/01 adalah bidang positif recolorable, bukan lubang. Warna bertekstur diratakan menjadi merah/navy/putih solid. Kurva diregularisasi menjadi chord/chamfer pendek. Hasil menunggu review visual pengguna, tidak diklaim pixel-perfect atau final produksi.

## Progres dan audit terbatas

- **299 master Drive unik** (+10); redraw saja **299/342 = 87,43%**.
- **18 alias sumber duplikat terverifikasi**, diwariskan tanpa perubahan.
- Cakupan **317/342 = 92,69%**, **25 sumber tersisa**.
- Sepuluh hash baru berbeda satu sama lain dan dari sumber master terdahulu; generator memeriksa sebelum ekspor. Motif mirip tidak otomatis dianggap duplikat.
- 342 adalah jumlah file yang dilaporkan, bukan total desain unik terverifikasi global. Snapshot historis tidak diubah.

## Artefak dan validasi

10 SVG path-only, 10 JSON native, 10 PNG preview, progress/provenance dan HTML perbandingan mandiri/offline dengan referensi asli serta pilihan latar putih/abu-abu. Raster hanya referensi pembanding, bukan master.

**164 tes lokal lulus:** 155 path-batch, 8 geometris dan 1 variasi. Meliputi konsistensi SVG/JSON, batas/penutupan path, persilangan polygon, nonkolisi ID/geometri/hash, progres/alias, huruf putih positif, facet atap terpisah, katalog tetap dan jeda APK.

**Tidak ada build APK, dispatch workflow, integrasi Android atau rilis.** Katalog tetap 105 variasi; APK terakhir v1.0.42. Tidak ada tes perangkat Android baru.

Reproduksi dengan PNG sumber lokal dan resvg:
```sh
python scripts/build_drive_batch_33.py
python -m unittest discover -s tests -p 'test_path_batches.py'
python -m unittest discover -s tests -p 'test*geometric*.py'
python -m unittest discover -s tests -p 'test_variation_vectors.py'
```
