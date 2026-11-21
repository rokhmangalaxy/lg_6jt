# Empat logo geometris — katalog APK

Logo 04 menggunakan master yang disetujui tanpa perubahan. Lampiran 01, 08, 09 dibangun ulang dari koordinat eksplisit: semua sisi menggunakan M/L/Z, dua M bercermin pada x=200, dan bentuk utama mengikuti sumber pilihan klien. Ini interpretasi geometris yang dirapikan, bukan salinan piksel identik. Logo 01 tetap hexagon, 08 tetap bersayap, 09 tetap diamond merah/navy.

SVG transparan adalah master; PNG preview memakai abu-abu terang agar bagian putih terlihat. Merah #DC2626, navy #173257, putih #FFFFFF adalah palet kerja. Seluruh latar APK tetap abu-abu terang, tidak hitam, sesuai versi terakhir. Bentuk yang sengaja terbuka pada bingkai 09 dipertahankan sebagai celah konstruksi, bukan kontur trace bergelombang.

Generator: `python scripts/build_geometric_catalog.py` (resvg-js di `.cache/mcm-redraw`). Generator memasang JSON dan PNG ke `android-logo/logo-assets`.

Navigasi tetap: satu logo, ❮/❯ dan swipe, empat swatch, tombol nomor 01–04, unduh PNG di header. Bottom navigation tetap disembunyikan; kode catatan tidak dihapus. Aplikasi merender path native antialias, bukan memperbesar raster sumber.

Tes: `python -m unittest discover -s tests -p 'test*geometric*.py'`; CI Android menjalankan unit test render 16 kombinasi, lint, inventory dan signature. Tidak ada klaim pengujian perangkat fisik atau bordir.

## Koreksi setelah v1.0.20
Logo slot 3 dan 4 sebelumnya berubah proporsinya terlalu jauh. Konstruksi sekarang mengikuti koordinat crop asli 404×351 untuk lampiran 8 dan 9 (file lampiran terbaru identik SHA-256 dengan referensi tersimpan). Slot 3 mengembalikan dua sisipan navy terpisah dan V bawah sempit; slot 4 mengembalikan proporsi huruf serta bingkai diamond tersegmentasi. Logo 04 dan lampiran 01 tidak diubah. `koreksi-03-04.html` menampilkan sumber versus koreksi secara offline. Ini tetap perapian geometris, bukan klaim identik setiap piksel.
