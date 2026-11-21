# Batch 29 — 10 master manual, tanpa APK

Sumber rasio_1 **6/07–09 + 7/01–07**. Nama PNG, Drive ID, SHA-256 dan lokasi master ada di `progress.json`. Seluruh sumber dibuka individual, polygon ditulis manual per sumber tanpa auto-trace, font atau substitusi desain generik. Render diperiksa kembali dalam montage; M kanan 7/06 dicerminkan agar kaki luar tetap terpisah dari facet frame.

## Konstruksi spesifik sumber

| Sumber | Struktur |
|---|---|
| 6/07 | M navy bersayap lebar, C merah dan dua chevron bawah merah/navy terpisah |
| 6/08 | Dua ring diamond navy/merah dengan counter transparan dan MCM navy positif |
| 6/09 | Cap navy luar dan cap merah dalam, M navy tinggi dan C merah |
| 7/01 | Diamond merah, cap/alas navy tunggal, MCM putih positif |
| 7/02 | Atap merah tebal dan MCM navy dengan C hexagonal berujung diagonal |
| 7/03 | Cap/alas merah dangkal dan MCM navy lebar |
| 7/04 | Enam facet ekstrusi rail merah atas/bawah terpisah dan MCM navy |
| 7/05 | Frame M merah besar terbuka, M navy dalam dan MCM navy kompak di bawah |
| 7/06 | Empat facet kompas merah/navy terpisah dan MCM navy |
| 7/07 | Dua bracket luar merah/navy terbuka saling mengapit, MCM navy kompak |

Celah antarkomponen mengikuti latar; huruf putih 7/01 positif recolorable, bukan lubang. Kedua ring 6/08 memakai counter evenodd transparan. Tekstur diratakan menjadi warna solid; kurva diregularisasi menjadi chord/chamfer pendek. Menunggu persetujuan visual pengguna, tidak diklaim pixel-perfect atau final produksi.

## Progres dan audit terbatas

- **259 master Drive unik** (+10); redraw saja **259/342 = 75,73%**.
- **18 alias sumber duplikat terverifikasi**, diwariskan tanpa perubahan.
- Cakupan sumber **277/342 = 80,99%**; **65 sumber tersisa**.
- Sepuluh hash sumber baru berbeda satu sama lain dan dari sumber master terdahulu, diperiksa sebelum ekspor. Motif mirip tidak otomatis dianggap duplikat.
- 342 adalah jumlah file yang dilaporkan, bukan jumlah desain unik terverifikasi global. Snapshot historis tidak diubah.

## Artefak dan validasi

10 SVG path-only, 10 JSON native, 10 PNG preview, provenance/progress dan HTML perbandingan mandiri/offline dengan referensi asli serta latar putih/abu-abu. Raster hanya referensi pembanding, bukan master.

**144 tes lokal lulus**: 135 path-batch, 8 geometris dan 1 variasi. Meliputi konsistensi SVG/JSON, batas/penutupan path, persilangan polygon, nonkolisi ID/geometri/hash, progres/alias, huruf putih positif, counter ring, enam facet rail serta katalog tetap/jeda APK.

**Tidak ada build APK, dispatch workflow, integrasi Android atau rilis.** Katalog tetap 105 variasi; APK terakhir v1.0.42. Tidak ada tes perangkat Android baru.

Reproduksi dengan PNG sumber lokal dan resvg:
```sh
python scripts/build_drive_batch_29.py
python -m unittest discover -s tests -p 'test_path_batches.py'
python -m unittest discover -s tests -p 'test*geometric*.py'
python -m unittest discover -s tests -p 'test_variation_vectors.py'
```
