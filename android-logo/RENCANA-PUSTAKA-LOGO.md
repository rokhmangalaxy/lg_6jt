# Rencana pustaka logo (342 logo hasil potong)

Catatan keputusan bersama, 20 November 2026. Dokumen ini bukan kode dan bukan janji rilis;
ia mengunci keputusan agar tidak bergeser dan menyimpan satu pekerjaan yang **ditunda**.

## Keputusan

1. **Tujuan**: logo hasil potong menjadi bagian aplikasi, memperkaya pilihan logo
   (menggantikan pola lima konsep saat ini). Bukan master vektor untuk produksi.
2. **Warna**: semua logo tampil dengan **warna asli**, termasuk lima konsep lama.
3. **Fitur enam permutasi palet** (merah/biru/putih): **ditunda**. Kode pemetaan warna
   tidak dihapus, tetapi tidak dipakai pada render. Lihat bagian *Ditunda* di bawah.
4. **Cakupan**: seluruh **342** logo (171 set *kotak* + 171 set *rasio*).
5. **Format**: **tidak memakai SVG.** Aset tampilan memakai WebP; PNG hasil potong tetap
   menjadi master di `drive_out/` dan folder Drive `mcm/logos`.

## Alasan menolak SVG

- Repositori ini belum pernah memuat SVG (`*.svg` = 0 berkas, termasuk riwayat git).
  Lima logo di `html/index.html` adalah PNG base64, bukan vektor.
- Logo hasil potong berkualitas raster: 6.683–9.194 warna unik per berkas. Trace otomatis
  menghasilkan layer noise (mis. `#FEFDFD`, `#FDF8F8`, `#FBE9E8`) dan tanpa `viewBox` seragam.
- Nilai vektor hanya berarti untuk master produksi (bordir/cetak), bukan untuk tampilan app.

## Ukuran aset (diukur pada 342 berkas)

| Format | Total | Catatan |
| --- | --- | --- |
| PNG sekarang | 28,0 MB | APK kini 941 KB → membengkak jadi ±29 MB |
| PNG quantize 256 + optimize | 18,7 MB | masih berat |
| WebP lossless | 20,3 MB | tidak sepadan |
| **WebP q85 (dipilih)** | **2,7 MB** | aset tampilan |
| JPEG q88 | 6,0 MB | tanpa alfa |
| **Thumbnail 160 px WebP** | **1,0 MB** | grid galeri |

## Rancangan teknis yang disepakati

- Aset di `app/src/main/assets/logos/` (`<nama>.webp`) dan `thumbs/` (160 px).
- `manifest.json` dibangkitkan skrip dari `drive_out/`: nama berkas, set (kotak/rasio),
  nomor lembar, indeks logo, dimensi, warna dominan. Menjadi satu-satunya sumber daftar.
- `MainActivity` memuat `index.html` seperti sekarang, tetapi gambar dibuka lewat
  **`WebViewAssetLoader`** (`https://appassets.androidplatform.net/assets/…`), bukan
  base64 di dalam HTML. Tetap offline; `allowFileAccess` dan `blockNetworkLoads` tidak
  dilonggarkan.
- Galeri: grid thumbnail + pencarian/filter per set, halaman detail dengan Prev/Next.
  342 titik navigasi tidak dipakai lagi.
- Label tampil: otomatis `Set Kotak 13 · 08` / `Set Rasio 7 · 03`, bukan nama berkas mesin.

## Ditunda — ingatkan lagi saat fitur palet digarap

`recolor()` di `html/index.html` saat ini **hardcoded**: `R==220` → slot merah,
`R==23` → slot biru, selain itu → slot putih. Ia hanya sah untuk artwork tiga warna solid
(lima konsep lama). Untuk logo baru, hampir semua piksel akan jatuh ke slot putih sehingga
logo hilang. Dua jalur yang sudah dinilai:

- **Mode 2 warna (duotone)**: latar + satu aksen dari enam permutasi. Jalan untuk semua
  logo, tetapi warna internal hilang.
- **Tiga warna per logo**: kuantisasi ke 3 warna saat build, lalu dipetakan ke slot.
  Struktur tiga nada bertahan, warna asli bergeser.

Belum dipilih. Jangan aktifkan tombol palet untuk logo baru sebelum salah satu jalur dipilih
dan diuji pada sampel.

## Catatan lain

- Ekspor PNG masih dinonaktifkan di Android; perlu diputuskan sebelum pustaka membesar.
- Logo berasal dari gambar hasil generasi AI, bukan tanda merek resmi dan bukan master bordir.
