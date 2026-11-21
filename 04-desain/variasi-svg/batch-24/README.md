# Batch 24 — 10 master rasio manual, tanpa APK

Sumber **rasio_1 1/02–09 dan 2/01–02**. Nama PNG, Drive ID, SHA-256 dan lokasi SVG/JSON dicatat di `progress.json`. ID keluarga rasio tetap terpisah dari berisi.

## Konstruksi spesifik sumber

| Sumber rasio | Struktur manual |
|---|---|
| 1/02 | Empat chevron atap/alas terbuka: merah luar, navy dalam; MCM navy |
| 1/03 | Atap merah, C merah runcing dan M navy dengan kaki sisi miring |
| 1/04 | Rail merah meruncing, M navy miring dan C navy membulat oblique |
| 1/05 | Cap/alas merah dan C merah; empat stub bracket navy terpisah dan M navy |
| 1/06 | Dua chevron samping merah, plate navy, enam lubang transparan dan MCM putih positif |
| 1/07 | Rail I-beam merah dengan sambungan melengkung pendek, MCM navy |
| 1/08 | Cap/alas navy, MCM merah dengan kaki M terbuka |
| 1/09 | Atap dua tingkat terbelah merah/navy, C merah panjang runcing dan M navy |
| 2/01 | Diamond merah dengan empat tip navy terpisah, MCM navy dengan aperture C persegi kecil |
| 2/02 | Cap/alas navy, cap dalam merah, C navy vertikal dan dua M merah |

Sepuluh sumber dibuka individual; render dibandingkan kembali dalam montage. Koordinat ditulis manual per sumber, bukan auto-trace, font atau penggantian desain generik. Kurva C dan sambungan rail diregularisasi sebagai chamfer/chord pendek. Enam lubang memakai polygon 16 sisi sebagai counter evenodd transparan; huruf putih 1/06 justru bidang positif recolorable. Celah antarkomponen mengikuti latar. Tekstur diratakan merah/navy/putih solid. Hasil masih menunggu review visual pengguna, tidak diklaim pixel-perfect atau final produksi.

## Progres dan audit terbatas

- **209 master Drive unik** (+10); redraw saja **209/342 = 61,11%**.
- Alias sumber duplikat terverifikasi tetap **18**, diwariskan tanpa perubahan.
- Cakupan sumber **227/342 = 66,37%**; **115 sumber tersisa**.
- Sepuluh hash baru berbeda satu sama lain dan dari sumber master terdahulu, diperiksa generator sebelum ekspor. Motif mirip tidak otomatis digabung.
- 342 adalah jumlah file yang sebelumnya dilaporkan, bukan total desain unik terverifikasi global. Audit hanya sumber unduhan; snapshot historis tidak diubah.

## Artefak dan validasi

10 SVG path-only, 10 JSON native, 10 PNG preview, provenance/progress dan `perbandingan.html` mandiri/offline dengan toggle latar putih/abu-abu. Raster hanya untuk referensi pembanding di HTML; master SVG tanpa bitmap/font.

**119 tes lokal lulus:** 110 path-batch + 8 geometris + 1 variasi. Memeriksa konsistensi SVG/JSON, penutupan/batas path, persilangan polygon, nonkolisi ID/geometri/hash, progres/alias, lubang mounting transparan dan huruf putih positif, warna 2/02, katalog tetap serta jeda job APK. Tidak ada tes perangkat Android baru.

**Tidak ada build APK, dispatch workflow, integrasi Android atau rilis.** Katalog tetap 105 variasi; APK terakhir v1.0.42.

Reproduksi dengan PNG sumber lokal dan resvg:
```sh
python scripts/build_drive_batch_24.py
python -m unittest discover -s tests -p 'test_path_batches.py'
python -m unittest discover -s tests -p 'test*geometric*.py'
python -m unittest discover -s tests -p 'test_variation_vectors.py'
```
