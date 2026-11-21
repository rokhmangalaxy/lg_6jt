# Prompt siap salin ke sesi chat lain

Salin teks di bawah ini, lalu lampirkan **satu gambar asli** sesuai nomor yang ingin dikerjakan. Mulai dari `variasi-05-asli.png`. Jika sesi lain memiliki akses repo, gambar asli tersedia di `logos/redraw/`.

---

Saya ingin Anda menggambar ulang logo dari gambar asli yang saya lampirkan. Ini pekerjaan **rekonstruksi bentuk**, bukan eksplorasi atau desain ulang. Hasil percobaan sebelumnya tidak sesuai; karena itu mulai dari kanvas kosong dan gunakan **gambar asli terlampir saja** sebagai acuan.

## Aturan acuan

- Jangan membuka, menyalin, membandingkan dengan, atau memperbaiki SVG/JSON/PNG hasil redraw lama, termasuk yang ada di folder lain dalam repo.
- Jangan memakai generator redraw lama atau koordinatnya sebagai template. Jangan melakukan auto-trace.
- Jangan mengubah berkas sumber `*-asli.png`. Semua hasil harus disimpan terpisah.
- Jangan menganggap huruf M dan C sebagai teks dengan font. Bentuk hurufnya adalah bentuk khusus yang harus digambar sebagai path.

## Target bentuk

1. Pelajari siluet luar, rasio lebar–tinggi, posisi huruf, ketebalan batang, potongan sudut, dan ruang negatif pada gambar asli.
2. Rekonstruksi bentuk secara manual dengan path vektor yang bersih. Pakai kurva Bézier jika sumber memiliki lengkungan; jangan mengganti lengkungan dengan sudut-sudut kasar hanya demi memudahkan implementasi.
3. Pertahankan karakter sumber. Jangan memaksakan simetri jika itu mengubah desain aslinya; jangan mengganti bentuk C atau konstruksi M menjadi bentuk generik.
4. Jaga setiap jarak pemisah: antarsisi huruf, huruf dengan bingkai, dan potongan putih. Tidak boleh ada bentuk yang menyentuh bingkai atau saling menimpa jika pada sumber terpisah.
5. Bedakan lubang/ruang negatif dengan objek putih. Ruang negatif harus berupa lubang yang mengikuti warna latar, sementara huruf putih yang memang merupakan objek tetap menjadi objek putih yang dapat diwarnai ulang.
6. Gunakan warna solid merah, navy, dan putih. Tanpa gradien, tekstur, bayangan, efek 3D, atau mockup. Palet aplikasi: merah `#DC2626`, navy `#173257`, putih `#FFFFFF`. Yang dinilai terutama ketepatan geometri, bukan tekstur/variasi warna raster sumber.

## Catatan khusus nomor 179

Hanya untuk `variasi-179-asli.png`: gambar ulang dari nol, dengan modifikasi **tekukan vertikal huruf C berada di tengah-tengah**. Pertahankan karakter C bertekuk, jangan diganti menjadi C font biasa atau C membulat generik. Jika maksud posisi tekukan belum jelas dari sumber, tanyakan sebelum menetapkan bentuknya; jangan menebak perubahan besar.

## Cara kerja dan penilaian

- Kerjakan **satu logo terlebih dahulu**, mulai Variasi 05. Jangan memproses seluruh daftar sekaligus dan jangan lanjut ke nomor berikutnya sebelum saya memberi penilaian.
- Setelah selesai, kirim pratinjau kecil **gambar asli di kiri | redraw baru di kanan**, dengan ukuran tampilan logo sebanding dan label nomor yang jelas. Target lebar keseluruhan sekitar 640–800 px, JPEG kualitas cukup untuk menilai tepi, idealnya di bawah 150 KB.
- Lampirkan gambar langsung di chat jika platform mendukung; jangan hanya mengatakan gambar ada di workspace. Jangan mengklaim gambar terlihat di chat bila platform hanya menyediakan viewer berkas. Bila lampiran langsung tidak tersedia, jelaskan keterbatasannya dan sediakan berkas gambar kecil yang mudah dibuka/diunduh.
- Periksa kembali hasil terhadap **sumber asli saja** sebelum mengirim: bentuk M, kontur C, celah negatif, bingkai, ketebalan garis, dan tidak ada kontur bersilangan. Tes geometri bukan bukti kemiripan visual.
- Jangan mengklaim "sesuai", "90% mirip", atau selesai disetujui sebelum saya menilai.
- Jangan build APK atau memasukkan hasil ke aplikasi sebelum saya menyetujui bentuknya.

## Hasil yang diminta

- SVG vektor sungguhan dengan path yang dapat diedit, bukan raster yang dibungkus SVG atau disisipkan sebagai base64.
- PNG pratinjau berlatar transparan.
- JPEG kecil perbandingan **asli + redraw baru** untuk penilaian.
- Nama berkas memuat nomor variasi, misalnya `variasi-05-redraw.svg`, `variasi-05-redraw.png`, dan `variasi-05-perbandingan.jpg`. Jika bekerja dalam repo, simpan hasil di `logos/redraw/hasil/`, jangan menimpa gambar asli.
- Utamakan ketelitian satu logo, bukan kecepatan jumlah. Jika ada bagian sumber yang ambigu atau resolusinya kurang, tanyakan atau minta potongan gambar lebih jelas daripada menebak.

Daftar pekerjaan, dengan urutan penilaian:
**05, 49, 50, 122, 123, 128, 179, 184, 188, 290, 294, 301, 328.**

Mulai dengan gambar asli pertama yang saya lampirkan. Untuk saat ini kerjakan **Variasi 05 saja**, lalu tunggu penilaian saya.
