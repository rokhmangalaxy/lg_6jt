package com.emrobinso.cutgridimages.image

import org.junit.Assert.assertEquals
import org.junit.Test

class PieceNamingTest {

    @Test
    fun `default naming uses three digits and underscore`() {
        assertEquals("mcm_001", PieceNaming.buildFileName("mcm", "_", 1, 3))
        assertEquals("mcm_012", PieceNaming.buildFileName("mcm", "_", 12, 3))
        assertEquals("mcm_1234", PieceNaming.buildFileName("mcm", "_", 1234, 3))
    }

    @Test
    fun `digit count is padded and kept within range`() {
        assertEquals("p_1", PieceNaming.buildFileName("p", "_", 1, 0))
        assertEquals("p_000001", PieceNaming.buildFileName("p", "_", 1, 9))
        assertEquals("p_0001", PieceNaming.buildFileName("p", "_", 1, 4))
    }

    @Test
    fun `separator falls back to underscore when blank`() {
        assertEquals("p_002", PieceNaming.buildFileName("p", "", 2, 3))
        assertEquals("p_002", PieceNaming.buildFileName("p", "   ", 2, 3))
        assertEquals("p-002", PieceNaming.buildFileName("p", "-", 2, 3))
    }

    @Test
    fun `project name is sanitized for file names`() {
        assertEquals("MCM-Logo_001", PieceNaming.buildFileName(" MCM Logo ", "_", 1, 3))
        assertEquals("a-b_001", PieceNaming.buildFileName("a/b", "_", 1, 3))
        assertEquals("cutgrid_001", PieceNaming.buildFileName("   ", "_", 1, 3))
        assertEquals("a-b_001", PieceNaming.buildFileName("a:b", "_", 1, 3))
    }

    @Test
    fun `index below one is clamped to one`() {
        assertEquals("p_001", PieceNaming.buildFileName("p", "_", 0, 3))
        assertEquals("p_001", PieceNaming.buildFileName("p", "_", -5, 3))
    }

    @Test
    fun `preview includes png extension`() {
        assertEquals("mcm_001.png", PieceNaming.previewName("mcm", "_", 3))
    }
}
