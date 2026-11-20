package com.emrobinso.cutgridimages.grid

import kotlin.math.abs
import kotlin.math.max

/** Kotak dalam fraksi 0..1 terhadap ukuran gambar. */
data class FractionRect(
    val left: Float,
    val top: Float,
    val right: Float,
    val bottom: Float,
)

/**
 * Mencari sel-sel isi pada lembar gambar (misalnya kumpulan logo) tanpa perlu tahu dulu
 * berapa baris dan kolomnya.
 *
 * Cara kerja:
 * 1. Warna latar dan toleransinya diambil dari cincin tepi gambar — mendukung latar putih,
 *    berwarna, bergradien halus, dan PNG transparan. Bintik noise dibersihkan lebih dulu.
 * 2. Pita **baris** dicari dari proyeksi seluruh gambar: celah di dalam satu logo tidak
 *    membentang selebar gambar, jadi logo bertingkat (bar + teks) tetap utuh.
 * 3. Di setiap pita baris, pita **kolom** dicari dari proyeksi pita itu saja, sehingga tiap baris
 *    boleh punya posisi kolom sendiri (umum pada lembar logo yang tidak sejajar).
 * 4. Celah yang jauh lebih sempit dari celah terlebar (pita hias di dalam logo) digabung, dan
 *    pita "serpihan" hasil resampling dibuang.
 *
 * Batas potongan diletakkan tepat di tengah celah, jadi tidak ada konten yang terpotong.
 * Fungsi ini murni (tanpa Android) supaya bisa diuji di JVM.
 */
object ContentGridDetector {

    /** Toleransi warna latar bawaan bila pemanggil tidak menentukan. */
    const val DEFAULT_TOLERANCE = 26

    /** Batas jumlah sel agar hasil tetap bisa dikelola. */
    const val MAX_CELLS = 36

    /** Di atas rasio ini gambar dianggap foto tanpa latar polos, deteksi dibatalkan. */
    private const val MAX_CONTENT_RATIO = 0.8f

    /** Celah minimal untuk dianggap pemisah, sebagai fraksi sisi gambar. */
    private const val MIN_GAP_RATIO = 0.008f

    /** Celah minimal dalam piksel (pada resolusi deteksi). */
    private const val MIN_GAP_PX = 4

    /** Batas minimal celah agar posisinya dipakai sebagai titik snap. */
    private const val SNAP_GAP_RATIO = 0.006f

    /** Posisi celah (fraksi 0..1) untuk snapping garis manual. */
    data class Gaps(val columns: FloatArray, val rows: FloatArray) {
        companion object {
            val EMPTY = Gaps(FloatArray(0), FloatArray(0))
        }
    }

    data class Result(
        val cells: List<FractionRect>,
        val rows: Int,
        val columns: Int,
        val gaps: Gaps,
    )

    /**
     * @param pixels piksel ARGB baris demi baris, panjang minimal `width * height`
     * @return null bila gambar tidak punya latar yang bisa dibedakan atau hanya ada satu sel
     */
    fun detect(
        pixels: IntArray,
        width: Int,
        height: Int,
        tolerance: Int = DEFAULT_TOLERANCE,
    ): Result? {
        if (width <= 0 || height <= 0 || pixels.size < width * height) return null

        val model = BackgroundModel.of(pixels, width, height)
        val effectiveTolerance = max(tolerance, model.tolerance)
        val mask = BooleanArray(width * height)
        var contentCount = 0
        for (index in mask.indices) {
            val isContent = model.isContent(pixels[index], effectiveTolerance)
            mask[index] = isContent
            if (isContent) contentCount++
        }
        if (contentCount == 0) return null
        despeckle(mask, width, height)
        // Latar tidak benar-benar polos (mis. foto): pemisahan sel akan mengarang hasil.
        if (contentCount > mask.size * MAX_CONTENT_RATIO) return null

        val gaps = Gaps(
            columns = gapCenters(mask, width, height, vertical = true),
            rows = gapCenters(mask, width, height, vertical = false),
        )

        // Baris ditentukan dari proyeksi GLOBAL: celah di dalam satu logo tidak membentang
        // selebar gambar, sehingga tidak ikut membelah.
        var rowBands = bands(BooleanArray(height) { y ->
            rowHasContent(mask, width, y)
        })
        rowBands = normalizeBands(rowBands, height)
        if (rowBands.isEmpty()) return null

        val rowCuts = cutsFrom(rowBands, height)
        val cells = ArrayList<FractionRect>()
        var widestRow = 0

        for (position in rowBands.indices) {
            val band = rowBands[position]
            var columnBands = bands(BooleanArray(width) { x ->
                columnHasContent(mask, width, x, band.first, band.last)
            })
            columnBands = normalizeBands(columnBands, width)
            if (columnBands.isEmpty()) continue
            widestRow = max(widestRow, columnBands.size)

            val columnCuts = cutsFrom(columnBands, width)
            for (column in 0 until columnBands.size) {
                cells += FractionRect(
                    left = columnCuts[column],
                    top = rowCuts[position],
                    right = columnCuts[column + 1],
                    bottom = rowCuts[position + 1],
                )
            }
        }

        if (cells.isEmpty() || cells.size > MAX_CELLS) return null
        val rows = rowBands.size
        return Result(cells = cells, rows = rows, columns = widestRow, gaps = gaps)
    }

    /** Titik tengah celah kosong yang membentang penuh, dipakai untuk menempelkan garis manual. */
    private fun gapCenters(
        mask: BooleanArray,
        width: Int,
        height: Int,
        vertical: Boolean,
    ): FloatArray {
        val size = if (vertical) width else height
        val other = if (vertical) height else width
        val minimum = max(2, (size * SNAP_GAP_RATIO).toInt())
        val centers = ArrayList<Float>()
        var runStart = -1
        var seenContent = false
        for (position in 0 until size) {
            var empty = true
            for (index in 0 until other) {
                val x = if (vertical) position else index
                val y = if (vertical) index else position
                if (mask[y * width + x]) {
                    empty = false
                    break
                }
            }
            if (empty) {
                if (runStart < 0) runStart = position
            } else {
                if (runStart >= 0) {
                    val length = position - runStart
                    if (seenContent && length >= minimum) {
                        centers += ((runStart + position - 1) / 2f) / size
                    }
                }
                runStart = -1
                seenContent = true
            }
        }
        return centers.toFloatArray()
    }

    /** Menghapus piksel konten yang menyendiri (bintik noise JPEG/resampling). */
    private fun despeckle(mask: BooleanArray, width: Int, height: Int) {
        val isolated = ArrayList<Int>()
        for (y in 0 until height) {
            for (x in 0 until width) {
                val index = y * width + x
                if (!mask[index]) continue
                val left = x > 0 && mask[index - 1]
                val right = x < width - 1 && mask[index + 1]
                val up = y > 0 && mask[index - width]
                val down = y < height - 1 && mask[index + width]
                if (!left && !right && !up && !down) isolated += index
            }
        }
        isolated.forEach { mask[it] = false }
    }

    private fun rowHasContent(mask: BooleanArray, width: Int, y: Int): Boolean {
        val offset = y * width
        for (x in 0 until width) if (mask[offset + x]) return true
        return false
    }

    private fun columnHasContent(
        mask: BooleanArray,
        width: Int,
        x: Int,
        top: Int,
        bottom: Int,
    ): Boolean {
        for (y in top..bottom) if (mask[y * width + x]) return true
        return false
    }

    /** Rentang berurutan yang berisi konten. */
    private fun bands(flags: BooleanArray): List<IntRange> {
        val result = ArrayList<IntRange>()
        var start = -1
        for (index in flags.indices) {
            if (flags[index]) {
                if (start < 0) start = index
            } else if (start >= 0) {
                result += start until index
                start = -1
            }
        }
        if (start >= 0) result += start until flags.size
        return result
    }

    /**
     * Menggabung pita yang dipisahkan celah sempit.
     *
     * Ambang = maksimum [absoluteMinGap] dan 25% celah terlebar: garis hias/garis tipis di dalam
     * logo (mis. pita putih pada kartu produk) tetap menyatu, sedangkan celah antar sel — yang
     * jelas jauh lebih lebar — tetap memisahkan.
     */
    private fun mergeBands(bands: List<IntRange>, absoluteMinGap: Int): List<IntRange> {
        if (bands.size < 2) return bands
        val widest = (1 until bands.size).maxOf { bands[it].first - bands[it - 1].last - 1 }
        val threshold = max(absoluteMinGap, (widest * 0.3f).toInt() + 1)
        val merged = ArrayList<IntRange>(bands.size)
        var current = bands.first()
        for (index in 1 until bands.size) {
            val next = bands[index]
            val gap = next.first - current.last - 1
            current = if (gap < threshold) current.first until next.last else {
                merged += current
                next
            }
        }
        merged += current
        return merged
    }

    /**
     * Membuang pita "serpihan" (lebih tipis dari 25% tinggi pita median) yang muncul akibat
     * resampling/anti-aliasing, lalu menggabungkan ulang.
     */
    private fun normalizeBands(bands: List<IntRange>, size: Int): List<IntRange> {
        val minGap = max(MIN_GAP_PX, (size * MIN_GAP_RATIO).toInt())
        var current = mergeBands(bands, minGap)
        repeat(2) {
            if (current.size < 2) return current
            val sizes = current.map { it.last - it.first + 1 }.sorted()
            val median = sizes[sizes.size / 2]
            val minimum = max(MIN_GAP_PX, (median * 0.25f).toInt())
            val kept = current.filter { it.last - it.first + 1 >= minimum }
            if (kept.isEmpty() || kept.size == current.size) return current
            current = mergeBands(kept, minGap)
        }
        return current
    }

    /** Batas sel: tepi gambar, lalu titik tengah celah antar pita. */
    private fun cutsFrom(bands: List<IntRange>, size: Int): FloatArray {
        val cuts = FloatArray(bands.size + 1)
        cuts[0] = 0f
        for (index in 0 until bands.size - 1) {
            val endOfLeft = bands[index].last + 1
            val startOfRight = bands[index + 1].first
            cuts[index + 1] = ((endOfLeft + startOfRight) / 2f) / size
        }
        cuts[cuts.size - 1] = 1f
        return cuts
    }

    /** Warna latar + toleransi adaptif dari cincin tepi gambar. */
    private class BackgroundModel(
        private val color: Int,
        private val transparent: Boolean,
        val tolerance: Int,
    ) {
        fun isContent(pixel: Int, tolerance: Int): Boolean {
            val alpha = (pixel ushr 24) and 0xFF
            if (transparent) return alpha >= 160
            if (alpha < 160) return false
            val dr = abs(((pixel shr 16) and 0xFF) - ((color shr 16) and 0xFF))
            val dg = abs(((pixel shr 8) and 0xFF) - ((color shr 8) and 0xFF))
            val db = abs((pixel and 0xFF) - (color and 0xFF))
            return max(dr, max(dg, db)) > tolerance
        }

        companion object {
            fun of(pixels: IntArray, width: Int, height: Int): BackgroundModel {
                val stepX = max(1, width / 160)
                val stepY = max(1, height / 160)
                val samples = ArrayList<Int>(capacity())
                for (x in 0 until width step stepX) {
                    samples += pixels[x]
                    samples += pixels[(height - 1) * width + x]
                }
                for (y in 0 until height step stepY) {
                    samples += pixels[y * width]
                    samples += pixels[y * width + width - 1]
                }
                val reds = samples.map { (it shr 16) and 0xFF }.sorted()
                val greens = samples.map { (it shr 8) and 0xFF }.sorted()
                val blues = samples.map { it and 0xFF }.sorted()
                val alphas = samples.map { (it ushr 24) and 0xFF }.sorted()
                val middle = samples.size / 2
                val alpha = alphas[middle]
                val red = reds[middle]
                val green = greens[middle]
                val blue = blues[middle]
                val color = (0xFF shl 24) or (red shl 16) or (green shl 8) or blue
                // Simpangan absolut median (MAD) cincin tepi: latar bergradien/noise tetap "kosong".
                val deviation = maxOf(
                    medianDeviation(samples) { (it shr 16) and 0xFF } - red,
                    medianDeviation(samples) { (it shr 8) and 0xFF } - green,
                    medianDeviation(samples) { it and 0xFF } - blue,
                )
                val tolerance = (deviation * 3 + 12).coerceIn(20, 80)
                return BackgroundModel(color, transparent = alpha < 128, tolerance = tolerance)
            }

            private fun capacity(): Int = 160 * 4 + 8

            private inline fun medianDeviation(samples: List<Int>, channel: (Int) -> Int): Int {
                val values = samples.map { channel(it) }
                val sorted = values.sorted()
                val median = sorted[sorted.size / 2]
                val deviations = values.map { abs(it - median) }.sorted()
                return median + deviations[deviations.size / 2]
            }
        }
    }
}
