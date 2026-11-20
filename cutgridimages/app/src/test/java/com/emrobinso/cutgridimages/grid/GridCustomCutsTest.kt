package com.emrobinso.cutgridimages.grid

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class GridCustomCutsTest {

    @Test
    fun `uniform cuts match the plain grid`() {
        val plain = GridSlicer.tileBounds(90, 60, 3, 2)
        val custom = GridSlicer.tilesFor(
            90,
            60,
            GridSlicer.uniformCuts(3),
            GridSlicer.uniformCuts(2),
        )
        assertEquals(plain.size, custom.size)
        assertEquals(plain.map { it.left to it.right }, custom.map { it.left to it.right })
        assertEquals(plain.map { it.top to it.bottom }, custom.map { it.top to it.bottom })
    }

    @Test
    fun `moved cuts produce the expected pixel edges`() {
        val tiles = GridSlicer.tilesFor(
            100,
            100,
            floatArrayOf(0f, 0.2f, 1f),
            floatArrayOf(0f, 0.7f, 1f),
        )
        assertEquals(4, tiles.size)
        assertEquals(listOf(0, 20, 0, 20), tiles.map { it.left })
        assertEquals(listOf(0, 0, 70, 70), tiles.map { it.top })
        assertEquals(listOf(20, 100, 20, 100), tiles.map { it.right })
        assertEquals(listOf(70, 70, 100, 100), tiles.map { it.bottom })
    }

    @Test
    fun `cuts out of order are made monotonic and can be empty`() {
        val tiles = GridSlicer.tilesFor(
            100,
            50,
            floatArrayOf(0f, 0.8f, 0.3f, 1f),
            GridSlicer.uniformCuts(1),
        )
        assertEquals(listOf(0, 80, 80), tiles.map { it.left })
        assertEquals(listOf(80, 80, 100), tiles.map { it.right })
        assertTrue(tiles[1].isEmpty)
        assertTrue(tiles[0].isEmpty.not())
        assertTrue(tiles[2].isEmpty.not())
    }

    @Test
    fun `custom cuts still cover the whole image`() {
        val width = 137
        val height = 89
        val tiles = GridSlicer.tilesFor(
            width,
            height,
            floatArrayOf(0f, 0.33f, 0.5f, 1f),
            floatArrayOf(0f, 0.25f, 1f),
        )
        assertEquals(6, tiles.size)
        assertEquals(0, tiles.first().left)
        assertEquals(0, tiles.first().top)
        assertEquals(width, tiles.last().right)
        assertEquals(height, tiles.last().bottom)
        val firstRow = tiles.take(3)
        assertEquals(width, firstRow.sumOf { it.width })
        val secondRow = tiles.drop(3)
        assertEquals(width, secondRow.sumOf { it.width })
    }

    @Test
    fun `single column keeps the full width`() {
        val tiles = GridSlicer.tilesFor(64, 64, GridSlicer.uniformCuts(1), GridSlicer.uniformCuts(1))
        assertEquals(1, tiles.size)
        assertEquals(64, tiles.first().width)
        assertEquals(64, tiles.first().height)
    }
}
