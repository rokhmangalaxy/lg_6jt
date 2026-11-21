# Batch 21 — 10 master rasio manual, tanpa APK

Sumber **rasio_1 15/08–09 dan 16/01–08**. ID keluarga rasio tetap terpisah dari berisi. Nama PNG, Drive ID, SHA-256 dan lokasi master SVG/JSON dicatat di `progress.json`.

## Konstruksi spesifik sumber

| Sumber rasio | Struktur |
|---|---|
| 15/08 | Bingkai kotak dua bagian navy/merah dengan celah diagonal, MCM navy |
| 15/09 | Chevron merah atas, dua puncak navy menyatu, MCM navy, baseline merah |
| 16/01 | Diamond merah, cap/alas navy utuh terpisah, MCM putih positif |
| 16/02 | Empat facet luar merah, M navy oblique, C navy tinggi dengan notch kecil bawah |
| 16/03 | Rail atas merah chamfer, rail bawah merah bertingkat, MCM navy |
| 16/04 | Atap merah dangkal, alas navy dangkal, M navy dan C merah tegak |
| 16/05 | Pilar merah terpisah dengan empat tip segitiga di dalam, MCM navy |
| 16/06 | Rail empat bagian merah/navy offset, M navy oblique dan C merah oblique |
| 16/07 | Atap merah terbelah, alas navy terbelah, M navy dan C navy tiga facet terpisah |
| 16/08 | Cap/alas merah, chevron samping navy terbuka, MCM navy |

Semua sepuluh referensi dibuka satu per satu dan render diperiksa kembali dalam montage. Titik ditulis manual berdasarkan proporsi masing-masing sumber, bukan auto-trace, font atau substitusi desain generik. Kurva C diregularisasi menjadi chamfer pendek. Huruf putih 16/01 adalah layer positif recolorable, bukan lubang. Celah antarsegmen tetap transparan. Tekstur warna diratakan merah/navy/putih solid. Hasil masih menunggu review visual pengguna, tidak diklaim pixel-perfect atau master produksi final.

## Progres dan audit terbatas

- **179 master Drive unik**, bertambah 10; redraw saja **179/342 = 52,34%**.
- **18 alias sumber duplikat terverifikasi** tetap diwariskan tanpa perubahan.
- Cakupan sumber **197/342 = 57,60%**; **145 sumber tersisa**.
- Sepuluh hash baru berbeda satu sama lain dan dari seluruh sumber master sebelumnya. Pemeriksaan dikunci sebelum ekspor; motif mirip tidak otomatis digabung.
- 342 adalah jumlah file yang sebelumnya dilaporkan, bukan total desain unik terverifikasi global. Audit hanya sumber unduhan; snapshot historis tidak diubah.

## Artefak dan validasi

10 SVG path-only, 10 JSON native, 10 PNG preview, provenance/progress dan HTML perbandingan mandiri/offline dengan toggle putih/abu-abu. Raster sumber hanya untuk pembanding, tidak ditanam di master SVG.

**104 tes lokal lulus:** 95 path-batch + 8 geometris + 1 variasi. Memeriksa SVG/JSON konsisten, batas/penutupan path, persilangan polygon, nonkolisi ID/geometri/hash, progres, alias tetap, layer putih positif dan C tersegmentasi, katalog tetap dan jeda job APK. Tidak ada tes perangkat Android baru.

**Tidak ada build APK, dispatch workflow, integrasi Android atau rilis.** Katalog tetap 105 variasi dan APK terakhir v1.0.42.

Reproduksi dengan PNG sumber lokal dan resvg:
```sh
python scripts/build_drive_batch_21.py
python -m unittest discover -s tests -p 'test_path_batches.py'
python -m unittest discover -s tests -p 'test*geometric*.py'
python -m unittest discover -s tests -p 'test_variation_vectors.py'
```
