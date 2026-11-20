# Pustaka logo HTML

Situs statis mandiri: `index.html` plus `assets/` berisi lima konsep lama (PNG) dan
seluruh logo hasil potong (WebP + thumbnail). Tanpa build, CDN, font eksternal, atau backend.
Buka `index.html` langsung atau jalankan dari root repository:

```sh
python3 -m http.server 8000 --bind 0.0.0.0 --directory html
```

Halaman menampilkan grid pustaka (**347 logo**: 5 konsep lama + 171 set *kotak* + 171 set
*rasio*), pencarian, filter per set, dan tampilan detail dengan Prev/Next. Semua logo
ditampilkan dengan warna aslinya; susunan warna belum aktif, lihat
`../android-logo/RENCANA-PUSTAKA-LOGO.md`.

## Struktur aset

| Jalur | Isi |
| --- | --- |
| `assets/logos/*.webp` | 347 tampilan penuh, WebP q85 (±2,9 MB) |
| `assets/thumbs/*.webp` | thumbnail 160 px untuk grid (±1,0 MB) |
| `assets/manifest.js` | `window.LOGO_LIBRARY` — id, label, set, dimensi |
| `assets/variasi-0*.png` | master lima konsep lama (3 warna solid) |

`index.html` **tidak** lagi menanam gambar sebagai base64 dan **tidak** memuat susunan
palet. Fungsi `recolor()` tetap ada di skrip untuk fitur yang ditunda.

## Membangun ulang aset

Master PNG hasil potong tidak disimpan di git (lihat `.gitignore`); sumbernya folder Drive
`mcm/logos` atau salinan lokal `drive_out/`.

```sh
python3 scripts/build_logo_assets.py
```

Skrip itu menulis `assets/logos/`, `assets/thumbs/`, `assets/manifest.js`, sekaligus
menyalin `index.html` menjadi `preview-logo-mcm.html` di root (hanya berbeda pada awalan
aset `html/`). Butuh Pillow dengan dukungan WebP.

## GitHub Pages

Target URL setelah berhasil diterbitkan: **https://rokhmangalaxy.github.io/lg_6jt/**. Ini URL yang diharapkan, **belum situs aktif**.

Status saat diperiksa: repository private, `has_pages: false`; API pengaturan Pages mengembalikan 403 untuk integrasi sesi ini. Tidak ada perubahan visibilitas repository atau aktivasi Pages yang dilakukan.

1. Pastikan konsep boleh dipublikasikan. Pages umumnya terbuka untuk publik; repository private tidak otomatis menjadikan situs privat. Jangan unggah data peserta atau dokumen rahasia.
2. Pemilik repository memeriksa ketersediaan Pages untuk paket akun dan repository private di **Settings → Pages**. Jika tidak tersedia, gunakan paket yang mendukung atau pilih hosting lain; jangan mengubah repository menjadi public tanpa keputusan eksplisit.
3. Setelah perubahan ini di-push dari branch kerja dan digabung lewat PR, buka **Settings → Pages → Build and deployment → Source: GitHub Actions**.
4. Buka **Actions → Publish logo preview → Run workflow**, pilih ref yang berisi versi yang ingin dipublikasikan. Workflow manual biasanya baru tampil setelah berkas workflow ada di default branch. Pengaturan environment `github-pages` juga harus mengizinkan ref tersebut.
5. Tunggu job deploy berhasil; gunakan URL dari hasil deployment sebagai konfirmasi alamat aktif.

Workflow `.github/workflows/pages.yml` hanya mengunggah **folder `html/`**, bukan riset, brief, atau seluruh repository. Publikasi tidak otomatis berjalan setiap push. README ini ikut menjadi berkas publik pada artifact; isinya tidak memuat rahasia.

## Pemeriksaan

```sh
node tests/test_logo_preview.cjs
```

Menguji sintaks skrip, mesin `recolor()` (masih dijaga untuk fitur yang ditunda), tidak ada
base64 tertanam, tidak ada kontrol palet, kesamaan `preview-logo-mcm.html` dengan
`index.html`, serta kontrak manifest: 347 item (5/171/171), id unik, setiap WebP ada,
dimensi sesuai manifest, thumbnail ≤160 px, dan anggaran aset <5 MB. Ini bukan pengujian
browser otomatis.

Catatan: logo berasal dari gambar hasil generasi AI, bukan tanda merek resmi dan bukan
master vektor/siap bordir. Palet kerja bukan warna resmi perusahaan.
