package com.emrobinso.cutgridimages.image

import kotlin.math.max

/**
 * Perhitungan penskalaan dekode yang murni (tanpa Android) agar bisa diuji di JVM.
 */
object ImageSizing {

    /**
     * Faktor `inSampleSize` pangkat dua terkecil sehingga sisi terpanjang gambar
     * setelah dekode tidak melebihi [maxDimension].
     *
     * @param width lebar asli piksel, > 0
     * @param height tinggi asli piksel, > 0
     * @param maxDimension batas sisi terpanjang setelah dekode, > 0
     */
    fun sampleSizeFor(width: Int, height: Int, maxDimension: Int): Int {
        require(width > 0) { "width harus positif, diterima $width" }
        require(height > 0) { "height harus positif, diterima $height" }
        require(maxDimension > 0) { "maxDimension harus positif, diterima $maxDimension" }

        val longestSide = max(width, height)
        var sampleSize = 1
        while (longestSide / sampleSize > maxDimension) {
            sampleSize *= 2
        }
        return sampleSize
    }
}
