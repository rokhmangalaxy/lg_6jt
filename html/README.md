# Preview HTML lima konsep logo

Situs statis mandiri: `index.html` dan lima PNG palet solid di `assets/`. Tanpa build, CDN, font eksternal, atau backend. Buka `index.html` langsung atau jalankan dari root repository:

```sh
python3 -m http.server 8000 --bind 0.0.0.0 --directory html
```

## GitHub Pages

Target URL setelah berhasil diterbitkan: **https://rokhmangalaxy.github.io/lg_6jt/**. Ini URL yang diharapkan, **belum situs aktif**.

Status saat diperiksa: repository private, `has_pages: false`; API pengaturan Pages mengembalikan 403 untuk integrasi sesi ini. Tidak ada perubahan visibilitas repository atau aktivasi Pages yang dilakukan.

1. Pastikan konsep boleh dipublikasikan. Pages umumnya terbuka untuk publik; repository private tidak otomatis menjadikan situs privat. Jangan unggah data peserta atau dokumen rahasia.
2. Pemilik repository memeriksa ketersediaan Pages untuk paket akun dan repository private di **Settings → Pages**. Jika tidak tersedia, gunakan paket yang mendukung atau pilih hosting lain; jangan mengubah repository menjadi public tanpa keputusan eksplisit.
3. Setelah perubahan ini di-push dari branch kerja dan digabung lewat PR, buka **Settings → Pages → Build and deployment → Source: GitHub Actions**.
4. Buka **Actions → Publish logo preview → Run workflow**, pilih ref yang berisi versi yang ingin dipublikasikan. Workflow manual biasanya baru tampil setelah berkas workflow ada di default branch. Pengaturan environment `github-pages` juga harus mengizinkan ref tersebut.
5. Tunggu job deploy berhasil; gunakan URL dari hasil deployment sebagai konfirmasi alamat aktif.

Workflow `.github/workflows/pages.yml` hanya mengunggah **folder `html/`**, bukan riset, brief, atau seluruh repository. Publikasi tidak otomatis berjalan setiap push. README ini ikut menjadi berkas publik pada artifact; isinya tidak memuat rahasia.

## Memperbarui gambar

Setelah mengubah logo solid di `03-konsep/solid/`, salin lima PNG ke `html/assets/`, periksa preview, lalu jalankan publikasi manual lagi. Gambar adalah konsep raster berbasis generasi AI, bukan master vektor/siap bordir. Palet kerja bukan warna resmi perusahaan.

## Navigasi dan warna interaktif

Galeri menampilkan satu konsep aktif dengan Prev/Next (berputar), tombol nomor 01–05, dan tombol panah keyboard. Enam tombol susunan palet memetakan area merah, biru, dan putih dari gambar sumber asli ke seluruh enam permutasi warna dasar. Tidak ada color picker atau warna tambahan. Pilihan terpisah per konsep bertahan selama halaman terbuka, bukan setelah reload. Area putih termasuk latar. Unduh PNG mengekspor warna konsep aktif; reset hanya berlaku pada konsep aktif.

Kelima sumber PNG tertanam di `index.html`; tidak perlu fetch atau server agar kanvas dapat dipakai ketika membuka file lokal. `preview-logo-mcm.html` di root adalah salinan mandiri yang sama. Tidak ada gambar tambahan per kombinasi warna. Setelah mengganti sumber artwork, data gambar tertanam pada HTML harus diperbarui juga; sekadar mengganti `assets/` tidak mengubah preview interaktif.

Pemeriksaan logika: `node tests/test_logo_preview.cjs` (sintaks, pemetaan warna simultan, sumber tetap utuh, reset, warna kustom, lima sumber tertanam, dan kesamaan versi offline). Ini bukan pengujian browser otomatis.

## Mode visual dan latar terkunci

UI kini mengutamakan satu logo besar, navigasi ikon, enam tombol swatch, reset, dan ekspor (HTML). Penjelasan teknis tidak ditampilkan pada layar utama.

Mask latar dihitung sekali per sumber dengan flood fill empat arah terhadap piksel putih yang tersambung ke tepi kanvas. Piksel latar ini selalu putih pada preview dan hasil ekspor, terlepas dari susunan palet. Bagian putih yang tertutup di dalam logo tetap dapat diwarnai. Bagian putih yang terbuka dan tersambung ke luar dianggap latar; pemisahan semantik lebih rinci memerlukan master vektor/mask manual. Ini tidak memperbaiki cropping pada artwork lama.

Tes `node tests/test_logo_preview.cjs` memeriksa keenam permutasi: latar tetap putih dan putih internal tertutup tetap dapat berubah. Pengujian ini logika piksel, bukan uji perangkat Android.

## Header, navigasi bawah, dan Catatan (update terbaru)

Urutan studio: topbar → logo → Prev/Next → Swatch 1/2/Hitam–Putih/Putih–Hitam → nomor logo. Swatch 1/2 mempertahankan putih internal; monokrom memetakan merah dan biru bersama ke hitam atau putih, putih internal menjadi warna kebalikan. Latar luar selalu putih pada Swatch 1/2 atau abu-abu #d1d5db pada dua mode monokrom. Ini menggantikan enam permutasi sebelumnya.

Navigasi bawah membuka Logo, Menu (reset/ekspor HTML), dan Catatan. Catatan memuat jenis Bug/Pengembangan, isi, waktu, dan nomor logo aktif. Teks ditampilkan dengan textContent, tidak sebagai HTML. Catatan dan draft disimpan lewat localStorage pada perangkat/origin yang sama; tidak disinkronkan ke GitHub. Hapus memerlukan konfirmasi. Jika storage gagal, UI menyampaikan bahwa data hanya bertahan sementara. Penghapusan data aplikasi/browser atau uninstall menghilangkan catatan. Pindah file/origin browser juga dapat membuat data lama tidak terlihat.

Android mengaktifkan DOM storage pada origin lokal tetap yang sama; tidak menambahkan akses jaringan atau jembatan JavaScript/native. Update package yang ditandatangani sama mempertahankan data aplikasi selama tidak dihapus oleh pengguna/OS. Perlu uji instalasi/update pada perangkat nyata.

## Counter huruf, swipe, dan ikon galaksi

Mask nameplate berupa batas ternormalisasi spesifik pada lima sumber raster. Semua piksel putih di area nama perusahaan, termasuk lubang O/A/P/R, dianggap latar, bukan fill putih simbol. Area simbol di luar nameplate tetap memakai aturan sebelumnya. Batas ini perlu disesuaikan bila gambar sumber/komposisi berubah.

Area logo mendukung swipe kiri/kanan melalui Pointer Events (juga drag mouse), ambang 55px, dominan horizontal, maksimal 900ms. Scroll vertikal tetap diizinkan; pointercancel membatalkan gesture. Tombol Prev/Next tetap tersedia.

Ikon launcher Android berupa spiral merah–biru pada putih, dengan adaptive icon dan fallback berbagai density. Sumber AI ada di `android-logo/icon-source/galaxy.png`, hasil palet solid dan margin aman ada pada resource Android. Ini ikon aplikasi, bukan kandidat logo perusahaan baru.

## Sepuluh konsep

Preview mandiri sekarang berisi 10 logo. Konsep 06–10 ada di `assets/variasi-06-native.png` sampai `variasi-10-native.png`, dengan nameplate yang konsisten. Warna solid tetap sama; mask nama baru dimulai pada 80% tinggi. UI preview mengikuti gaya neumorphism, sedangkan aplikasi Android tetap memakai implementasi native terpisah.
