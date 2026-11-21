# Putaran 04 — master konsolidasi dan shortcut catatan

Dua master kerja manual disiapkan dari enam item yang tersisa:

- 115, 169, 205 → master 205 (MCM navy pada diamond merah).
- 304, 313, 322 → master 313 (MCM putih pada diamond merah).

Tip navy dan diamond diseimbangkan, M kanan dicerminkan, C dirapikan dengan radius
manual. Perbedaan cap kontinu 322 sengaja tidak dipertahankan sebagai varian master
tersendiri. Sumber keenam item dapat dilihat di HTML offline. Tidak ada sumber dihapus.

Cakupan kerja 29/29 (100%): 23 koreksi individual + 6 anggota diwakili 2 master.
Ini **bukan** 29 persetujuan visual, bukan 29 item yang sudah dipasang di aplikasi,
dan bukan pengurangan katalog. Pemetaan alias/hide di katalog belum diterapkan;
ID lama tetap ada, favorit dan catatan tidak dimigrasikan otomatis.

## Shortcut di aplikasi

`Seluruh catatan` kini memiliki tombol dua kolom untuk langsung membuka logo
perbaikan berdasarkan ID stabil. Daftar awal 29 item dari review pengguna disimpan
terpisah dalam `temporary-review/repair-shortcuts.json`, tidak disalin ke preferences.
Rating lokal terbaru diutamakan: Sesuai/Belum dicek mengeluarkan item dari shortcut;
Perlu perbaikan menambah item baru. Kedua anggota yang akan digabung tetap dapat
dibuka satu per satu sampai konsolidasi aplikasi diterapkan.

Ketuk shortcut menyimpan posisi dan membuka pasangan sumber/redraw yang sudah
terpaket pada versi aplikasi; **tidak** memakai pewarisan radio Next. Tidak mengubah
radio, notes, clipboard, favorit maupun dark mode. Catatan tersimpan dan salin-semua
masih bekerja dengan format/order semula. Shortcut tidak otomatis menampilkan salinan
kerja koreksi karena aset studio/review belum diganti pada putaran ini.

Validasi lokal: 39 tes perbaikan, 3 tes review statis/packaging dan 170 tes batch
lulus. Render dua master diperiksa. Tes Robolectric tambahan meliputi baseline,
rating lokal, shortcut baru, navigasi ID, tanpa inheritance, catatan dan recreation;
belum dijalankan karena Java/SDK tidak tersedia lokal. Tidak build APK pada putaran
ini; APK v1.0.79 belum memiliki shortcut ini.

Reproduksi master: `python scripts/build_review_repairs_04.py`.
