# Cut Grid Images — Android Kotlin

Aplikasi Android untuk **memotong satu gambar menjadi grid petak** dengan kontrol kolom dan baris
yang presisi, memilih petak mana yang dipakai, lalu menyimpannya ke galeri perangkat.

Paket aplikasi: `com.emrobinso.cutgridimages`. Tanpa dependensi runtime eksternal, tanpa internet;
semua pemrosesan di perangkat.

## Unduh APK

APK debug dibangun otomatis dan diterbitkan sebagai aset Release di setiap perubahan folder ini:

- Halaman rilis: <https://github.com/rokhmangalaxy/lg_6jt/releases>
- Berkas terbaru: `app-debug.apk` pada rilis `cutgridimages-v<N>` (tag mengikuti nomor run workflow).

Pasang di Android 8+ (minSdk 26) dan izinkan pemasangan dari sumber tidak dikenal bila diminta.
APK ditandatangani *debug keystore* milik runner CI, sehingga APK dari run berbeda memakai kunci
berbeda: uninstall dulu sebelum memasang versi baru. `sha256` setiap build dicetak di catatan rilis.

## Tiga layar

Navigasi bawah: **Beranda · Galeri · Pengaturan**.

### 1. Beranda

- Kotak isian bergaris putus-putus (**placeholder**) yang membuka pemilih gambar sistem
  (Storage Access Framework) dengan **multi-seleksi**. Tidak butuh izin baca.
- Gambar yang ditambahkan muncul sebagai **thumbnail mini dalam wadah 5 kolom × 2 baris yang bisa
  digulir vertikal**, ditambah satu petak `+` untuk menambah gambar lagi.
- Mengetuk thumbnail menjadikannya **gambar utama** pada editor.
- Tombol **Atur grid** membuka mode grid dengan **kolom/baris yang bisa dinaikkan/diturunkan
  (1–10 masing-masing)** dan pratinjau garis grid tepat di atas gambar.
- Mode **Seleksi**: mengetuk petak di gambar memberi **overlay warna semi-transparan** (warna dari
  Pengaturan, bawaan hijau muda) sebagai penanda petak yang dipilih; ketuk lagi untuk melepasnya.
- Tombol **Simpan (n)**, **Simpan semua**, dan **Bersihkan pilihan**; hasil disimpan sebagai
  potongan di layar Galeri (bukan langsung ke galeri perangkat).

### 2. Galeri

- Menampung potongan yang dipilih/dibuat dari Beranda.
- Tiga mode tampilan: **Daftar**, **Grid 3** (3 kolom), **Grid 5** (5 kolom), masing-masing dengan
  **paginasi** (10 / 9 / 15 item per halaman).
- **Multi-seleksi** (ketuk item) dengan tombol **Batal** dan **Hapus** (dialog konfirmasi).
- Aksi menu utama: **Simpan (n)** untuk seleksi dan **Simpan semua** — menulis berkas PNG ke
  `Pictures/CutGridImages` (Android 10+ lewat MediaStore tanpa izin; Android 8–9 meminta izin
  tulis).

### 3. Pengaturan

- **Nama proyek** (awalan nama berkas).
- **Jumlah digit nomor** bawaan **3** (boleh 1–6).
- **Pemisah karakter** bawaan **`_`**.
- **Warna transparansi seleksi** bawaan **hijau muda** (`#8BC34A`), 8 pilihan warna.
- **Pratinjau nama berkas** yang langsung berubah saat isian diubah, tombol **Simpan
  pengaturan**, dan **Hapus semua data gambar** (potongan + daftar sumber) dengan konfirmasi.

## Penamaan berkas

`<nama proyek><pemisah><nomor dengan digit tetap>.png`, misalnya `mcm_001.png`, `mcm_002.png`.
Nama proyek dibersihkan dari karakter yang tidak sah untuk nama berkas (spasi → `-`, garis miring
dan titik dua → `-`), pemisah kosong kembali ke `_`, dan nomor berjalan per proyek.

## Penyimpanan

- Potongan hasil seleksi disimpan sebagai PNG di penyimpanan internal aplikasi
  (`filesDir/pieces/`) dengan indeks `filesDir/pieces.json` — belum menyentuh galeri perangkat.
- Daftar URI gambar yang ditambahkan disimpan di `SharedPreferences` (`cutgrid_sources`), ditambah
  izin baca persisten bila penyedia mendukungnya.
- Setiap gambar yang berhasil dibaca **disalin** ke `filesDir/sources/` (JPEG, atau PNG bila
  beralfa) sehingga pemuatan berikutnya tidak bergantung pada izin URI penyedia dokumen —
  URI dari "Buka dengan"/"Bagikan" pun tetap bisa dibuka setelah aplikasi ditutup.
  Ketuk lama thumbnail di Beranda untuk menghapus gambar beserta salinannya.
- Pengaturan disimpan di `SharedPreferences` bernama `cutgrid_settings`.
- Ekspor ke perangkat menulis ke `Pictures/CutGridImages`:
  - Android 10+ (`API 29+`): MediaStore, tanpa izin apa pun.
  - Android 8–9 (`API 26–28`): penyimpanan publik + MediaScanner, meminta izin tulis saat ekspor.
- Orientasi EXIF diterapkan, jadi potongan tidak miring untuk foto kamera.
- Menerima gambar dari aplikasi lain lewat **Buka dengan** / **Bagikan**
  (`ACTION_VIEW` / `ACTION_SEND`) ke layar Beranda.

## Struktur

```
cutgridimages/
├── settings.gradle.kts, build.gradle.kts, gradle.properties
├── build-apk.sh, CI-ALTERNATIF.md
└── app/
    ├── build.gradle.kts
    └── src/
        ├── main/
        │   ├── AndroidManifest.xml
        │   ├── java/com/emrobinso/cutgridimages/
        │   │   ├── HomeActivity.kt        # Beranda: pilih gambar, thumbnail, grid, seleksi, simpan
        │   │   ├── GalleryActivity.kt     # Galeri: mode list/grid3/grid5, paginasi, hapus, ekspor
        │   │   ├── SettingsActivity.kt    # Pengaturan: proyek, digit, pemisah, warna, hapus data
        │   │   ├── grid/GridSlicer.kt     # matematika grid (murni Kotlin, teruji)
        │   │   ├── image/ImageSizing.kt   # ukuran sampel dekode (murni Kotlin, teruji)
        │   │   ├── image/PieceNaming.kt   # nama berkas potongan (murni Kotlin, teruji)
        │   │   ├── image/ImageLoader.kt   # dekode + rotasi EXIF
        │   │   ├── image/Thumbnails.kt    # dekode sampel untuk thumbnail
        │   │   ├── image/PieceExporter.kt # tulis potongan ke Pictures/CutGridImages
        │   │   ├── data/AppSettings.kt    # AppSettings + SettingsStore
        │   │   ├── data/ImageSourceStore.kt # daftar URI gambar + izin baca persisten
        │   │   ├── data/PieceStore.kt     # potongan PNG + indeks JSON
        │   │   ├── ui/GridEditorView.kt   # kanvas gambar, garis grid, overlay seleksi
        │   │   └── ui/Ui.kt               # pembantu dp/sp/latar membulat
        │   └── res/…                      # layout 4 berkas, warna, tema, ikon adaptif, drawable
        └── test/java/com/emrobinso/cutgridimages/
            ├── grid/GridSlicerTest.kt
            ├── image/ImageSizingTest.kt
            └── image/PieceNamingTest.kt
```

## Build melalui GitHub Actions

Workflow **Build Cut Grid Images APK** (`.github/workflows/cutgridimages-apk.yml`) berjalan saat
folder ini berubah, pada pull request, atau manual dari tab Actions.

Workflow menjalankan unit test (`testDebugUnitTest`) dan membangun APK debug; lint berjalan sebagai
langkah informasi sehingga temuannya tidak menghalangi artifact. Bila berhasil, unduh artifact
**cutgridimages-debug-apk**, ekstrak ZIP, lalu pasang `app-debug.apk`
(izinkan pemasangan dari sumber aplikasi pengunduh bila diminta). Ini APK debug untuk pengujian,
bukan rilis Play Store dan belum ditandatangani untuk distribusi.

Status: repository sudah **publik**, sehingga job Actions memakai runner standar gratis. Build
rilis `cutgridimages-v10` (run 44684760440) menyelesaikan `testDebugUnitTest`, `assembleDebug`,
lint (informatif), unggah artifact, dan penerbitan aset Release tanpa kegagalan.

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

- **19 unit test** untuk `GridSlicer`, `ImageSizing`, dan `PieceNaming` lulus (dijalankan dengan
  `kotlinc` 2.4.21 dan JUnit 4 API).
- Seluruh 10 sumber `app/src/main` (tiga activity, `ui/`, `data/`, `grid/`, `image/`) dikompilasi
  tanpa peringatan terhadap `android.jar` API 35.
- AAPT2 berhasil mengompilasi seluruh `res/` (4 layout + drawable + tema) dan menautkannya ke
  `base.apk` dengan `AndroidManifest.xml` baru — `dump badging` melaporkan label
  *Cut Grid Images*, ikon adaptif, dan `launchable-activity: com.emrobinso.cutgridimages.HomeActivity`
  (`--target-sdk-version 35`, `minSdkVersion 26`). `apksigner` juga berhasil menandatangani APK
  hasil tautan itu (skema v2 + v3 terverifikasi).
- **Build lengkap di GitHub Actions sudah berhasil** (run 44684760440, rilis `cutgridimages-v10`).
  APK yang dihasilkan diperiksa langsung di runner:
  - `package: name='com.emrobinso.cutgridimages' versionCode='10' versionName='1.0.10'
    compileSdkVersion='35'`, `targetSdkVersion:'35'`,
    `launchable-activity: HomeActivity` dengan label *Cut Grid Images*;
  - isi arsip: `classes.dex` (2,3 MB) + `classes2.dex`…`classes5.dex`, `resources.arsc`,
    `AndroidManifest.xml`, 25 entri total;
  - ukuran 901.652 byte, `sha256`
    `3a7723a49801e3788b5cf1e98f50fa812e8cde96343b347a6ff438757e0d96de`;
  - tanda tangan `apksigner verify`: DN `C=US, O=Android, CN=Android Debug`,
    sertifikat SHA-256 `58e6fe9facc6d74a3be5e082f230ac63ff888c47bef7006e329db90e071769ba`.
- **Sandbox agen tidak dapat merakit APK penuh** karena tidak ada dexer JVM (`d8`/`r8`) dan host
  unduhan besar (Google Maven, `objects.githubusercontent.com`, `release-assets.githubusercontent.com`,
  `*.blob.core.windows.net`) diblokir; karena itu job CI dipakai untuk menghasilkan APK yang bisa
  dipasang.
- Belum diuji: pemasangan di perangkat/emulator dan alur UI secara manual (build & unit test sudah
  hijau).

## Batasan yang diketahui

- Gambar didekode maksimum 4096 piksel pada sisi terpanjang (`ImageLoader.MAX_DIMENSION`) agar
  hemat memori; petak mengikuti resolusi tersebut.
- Grid lebih rapat daripada gambar (misalnya 10 × 10 pada gambar 5 piksel) akan melewati petak
  kosong, jadi jumlah potongan bisa kurang dari `kolom × baris`.
- Ekspor berjalan di satu thread latar; indikator kemajuan hanya berupa teks status, bukan progres
  per petak.
- Potongan disimpan di penyimpanan internal aplikasi sampai diekspor; menghapus data aplikasi
  (atau tombol *Hapus semua data gambar*) menghilangkan potongan yang belum diekspor.
- Tidak ada penandatanganan release, tidak ada iklan, dan tidak ada unggahan jaringan.
