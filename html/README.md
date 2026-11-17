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
