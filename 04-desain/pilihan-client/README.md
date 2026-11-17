# Pilihan klien — empat logo di APK

Sesuai permintaan pengguna, katalog APK hanya berisi:
1. `client-logo-04.png`: simbol no.4 yang sudah diekstrak, tanpa teks nama perusahaan.
2. `client-attachment-01.png`: kiri atas dari lampiran (nomor 1).
3. `client-attachment-08.png`: tengah bawah dari lampiran (nomor 8).
4. `client-attachment-09.png`: kanan bawah dari lampiran (nomor 9).

Penomoran lampiran: kiri ke kanan, atas ke bawah pada grid 3×3. `lampiran-asli.png` adalah gambar yang dikirim pengguna. Garis pembatas sel tidak disertakan. Simbol dipotong dan warna dinormalkan ke merah/biru/putih solid; tidak digenerasi ulang. Karena sumber berupa raster, hasil ini bukan vektor dan tetap memiliki batas resolusi sumber.

Sumber empat logo aplikasi berada di `android-logo/logo-assets/`, terpisah dari arsip eksplorasi lama. Bagian hitam pada lampiran dijadikan alpha transparan; putih huruf dipertahankan. Aplikasi mengisi alpha dengan hitam untuk Swatch 1/2 pada tiga simbol lampiran (mengikuti gambar asli), putih untuk logo no.4, atau gray pada monokrom. Dengan demikian area ruang dalam simbol mengikuti background tanpa menghapus huruf putih.

Reproduksi: `python scripts/prepare_client_selection.py` (memerlukan ImageMagick). Data catatan lama tidak dihapus. Preferensi pilihan katalog baru memakai kunci terpisah agar tidak mengambil swatch dari logo lama yang tidak berkaitan.

HTML preview lama dan eksplorasi di repository tetap menjadi arsip; permintaan empat logo diterapkan pada katalog APK.

## Perbaikan kontur dan latar (update terbaru)

Latar hitam kini dihapus dari seluruh preset. Semua logo ditampilkan pada abu-abu terang #D1D5DB agar inisial putih tetap terbaca, termasuk pada preview dan PNG unduhan.

Sumber PNG kecil tetap disimpan sebagai referensi, tetapi **bukan lagi sumber render utama APK**. `scripts/trace_selected_logos.cjs` menelusuri batas bidang menjadi path L/Q, membuang fragmen warna kecil dan fringe biru pada lampiran 01 yang tidak ada sebagai elemen desain. Hasil SVG ada di `vector/`, dan command path JSON di `android-logo/logo-assets/`. APK menggambar path dengan Canvas/Paint antialias pada maksimum sisi 1600px; tidak memperbesar bitmap 300–400px dan tidak melakukan kuantisasi ulang setelah menggambar.

Ini tracing dari raster, bukan master orisinal perusahaan: kontur dapat sedikit berbeda dari sumber dan beberapa ketidakteraturan bentuk sumber masih memerlukan penyuntingan vektor manual. Resolusi lebih tinggi tidak mengembalikan detail yang tidak tersedia di gambar asal.

Reproduksi tracing:
```sh
npm install --prefix .cache/logo-trace imagetracerjs pngjs @resvg/resvg-js
node scripts/trace_selected_logos.cjs
```
