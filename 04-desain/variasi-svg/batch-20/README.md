# Batch 20 — 10 master rasio manual, tanpa APK

Sumber **rasio_1 14/07–09 dan 15/01–07**. Pencarian berisi__20 tidak menemukan sumber pada folder yang sama; batch diteruskan lintas kelompok rasio agar mencapai sepuluh master baru. ID keluarga rasio terpisah dari berisi (`exp-rasio-014-07` dan seterusnya). Provenance nama sumber, Drive ID, SHA-256 dan master ada di `progress.json`.

## Struktur sumber yang dipertahankan

| Sumber rasio | Konstruksi manual |
|---|---|
| 14/07 | Frame M terbuka berukuran besar: V navy atas dan pilar merah, MCM navy kecil di bawah |
| 14/08 | Dua nameplate merah dengan empat lubang mounting transparan, MCM navy |
| 14/09 | Hexagon vertikal merah terpisah, M navy miring kiri/kanan, C navy tinggi |
| 15/01 | Diamond merah dengan empat ujung navy terpisah, MCM navy kompak |
| 15/02 | Dua panah merah ke atas, pilar samping navy, MCM navy bawah |
| 15/03 | Slab merah oblique, strip navy atas/bawah, MCM putih positif mengikuti kemiringan |
| 15/04 | Enam segmen hexagon terpisah dua warna, MCM navy dan C persegi |
| 15/05 | Rail atas merah dan bawah navy dengan cekungan tengah, MCM navy |
| 15/06 | I-beam perspektif dengan permukaan merah/navy terpisah, MCM navy di kanan |
| 15/07 | Bagian segitiga merah luar terpisah dan MCM navy angular |

Semua sepuluh referensi dibuka satu per satu; hasil render diperiksa kembali secara visual dalam montage. Koordinat diukur manual per sumber, bukan auto-trace, font atau substitusi desain generik. Kurva C disederhanakan sebagai chamfer pendek; lubang mounting sebagai polygon 16 sisi. Lubang mengikuti latar lewat fill-rule evenodd, bukan lingkaran putih. Huruf putih 15/03 merupakan layer positif recolorable. Celah antarsegmen transparan. Tekstur diratakan merah/navy/putih solid. Hasil belum disetujui pengguna, tidak diklaim pixel-perfect atau siap produksi.

## Progres dan audit terbatas

- **169 master Drive unik**, bertambah 10; redraw saja **169/342 = 49,42%**.
- Alias duplikat sumber terverifikasi tetap **18**, diwariskan tanpa perubahan.
- Cakupan sumber **187/342 = 54,68%**; **155 sumber tersisa**.
- Sepuluh hash sumber baru berbeda satu sama lain dan dari semua sumber master terdahulu. Generator mengunci pemeriksaan tersebut sebelum ekspor. Motif mirip tidak otomatis digabung.
- 342 tetap jumlah file yang dilaporkan, bukan jumlah desain unik terverifikasi global. Audit hanya mencakup sumber unduhan; snapshot historis tidak diubah.

## Artefak dan validasi

10 SVG path-only, 10 JSON native, 10 PNG preview, provenance/progress dan `perbandingan.html` mandiri/offline. HTML menyandingkan raster sumber dan SVG dengan toggle latar putih/abu-abu.

**99 tes lokal lulus:** 90 path-batch + 8 geometris + 1 variasi. Tes mencakup konsistensi SVG/JSON, penutupan/batas path, persilangan polygon, nonkolisi ID/hash/geometri, progres/alias tetap, empat counter mounting tanpa layer putih, huruf putih positif, katalog tetap dan job APK dijeda. Tidak ada tes perangkat Android baru.

**Tidak membangun APK, dispatch workflow, integrasi Android, atau rilis.** Katalog tetap 105 variasi; APK terakhir v1.0.42.

Reproduksi dengan sumber PNG lokal dan resvg:
```sh
python scripts/build_drive_batch_20.py
python -m unittest discover -s tests -p 'test_path_batches.py'
python -m unittest discover -s tests -p 'test*geometric*.py'
python -m unittest discover -s tests -p 'test_variation_vectors.py'
```
