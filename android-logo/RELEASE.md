# Demo release update

Atas persetujuan pengguna, build kini memakai **kunci uji AOSP publik yang tetap** di `demo-signing/`, bukan Actions secrets. Hanya untuk demo internal. Siapa pun dapat menggunakan kunci publik ini untuk menandatangani APK; jangan dipakai untuk produksi atau aplikasi dengan izin sensitif.

Application ID tetap `id.mcm.logopreview`, sertifikat tetap, versionCode mengikuti nomor run baru workflow. Update demo → demo dapat menimpa; re-run run yang sama tidak menaikkan versionCode. Debug/sertifikat lain tidak termasuk jaminan ini. Pergantian kunci di masa depan dapat memerlukan uninstall.

Workflow ubuntu-24.04 memakai SDK bawaan runner, membangun release, memverifikasi tanda tangan, dan mengunggah file `.apk` langsung sebagai GitHub Release asset. Repository private tetap memerlukan login GitHub untuk unduhan. Belum ada janji kompatibilitas perangkat sebelum diuji.

Untuk produksi, ganti demo signing dengan keystore privat proyek yang dibackup aman dan disimpan dalam Actions secrets; jangan commit kunci produksi.
