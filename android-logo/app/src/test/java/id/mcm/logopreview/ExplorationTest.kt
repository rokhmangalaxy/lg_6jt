package id.mcm.logopreview

import android.app.Application
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[34])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class ExplorationTest {
    @Test fun unifiedCatalogWrapsAndOriginalIndicesStayFixed(){
        assertEquals(4,LogoCatalog.next(3,1));assertEquals(329,LogoCatalog.next(0,-1))
        assertEquals(0,LogoCatalog.next(329,1));assertEquals(3,LogoCatalog.next(4,-1))
        assertEquals("client-attachment-09.png",LogoCatalog.files[3])
        assertEquals("exploration/exp-001-01.png",LogoCatalog.files[4])
    }
    @Test fun pilotSupportsSwatchesTransparencyAndUniforms(){
        val app:Application=RuntimeEnvironment.getApplication()
        for(logo in 4 until LogoCatalog.count)for(preset in 0..3){
            val mark=LogoVectorRenderer.render(app.assets,logo,preset,600,true)
            assertEquals(0,mark.getPixel(0,0))
            val pixels=IntArray(mark.width*mark.height);mark.getPixels(pixels,0,mark.width,0,0,mark.width,mark.height)
            assertTrue(pixels.any{it != 0 && it in LogoPixels.presets[preset]})
            // These newer source designs use transparent counters, not white material.
            assertTrue(pixels.any{it != 0})
            mark.recycle()
            val mockup=UniformRenderer.render(app.assets,logo,preset,true,0)
            assertEquals(600,mockup.width);mockup.recycle()
        }
    }
}
