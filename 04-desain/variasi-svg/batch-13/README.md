# Batch 13 — satu master baru + sembilan duplikat terverifikasi

Sumber 11/09 direkonstruksi manual sebagai hexagon/shield navy dengan MCM merah tinggi. Sumber asli dan render master telah dibuka dan ditinjau. Koordinat disimetriskan sesuai konsep; tekstur diratakan, bukan auto-trace atau salinan piksel identik. Menunggu review visual pengguna.

**Seluruh kelompok 12/01–09 identik byte-per-byte/SHA-256 dengan kelompok 11/01–09.** Tidak dibuat geometri atau entri aplikasi baru untuk duplikat tersebut. Pemetaan alias dan hash disimpan di `progress.json`. Folder keseluruhan belum diaudit: 342 adalah jumlah file sumber yang sebelumnya dilaporkan, bukan jumlah desain unik.

## Progres
- **99 master Drive unik** dibuat manual (11 kelompok × 9); naik **1**, bukan 10.
- **9 sumber duplikat** terpetakan ke master yang sama.
- **108 dari 342 sumber** tercakup termasuk duplikat: **31,58%**, sisa **234**.
- Redraw unik dibagi 342 file: **28,95%**. Ini bukan persentase seluruh desain unik, karena total unik belum terverifikasi.
- Dua studi tambahan aplikasi tidak dihitung sebagai sumber Drive.

## APK diminta secara eksplisit
Instruksi pengguna terbaru: “lanjut,lalu build apk”. Penahanan total sebelumnya diganti **build manual saja** (`workflow_dispatch`); PR/push tetap tidak membuat APK. Seluruh master selesai dari batch 03–13 diintegrasikan tanpa mengubah 11 ID/indeks awal. APK berisi **105 variasi**: 99 master Drive + 4 logo awal + 2 studi. Kelompok 12 tidak diduplikasi.

Master historis tetap tersimpan sebagai snapshot. `scripts/integrate_vector_masters.py` menambahkan native JSON identik master dan PNG thumbnail transparan; tampilan/recolor/export utama tetap dirender dari path native, bukan PNG. Sertifikat demo tetap sama untuk pembaruan tanpa uninstall. Ini bukan klaim seluruh koleksi telah selesai atau lolos uji perangkat fisik.

## Artefak dan validasi
SVG, JSON, preview PNG, HTML perbandingan offline, dan progress/provenance. Tes mengecek geometri SVG/JSON, kontur tertutup dan tidak menyilang secara proper, hash alias, jumlah katalog, 11 ID awal tetap, tidak ada entri kelompok 12 duplikat, kesamaan JSON master/native, serta build hanya manual. Render Android/swatches/uniform dan APK inventory diuji melalui workflow rilis.

Reproduksi membutuhkan sumber lokal dan resvg:
```sh
python scripts/build_drive_batch_13.py
python scripts/integrate_vector_masters.py
python -m unittest discover -s tests -p 'test_path_batches.py'
```
