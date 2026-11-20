# Cut Grid Images — Android Kotlin

Aplikasi Android kecil untuk **memotong satu gambar menjadi grid petak** (misalnya 3 × 3 untuk
unggahan berurutan di media sosial) lalu menyimpan setiap petak ke galeri.

Paket aplikasi: `com.emrobinso.cutgridimages`.

## Fitur

- Pilih gambar lewat pemilih berkas sistem (Storage Access Framework) — tidak butuh izin baca.
- Grid 1–10 kolom dan 1–10 baris, dengan pratinjau garis grid tepat di atas area gambar.
- Keluaran PNG (transparansi dipertahankan) atau JPEG (latar putih, kualitas 95).
- Petak disimpan ke `Pictures/CutGridImages`:
  - Android 10+ (`API 29+`): MediaStore, tanpa izin apa pun.
  - Android 8–9 (`API 26–28`): penyimpanan publik + MediaScanner, meminta izin tulis saat ekspor.
- Menerima gambar dari aplikasi lain lewat **Buka dengan** / **Bagikan** (`ACTION_VIEW` / `ACTION_SEND`).
- Orientasi EXIF diterapkan, jadi potongan tidak miring untuk foto kamera.
- Tanpa dependensi runtime eksternal dan tanpa izin internet; semua pemrosesan di perangkat.

Nama berkas hasil: `cutgrid_<yyyyMMdd_HHmmss>_r<baris>c<kolom>.<png|jpg>`, misalnya
`cutgrid_20261120_141530_r2c3.png`.

## Struktur

```
cutgridimages/
├── settings.gradle.kts, build.gradle.kts, gradle.properties
└── app/
    ├── build.gradle.kts
    └── src/
        ├── main/
        │   ├── AndroidManifest.xml
        │   ├── java/com/emrobinso/cutgridimages/
        │   │   ├── MainActivity.kt          # alur pilih → atur → ekspor
        │   │   ├── grid/GridSlicer.kt       # matematika grid (murni Kotlin, teruji)
        │   │   ├── image/ImageSizing.kt     # ukuran sampel dekode (murni Kotlin, teruji)
        │   │   ├── image/ImageLoader.kt     # dekode + rotasi EXIF
        │   │   ├── image/TileExporter.kt    # potong bitmap, tulis ke galeri
        │   │   └── ui/GridPreviewView.kt    # pratinjau bitmap + garis grid
        │   └── res/…                       # layout, warna, tema, ikon adaptif
        └── test/java/com/emrobinso/cutgridimages/
            ├── grid/GridSlicerTest.kt
            └── image/ImageSizingTest.kt
```

## Build melalui GitHub Actions

Workflow **Build Cut Grid Images APK** (`.github/workflows/cutgridimages-apk.yml`) berjalan saat
folder ini berubah, pada pull request, atau manual dari tab Actions.

Workflow menjalankan unit test (`testDebugUnitTest`), membangun APK debug, dan lint. Bila berhasil,
unduh artifact **cutgridimages-debug-apk**, ekstrak ZIP, lalu pasang `app-debug.apk`
(izinkan pemasangan dari sumber aplikasi pengunduh bila diminta). Ini APK debug untuk pengujian,
bukan rilis Play Store dan belum ditandatangani untuk distribusi.

Toolchain: JDK 17, Gradle 8.9, AGP 8.7.3, Kotlin 2.0.21, compile/target SDK 35, min SDK 26
(Android 8+). Tidak ada Gradle wrapper biner di repository; Gradle disiapkan oleh workflow.

## Build lokal

Buka folder `cutgridimages/` di Android Studio (JDK 17, SDK 35), atau:

```sh
cd cutgridimages
gradle testDebugUnitTest assembleDebug
```

Hasil: `app/build/outputs/apk/debug/app-debug.apk`. Build pertama memerlukan internet untuk
Google Maven, Maven Central, dan komponen SDK Android.

## Batasan yang diketahui

- Gambar didekode maksimum 4096 piksel pada sisi terpanjang (`ImageLoader.MAX_DIMENSION`) agar
  hemat memori; petak mengikuti resolusi tersebut.
- Grid lebih rapat daripada gambar (misalnya 10 × 10 pada gambar 5 piksel) akan melewati petak
  kosong, jadi jumlah berkas bisa kurang dari `kolom × baris`.
- Ekspor berjalan di satu thread latar; indikator kemajuan hanya berupa teks status, bukan progres
  per petak.
- Membuka aplikasi ulang memuat kembali gambar terakhir pada sesi yang sama; tidak ada riwayat
  gambar atau pengaturan yang disimpan permanen.
- Tidak ada penandatanganan release, tidak ada iklan, dan tidak ada unggahan jaringan.
