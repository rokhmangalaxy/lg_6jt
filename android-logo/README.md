# MCM Logo Studio — Android Kotlin

Aplikasi Android Kotlin dengan WebView lokal, bukan website remote. Memuat lima logo tertanam dari `../html/index.html`, satu per halaman, navigasi Prev/Next, dan enam permutasi palet merah/biru/putih melalui pemetaan piksel Canvas. Tidak memerlukan izin internet, server sandbox, atau gambar baru per susunan warna.

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

## Batas versi awal
- Menggunakan UI HTML/Canvas yang dibungkus Activity Kotlin; bukan UI native Compose.
- Unduh PNG disembunyikan pada Android: ekspor native belum diimplementasikan. Gunakan HTML mandiri untuk mengunduh PNG.
- Pilihan warna hanya bertahan selama halaman aktif; pemuatan ulang/rotasi Activity akan meresetnya.
- Latar putih dan bagian putih logo berasal dari satu kelompok warna; belum dapat dipisahkan.
- Jangan memasukkan kunci signing ke repository. Versi release memerlukan konfigurasi signing terpisah.

## Update UI visual

Logo besar, panah navigasi, tombol swatch tanpa teks panjang. HTML yang sama otomatis dikemas saat build. Latar putih dikunci berdasarkan mask piksel putih yang tersambung tepi; bagian putih internal tertutup ikut palet. Signing demo tetap memakai identitas publik AOSP yang sama (lihat `RELEASE.md`), sehingga release baru dengan versionCode lebih tinggi dapat memperbarui demo sebelumnya. Masih perlu uji pada perangkat.
