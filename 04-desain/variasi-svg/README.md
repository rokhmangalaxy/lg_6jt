# Master variasi 05 dan 06

Redraw koordinat manual dari dua sumber Drive yang telah ditinjau (kelompok 1, nomor 01 dan 08). SVG berisi path M/L/Z murni, tanpa raster tertanam; JSON native di `assets/exploration` berasal dari titik yang sama. PNG hanya thumbnail/arsip, bukan sumber render aplikasi. Raster runtime dan importer floodfill lama sudah dihapus.

Bentuk sumber dipertahankan secara geometris; ketidakteraturan raster, tekstur warna dan lengkung kecil dirapikan. Bukan klaim identik piksel atau artwork resmi. Semua enam variasi belum diputuskan dan ditampilkan bersama, tanpa label pilihan klien atau eksplorasi. ID aset lama tetap agar preferensi swatch tidak hilang.

Reproduksi: `npm install --prefix .cache/mcm-redraw @resvg/resvg-js && python scripts/build_variation_vectors.py`. Pemetaan Drive dan hash sumber tetap di `android-logo/app/src/main/assets/exploration/catalog.json`. Folder internal `exploration` dipertahankan hanya sebagai namespace ID, bukan kategori antarmuka.
