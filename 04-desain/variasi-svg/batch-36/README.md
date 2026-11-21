# Batch 36 — lima sumber terakhir, tanpa APK

Sumber rasio_1 **tanpa nomor tambahan /05–09**, nama persis `Max_a_Gambar_kotak_rasio_1_logo-NN.png`. Berbeda dari kelompok rasio 1 bernomor tambahan. group=0 hanya sentinel internal; ID memakai `exp-rasio-unnumbered-NN`. Provenance ada di `progress.json`.

Lima sumber dibuka individual; polygon diukur dan ditulis manual, bukan auto-trace, font atau substitusi generik. Render diperiksa dalam montage. Target biasanya 10 unik, tetapi hanya lima sumber tersisa; tidak menambah desain rekaan.

| Sumber | Struktur |
|---|---|
| /05 | Cap/alas navy dengan notch, MCM merah tinggi |
| /06 | Dua rail I-beam merah berlekuk, MCM navy ber-chamfer |
| /07 | Cap/alas lipatan merah turun, dua M navy meruncing dan C navy perspektif |
| /08 | C merah tinggi dengan mulut diagonal, dua M navy bersayap |
| /09 | Tower merah terbelah, dua kaki atap navy terpisah, MCM merah dan dua baseline navy |

Seluruh celah mengikuti latar; tidak ada bidang putih di batch ini. Tekstur diratakan menjadi warna solid; kurva diregularisasi dengan chord/chamfer pendek. Hasil masih menunggu persetujuan visual, tidak diklaim pixel-perfect atau final produksi.

## Penutupan cakupan sumber

- **324 master Drive unik** (+5); redraw saja **324/342 = 94,74%**.
- **18 alias exact-byte**, diwariskan tanpa perubahan dan diverifikasi ulang hash-nya terhadap master tujuan.
- **342/342 sumber tercakup = 100%; sisa 0** terhadap inventaris sumber yang dilaporkan.
- Ini menyelesaikan cakupan sumber, bukan persetujuan visual, integrasi aplikasi atau rilis.

## Audit inventaris yang dapat direproduksi

`audit_inventory.json` mencatat seluruh 342 nama PNG, Drive ID, SHA-256, jenis master/alias dan master tujuan. Generator mencocokkan:

1. Seluruh progress batch dan dua master awal 1/01 serta 1/08 dari katalog historis, tanpa mengubah katalog.
2. 324 ID master unik, 324 hash sumber master unik, 18 alias dengan hash sama persis dengan master tujuan.
3. 342 nama sumber unik dan 342 Drive ID unik; setiap master memiliki SVG dan JSON native yang ada.
4. Seluruh 342 PNG lokal cocok dengan nama provenance dan inventaris: berisi 1–19, rasio bernomor 1–18, serta rasio tanpa nomor tambahan, masing-masing 01–09. Tidak ada sumber lokal tak tercakup atau ekstra.

**Batas audit:** seluruh PNG yang telah diunduh, bukan listing penuh Drive terbaru atau deduplikasi kesamaan visual semantik. Motif mirip tidak otomatis disamakan; 324 adalah master dengan sumber byte-unik, bukan klaim 324 konsep visual berbeda. Snapshot historis tidak diubah.

## Artefak dan validasi

5 SVG path-only, 5 JSON native, 5 PNG preview, progress/provenance, audit inventaris, dan HTML mandiri/offline dengan sumber asli serta pilihan latar putih/abu-abu. Raster hanya referensi, bukan master.

**179 tes lokal lulus:** 170 path-batch, 8 geometris dan 1 variasi. Mencakup konsistensi SVG/JSON, batas/penutupan path, persilangan polygon, nonkolisi ID/geometri/hash, progres/alias, inventaris 342 sumber, katalog tetap dan jeda APK.

**Tidak ada build APK, dispatch workflow, integrasi Android atau rilis.** Katalog tetap 105 variasi; APK terakhir v1.0.42. Tidak ada tes perangkat Android baru. Seluruh master masih memerlukan persetujuan visual sebelum integrasi.

Reproduksi dengan seluruh PNG sumber lokal dan resvg:
```sh
python scripts/build_drive_batch_36.py
python -m unittest discover -s tests -p 'test_path_batches.py'
python -m unittest discover -s tests -p 'test*geometric*.py'
python -m unittest discover -s tests -p 'test_variation_vectors.py'
```
