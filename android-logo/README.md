# MCM Logo Studio — Android Kotlin

Aplikasi Android Kotlin dengan WebView lokal, bukan website remote. Memuat pustaka
**347 logo** (5 konsep lama + 342 hasil potong) dari `../html/`: grid dengan pencarian dan
filter set, lalu tampilan detail dengan Prev/Next. Semua logo memakai warna aslinya.

Aset disajikan lewat **`WebViewAssetLoader`** pada origin `https://appassets.androidplatform.net`,
jadi halaman dapat memakai jalur relatif (`assets/logos/*.webp`) tanpa mengaktifkan akses
`file://`. Manifest Android tidak meminta izin INTERNET.

## Status build
Proyek dan workflow build sudah disiapkan. **APK belum dibangun atau diuji di perangkat.** Workspace saat ini tidak memiliki JDK/Android SDK/Gradle dan akses unduh dibatasi, sehingga dependensi Google Maven/Android SDK tidak bisa dipenuhi secara lokal.

## Build melalui GitHub Actions
Setelah perubahan di-push pada branch kerja, workflow **Build Android APK** berjalan otomatis. Alternatif: setelah workflow tersedia pada default branch, jalankan dari Actions → Build Android APK → Run workflow dan pilih ref yang ingin dibangun.

Jika build dan lint berhasil, unduh artifact **mcm-logo-studio-debug-apk**, ekstrak ZIP, lalu pasang `app-debug.apk` di Android (izinkan pemasangan dari sumber aplikasi pengunduh Anda bila diminta). Ini APK debug untuk review internal, bukan rilis Play Store. Artifact mengikuti izin repository, bukan publikasi GitHub Pages.

Build memakai JDK 17, Gradle 8.9, AGP 8.7.3, Kotlin 2.0.21, compile/target SDK 35, min SDK 26 (Android 8+). Workflow menyiapkan toolchain; tidak ada Gradle wrapper biner dalam repository.

## Build lokal / Android Studio
Buka folder `android-logo/` di Android Studio dengan JDK 17 dan SDK 35. Jalankan Gradle 8.9:

```sh
cd android-logo
gradle assembleDebug lintDebug
```

Output: `app/build/outputs/apk/debug/app-debug.apk`. Build pertama memerlukan internet untuk Google Maven, Maven Central, dan SDK Android.

Aset pustaka disalin otomatis dari `../html/` ke `web/` di dalam assets oleh task
`syncLogoAssets`; perkiraan ukuran APK ±5 MB (WebP 3,84 MB).

## Batas versi awal
- Menggunakan UI HTML yang dibungkus Activity Kotlin; bukan UI native Compose.
- Ekspor/unduh gambar belum tersedia di Android.
- Susunan warna (enam permutasi merah/biru/putih) dinonaktifkan; logo tampil dengan warna asli. Rencana dan alasan ada di `RENCANA-PUSTAKA-LOGO.md`.
- Galeri memuat thumbnail 160 px; gambar penuh dimuat saat detail dibuka.
- Jangan memasukkan kunci signing ke repository. Versi release memerlukan konfigurasi signing terpisah.
