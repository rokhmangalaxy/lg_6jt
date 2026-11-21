# Review perbaikan — putaran 01

29 item berstatus Perlu perbaikan dicatat pada `review.json`, termasuk 11 item tanpa
keterangan. Catatan pengguna dipertahankan; 98 dipisahkan sebagai catatan fitur.
Nama variasi dipetakan melalui katalog v1.0.79, bukan posisi daftar review.

## Selesai pada putaran ini (menunggu review visual)

- 05: empat ujung diamond dilunakkan; bentuk huruf tidak diubah.
- 44: cap C merah diganti dari puncak datar menjadi satu apex tengah sesuai sumber.
- 50: slit putih/transparan tengah dihentikan di bawah counter C; tidak lagi menempel
  pada ujung C. Slit bawah tetap dipertahankan, bukan dihapus seluruhnya.

Tiga SVG dan JSON adalah **salinan kerja koreksi**, bukan perubahan snapshot batch
atau aset aplikasi. HTML offline memperlihatkan sumber / sebelum / koreksi.
Koordinat ditulis manual; tanpa auto-trace. Render resvg diperiksa kembali.

## Kandidat konsolidasi visual

- 115, 169, 205 → master kerja 205 (MCM navy di atas diamond merah).
- 304, 313, 322 → master kerja 313 (MCM putih di atas diamond merah).

Ini penilaian visual keluarga bentuk, bukan skor matematis 90%. Pada 322 cap navy
kontinu memang berbeda dari empat tip 304/313; usulan konsolidasi memilih versi 313
secara sengaja, bukan mengklaim ketiganya identik byte/piksel. Perbandingan sumber
ketiganya disertakan agar keputusan dapat ditinjau. Tidak ada ID dihapus dan pemetaan
aplikasi **belum diterapkan**; jangan menganggap jumlah katalog sudah berkurang.
Kandidat lain seperti 278/284 tetap terpisah karena konstruksinya berbeda.

26 item belum dikoreksi, termasuk enam anggota kandidat konsolidasi; status detail
ada di `review.json`. Semua item tanpa keterangan tetap perlu pemeriksaan sumber
lebih rinci, bukan dianggap sesuai. Logo berstatus Sesuai tidak disentuh.

Validasi lokal: 8 tes dari modul `test_review_repairs.py` lulus (termasuk pemeriksaan
polygon tidak bersilangan dan tiga koordinat koreksi). Tidak ada build APK atau tes
perangkat pada putaran ini. Katalog 330, favorit, catatan lokal dan APK v1.0.79 tetap.

Reproduksi: `python scripts/build_review_repairs_01.py`
