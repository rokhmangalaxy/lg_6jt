package com.emrobinso.cutgridimages.grid

import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test
import kotlin.math.abs

class ContentGridDetectorTest {

    private val white = 0xFFFFFFFF.toInt()
    private val navy = 0xFF1E3A8A.toInt()

    /** Lembar putih dengan kotak-kotak isi; setiap kotak = [left, top, right, bottom]. */
    private fun sheet(width: Int, height: Int, blocks: List<IntArray>): IntArray {
        val pixels = IntArray(width * height) { white }
        blocks.forEach { block ->
            for (y in block[1] until block[3]) {
                for (x in block[0] until block[2]) {
                    pixels[y * width + x] = navy
                }
            }
        }
        return pixels
    }

    @Test
    fun `three by three logos are detected as nine cells`() {
        val width = 300
        val height = 300
        val blocks = mutableListOf<IntArray>()
        for (row in 0 until 3) {
            for (column in 0 until 3) {
                val left = 10 + column * 100
                val top = 10 + row * 100
                blocks += intArrayOf(left, top, left + 70, top + 70)
            }
        }
        val result = ContentGridDetector.detect(
            sheet(width, height, blocks), width, height,
            expectedColumns = 3, expectedRows = 3,
        )
        assertNotNull(result)
        assertEquals(9, result!!.cells.size)
        assertEquals(3, result.rows)
        assertEquals(3, result.columns)

        val firstCut = result.cells[0].right
        assertTrue("batas kolom harus di tengah celah", abs(firstCut - 0.3167f) < 0.02f)
        assertEquals(0f, result.cells[0].left, 0.001f)
        assertEquals(1f, result.cells[8].right, 0.001f)
        assertEquals(1f, result.cells[8].bottom, 0.001f)
    }

    @Test
    fun `thin gaps inside a logo are merged back into one cell`() {
        val width = 300
        val height = 100
        // Satu logo yang punya garis putih 3 px di tengahnya (mirip logo bracket).
        val pixels = sheet(
            width, height,
            listOf(
                intArrayOf(20, 20, 120, 80),
                intArrayOf(123, 20, 280, 80),
            ),
        )
        val result = ContentGridDetector.detect(
            pixels, width, height,
            expectedColumns = 1, expectedRows = 1,
        )
        assertNotNull(result)
        assertEquals(1, result!!.cells.size)
        assertEquals(0f, result.cells[0].left, 0.001f)
        assertEquals(1f, result.cells[0].right, 0.001f)
    }

    @Test
    fun `each row keeps its own column boundaries`() {
        val width = 300
        val height = 300
        val pixels = sheet(
            width, height,
            listOf(
                // baris 1: tiga kotak rata
                intArrayOf(10, 10, 80, 80),
                intArrayOf(110, 10, 180, 80),
                intArrayOf(210, 10, 280, 80),
                // baris 2: kotak tengah jauh lebih lebar dan bergeser
                intArrayOf(40, 110, 150, 180),
                intArrayOf(170, 110, 260, 180),
            ),
        )
        val result = ContentGridDetector.detect(
            pixels, width, height,
            expectedColumns = 3, expectedRows = 2,
        )
        assertNotNull(result)
        assertEquals(5, result!!.cells.size)
        assertEquals(2, result.rows)
        assertEquals(3, result.columns)
    }

    @Test
    fun `photo without plain background collapses to one cell`() {
        val width = 120
        val height = 90
        val pixels = IntArray(width * height) { index ->
            val shade = (index * 7) and 0xFF
            (0xFF shl 24) or (shade shl 16) or (shade shl 8) or shade
        }
        val result = ContentGridDetector.detect(pixels, width, height)
        // Tidak ada celah kosong: aplikasi menganggap ini gagal (butuh >= 2 sel).
        assertNotNull(result)
        assertEquals(1, result!!.cells.size)
    }

    @Test
    fun `blank sheet has no cells`() {
        val pixels = IntArray(100 * 100) { white }
        assertNull(ContentGridDetector.detect(pixels, 100, 100))
    }

    @Test
    fun `fraction rects are converted to pixel tiles in row major order`() {
        val rects = listOf(
            FractionRect(0f, 0f, 0.5f, 0.5f),
            FractionRect(0.5f, 0f, 1f, 0.5f),
            FractionRect(0f, 0.5f, 1f, 1f),
        )
        val tiles = GridSlicer.tilesFrom(rects, 100, 100)
        assertEquals(3, tiles.size)
        assertEquals(listOf(0, 50, 0), tiles.map { it.left })
        assertEquals(listOf(50, 100, 100), tiles.map { it.right })
        assertEquals(listOf(0, 0, 50), tiles.map { it.top })
        assertEquals(listOf(50, 50, 100), tiles.map { it.bottom })
        assertEquals(listOf(0, 0, 1), tiles.map { it.row })
        assertEquals(listOf(0, 1, 0), tiles.map { it.column })
        assertEquals(listOf(0, 1, 2), tiles.map { it.index })
        assertTrue(tiles.none { it.isEmpty })
    }
}
