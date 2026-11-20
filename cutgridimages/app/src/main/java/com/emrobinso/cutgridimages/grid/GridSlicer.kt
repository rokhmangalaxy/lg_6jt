package com.emrobinso.cutgridimages.grid

/** Ukuran grid minimum per sumbu. */
const val MIN_GRID = 1

/** Ukuran grid maksimum per sumbu; menahan hasil agar tetap masuk akal. */
const val MAX_GRID = 10

/**
 * Satu petak hasil pemotongan, dalam koordinat piksel bitmap sumber.
 * Batas kanan/bawah bersifat eksklusif, sama seperti [android.graphics.Bitmap.createBitmap].
 */
data class GridTile(
    val index: Int,
    val row: Int,
    val column: Int,
    val left: Int,
    val top: Int,
    val right: Int,
    val bottom: Int,
) {
    val width: Int get() = right - left
    val height: Int get() = bottom - top

    val isEmpty: Boolean get() = width <= 0 || height <= 0
}

/**
 * Membagi gambar menjadi grid baris × kolom tanpa celah dan tanpa sisa.
 *
 * Posisi tepi dihitung dengan pembagian bilangan bulat, sehingga petak menutup
 * seluruh gambar persis; selisih lebar antar petak paling banyak satu piksel.
 * Fungsi ini murni (tanpa Android) supaya bisa diuji di JVM.
 */
object GridSlicer {

    /**
     * @param width lebar gambar sumber dalam piksel, harus > 0
     * @param height tinggi gambar sumber dalam piksel, harus > 0
     * @param columns jumlah kolom, [MIN_GRID]..[MAX_GRID]
     * @param rows jumlah baris, [MIN_GRID]..[MAX_GRID]
     * @return daftar petak berurutan baris demi baris (row-major), ukuran `columns * rows`.
     *   Bila grid lebih rapat daripada gambar, beberapa petak bisa kosong ([GridTile.isEmpty]).
     */
    fun tileBounds(width: Int, height: Int, columns: Int, rows: Int): List<GridTile> {
        require(width > 0) { "width harus positif, diterima $width" }
        require(height > 0) { "height harus positif, diterima $height" }
        require(columns in MIN_GRID..MAX_GRID) { "columns harus ${MIN_GRID}..${MAX_GRID}, diterima $columns" }
        require(rows in MIN_GRID..MAX_GRID) { "rows harus ${MIN_GRID}..${MAX_GRID}, diterima $rows" }

        val columnEdges = edges(width, columns)
        val rowEdges = edges(height, rows)
        val tiles = ArrayList<GridTile>(columns * rows)
        var index = 0
        for (row in 0 until rows) {
            for (column in 0 until columns) {
                tiles += GridTile(
                    index = index++,
                    row = row,
                    column = column,
                    left = columnEdges[column],
                    top = rowEdges[row],
                    right = columnEdges[column + 1],
                    bottom = rowEdges[row + 1],
                )
            }
        }
        return tiles
    }

    /** Tepi ke-`i` dari `parts` bagian sepanjang `total`, dihitung tanpa sisa pembulatan. */
    private fun edges(total: Int, parts: Int): IntArray =
        IntArray(parts + 1) { position -> (position.toLong() * total / parts).toInt() }

    /** Posisi tepi seragam 0..1 untuk [parts] bagian (dipakai grid yang belum digeser). */
    fun uniformCuts(parts: Int): FloatArray {
        require(parts >= MIN_GRID) { "parts minimal $MIN_GRID" }
        return FloatArray(parts + 1) { position -> position.toFloat() / parts }
    }

    /**
     * Petak dengan batas yang bisa digeser per sumbu.
     *
     * @param columnCuts posisi garis kolom dalam fraksi 0..1; ukuran `columns + 1`, elemen
     *   pertama 0f dan terakhir 1f, nilai harus naik.
     * @param rowCuts posisi garis baris dalam fraksi 0..1; ukuran `rows + 1`.
     * @return petak berurutan baris demi baris; petak dengan lebar/tinggi 0 menjadi
     *   [GridTile.isEmpty] (tidak bisa dipotong, dilewati saat menyimpan).
     */
    fun tilesFor(
        width: Int,
        height: Int,
        columnCuts: FloatArray,
        rowCuts: FloatArray,
    ): List<GridTile> {
        require(width > 0) { "width harus positif, diterima $width" }
        require(height > 0) { "height harus positif, diterima $height" }
        require(columnCuts.size >= 2) { "columnCuts minimal 2 elemen" }
        require(rowCuts.size >= 2) { "rowCuts minimal 2 elemen" }

        val columnEdges = pixelEdges(columnCuts, width)
        val rowEdges = pixelEdges(rowCuts, height)
        val columns = columnEdges.size - 1
        val rows = rowEdges.size - 1
        val tiles = ArrayList<GridTile>(columns * rows)
        var index = 0
        for (row in 0 until rows) {
            for (column in 0 until columns) {
                tiles += GridTile(
                    index = index++,
                    row = row,
                    column = column,
                    left = columnEdges[column],
                    top = rowEdges[row],
                    right = columnEdges[column + 1],
                    bottom = rowEdges[row + 1],
                )
            }
        }
        return tiles
    }

    /** Fraksi 0..1 menjadi tepi piksel yang selalu naik dan menutup sisi 0..[size]. */
    private fun pixelEdges(cuts: FloatArray, size: Int): IntArray {
        val edges = IntArray(cuts.size)
        for (position in cuts.indices) {
            val fraction = cuts[position].coerceIn(0f, 1f)
            edges[position] = Math.round(fraction * size).coerceIn(0, size)
        }
        edges[0] = 0
        edges[edges.size - 1] = size
        for (position in 1 until edges.size) {
            if (edges[position] < edges[position - 1]) edges[position] = edges[position - 1]
        }
        return edges
    }
}
