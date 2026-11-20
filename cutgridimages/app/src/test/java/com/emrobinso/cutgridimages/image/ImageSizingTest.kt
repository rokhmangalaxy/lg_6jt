package com.emrobinso.cutgridimages.image

import org.junit.Assert.assertEquals
import org.junit.Assert.assertThrows
import org.junit.Assert.assertTrue
import org.junit.Test
import kotlin.math.max

class ImageSizingTest {

    @Test
    fun `large images are downsampled by powers of two`() {
        assertEquals(2, ImageSizing.sampleSizeFor(width = 8000, height = 6000, maxDimension = 4096))
        assertEquals(4, ImageSizing.sampleSizeFor(width = 16000, height = 100, maxDimension = 4096))
    }

    @Test
    fun `images within the limit keep full resolution`() {
        assertEquals(1, ImageSizing.sampleSizeFor(width = 4096, height = 4096, maxDimension = 4096))
        assertEquals(1, ImageSizing.sampleSizeFor(width = 100, height = 100, maxDimension = 4096))
    }

    @Test
    fun `portrait images use the long side`() {
        // 9000 / 2 masih 4500 > 4096, jadi sampel berikutnya (4) yang dipakai.
        assertEquals(4, ImageSizing.sampleSizeFor(width = 1000, height = 9000, maxDimension = 4096))
        assertEquals(1, ImageSizing.sampleSizeFor(width = 1000, height = 4096, maxDimension = 4096))
    }

    @Test
    fun `one pixel over the limit triggers downsampling`() {
        assertEquals(2, ImageSizing.sampleSizeFor(width = 4097, height = 100, maxDimension = 4096))
    }

    @Test
    fun `result never exceeds the maximum dimension`() {
        val cases = listOf(
            Triple(1, 1, 4096),
            Triple(5000, 4000, 2048),
            Triple(12000, 900, 1024),
            Triple(900, 12000, 1000),
            Triple(8192, 8192, 4096),
        )
        cases.forEach { (width, height, limit) ->
            val sample = ImageSizing.sampleSizeFor(width, height, limit)
            assertTrue(
                "sample $sample untuk ${width}x$height batas $limit",
                max(width, height) / sample <= limit,
            )
            assertEquals(0, sample and (sample - 1)) // pangkat dua
        }
    }

    @Test
    fun `rejects invalid dimensions`() {
        assertThrows(IllegalArgumentException::class.java) {
            ImageSizing.sampleSizeFor(0, 100, 4096)
        }
        assertThrows(IllegalArgumentException::class.java) {
            ImageSizing.sampleSizeFor(100, 0, 4096)
        }
        assertThrows(IllegalArgumentException::class.java) {
            ImageSizing.sampleSizeFor(100, 100, 0)
        }
    }
}
