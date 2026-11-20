# Alternatif CI untuk build APK Cut Grid Images

Job GitHub Actions pada repository **privat** memakai kuota menit berbayar; bila kuota habis atau
pembayaran/spending limit bermasalah, job tidak dijalankan sama sekali. Dokumen ini membandingkan
jalan keluar yang benar-benar bisa dipakai repo ini, sekaligus menunjukkan berkas konfigurasi yang
sudah disiapkan.

Angka kuota per November 2026; selalu cek ulang halaman harga masing-masing layanan sebelum
memutuskan. Semua jalur memakai toolchain yang sama — JDK 17, Gradle 8.9, compile/target SDK 35 —
dan menjalankan `testDebugUnitTest` lalu `assembleDebug`, jadi APK yang dihasilkan setara.

## Ringkasan

| Layanan | Kuota gratis | Android siap pakai | Setup di sisi Anda | Berkas di repo |
| --- | --- | --- | --- | --- |
| **GitHub Actions, repo publik** | Runner standar **tanpa batas menit** untuk repo publik; repo privat 2.000 menit/bulan | Workflow sendiri | Ubah visibilitas repo (±30 detik) | `.github/workflows/cutgridimages-apk.yml` |
| **Codemagic** | **500 menit build/bulan**, 1 build paralel, 1 anggota tim, batas 120 menit per build | Ya, image Linux/macOS + Android SDK | Login → Add application → pilih repo → Start build | `codemagic.yaml` (mesin default; `linux_x2`/`linux_x4` butuh billing aktif) |
| **CircleCI** | **30.000 kredit/bulan** (≈3.000 menit mesin medium, ≈6.000 menit small), 5 user | Ya, image `cimg/android` | Login → Set up Project | `.circleci/config.yml` |
| **GitLab CI** | **400 compute menit/bulan**, 5 user, 10 GiB | Ya, image `cimg/android` | New project → Import from GitHub (kode ikut tersalin) | `.gitlab-ci.yml` |
| **Bitrise** | Hobby: 1 app privat, **300 kredit/bulan**, 1 user, timeout 90 menit | Ya, khusus mobile | Daftar → Add app → setup lewat UI | — (konfigurasi di UI) |
| **Self-hosted runner** | Menit gratis (mesin sendiri) | Anda yang menyiapkan SDK | Daftarkan runner + butuh entitlement Actions | contoh di bawah |
| **Build lokal** | Tak terbatas, tanpa layanan pihak ketiga | Android Studio/Gradle | `./build-apk.sh` | `build-apk.sh` |

## Kapan memilih yang mana

1. **Repo boleh publik** → GitHub Actions. Nol setup baru, workflow sudah ada, tidak ada kuota menit
   untuk runner standar. Ini jalur tercepat dan yang Anda pilih.
2. **Repo harus privat, ingin paling sedikit ribet** → **Codemagic**. YAML sudah siap dan langsung
   terbaca; 500 menit/bulan cukup untuk puluhan build APK kecil ini (satu build dingin ±3–5 menit,
   berikutnya ±2–3 menit dengan cache).
3. **Repo privat, butuh kuota lebih besar atau beberapa job paralel** → **CircleCI** (30.000 kredit
   ≈ 3.000–6.000 menit tergantung ukuran mesin, 5 user).
4. **Sudah punya akun GitLab / ingin cermin repo** → **GitLab CI**. Kuotanya paling kecil (400 menit),
   dan kode akan tersalin ke GitLab.
5. **Butuh langkah khas mobile** (signing terkelola, unggah ke Play Console) → **Bitrise**, walau
   setup-nya paling manual dan kuota kreditnya paling sedikit.
6. **Tidak mau bergantung layanan CI** → build lokal (`./build-apk.sh`) atau self-hosted runner.

## Cara memakai konfigurasi yang sudah ada

### Codemagic

1. Masuk ke <https://codemagic.io> dengan akun GitHub, tambahkan repository ini.
2. Codemagic mendeteksi `codemagic.yaml` di root repo; pilih workflow
   **Cut Grid Images — debug APK** lalu **Start new build**.
3. APK dan laporan test tersedia di tab **Artifacts**.

### CircleCI

1. Masuk ke <https://app.circleci.com> dengan akun GitHub → **Projects** → **Set up Project**.
2. Pilih repository ini; CircleCI memakai `.circleci/config.yml` yang sudah ada.
3. Unduh hasil dari tab **Artifacts** job `build-cutgridimages`.

### GitLab CI

1. Buat project baru → **Import project** → **GitHub** → pilih repo ini.
2. Pipeline berjalan otomatis memakai `.gitlab-ci.yml`; APK ada di **Build → Jobs → Artifacts**.

### Bitrise

Tidak ada berkas konfigurasi karena Bitrise menyimpan workflow di UI. Pilih template **Android**
saat menambahkan app, lalu tambahkan step `Gradle Unit Test` dan `Android Build` dengan
`./gradlew`/`gradle assembleDebug`. Karena repo ini tidak menyertakan Gradle wrapper, tambahkan
langkah yang memasang Gradle 8.9 seperti pada konfigurasi lain.

### Self-hosted runner (PC sendiri)

Menit self-hosted tidak dihitung sebagai kuota, tetapi job tetap memerlukan entitlement Actions.
Jika entitlement sudah pulih, tambahkan workflow berikut dan jalankan runner di mesin yang punya
JDK 17 + Android SDK:

```yaml
name: Build Cut Grid Images APK (self-hosted)
on:
  workflow_dispatch:
jobs:
  build:
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v5
      - run: |
          cd cutgridimages
          gradle --no-daemon testDebugUnitTest assembleDebug
      - uses: actions/upload-artifact@v4
        with:
          name: cutgridimages-debug-apk
          path: cutgridimages/app/build/outputs/apk/debug/app-debug.apk
```

## Pertimbangan keamanan dan privasi

- Codemagic, CircleCI, dan Bitrise memakai integrasi OAuth/GitHub App: mereka mendapat akses baca
  ke repository yang Anda hubungkan (bisa dicabut kapan saja dari GitHub Settings → Applications).
- GitLab **menyalin** isi repo ke server GitLab; pastikan project GitLab-nya privat bila repo GitHub
  tetap privat.
- Semua konfigurasi hanya menjalankan build; tidak ada credential atau signing key yang disimpan.
  APK yang dihasilkan adalah **APK debug**, bukan rilis bertanda tangan produksi.
- Repo ini tidak berisi kredensial (sudah diperiksa); `android-logo/demo-signing/*` adalah kunci
  demo AOSP yang memang publik.

## Batas yang sama untuk semua jalur

- Semua konfigurasi memasang **Gradle 8.9** dan **platform android-35 + build-tools 35.0.0** bila
  belum ada, jadi hasilnya tidak bergantung pada versi bawaan image runner.
- Build pertama mengunduh AGP, Kotlin, dan SDK platform 35 (~1–2 menit tambahan).
- Semua runner memakai Gradle 8.9 yang diunduh saat build karena repo tidak menyimpan wrapper biner;
  kalau Anda ingin build lebih cepat/offline, menambahkan Gradle wrapper adalah langkah berikutnya.
- APK debug hanya untuk pengujian internal; distribusi publik tetap butuh signing config terpisah.
