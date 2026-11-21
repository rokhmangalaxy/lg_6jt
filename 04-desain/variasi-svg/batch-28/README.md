# Batch 28 — 10 master manual, tanpa APK

Sumber rasio_1 **5/06–09 + 6/01–06**. Nama sumber, Drive ID, SHA-256 dan lokasi master dicatat di `progress.json`. Semua sumber dibuka individual; koordinat polygon ditulis manual per sumber tanpa auto-trace, font atau penggantian desain generik. Render diperiksa kembali dalam montage.

## Konstruksi spesifik sumber

| Sumber | Struktur |
|---|---|
| 5/06 | M navy dengan kaki berkait ke dalam, C merah angular panjang |
| 5/07 | Ring hexagon navy dengan counter transparan, inset merah dan MCM putih positif |
| 5/08 | C merah vertikal runcing dengan ujung diagonal, dua M navy diukur independen |
| 5/09 | Enam rail sayap navy terpisah, cap/alas merah terbuka dan MCM navy sempit |
| 6/01 | Diamond merah, empat tip navy terpisah, MCM putih positif angular |
| 6/02 | Cap/alas merah terbuka dan MCM navy kompak |
| 6/03 | Cap merah bertingkat terbelah, dua facet dalam navy, dua rail alas merah/navy dan arrow navy |
| 6/04 | Ring merah dengan window transparan, dua segitiga merah dalam dan MCM navy |
| 6/05 | Rail dan C merah oblique, M navy miring |
| 6/06 | Enam facet frame merah/navy terpisah dan MCM navy tapered |

Celah antarkomponen mengikuti latar. Bidang putih 5/07 dan 6/01 positif recolorable, bukan lubang. Ring memakai counter evenodd transparan. Tekstur diratakan merah/navy/putih solid; kurva diregularisasi menjadi chord/chamfer pendek. Hasil menunggu persetujuan visual, tidak diklaim pixel-perfect atau final produksi.

## Progres dan audit terbatas

- **249 master Drive unik** (+10); redraw saja **249/342 = 72,81%**.
- **18 alias sumber duplikat terverifikasi**, diwariskan tanpa perubahan.
- Cakupan sumber **267/342 = 78,07%**, **75 sumber tersisa**.
- Sepuluh hash sumber baru berbeda satu sama lain dan dari sumber master terdahulu, diperiksa sebelum ekspor. Motif mirip tidak otomatis dianggap duplikat.
- 342 adalah jumlah file yang dilaporkan, bukan jumlah desain unik terverifikasi global. Snapshot historis tidak diubah.

## Artefak dan validasi

10 SVG path-only, 10 JSON native, 10 PNG preview, provenance/progress dan HTML perbandingan mandiri/offline dengan referensi asli serta pilihan latar putih/abu-abu. Raster hanya referensi pembanding, bukan master.

**139 tes lokal lulus**: 130 path-batch, 8 geometris dan 1 variasi. Mencakup konsistensi SVG/JSON, batas/penutupan path, persilangan polygon, nonkolisi ID/geometri/hash, progres/alias, huruf putih positif, counter ring, katalog tetap serta jeda APK.

**Tidak ada build APK, dispatch workflow, integrasi Android atau rilis.** Katalog tetap 105 variasi; APK terakhir v1.0.42. Tidak ada tes perangkat Android baru.

Reproduksi dengan PNG sumber lokal dan resvg:
```sh
python scripts/build_drive_batch_28.py
python -m unittest discover -s tests -p 'test_path_batches.py'
python -m unittest discover -s tests -p 'test*geometric*.py'
python -m unittest discover -s tests -p 'test_variation_vectors.py'
```
