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

## Migrasi native Kotlin (versi berikutnya)

APK sekarang menggunakan **Android Views + Canvas/Bitmap native**, bukan WebView/HTML/JavaScript. HTML mandiri tetap tersedia sebagai preview web terpisah, tetapi tidak lagi dikemas oleh APK. Build hanya menyalin lima PNG asli.

- Area logo memakai layout weight, gambar fit-center tanpa mengubah rasio; header 56dp, navbar bawah 60dp, Prev/Next 48dp, swatch 64dp, nomor 48dp. System bar/keyboard insets ditangani melalui WindowInsets.
- Decode, mask, dan perubahan warna dijalankan serial di background executor; hasil Bitmap di-cache maksimal delapan kombinasi, sumber/mask maksimal lima logo. Request lama tidak boleh menimpa pilihan terbaru.
- Empat preset, mask lubang huruf nameplate, swipe native, ikon galaksi, menu/reset, dan catatan lokal dipertahankan.
- Pilihan logo/palet, draft, dan catatan native tersimpan dalam SharedPreferences privat. Jenis catatan Bug/Pengembangan, waktu dan nomor logo dicatat. Penghapusan perlu konfirmasi.
- **Catatan WebView lama belum dimigrasikan.** Storage WebView tidak dihapus oleh kode ini, tetapi catatan lama tidak tampil dalam UI native. Jika penting, salin catatan sebelum memperbarui. Jangan uninstall/hapus data bila ingin mempertahankan data lama.
- Tidak ada ekspor PNG native (sama seperti APK sebelumnya). Masih ada pada HTML mandiri.
- Unit test Kotlin `LogoPixelsTest` menguji mask/counter, empat preset, reset, dan immutability. Jalankan `gradle testDebugUnitTest assembleDebug lintDebug` atau workflow release untuk versi release.

Performa subjektif, ukuran font besar, layar pendek/landscape, TalkBack, dan update dengan catatan lama masih perlu pengujian perangkat nyata. Signing dan application ID tidak berubah.

## Sepuluh konsep + neumorphism

Katalog native kini 10 logo: lima lama tetap pada indeks yang sama, ditambah Hexa Frame, Folded MCM, Shield, Interlock, dan Precision Cut. `LogoCatalog` menjadi sumber jumlah/nama/file; navigasi wrap 10→1 dan 1→10. Nomor 01–10 dapat digeser horizontal, masing-masing target 52dp. Pilihan palet lama dan catatan native tetap pada namespace SharedPreferences yang sama.

UI neumorphism memakai latar #E9EEF5, relief bayangan terang di kiri atas dan gelap di kanan bawah. Tombol terpilih/tertekan memakai tampilan inset dengan penanda warna/border agar tidak hanya bergantung pada bayangan. Kartu gambar tetap putih/abu-abu sesuai preset, efek UI tidak dicampur ke piksel logo. Semua digambar native melalui `NeoSurface`/Canvas, bukan WebView.

Cache sumber dibatasi 3 gambar dan cache hasil 8 kombinasi; antrean render yang sudah usang dilewati. Bayangan memakai software layer lokal pada kontrol/kartu, sehingga kelancaran masih harus divalidasi di perangkat kelas bawah. Katalog dan mask nameplate tambahan tercakup unit test. HTML offline ikut diperbarui menjadi 10 logo dan gaya neumorphism sebagai preview terpisah, bukan UI di APK.

## Client review: download PNG dan navigasi bawah disembunyikan

Tombol simbol ↓ pada header membuka Android Storage Access Framework (`ACTION_CREATE_DOCUMENT`, image/png), sehingga pengguna memilih lokasi/nama file tanpa izin storage luas. PNG berisi Bitmap hasil swatch aktif pada resolusi sumber asli, bukan screenshot layar; shadow neumorphism, header, dan kontrol tidak ikut diekspor. Pilihan logo/preset disnapshot saat tombol ditekan. Cancel tidak mengubah sumber atau swatch. Nama default `MCM-logo-XX-swatch-N.png`.

Preview/loading menonaktifkan tombol sampai gambar tersedia. Export dan kompresi berjalan pada executor latar. Status berhasil/gagal diberikan; saat gagal, pengguna dapat mencoba lagi. Background putih/gray dan counter teks mengikuti preview. PNG masih raster konsep, bukan SVG/master vektor/berkas mesin bordir.

Navigasi bawah Logo/Menu/Catatan sementara tidak ditampilkan; aplikasi selalu membuka studio. Semua SharedPreferences catatan/draft lama tetap disimpan, tidak dihapus. UI HTML terpisah juga menyembunyikan navigasi bawah dan memindahkan tombol unduh ke header.

Tes decoder Android memperluas 10 logo × 4 swatch ke proses encode/decode PNG, memeriksa ukuran serta piksel representatif. Pemilih lokasi Android dan akses provider penyimpanan tetap perlu diuji pada perangkat nyata.

## Pilihan klien: hanya empat logo

Katalog terbaru menggantikan sepuluh eksplorasi dengan simbol no.4 tanpa wordmark, lalu lampiran sel 1/8/9 (grid kiri ke kanan, atas ke bawah). APK mengemas tepat empat PNG di `logo-assets/`, tidak lagi seluruh `html/assets/`. Lihat `../04-desain/pilihan-client/README.md`.

Mask background memakai alpha eksplisit agar lubang/outline hitam pada referensi dipisahkan dari huruf putih. Swatch 1/2 pada tiga simbol lampiran memakai background hitam sesuai referensi, sedangkan no.4 tetap putih. Mode monokrom semuanya gray. Preview/ekspor native menggunakan jalur render yang sama. Pilihan katalog baru memakai preferensi tersendiri; catatan lama tidak disentuh.

## Perbaikan preview bergerigi dan background

Semua 4 logo × 4 swatch sekarang memakai background abu-abu terang #D1D5DB, tanpa background hitam. Ini mempertahankan keterbacaan inisial putih. PNG referensi tidak lagi digunakan langsung sebagai bitmap preview yang diperbesar.

`LogoVectorRenderer` membaca path M/L/Q/Z dari JSON pendamping, menggambar dengan Android Canvas dan Paint.ANTI_ALIAS_FLAG ke bitmap bersisi maksimum 1600px. Preview dan unduhan memakai bitmap render yang sama. Cache hasil dibatasi 32 MiB, bukan hanya jumlah gambar. Perubahan warna diterapkan pada fill path sebelum rasterisasi, sehingga piksel antialias tidak dikuantisasi menjadi tepi keras lagi.

Tracing tetap berasal dari raster kecil, bukan master perusahaan. Kontur utamanya dipertahankan, fragmen kecil dibersihkan; bukan jaminan siap cetak/bordir. JSON dan SVG bisa dirapikan lebih lanjut. Tes native mengecek nonempty render, background nonhitam, piksel antialias, serta round-trip ekspor pada semua 16 kombinasi.

## Studio Seragam (integrasi native)
Navigasi bawah Logo | Seragam. Tab Seragam selalu mengambil `current` dan `selections[current]` yang sama dengan tab Logo; tidak ada pemilih logo terpisah. Tab, jenis produk, sudut serta snapshot ekspor dipertahankan saat rotasi. Pilihan logo dan swatch tetap tersimpan di preferensi.

Sumber foto: prototipe pengguna `kotlin/Studio Seragam/Studio-Seragam-source.zip`. Menggunakan tiga sudut topi dan kemeja (depan, serong depan, belakang); aset serong belakang duplikat tidak ditawarkan. Renderer menempelkan master transparan, bukan latar abu-abu preview, dengan fit aspect ratio. Ekspor JPG melalui document picker mendukung Android 8+, memakai snapshot pilihan saat unduh diklik. Ini mockup foto 2D, tidak ada klaim bordir produksi; simulasi benang dan recolor kain belum disertakan.

## Koleksi eksplorasi — pilot
Tab Logo memiliki koleksi terpisah Pilihan Klien (empat indeks lama tidak berubah) dan Eksplorasi (dua sampel kelompok 1, nomor 01/08). Navigasi hanya berputar di koleksi aktif. Swatch disimpan per logo dan renderer yang sama dipakai tab Seragam serta ekspor.

`app/src/main/assets/exploration/catalog.json` memetakan ID stabil, nama tampilan, nama asli, Drive ID, hash sumber, dan status pilot. File Drive tidak di-rename. Generator `scripts/prepare_exploration_pilot.py` memerlukan dua unduhan sumber di folder lokal `google_drive/` dan ImageMagick. PNG dipisahkan dari latar putih terhubung dengan floodfill; area putih tertutup dipertahankan sebagai artwork. Palet dipetakan saat runtime untuk empat swatch. Ini raster, bukan SVG geometris baru: pembesaran tidak menciptakan detail tambahan.

Folder Drive dilaporkan memiliki 342 file. Hanya dua sampel yang diimpor dan diperiksa pada tahap ini. Hash kedua sumber berbeda; belum ada klaim deduplikasi visual atau audit seluruh 342 file. Perlu peninjauan dan pemrosesan batch berikutnya sebelum katalog penuh ditambahkan. Seluruh aset klien dan seragam lama tetap utuh.

## Koreksi setelah v1.0.25
Semua enam logo berada dalam satu katalog bernama Variasi 01–06; belum ada keputusan klien. Pemisah koleksi dihapus. Preview utama kotak di atas, grid thumbnail tiga kolom yang bisa digulir di bawah swatch. Swipe/prev/next kini menjangkau seluruh enam variasi. Tab bawah tetap Logo | Seragam.

Variasi 05/06 sekarang memakai master SVG manual dan JSON native dari titik yang sama; raster renderer serta importer floodfill dihentikan. PNG yang tersisa hanya thumbnail/arsip; preview, mockup dan ekspor dirender dari path native. Sisa file Drive belum diimpor. Bagian dokumentasi pilot raster di atas merupakan riwayat, bukan perilaku saat ini.

## Favorit, kolase, variasi 07–08
Navigasi bawah berbentuk pill datar dengan latar bar khusus: Logo | ♥ Favorit | Seragam. Hati di kanan bawah bidang preview menambah/menghapus favorit. Favorit disimpan lokal dengan ID aset stabil, bukan nomor halaman; grid 3 atau 5 kolom, dua baris per halaman, tombol prev/next, kosong dan penghapusan halaman terakhir ditangani. Ketuk thumbnail favorit untuk kembali ke logo tersebut beserta swatch terakhirnya.

Seragam menyediakan sudut Kolase: komposisi tiga sudut produk aktif, tetap memakai logo/swatch yang sama, dengan ekspor JPG 1200×1200 melalui header. Jenis produk, sudut kolase, grid favorit dan halaman saat rotasi dipertahankan.

Variasi 07 (shield) dan 08 (triangle) adalah studi geometris baru dari keluarga bentuk pada referensi sembilan logo sebelumnya, bukan unduhan Drive tambahan atau salinan piksel. Master SVG dan JSON dihasilkan bersama oleh `scripts/build_more_variations.py`. Seluruh delapan variasi memakai path native; file Drive lain belum diimpor.

## Batch Drive 02 — Variasi 09–11
Kelompok Drive 1 nomor 02,03,04 digambar ulang dengan koordinat manual menjadi master SVG dan JSON native; bukan auto-trace. Tiga ID baru ditambahkan di akhir katalog sehingga delapan ID dan favorit lama tidak bergeser. Warna sumber bertekstur dijadikan solid dan M kiri/kanan disimetriskan. Sumber 02/04 adalah M merah dan C navy tanpa bingkai baru; sumber 03 mempertahankan bingkai hexagon navy dengan MCM merah.

Generator `scripts/build_drive_batch_02.py` menghasilkan perbandingan offline di `04-desain/variasi-svg/batch-02/perbandingan.html` dan progres di `progress.json`. Audit SHA256 hanya mencakup lima sumber Drive yang sudah diunduh; tidak ada klaim seluruh folder telah diaudit. Progres kelompok 1: 01,02,03,04,08 selesai (5/9), tersisa 05,06,07,09. Folder lain belum dikerjakan. Tiga redraw tetap perlu review visual pengguna, bukan master produksi yang disetujui.

## Interim vector catalog — explicit APK request
The user requested an interim APK before the full Drive collection is complete.
The catalog now has 105 variations: 99 unique Drive masters, four original selections,
and two studies. Original 11 IDs/indices remain unchanged. Group 12 source files are
SHA-256-identical to group 11 and mapped as aliases, never duplicated in the app.
Native JSON is copied verbatim from batch masters. APK builds are manual dispatch
only; PR/push run path checks. The public demo signing identity is unchanged.

## Review sementara (permintaan build setelah batch 36)

Menu → **Review logo asli + catatan** membuka halaman terpisah untuk 324 master Drive.
324 pasangan sumber asli/redraw tersedia offline; 18 alias identik tidak diulang.
Katalog utama tetap 105 variasi dan indeks favorit lama tidak diubah.
Tiga status manual, satu catatan per master, tombol salin identitas + status + catatan.
Dark mode default aktif, dapat ditoggle dan diingat. Catatan/status/posisi otomatis
tersimpan di SharedPreferences `temporary-logo-review`, terpisah dari catatan pengembangan.
Catatan hanya di perangkat ini dan hilang bila data aplikasi dihapus/uninstall; belum ada sinkronisasi.
Sumber raster tetap berlatar putih; dark mode meredupkan UI, bukan mengubah sumber acuan.

Untuk mencabut: hapus `TemporaryReviewActivity.kt`, entri activity manifest, tombol pada
`showMenu`, folder aset `temporary-review`, generator `prepare_temporary_review.py`, dan tes terkait.
Tidak memerlukan migrasi katalog/favorit. APK kini hanya dibangun melalui manual workflow_dispatch;
automatic push/PR tetap tidak membangun Android. Signing tetap identitas demo sebelumnya.

### Hasil build review sementara

- APK **v1.0.72**, versionCode **72**, tetap package `id.mcm.logopreview`.
- Release: https://github.com/rokhmangalaxy/lg_6jt/releases/download/android-v1.0.72/mcm-logo-studio-release.apk
- CI run **44861163852**, source **2c6d342eac8fdebe7aaa16e1a27858e4bef7ba80**: success.
- Tes Android release (termasuk navigasi/status/catatan/dark mode dan recreation), lint,
  inventaris 105 katalog + 324 pasangan review, serta signature verification lulus di CI.
- Ukuran asset release **36,615,116 byte**. Digest yang dilaporkan GitHub:
  `38a6823d76f0cb99964faa12d8bd0a07cfda526cbcee9ceb229c25934346c539`.
- Unduh biner ke sandbox gagal EOF pada host release-assets; APK tidak tersedia lokal,
  digest di atas metadata GitHub, bukan hash ulang lokal. Belum diuji pada perangkat fisik.
- Build manual sebelumnya gagal (kompilasi tes awal; kemudian aturan inventaris lama),
  run final di atas sudah melewati semua tahap dan memublikasikan release.

## Koreksi setelah laporan pengguna v1.0.72

v1.0.72 mempertahankan 105 katalog dan salah menempatkan tombol review dalam
`showMenu()` yang tidak dijangkau navigasi. Ini bug implementasi, bukan masalah pengguna.
Perbaikan: tombol **☾ Review asli · Catatan · Dark mode** selalu terlihat di bawah header,
langsung membuka review master yang sedang dipilih (pilihan original/studi tanpa pasangan
menggunakan posisi review terakhir). Katalog kini **330 variasi = 324 master Drive + 4 original
+ 2 studi**. Seluruh 105 indeks lama dipertahankan; 225 master ditambahkan di belakang.
Catatan v1.0.72 tetap memakai preference dan stable ID sama. Tambahan tes launcher memastikan
tombol benar-benar bisa dijangkau, bukan hanya ada dalam source code.

### Review: navigasi dan penilaian cepat

Di bawah pasangan gambar: **❮ | tiga radio penilaian | ❯**. Radio disimpan setiap
perubahan. Next mewariskan nilai item yang ditinggalkan hanya jika item tujuan belum
memiliki nilai tersimpan, termasuk menyimpan default warisan itu. Nilai tujuan yang
sudah ada tidak ditimpa; Prev tidak mewariskan nilai. Catatan manual tidak ikut disalin
ke item lain dan tetap autosave. Salin catatan menghasilkan
`Variasi NN:Perlu perbaikan, isi penilaian manual` dengan nama katalog, bukan nomor
posisi review atau ID sumber. Preference lama tetap kompatibel.
