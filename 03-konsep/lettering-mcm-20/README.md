# 20 variasi lettering MCM

Eksplorasi bentuk inisial tanpa wadah kotak atau lingkaran, melanjutkan arah sederhana dari konsep no. 4. Ini bukan 20 varian warna dari bentuk yang sama: proporsi, konstruksi, potongan, atau hubungan antarhuruf dieksplorasi berbeda. Nomor 18 mencoba lowercase; lainnya uppercase.

## Buka galeri

`index.html` mandiri, semua SVG tertanam dan bisa dibuka offline. Tombol SVG/PNG mengunduh masing-masing konsep; PNG dirender 1600×800. `mcm-20-svg-png.zip` berisi seluruh 20 SVG, 20 PNG, dan manifest.

Semua lettering dibuat dari path/polygon SVG geometris, bukan font yang perlu diinstal. SVG bisa diedit di Inkscape/Illustrator. Celah putih masih berupa bidang/garis putih dalam beberapa eksplorasi, bukan selalu boolean knockout; background putih disengaja.

## Daftar

| No. | Arah | Eksplorasi |
|---|---|---|
| 01 | Geometris Tegas | Batang tebal dan potongan lurus; dasar pembanding. |
| 02 | Rapat Vertikal | Huruf ramping, lebih tinggi, dengan ruang antarhuruf rapat. |
| 03 | Bentang Lebar | Proporsi melebar dan valley M lebih rendah. |
| 04 | C Pilar | C lebih tinggi menjadi pusat; dua M sejajar di sisi. |
| 05 | Maju Presisi | Seluruh lettering condong, bukan wadah miring. |
| 06 | Stencil Lurus | Satu celah horizontal lebar membagi lettering menjadi bidang produksi. |
| 07 | Puncak Pendek | Valley M dangkal dengan C berujung tebal merah. |
| 08 | Valley Dalam | M berlekuk dalam; bukaan C dipersempit dengan ujung tebal. |
| 09 | Potong Diagonal | Celah diagonal memisahkan bagian atas dan bawah. |
| 10 | Sambungan Bawah | Tiga inisial dihubungkan oleh satu bidang bawah. |
| 11 | Dua Bidang | Dua zona warna solid, dipisahkan celah lurus tipis. |
| 12 | Monoline Struktural | Ketebalan garis seragam; C terbuka dan sudut tegas. |
| 13 | Rel Ganda | Batang rangkap yang terpisah celah putih; perlu uji ukuran kecil. |
| 14 | Bahu Bertingkat | Konstruksi M bertingkat; motif proses bertahap. |
| 15 | Ujung Terbuka | C berupa tiga batang terpisah; M memakai puncak rata. |
| 16 | Chamfer Metal | Sudut luar C dipotong; M diberi chamfer pada kaki. |
| 17 | Sayap Seimbang | Dua M saling bercermin dengan bidang C sebagai poros. |
| 18 | mcm Huruf Kecil | Interpretasi lowercase bersudut, tanpa wadah. |
| 19 | C Jembatan | C lebih lebar dan rendah, dua M menjadi pilar samping. |
| 20 | Kaki Terpisah | Batang huruf diangkat dari tiga kaki merah yang terpisah. |

## Seleksi awal yang disarankan
- 01: pembanding paling sederhana.
- 04: pusat visual C yang lebih dominan, mengingatkan karakter konsep no. 4.
- 12: konstruksi garis yang ringan dan bersih.
- 16: potongan sudut yang dekat dengan bahasa visual fabrikasi.

Ini penilaian awal desain, bukan hasil penilaian klien. Belum dilakukan audit kemiripan merek, uji ukuran seragam, uji bordir, dan verifikasi filosofi resmi. Varian stencil/rel ganda terutama perlu uji detail kecil. Ke-20 konsep belum dimasukkan ke APK.

## Reproduksi

Dari root repository:

```sh
npm install --prefix .cache/mcm-render @resvg/resvg-js
python scripts/build_mcm_lettering.py
```

Renderer resvg hanya dipakai untuk ekspor PNG; galeri/SVG hasilnya tidak membutuhkan dependency eksternal.
