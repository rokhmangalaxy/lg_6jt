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

Workflow menjalankan unit test (`testDebugUnitTest`) dan membangun APK debug; lint berjalan sebagai
langkah informasi sehingga temuannya tidak menghalangi artifact. Bila berhasil, unduh artifact
**cutgridimages-debug-apk**, ekstrak ZIP, lalu pasang `app-debug.apk`
(izinkan pemasangan dari sumber aplikasi pengunduh bila diminta). Ini APK debug untuk pengujian,
bukan rilis Play Store dan belum ditandatangani untuk distribusi.

Status: workflow sudah disiapkan, tetapi **APK belum dibangun di CI** pada sesi ini (Actions
repository belum menjalankan job).

Toolchain: JDK 17, Gradle 8.9, AGP 8.7.3, Kotlin 2.0.21, compile/target SDK 35, min SDK 26
(Android 8+). Tidak ada Gradle wrapper biner di repository; Gradle disiapkan oleh workflow.

## Build lokal

Buka folder `cutgridimages/` di Android Studio (JDK 17, SDK 35), atau jalankan skrip yang sudah
tersedia (memeriksa JDK, Android SDK, dan Gradle lebih dulu):

```sh
cd cutgridimages
./build-apk.sh          # debug + unit test
./build-apk.sh release  # release (belum ditandatangani)
```

Padanan manualnya:

```sh
cd cutgridimages
gradle testDebugUnitTest assembleDebug
```

Hasil: `app/build/outputs/apk/debug/app-debug.apk`. Build pertama memerlukan internet untuk
Google Maven, Maven Central, dan komponen SDK Android.

## Jika GitHub Actions kena limit

Job Actions pada repository **privat** memakai kuota menit berbayar; bila kuota habis atau
pembayaran/spending limit bermasalah, job tidak dijalankan sama sekali (pesan: *"The job was not
started because recent account payments have failed or your spending limit needs to be
increased"*). Workflow tidak perlu diubah; pilih salah satu jalan keluar:

1. **Jadikan repository publik.** Repository publik memakai runner standar gratis tanpa kuota
   menit, sehingga workflow langsung bisa berjalan. Periksa dulu tidak ada berkas sensitif.
2. **Perbaiki billing.** Settings → Billing & plans: perbarui metode pembayaran atau naikkan
   spending limit, lalu jalankan ulang workflow dari tab Actions.
3. **Build mandiri.** Pakai `./build-apk.sh` di komputer sendiri (Android Studio/Gradle) — tidak
   memerlukan Actions sama sekali.
4. **CI alternatif.** `codemagic.yaml` atau konfigurasi CircleCI bisa memakai runner gratis
   terpisah dari kuota GitHub; perlu menghubungkan repository di layanan tersebut.

Hemat menit Actions: workflow hanya berjalan saat berkas `cutgridimages/**` berubah, punya
`concurrency` dengan `cancel-in-progress`, dan memakai cache Gradle dari `gradle/actions/setup-gradle`.

Perbandingan lengkap jalur build (Codemagic, CircleCI, GitLab CI, Bitrise, self-hosted, lokal)
beserta konfigurasi yang sudah disiapkan: **[CI-ALTERNATIF.md](CI-ALTERNATIF.md)**.

## Verifikasi yang sudah dilakukan

- 13 unit test untuk `GridSlicer` dan `ImageSizing` lulus (dijalankan dengan `kotlinc` 2.4.21 dan
  JUnit 4 API).
- Seluruh sumber `app/src/main` dikompilasi tanpa peringatan terhadap `android.jar` API 35.
- AAPT2 (build-tools 28) berhasil mengompilasi seluruh `res/` dan menautkannya ke `base.apk`
  (`--target-sdk-version 35`, label & ikon adaptif terbaca), lalu `apksigner` menandatangani APK
  itu (skema v2 + v3 terverifikasi).
- **APK lengkap belum bisa dirakit di sandbox:** satu-satunya komponen yang tidak tersedia adalah
  dexer JVM (`d8`/`r8`). GitHub release assets (host `objects.githubusercontent.com`), Google Maven,
  dan Maven Central tidak dapat diakses dari sandbox; jar `d8.jar` yang ditemukan di repo GitHub
  semuanya pointer Git LFS. Karena itu job CI (Actions/Codemagic/CircleCI) atau build di mesin
  sendiri tetap diperlukan untuk menghasilkan APK yang bisa dipasang.
- Belum diuji: lint penuh dan pemasangan di perangkat/emulator.

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
