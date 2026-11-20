package com.emrobinso.cutgridimages.grid

/** Kotak dalam fraksi 0..1 terhadap ukuran gambar. */
data class FractionRect(
    val left: Float,
    val top: Float,
    val right: Float,
    val bottom: Float,
)

/**
 * Mencari kotak-kotak isi pada lembar gambar berlatar polos (misalnya 3×3 logo di atas putih).
 *
 * Cara kerja: latar diambil dari pojok gambar, lalu tiap baris/kolom diperiksa apakah seluruhnya
 * berwarna latar. Celah kosong yang lebar dipakai sebagai batas sel; celah sempit (bagian dalam
 * logo) digabung kembali. Deteksi dilakukan **per pita baris**, karena tiap baris logo biasanya
 * punya posisi kolom yang berbeda.
 *
 * Fungsi ini murni (tanpa Android) supaya bisa diuji di JVM.
 */
object ContentGridDetector {

    /** Toleransi warna latar per kanal (0..255). */
    const val DEFAULT_TOLERANCE = 24

    /** Pita yang lebih tipis dari 0,4% sisi dianggap noise. */
    private const val MIN_BAND_RATIO = 0.004f

    /** Batas jumlah kotak agar tidak melebihi [MAX_GRID]. */
    private const val MAX_CELLS = MAX_GRID

    data class Result(
        val cells: List<FractionRect>,
        val rows: Int,
        val columns: Int,
    )

    /**
     * @param pixels piksel ARGB baris demi baris, panjang minimal `width * height`
     * @param expectedColumns perkiraan jumlah kolom (dipakai untuk menggabung celah kecil)
     * @param expectedRows perkiraan jumlah baris
     * @return null bila tidak ada isi yang bisa dikenali (misalnya foto penuh warna)
     */
    fun detect(
        pixels: IntArray,
        width: Int,
        height: Int,
        expectedColumns: Int = MAX_CELLS,
        expectedRows: Int = MAX_CELLS,
        tolerance: Int = DEFAULT_TOLERANCE,
    ): Result? {
        if (width <= 0 || height <= 0 || pixels.size < width * height) return null
        val background = backgroundOf(pixels, width, height)

        val rowContent = BooleanArray(height) { y ->
            rowHasContent(pixels, width, y, background, tolerance)
        }
        var rowBands = bands(rowContent, minBand(height))
        rowBands = mergeUntil(rowBands, expectedRows.coerceIn(1, MAX_CELLS), height)
        if (rowBands.isEmpty()) return null

        val rowCuts = cutsFrom(rowBands, height)
        val cells = ArrayList<FractionRect>()
        var widestRow = 0

        for (position in rowBands.indices) {
            val band = rowBands[position]
            val columnContent = BooleanArray(width) { x ->
                columnHasContent(pixels, width, x, band.first, band.last, background, tolerance)
            }
            var columnBands = bands(columnContent, minBand(width))
            columnBands = mergeUntil(columnBands, expectedColumns.coerceIn(1, MAX_CELLS), width)
            if (columnBands.isEmpty()) continue
            widestRow = maxOf(widestRow, columnBands.size)

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

        if (cells.isEmpty()) return null
        return Result(cells = cells, rows = rowBands.size, columns = widestRow)
    }

    /** Warna latar: rata-rata empat pojok (median per kanal tidak diperlukan di sini). */
    private fun backgroundOf(pixels: IntArray, width: Int, height: Int): Int {
        val corners = intArrayOf(
            pixels[0],
            pixels[width - 1],
            pixels[(height - 1) * width],
            pixels[height * width - 1],
        )
        val red = corners.map { (it shr 16) and 0xFF }.sorted()[1]
        val green = corners.map { (it shr 8) and 0xFF }.sorted()[1]
        val blue = corners.map { it and 0xFF }.sorted()[1]
        return (0xFF shl 24) or (red shl 16) or (green shl 8) or blue
    }

    private fun differs(color: Int, background: Int, tolerance: Int): Boolean {
        val dr = kotlin.math.abs(((color shr 16) and 0xFF) - ((background shr 16) and 0xFF))
        val dg = kotlin.math.abs(((color shr 8) and 0xFF) - ((background shr 8) and 0xFF))
        val db = kotlin.math.abs((color and 0xFF) - (background and 0xFF))
        return dr > tolerance || dg > tolerance || db > tolerance
    }

    private fun rowHasContent(
        pixels: IntArray,
        width: Int,
        y: Int,
        background: Int,
        tolerance: Int,
    ): Boolean {
        val offset = y * width
        for (x in 0 until width) {
            if (differs(pixels[offset + x], background, tolerance)) return true
        }
        return false
    }

    private fun columnHasContent(
        pixels: IntArray,
        width: Int,
        x: Int,
        top: Int,
        bottom: Int,
        background: Int,
        tolerance: Int,
    ): Boolean {
        for (y in top..bottom) {
            if (differs(pixels[y * width + x], background, tolerance)) return true
        }
        return false
    }

    private fun minBand(size: Int): Int = (size * MIN_BAND_RATIO).toInt().coerceAtLeast(1)

    /** Rentang berurutan yang berisi konten dan cukup tebal. */
    private fun bands(flags: BooleanArray, minLength: Int): List<IntRange> {
        val result = ArrayList<IntRange>()
        var start = -1
        for (index in flags.indices) {
            if (flags[index]) {
                if (start < 0) start = index
            } else if (start >= 0) {
                if (index - start >= minLength) result += start until index
                start = -1
            }
        }
        if (start >= 0 && flags.size - start >= minLength) result += start until flags.size
        return result
    }

    /** Menggabung pita yang dipisahkan celah tersempit sampai jumlahnya <= [max]. */
    private fun mergeUntil(bands: List<IntRange>, max: Int, size: Int): List<IntRange> {
        val merged = bands.toMutableList()
        while (merged.size > max) {
            var bestIndex = -1
            var bestGap = Int.MAX_VALUE
            for (index in 0 until merged.size - 1) {
                val gap = merged[index + 1].first - merged[index].last
                if (gap < bestGap) {
                    bestGap = gap
                    bestIndex = index
                }
            }
            if (bestIndex < 0) break
            val left = merged[bestIndex]
            val right = merged[bestIndex + 1]
            merged[bestIndex] = left.first until right.last
            merged.removeAt(bestIndex + 1)
            if (bestGap < 0 && merged.size > max) break
        }
        if (merged.isEmpty()) return merged
        // Pastikan pita pertama/menutup sisi; cutsFrom yang mengatur tepi 0..size.
        return merged
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
}
