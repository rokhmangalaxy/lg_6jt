# Release dan update tanpa uninstall

## Persyaratan identitas update
- Application ID selalu `id.mcm.logopreview`.
- Semua release ditandatangani dengan **keystore dan alias yang sama**.
- `versionCode` harus lebih tinggi dari versi terpasang. Workflow memakai `github.run_number`; jangan membuat ulang workflow/reset nomor tanpa mengatur versi agar tetap naik. Re-run run yang sama bukan versi update baru.
- APK debug yang pernah dipasang tidak bisa ditimpa release dengan sertifikat berbeda. Aturan ini berlaku untuk rantai **release → release**, bukan semua APK dari sumber lain.

## Sekali saja: pemilik menyiapkan signing
Buat keystore lewat Android Studio → Build → Generate Signed App Bundle / APK → APK → Create new. Simpan backup offline yang aman beserta password. Jangan unggah keystore atau password ke chat, repository, atau Release asset. Kehilangan kunci dapat membuat aplikasi tidak bisa diperbarui dengan identitas yang sama.

Di Settings → Secrets and variables → Actions, siapkan repository secrets:
- `ANDROID_KEYSTORE_BASE64`: encoding base64 dari file keystore (bukan enkripsi; tetap rahasia).
- `ANDROID_KEYSTORE_PASSWORD`.
- `ANDROID_KEY_ALIAS`.
- `ANDROID_KEY_PASSWORD`.

Integrasi workspace saat ini menerima HTTP 403 pada API Actions secrets sehingga tidak dapat menyiapkan secret ini. Tidak ada keystore sementara atau kunci baru per-build yang dipakai sebagai pengganti.

## Build dan download
Workflow **Build Android APK** berjalan setelah merge perubahan terkait ke `main` atau dijalankan manual. PR hanya menjalankan debug build/lint tanpa mengakses kunci. Release berhenti dengan pesan jelas jika secret belum lengkap.

Setelah build signed release dan verifikasi sertifikat berhasil, workflow membuat GitHub Release dan mengunggah asset **mcm-logo-studio-release.apk** langsung, bukan ZIP. Buka link APK asset pada release tersebut. Untuk repository private, pengguna perlu login dan akses repository; bukan tautan publik anonim. File keystore tidak pernah dipublikasikan.

Pada Android, izinkan instalasi dari aplikasi pengunduh, lalu buka APK versi baru untuk memperbarui. Uji pertama pada perangkat tetap diperlukan; menandatangani dan menaikkan versi tidak menjamin kompatibilitas setiap perangkat.
