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
