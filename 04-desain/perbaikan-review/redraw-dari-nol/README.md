# Redraw ulang dari nol — 13 item yang ditolak

Daftar: 05, 49, 50, 122, 123, 128, 179, 184, 188, 290, 294, 301, 328.
Feedback terbaru dicatat di `feedback.json`. Item tidak disebutkan tidak dinyatakan
Sesuai secara implisit, dan tidak diubah oleh pekerjaan ini.

Semua koordinat ditulis baru di `scripts/redraw_review_from_source.py` berdasarkan
pemeriksaan gambar sumber asli saja. Generator tidak memuat vectorAsset, SVG/JSON
batch lama atau PNG redraw lama. Tidak ada auto-trace. Native M/L/Z dengan even-odd
dan palet solid. Diamond 05 memakai aproksimasi kurva manual pada empat sudut.

179: tekukan C luar atas/bawah dan dalam atas/bawah memakai sumbu vertikal x=500
pada kanvas lebar 1000. Ini interpretasi catatan pengguna dan masih perlu dinilai.

Perbandingan HTML hanya memuat sumber asli dan hasil baru. Semua sumber asli
terjaga. Hasil baru sudah mengganti 13 JSON/PNG studio dan 13 PNG redraw review,
melalui installer terpisah yang tidak membaca geometri lama. Nomor/ID, favorit,
radio dan notes tidak direset, navigasi perbaikan tetap di bawah penilaian biasa.

Reproduksi:
1. `python scripts/redraw_review_from_source.py`
2. `python scripts/install_source_only_redraw.py`
   (memerlukan resvg-js di `.cache/mcm-redraw/node_modules`).
Jika pipeline koreksi historis dijalankan ulang, jalankan dua langkah di atas
paling akhir agar tidak menimpa hasil baru dengan koreksi yang sudah ditolak.

13/13 salinan redraw baru selesai (100%), tersisa 0 di daftar ini; **semuanya
menunggu review visual pengguna**. Ini bukan klaim bahwa 13 logo sudah sesuai.
Validasi lokal: 11 tes fresh-redraw, 4 tes packaging/review, 170 tes batch historis
lulus. Pemeriksaan meliputi kontur tidak bersilangan, batas koordinat, jarak huruf
49 dari bingkai, dan sumbu lipatan C 179. Geometri/render diperiksa hanya dengan
sumber asli dan hasil baru; tes otomatis bukan penilaian kesetiaan visual.
