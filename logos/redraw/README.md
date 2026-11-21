# Paket sumber redraw untuk sesi chat lain

Folder ini berisi **13 gambar asli saja**, disalin tanpa resize, kompresi ulang,
perubahan warna, atau perubahan piksel. Tidak ada hasil redraw lama di sini.

- `PROMPT.md`: instruksi siap salin ke chat lain; mulai satu logo (05), tunggu penilaian.
- `variasi-NN-asli.png`: gambar sumber asli dengan nomor variasi aplikasi.
- `manifest.json`: pemetaan nomor, ID stabil, nama sumber, catatan pengguna, dan SHA-256.

Urutan: 05, 49, 50, 122, 123, 128, 179, 184, 188, 290, 294, 301, 328.
Untuk 179 terdapat permintaan khusus tekukan vertikal huruf C di tengah-tengah.

Cara pakai: buka `PROMPT.md`, salin promptnya, lalu lampirkan `variasi-05-asli.png`
ke sesi chat lain. Untuk chat tanpa akses repo, mengirim prompt saja tidak memberi
akses ke gambar: gambarnya juga harus dilampirkan. Lampirkan sumber berikutnya
hanya setelah hasil pertama dinilai. Jangan lampirkan hasil redraw sebelumnya.

Tidak ada perubahan aplikasi atau build APK pada penyerahan sumber ini.
