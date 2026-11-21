# Batch 23 — 10 master rasio manual, tanpa APK

Sumber **rasio_1 18/01–09 dan 1/01**. Pencarian rasio_1_19/01 tidak menemukan file pada folder yang sama; dilanjutkan ke kelompok rasio 1 yang belum dikerjakan agar mencapai sepuluh master. Nama PNG, Drive ID, SHA-256 dan lokasi SVG/JSON ada dalam `progress.json`. ID keluarga rasio tetap terpisah dari berisi.

## Struktur spesifik sumber

| Sumber rasio | Konstruksi manual |
|---|---|
| 18/01 | Diamond merah, empat facet navy terpisah, MCM navy kompak |
| 18/02 | Rail I-beam navy dengan sambungan fillet pendek, empat gusset merah, M navy/C merah |
| 18/03 | Empat facet frame merah/navy, C merah vertikal dan M navy |
| 18/04 | Rail perspektif dua tingkat dua warna, M navy dan C merah |
| 18/05 | Dua rail solid, M navy dan C merah oblique |
| 18/06 | Ring navy dengan delapan lubang mounting transparan, bidang merah dan MCM navy |
| 18/07 | C merah tinggi dengan lengan miring, M navy, alas navy dua tingkat |
| 18/08 | C hexagon merah di antara dua M navy berbahu tinggi |
| 18/09 | Dua ring diamond tipis navy/merah, empat titik mounting navy positif, M navy dan C merah |
| 1/01 | Diamond merah lebar, empat tip navy terpisah dan MCM navy |

Semua sepuluh sumber dibuka individual dan hasil render dibandingkan kembali dalam montage. Draft 18/07 dikoreksi panjang bawah C agar celah terhadap alas tetap terbuka sesuai referensi; tes mengunci batas bawahnya. Titik ditulis manual per sumber, bukan auto-trace, font atau substitusi desain generik. Kurva/fillet diregularisasi sebagai chamfer pendek; lubang/titik lingkaran memakai polygon 16 sisi. Tekstur diratakan merah/navy/putih solid. Lubang 18/06 mengikuti latar lewat counter evenodd; empat titik 18/09 justru bidang navy positif. Celah ring tetap transparan. Hasil masih menunggu review visual pengguna, tidak diklaim pixel-perfect atau final produksi.

## Progres dan audit terbatas

- **199 master Drive unik** (+10); redraw saja **199/342 = 58,19%**.
- Alias duplikat sumber terverifikasi tetap **18**, diwariskan tanpa perubahan.
- Cakupan sumber **217/342 = 63,45%**; **125 sumber tersisa**.
- Sepuluh hash sumber baru berbeda satu sama lain dan dari sumber master terdahulu; generator memeriksa sebelum ekspor. Motif mirip tidak otomatis dianggap duplikat.
- 342 adalah jumlah file yang sebelumnya dilaporkan, bukan total desain unik terverifikasi global. Audit hanya sumber unduhan; snapshot lama tidak diubah.

## Artefak dan validasi

10 SVG path-only tanpa bitmap/font, 10 JSON native, 10 PNG preview, provenance/progress dan HTML perbandingan mandiri/offline dengan toggle latar putih/abu-abu. Raster hanya untuk referensi pembanding di HTML.

**114 tes lokal lulus:** 105 path-batch + 8 geometris + 1 variasi. Memeriksa kesamaan SVG/JSON, penutupan/batas path, persilangan polygon, nonkolisi ID/geometri/hash, progres/alias, lubang mounting vs titik positif, celah bawah C 18/07, katalog tetap dan jeda job APK. Tidak ada tes perangkat Android baru.

**Tidak ada build APK, dispatch workflow, integrasi Android atau rilis.** Katalog tetap 105 variasi; APK terakhir v1.0.42.

Reproduksi dengan sumber PNG lokal dan resvg:
```sh
python scripts/build_drive_batch_23.py
python -m unittest discover -s tests -p 'test_path_batches.py'
python -m unittest discover -s tests -p 'test*geometric*.py'
python -m unittest discover -s tests -p 'test_variation_vectors.py'
```
