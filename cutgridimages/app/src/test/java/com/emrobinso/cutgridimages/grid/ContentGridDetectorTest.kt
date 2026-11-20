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
    private val crimson = 0xFFD32027.toInt()

    /** Membangun lembar gambar: latar [background], kotak isi, dan garis tipis [stripes]. */
    private fun sheet(
        width: Int,
        height: Int,
        background: Int,
        blocks: List<IntArray>,
        stripes: List<IntArray> = emptyList(),
        color: Int = navy,
    ): IntArray {
        val pixels = IntArray(width * height) { background }
        blocks.forEach { block ->
            for (y in block[1] until block[3]) {
                for (x in block[0] until block[2]) pixels[y * width + x] = color
            }
        }
        stripes.forEach { stripe ->
            for (y in stripe[1] until stripe[3]) {
                for (x in stripe[0] until stripe[2]) pixels[y * width + x] = background
            }
        }
        return pixels
    }

    /** Kotak-kotak tersusun [columns] × [rows] dengan celah seragam. */
    private fun grid(
        columns: Int,
        rows: Int,
        cell: Int,
        gap: Int,
        margin: Int,
    ): List<IntArray> {
        val blocks = ArrayList<IntArray>()
        for (row in 0 until rows) {
            for (column in 0 until columns) {
                val left = margin + column * (cell + gap)
                val top = margin + row * (cell + gap)
                blocks += intArrayOf(left, top, left + cell, top + cell)
            }
        }
        return blocks
    }

    @Test
    fun `three by three sheet is split into nine cells`() {
        val width = 1200
        val height = 1200
        val pixels = sheet(width, height, white, grid(columns = 3, rows = 3, cell = 320, gap = 60, margin = 40))
        val result = ContentGridDetector.detect(pixels, width, height)
        assertNotNull(result)
        assertEquals(9, result!!.cells.size)
        assertEquals(3, result.rows)
        assertEquals(3, result.columns)
        assertEquals(0f, result.cells.first().left, 0.001f)
        assertEquals(1f, result.cells.last().right, 0.001f)
    }

    @Test
    fun `colored background is supported`() {
        val width = 1200
        val height = 800
        val paleBlue = 0xFFEAF2FF.toInt()
        val pixels = sheet(width, height, paleBlue, grid(columns = 3, rows = 2, cell = 300, gap = 60, margin = 40))
        val result = ContentGridDetector.detect(pixels, width, height)
        assertNotNull(result)
        assertEquals(6, result!!.cells.size)
        assertEquals(2, result.rows)
        assertEquals(3, result.columns)
    }

    @Test
    fun `transparent background is supported`() {
        val width = 800
        val height = 800
        val pixels = sheet(width, height, 0x00000000, grid(columns = 2, rows = 2, cell = 300, gap = 60, margin = 40))
        val result = ContentGridDetector.detect(pixels, width, height)
        assertNotNull(result)
        assertEquals(4, result!!.cells.size)
        assertEquals(2, result.rows)
        assertEquals(2, result.columns)
    }

    @Test
    fun `subtle gradient background is supported`() {
        val width = 900
        val height = 900
        val blocks = grid(columns = 2, rows = 2, cell = 320, gap = 70, margin = 45)
        val pixels = IntArray(width * height)
        for (y in 0 until height) {
            for (x in 0 until width) {
                val shade = 246 + (x % 7)
                pixels[y * width + x] = (0xFF shl 24) or (shade shl 16) or (shade shl 8) or 255
            }
        }
        blocks.forEach { block ->
            for (y in block[1] until block[3]) {
                for (x in block[0] until block[2]) pixels[y * width + x] = navy
            }
        }
        val result = ContentGridDetector.detect(pixels, width, height)
        assertNotNull(result)
        assertEquals(4, result!!.cells.size)
    }

    @Test
    fun `thin white stripe inside a logo is not a separator`() {
        val width = 1200
        val height = 800
        val blocks = grid(columns = 3, rows = 2, cell = 300, gap = 60, margin = 40)
        // Logo tengah kiri punya garis putih 8 px (0,67% lebar) di tengahnya.
        val stripe = intArrayOf(blocks[0][0] + 140, blocks[0][1], blocks[0][0] + 148, blocks[0][3])
        val pixels = sheet(width, height, white, blocks, stripes = listOf(stripe))
        val result = ContentGridDetector.detect(pixels, width, height)
        assertNotNull(result)
        assertEquals(6, result!!.cells.size)
    }

    @Test
    fun `logos without gaps collapse to a single cell`() {
        val width = 800
        val height = 400
        val pixels = sheet(
            width, height, white,
            listOf(
                intArrayOf(50, 50, 380, 350),
                intArrayOf(380, 50, 700, 350),
            ),
        )
        val result = ContentGridDetector.detect(pixels, width, height)
        assertNotNull(result)
        assertEquals(1, result!!.cells.size)
    }

    @Test
    fun `gap centers are reported for snapping`() {
        val width = 1000
        val height = 400
        val pixels = sheet(
            width, height, white,
            listOf(
                intArrayOf(50, 50, 400, 350),
                intArrayOf(600, 50, 950, 350),
            ),
        )
        val result = ContentGridDetector.detect(pixels, width, height)
        assertNotNull(result)
        assertEquals(1, result!!.gaps.columns.size)
        assertEquals(0.5f, result.gaps.columns[0], 0.01f)
        assertTrue(result.gaps.rows.isEmpty())
    }

    @Test
    fun `blank sheet has no cells`() {
        assertNull(ContentGridDetector.detect(IntArray(200 * 200) { white }, 200, 200))
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
        assertTrue(tiles.none { it.isEmpty })
    }

    @Test
    fun `crimson logos on white are detected too`() {
        val width = 600
        val height = 600
        val pixels = sheet(
            width, height, white,
            listOf(
                intArrayOf(40, 40, 240, 240),
                intArrayOf(320, 40, 520, 240),
                intArrayOf(40, 320, 240, 520),
            ),
            color = crimson,
        )
        val result = ContentGridDetector.detect(pixels, width, height)
        assertNotNull(result)
        assertEquals(3, result!!.cells.size)
        assertEquals(2, result.rows)
        assertTrue(abs(result.cells[1].left - 0.4667f) < 0.02f)
    }

    @Test
    fun `four by two sheet is split into eight cells`() {
        val width = 1200
        val height = 1200
        val pixels = sheet(width, height, white, grid(columns = 4, rows = 2, cell = 250, gap = 50, margin = 40))
        val result = ContentGridDetector.detect(pixels, width, height)
        assertNotNull(result)
        assertEquals(8, result!!.cells.size)
        assertEquals(2, result.rows)
        assertEquals(4, result.columns)
    }

    @Test
    fun `two by five sheet is split into ten cells`() {
        val width = 1200
        val height = 1200
        val pixels = sheet(width, height, white, grid(columns = 2, rows = 5, cell = 180, gap = 40, margin = 40))
        val result = ContentGridDetector.detect(pixels, width, height)
        assertNotNull(result)
        assertEquals(10, result!!.cells.size)
        assertEquals(5, result.rows)
        assertEquals(2, result.columns)
    }

    @Test
    fun `single column list is split per row`() {
        val width = 1200
        val height = 1200
        val blocks = (0 until 4).map { row ->
            intArrayOf(40, 60 + row * 280, 1120, 300 + row * 280)
        }
        val result = ContentGridDetector.detect(sheet(width, height, white, blocks), width, height)
        assertNotNull(result)
        assertEquals(4, result!!.cells.size)
        assertEquals(4, result.rows)
        assertEquals(1, result.columns)
    }

    @Test
    fun `aligned white bands inside logos do not split rows`() {
        val width = 1200
        val height = 1200
        val blocks = grid(columns = 3, rows = 2, cell = 300, gap = 60, margin = 40)
        val bands = ArrayList<IntArray>()
        blocks.forEach { block ->
            for (step in 1..2) {
                val y = block[1] + (block[3] - block[1]) * step / 3
                bands += intArrayOf(block[0], y - 6, block[2], y + 6)
            }
        }
        val result = ContentGridDetector.detect(sheet(width, height, white, blocks, stripes = bands), width, height)
        assertNotNull(result)
        assertEquals(6, result!!.cells.size)
        assertEquals(2, result.rows)
        assertEquals(3, result.columns)
    }

    @Test
    fun `isolated speckles do not create extra cells`() {
        val width = 900
        val height = 900
        val gray = 0xFF9A9A9A.toInt()
        val pixels = IntArray(width * height) { index ->
            if ((index * 37) % 977 == 0) 0xFF202020.toInt() else gray
        }
        grid(columns = 2, rows = 2, cell = 320, gap = 70, margin = 45).forEach { block ->
            for (y in block[1] until block[3]) {
                for (x in block[0] until block[2]) pixels[y * width + x] = white
            }
        }
        val result = ContentGridDetector.detect(pixels, width, height)
        assertNotNull(result)
        assertEquals(4, result!!.cells.size)
        assertEquals(2, result.rows)
        assertEquals(2, result.columns)
    }
}
