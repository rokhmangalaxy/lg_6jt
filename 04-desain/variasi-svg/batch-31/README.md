# Batch 31 — 10 master manual, tanpa APK

Sumber rasio_1 **8/09 + 9/01–09**. Nama PNG, Drive ID, SHA-256 dan lokasi master ada di `progress.json`. Semua sumber dibuka individual; koordinat polygon ditulis manual per sumber, bukan auto-trace, font atau substitusi desain generik. Render diperiksa kembali dalam montage.

## Konstruksi spesifik sumber

| Sumber | Struktur |
|---|---|
| 8/09 | Dua flag diagonal merah terpisah dan MCM navy oblique |
| 9/01 | Diamond merah, empat tip navy terpisah, MCM navy positif |
| 9/02 | Lipatan merah mengarah bawah, pier luar navy dan pier dalam merah, MCM navy kompak |
| 9/03 | Empat rail navy terpisah dengan chamfer, MCM merah |
| 9/04 | M navy oblique, C merah, stripe merah dan baseline navy berkait |
| 9/05 | Empat facet frame merah terbelah, M navy dan C navy panjang ber-chord pendek |
| 9/06 | M navy bersayap dengan kaki runcing, C merah angular |
| 9/07 | Box perspektif: atap/alas dan wall dekat merah, empat panel jauh navy terpisah, MCM navy perspektif |
| 9/08 | Dua pier navy tinggi, lipatan M merah positif, MCM navy di bawah |
| 9/09 | Cap/alas merah dangkal berujung datar, MCM navy lebar dengan C ber-chord pendek |

Celah antarkomponen mengikuti latar. Huruf navy 9/01 adalah bidang positif recolorable, bukan lubang. Batch ini tidak memakai bidang putih. Tekstur diratakan merah/navy solid; kurva diregularisasi menjadi chord/chamfer pendek. Hasil menunggu persetujuan visual pengguna, tidak diklaim pixel-perfect atau final produksi.

## Progres dan audit terbatas

- **279 master Drive unik** (+10); redraw saja **279/342 = 81,58%**.
- **18 alias sumber duplikat terverifikasi**, diwariskan tanpa perubahan.
- Cakupan sumber **297/342 = 86,84%**, **45 sumber tersisa**.
- Sepuluh hash baru berbeda satu sama lain dan dari sumber master terdahulu; generator memeriksanya sebelum ekspor. Motif mirip tidak otomatis dianggap duplikat.
- 342 adalah jumlah file yang dilaporkan, bukan jumlah desain unik terverifikasi global. Snapshot historis tidak diubah.

## Artefak dan validasi

10 SVG path-only, 10 JSON native, 10 PNG preview, provenance/progress dan HTML perbandingan mandiri/offline dengan referensi asli serta pilihan latar putih/abu-abu. Raster hanya referensi pembanding, bukan master.

**154 tes lokal lulus**: 145 path-batch, 8 geometris dan 1 variasi. Meliputi konsistensi SVG/JSON, penutupan/batas path, persilangan polygon, nonkolisi ID/geometri/hash, progres/alias, huruf navy positif, panel perspektif terpisah, katalog tetap dan jeda APK.

**Tidak ada build APK, dispatch workflow, integrasi Android atau rilis.** Katalog tetap 105 variasi; APK terakhir v1.0.42. Tidak ada tes perangkat Android baru.

Reproduksi dengan PNG sumber lokal dan resvg:
```sh
python scripts/build_drive_batch_31.py
python -m unittest discover -s tests -p 'test_path_batches.py'
python -m unittest discover -s tests -p 'test*geometric*.py'
python -m unittest discover -s tests -p 'test_variation_vectors.py'
```
