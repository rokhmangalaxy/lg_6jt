# Batch 26 — 10 master manual, tanpa APK

Sumber rasio_1 **3/04–09 + 4/01–04**. Nama asli, Drive ID, SHA-256 dan lokasi SVG/JSON dicatat pada `progress.json`. Semua sumber dibuka individual sebelum polygon ditulis manual; render diperiksa kembali dalam montage. Tidak memakai auto-trace, font, atau substitusi desain generik.

## Konstruksi spesifik sumber

| Sumber | Struktur |
|---|---|
| 3/04 | Atap merah dan rail navy terpisah, alas merah, MCM navy dengan C ber-chamfer pendek |
| 3/05 | Cap/alas navy, MCM merah dengan C membulat pendek |
| 3/06 | Atap/alas merah terbuka, M navy sempit dan C navy vertikal panjang |
| 3/07 | Rail merah miring asimetris, MCM navy oblique |
| 3/08 | M navy bersudut tinggi, C merah, chevron bawah merah/navy dan stub merah terpisah |
| 3/09 | Tiga panel atap merah terpisah, plate navy, MCM putih positif dan strip alas merah |
| 4/01 | Ring diamond navy dengan counter transparan, diamond merah terpisah dan MCM putih positif |
| 4/02 | Atap merah, alas navy, M navy dan C merah ber-chamfer |
| 4/03 | Slab merah chamfer terpisah atas/bawah, MCM navy |
| 4/04 | Dua chevron merah atap, segitiga tengah navy independen dan MCM navy |

Celah antarkomponen mengikuti latar. Huruf putih adalah bidang positif recolorable, bukan lubang. Ring 4/01 memakai counter evenodd transparan. Tekstur sumber diratakan menjadi merah/navy/putih solid; kurva diregularisasi dengan chord/chamfer pendek. Hasil menunggu persetujuan visual, tidak diklaim pixel-perfect atau final produksi.

## Progres dan audit terbatas

- **229 master Drive unik** (+10); redraw saja **229/342 = 66,96%**.
- **18 alias sumber duplikat terverifikasi**, diwariskan tanpa perubahan.
- Cakupan **247/342 = 72,22%**, **95 sumber tersisa**.
- Sepuluh hash baru berbeda satu sama lain dan dari sumber master terdahulu; generator memeriksanya sebelum ekspor. Motif mirip tidak otomatis dianggap duplikat.
- 342 adalah jumlah file yang dilaporkan, bukan jumlah desain unik terverifikasi global. Snapshot historis tidak diubah.

## Artefak dan validasi

10 SVG path-only, 10 JSON native, 10 PNG preview, provenance/progress dan HTML perbandingan mandiri/offline dengan sumber asli serta pilihan latar putih/abu-abu. Bitmap hanya referensi pembanding, bukan master.

**129 tes lokal lulus**: 120 path-batch, 8 geometris, 1 variasi. Memeriksa konsistensi SVG/JSON, penutupan/batas path, persilangan polygon, nonkolisi ID/geometri/hash, progres/alias, bidang putih positif, ring transparan, panel atap terpisah serta katalog/jeda APK.

**Tidak ada build APK, dispatch workflow, integrasi Android atau rilis.** Katalog tetap 105 variasi, APK terakhir v1.0.42. Tidak ada validasi perangkat Android baru.

Reproduksi dengan PNG sumber lokal dan resvg:
```sh
python scripts/build_drive_batch_26.py
python -m unittest discover -s tests -p 'test_path_batches.py'
python -m unittest discover -s tests -p 'test*geometric*.py'
python -m unittest discover -s tests -p 'test_variation_vectors.py'
```
