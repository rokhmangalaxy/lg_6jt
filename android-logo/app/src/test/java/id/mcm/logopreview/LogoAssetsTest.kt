package id.mcm.logopreview

import android.app.Application
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode

/** Decode the real packaged source images through Android's native graphics stack. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [34])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class LogoAssetsTest {
    @Test fun everyCatalogAssetDecodesAndRendersAllFourSwatches() {
        val app: Application = RuntimeEnvironment.getApplication()
        val available = app.assets.list("")!!.toSet()
        for ((index, file) in LogoCatalog.files.withIndex()) {
            assertTrue("Missing packaged asset: $file", file in available)
            val options = BitmapFactory.Options().apply {
                inPreferredConfig = Bitmap.Config.ARGB_8888
                inScaled = false
            }
            val bitmap = app.assets.open(file).use { BitmapFactory.decodeStream(it,null,options) }
            assertNotNull("Android cannot decode: $file", bitmap)
            val b = bitmap!!
            assertTrue("Invalid size: $file", b.width > 0 && b.height > 0)
            val pixels = IntArray(b.width*b.height)
            b.getPixels(pixels,0,b.width,0,0,b.width,b.height)
            assertTrue("Blank source: $file", pixels.any { it == 0xff173257.toInt() || it == 0xffdc2626.toInt() })
            val mask = LogoPixels.mask(pixels,b.width,b.height,index)
            for (preset in 0..3) {
                val result = LogoPixels.recolor(pixels,mask,preset)
                val output = Bitmap.createBitmap(result,b.width,b.height,Bitmap.Config.ARGB_8888)
                assertEquals("Wrong background: $file preset=$preset", LogoPixels.presets[preset][3],output.getPixel(0,0))
                assertTrue("Empty preview: $file preset=$preset", result.any { it != LogoPixels.presets[preset][3] })
                output.recycle()
            }
            b.recycle()
        }
    }
}
