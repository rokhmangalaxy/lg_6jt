# Batch 34 — 10 master manual, tanpa APK

Sumber rasio_1 **12/03–09 + 13/01–03**. Nama PNG, Drive ID, SHA-256 dan lokasi master tercatat di `progress.json`. Setiap sumber dibuka individual, polygon diukur dan ditulis manual per sumber; bukan auto-trace, font, atau substitusi generik. Render diperiksa dalam montage.

## Konstruksi spesifik sumber

| Sumber | Struktur |
|---|---|
| 12/03 | Chevron merah turun, empat pier navy terpisah, MCM navy kompak |
| 12/04 | Dua flag merah dan MCM navy oblique angular |
| 12/05 | Dua bidang atap navy, dua sliver merah terpisah di bawahnya, C merah panjang dan baseline merah |
| 12/06 | Dua bagian frame navy terputus dengan dua insert slash merah, MCM navy |
| 12/07 | Keel merah turun dan empat bar sayap merah, M navy tinggi dengan kaki miring, C navy |
| 12/08 | Ring hexagon merah berlubang, C merah panjang terpisah, dua M navy tinggi |
| 12/09 | Tiga flag atas merah/navy, dua flag alas, MCM navy miring |
| 13/01 | Diamond merah, empat tip navy dan MCM putih positif |
| 13/02 | Atap merah dangkal, keel navy dan C merah lebar |
| 13/03 | Lipatan atas merah, dua pier navy dan chevron navy tengah, MCM navy di bawah |

Celah antarkomponen mengikuti latar. Putih 13/01 adalah bidang positif recolorable, bukan lubang. Ring 12/08 memakai evenodd; C merah di dalam merupakan bidang positif terpisah. Warna bertekstur diratakan menjadi merah/navy/putih solid; kurva diregularisasi dengan chord/chamfer pendek. Hasil menunggu persetujuan visual pengguna, tidak diklaim pixel-perfect atau final produksi.

## Progres dan audit terbatas

- **309 master Drive unik** (+10); redraw saja **309/342 = 90,35%**.
- **18 alias sumber duplikat terverifikasi**, diwariskan tanpa perubahan.
- Cakupan **327/342 = 95,61%**, **15 sumber tersisa**.
- Sepuluh hash baru berbeda satu sama lain dan dari sumber master terdahulu; generator memeriksa sebelum ekspor. Motif mirip tidak otomatis dianggap duplikat.
- 342 adalah jumlah file yang dilaporkan, bukan total desain unik terverifikasi global. Snapshot historis tidak diubah.

## Artefak dan validasi

10 SVG path-only, 10 JSON native, 10 PNG preview, progress/provenance dan HTML mandiri/offline dengan referensi asli serta pilihan latar putih/abu-abu. Raster hanya referensi pembanding, bukan master.

**169 tes lokal lulus:** 160 path-batch, 8 geometris dan 1 variasi. Mencakup konsistensi SVG/JSON, batas/penutupan path, persilangan polygon, nonkolisi ID/geometri/hash, progres/alias, huruf putih positif, ring hexagon, pier terpisah, katalog tetap dan jeda APK.

**Tidak ada build APK, dispatch workflow, integrasi Android atau rilis.** Katalog tetap 105 variasi; APK terakhir v1.0.42. Tidak ada tes perangkat Android baru.

Reproduksi dengan PNG sumber lokal dan resvg:
```sh
python scripts/build_drive_batch_34.py
python -m unittest discover -s tests -p 'test_path_batches.py'
python -m unittest discover -s tests -p 'test*geometric*.py'
python -m unittest discover -s tests -p 'test_variation_vectors.py'
```
