package com.emrobinso.cutgridimages.grid

import org.junit.Assert.assertEquals
import org.junit.Assert.assertThrows
import org.junit.Assert.assertTrue
import org.junit.Test

class GridSlicerTest {

    @Test
    fun `square image splits into nine equal tiles`() {
        val tiles = GridSlicer.tileBounds(width = 300, height = 300, columns = 3, rows = 3)

        assertEquals(9, tiles.size)
        tiles.forEach { tile ->
            assertEquals(100, tile.width)
            assertEquals(100, tile.height)
        }

        val middle = tiles[4]
        assertEquals(4, middle.index)
        assertEquals(1, middle.row)
        assertEquals(1, middle.column)
        assertEquals(100, middle.left)
        assertEquals(100, middle.top)
        assertEquals(200, middle.right)
        assertEquals(200, middle.bottom)
    }

    @Test
    fun `tiles cover the whole image without gaps or overlaps`() {
        val width = 997
        val height = 613
        val columns = 5
        val rows = 3
        val tiles = GridSlicer.tileBounds(width, height, columns, rows)

        assertEquals(columns * rows, tiles.size)
        assertEquals(0, tiles.first().left)
        assertEquals(0, tiles.first().top)
        assertEquals(width, tiles.last().right)
        assertEquals(height, tiles.last().bottom)

        tiles.chunked(columns).forEach { rowTiles ->
            assertEquals(columns, rowTiles.size)
            assertEquals(width, rowTiles.sumOf { it.width })
            rowTiles.zipWithNext().forEach { (left, right) -> assertEquals(left.right, right.left) }
        }

        for (column in 0 until columns) {
            val columnTiles = tiles.filter { it.column == column }
            assertEquals(rows, columnTiles.size)
            assertEquals(height, columnTiles.sumOf { it.height })
            columnTiles.zipWithNext().forEach { (top, bottom) -> assertEquals(top.bottom, bottom.top) }
        }
    }

    @Test
    fun `uneven tiles differ by at most one pixel`() {
        val tiles = GridSlicer.tileBounds(width = 1000, height = 700, columns = 7, rows = 6)

        for (column in 0 until 7) {
            val widths = tiles.filter { it.column == column }.map { it.width }
            assertTrue("lebar kolom $column: $widths", widths.maxOrNull()!! - widths.minOrNull()!! <= 1)
        }
        for (row in 0 until 6) {
            val heights = tiles.filter { it.row == row }.map { it.height }
            assertTrue("tinggi baris $row: $heights", heights.maxOrNull()!! - heights.minOrNull()!! <= 1)
        }
    }

    @Test
    fun `tiles are ordered row by row`() {
        val tiles = GridSlicer.tileBounds(width = 200, height = 100, columns = 2, rows = 2)

        assertEquals(listOf(0, 0, 1, 1), tiles.map { it.row })
        assertEquals(listOf(0, 1, 0, 1), tiles.map { it.column })
        assertEquals(listOf(0, 100, 0, 100), tiles.map { it.left })
        assertEquals(listOf(0, 0, 50, 50), tiles.map { it.top })
        assertEquals(listOf(0, 1, 2, 3), tiles.map { it.index })
    }

    @Test
    fun `grid finer than the image keeps empty tiles but still covers everything`() {
        val tiles = GridSlicer.tileBounds(width = 2, height = 2, columns = 4, rows = 4)

        assertEquals(16, tiles.size)
        assertEquals(4, tiles.count { !it.isEmpty })
        assertEquals(2, tiles.maxOf { it.right })
        assertEquals(2, tiles.maxOf { it.bottom })
    }

    @Test
    fun `rejects invalid sizes and grid counts`() {
        assertThrows(IllegalArgumentException::class.java) { GridSlicer.tileBounds(0, 100, 2, 2) }
        assertThrows(IllegalArgumentException::class.java) { GridSlicer.tileBounds(100, -1, 2, 2) }
        assertThrows(IllegalArgumentException::class.java) {
            GridSlicer.tileBounds(100, 100, MIN_GRID - 1, 2)
        }
        assertThrows(IllegalArgumentException::class.java) {
            GridSlicer.tileBounds(100, 100, MAX_GRID + 1, 2)
        }
        assertThrows(IllegalArgumentException::class.java) {
            GridSlicer.tileBounds(100, 100, 2, MAX_GRID + 1)
        }
    }

    @Test
    fun `single cell grid equals the whole image`() {
        val tile = GridSlicer.tileBounds(width = 123, height = 45, columns = 1, rows = 1).single()

        assertEquals(0, tile.left)
        assertEquals(0, tile.top)
        assertEquals(123, tile.right)
        assertEquals(45, tile.bottom)
    }
}
