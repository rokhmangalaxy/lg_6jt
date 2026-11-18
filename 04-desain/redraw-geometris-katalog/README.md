# Empat logo geometris — katalog APK

Logo 04 menggunakan master yang disetujui tanpa perubahan. Lampiran 01, 08, 09 dibangun ulang dari koordinat eksplisit: semua sisi menggunakan M/L/Z, dua M bercermin pada x=200, dan bentuk utama mengikuti sumber pilihan klien. Ini interpretasi geometris yang dirapikan, bukan salinan piksel identik. Logo 01 tetap hexagon, 08 tetap bersayap, 09 tetap diamond merah/navy.

SVG transparan adalah master; PNG preview memakai abu-abu terang agar bagian putih terlihat. Merah #DC2626, navy #173257, putih #FFFFFF adalah palet kerja. Seluruh latar APK tetap abu-abu terang, tidak hitam, sesuai versi terakhir. Bentuk yang sengaja terbuka pada bingkai 09 dipertahankan sebagai celah konstruksi, bukan kontur trace bergelombang.

Generator: `python scripts/build_geometric_catalog.py` (resvg-js di `.cache/mcm-redraw`). Generator memasang JSON dan PNG ke `android-logo/logo-assets`.

Navigasi tetap: satu logo, ❮/❯ dan swipe, empat swatch, tombol nomor 01–04, unduh PNG di header. Bottom navigation tetap disembunyikan; kode catatan tidak dihapus. Aplikasi merender path native antialias, bukan memperbesar raster sumber.

Tes: `python -m unittest discover -s tests -p 'test*geometric*.py'`; CI Android menjalankan unit test render 16 kombinasi, lint, inventory dan signature. Tidak ada klaim pengujian perangkat fisik atau bordir.
