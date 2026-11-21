# Batch 25 — 10 master manual, tanpa APK

Sumber rasio_1 **2/03–09 + 3/01–03**; identitas Drive, SHA-256 dan lokasi master ada di `progress.json`. Sepuluh sumber dibuka individual sebelum koordinat polygon ditulis manual, tanpa auto-trace, font, atau substitusi desain generik. Render diperiksa kembali dalam montage.

## Struktur per sumber

- 2/03: atap/alas merah dangkal, dua M navy dan C navy vertikal.
- 2/04: empat rail merah/navy, M miring navy dan C miring merah.
- 2/05: empat facet atap/alas terpisah merah/navy dan MCM navy.
- 2/06: rail merah berlekuk ke dalam, MCM navy tegak.
- 2/07: cap/alas dan C merah panjang, M navy dengan sisi bersudut.
- 2/08: atap navy dengan pier tengah merah; MCM navy, baseline merah.
- 2/09: cap/alas navy, pier sisi merah, C merah panjang dan M navy.
- 3/01: diamond merah dengan empat tip navy terpisah dan MCM putih positif.
- 3/02: atap merah dan alas merah berujung terpisah, C navy panjang.
- 3/03: plate navy chamfer dengan strip merah dan MCM putih positif.

Celah antarkomponen transparan; huruf putih adalah bidang positif recolorable. Warna solid merah/navy/putih menggantikan tekstur sumber. Kurva C diregularisasi menjadi chamfer pendek. Hasil masih menunggu persetujuan visual, bukan klaim pixel-perfect atau final produksi.

## Progres dan audit terbatas

- **219 master unik** (+10); redraw saja **219/342 = 64,04%**.
- **18 alias sumber duplikat terverifikasi**, tidak berubah.
- Cakupan sumber **237/342 = 69,30%**, **105 sumber tersisa**.
- Sepuluh SHA-256 sumber baru berbeda satu sama lain dan dari sumber master sebelumnya; pemeriksaan berjalan sebelum ekspor. Kemiripan motif tidak otomatis dianggap duplikat.
- 342 adalah jumlah file yang dilaporkan, bukan total desain unik terverifikasi global. Snapshot historis tidak diubah.

## Artefak dan validasi

10 SVG path-only, 10 JSON native, 10 PNG preview, provenance/progress, dan `perbandingan.html` mandiri/offline berisi referensi asli serta kontrol latar putih/abu-abu. Raster hanya referensi pembanding, bukan master.

**124 tes lokal lulus**: 115 path-batch, 8 geometris, 1 variasi. Meliputi konsistensi SVG/JSON, batas dan penutupan path, persilangan polygon, nonkolisi ID/geometri/hash, progres/alias, huruf putih positif, serta katalog dan jeda build APK.

**Tidak ada build APK, dispatch workflow, integrasi Android atau rilis.** Katalog tetap 105 variasi, APK terakhir v1.0.42. Tidak ada validasi perangkat Android baru.

Reproduksi dengan PNG sumber lokal dan resvg:
```sh
python scripts/build_drive_batch_25.py
python -m unittest discover -s tests -p 'test_path_batches.py'
python -m unittest discover -s tests -p 'test*geometric*.py'
python -m unittest discover -s tests -p 'test_variation_vectors.py'
```
