# Redraw geometris logo no.4 — kandidat untuk persetujuan

## Tujuan
Mengganti kontur auto-trace yang bergelombang dengan konstruksi titik/garis eksplisit. Ini redraw manual melalui koordinat, bukan penelusuran piksel otomatis atau sekadar memperbesar PNG.

## Isi
- **`mcm-04-geometris.svg`**: master kandidat, satu path dengan empat kontur dan fill-rule evenodd; latar serta area MCM transparan.
- `mcm-04-geometris-putih.png`: ekspor pada putih, lebar 2400px.
- `mcm-04-geometris-transparan.png`: ekspor transparan, lebar 2400px.
- **`perbandingan.html`**: sumber raster dan redraw, offline, slider pembesaran hingga 400%, pilihan latar putih/abu-abu, unduh SVG/PNG.
- `diagram-konstruksi.svg`: sumbu dan batas konstruksi, bukan artwork final.
- `konstruksi.json`: parameter bentuk dan koordinat.
- `mcm-04-geometris.json`: kandidat data native Android, belum dimasukkan ke katalog aplikasi.

## Aturan konstruksi
- Canvas 340×300; sumbu vertikal x=170.
- Diamond: (170,32), (308,150), (170,268), (32,150). Empat sisi lurus, sudut tegas.
- M kanan tepat merupakan mirror M kiri pada x=170.
- C tinggi mempertahankan karakter huruf pusat. Ujung/shoulder dibuat chamfer, bukan kurva.
- Seluruh artwork hanya memiliki perintah M/L/Z, tanpa kurva Bézier, font atau gambar tertanam.
- Merah #DC2626. Putih yang terlihat pada PNG berasal dari background; inisial adalah ruang negatif sungguhan.

## Perbedaan yang disengaja
Tidak diklaim identik piksel demi piksel: ketidakteraturan sumber dibuang, dua M disamakan, ujung diamond yang membulat menjadi tegas, dan C dirapikan ke potongan lurus. Jika klien ingin mempertahankan lengkung C, itu dapat dibuat sebagai lengkung terukur di iterasi berikutnya, tanpa mengubah sisi yang seharusnya lurus.

SVG tetap bergeometri lurus pada pembesaran berapa pun, tetapi layar dan PNG tetap dirasterisasi sehingga pada zoom ekstrem masih ada piksel antialias. Keunggulan SVG adalah dapat dirender ulang pada resolusi yang dibutuhkan, bukan menjadikan layar bebas piksel.

**Status:** belum pengganti resmi logo atau master produksi yang disetujui. Tiga logo lampiran dan APK tidak diubah. Perlu penilaian visual pengguna, uji ukuran kecil/bordir, dan pemeriksaan kemiripan merek.

## Reproduksi dan pemeriksaan
```sh
npm install --prefix .cache/mcm-redraw @resvg/resvg-js
python scripts/build_logo04_geometric.py
python -m unittest discover -s tests -p 'test_logo04_geometric.py'
```

Tes memeriksa tipe perintah path, mirror dua M, diamond empat sisi, posisi seluruh lubang di dalam bidang, kandidat JSON, serta dimensi ekspor. Tes geometri bukan persetujuan estetis atau uji produksi.
