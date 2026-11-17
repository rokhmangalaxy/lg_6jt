package id.mcm.logopreview

import android.app.Application
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import java.io.ByteArrayOutputStream
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
        assertEquals(LogoCatalog.files.toSet(),available.filter { !it.contains("/") && it.endsWith(".png") }.toSet())
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
            val decoded = IntArray(b.width*b.height)
            b.getPixels(decoded,0,b.width,0,0,b.width,b.height)
            val pixels = LogoPixels.normalize(decoded)
            assertTrue("Blank source: $file", pixels.any { it == 0xff173257.toInt() || it == 0xffdc2626.toInt() })
            val mask = LogoPixels.mask(pixels,b.width,b.height,index)
            for (preset in 0..3) {
                val output = LogoVectorRenderer.render(app.assets,index,preset)
                assertEquals(1600,maxOf(output.width,output.height))
                val result=IntArray(output.width*output.height)
                output.getPixels(result,0,output.width,0,0,output.width,output.height)
                val solidColors=LogoPixels.presets[preset].toSet()+LogoCatalog.background(index,preset)
                assertTrue("Missing antialiasing: $file preset=$preset",result.any {it !in solidColors})
                assertEquals("Wrong background: $file preset=$preset", LogoCatalog.background(index,preset),output.getPixel(0,0))
                assertTrue("Empty preview: $file preset=$preset", result.any { it != LogoCatalog.background(index,preset) })
                val bytes=ByteArrayOutputStream().also { LogoExporter.write(output,it) }.toByteArray()
                val exported=BitmapFactory.decodeByteArray(bytes,0,bytes.size)!!
                assertEquals("Export width: $file",output.width,exported.width)
                assertEquals("Export height: $file",output.height,exported.height)
                assertEquals("Export background: $file",output.getPixel(0,0),exported.getPixel(0,0))
                assertEquals("Export content: $file",output.getPixel(output.width/2,output.height/2),exported.getPixel(output.width/2,output.height/2))
                exported.recycle()
                output.recycle()
            }
            b.recycle()
        }
    }
}
