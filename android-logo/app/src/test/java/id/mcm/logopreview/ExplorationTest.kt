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
    @Test fun collectionsNeverMixAndOriginalIndicesStayFixed(){
        assertEquals(0,LogoCatalog.next(3,1));assertEquals(3,LogoCatalog.next(0,-1))
        assertEquals(4,LogoCatalog.next(5,1));assertEquals(5,LogoCatalog.next(4,-1))
        assertEquals("client-attachment-09.png",LogoCatalog.files[3])
        assertEquals("exploration/exp-001-01.png",LogoCatalog.files[4])
    }
    @Test fun pilotSupportsSwatchesTransparencyAndUniforms(){
        val app:Application=RuntimeEnvironment.getApplication()
        for(logo in 4..5)for(preset in 0..3){
            val mark=LogoVectorRenderer.render(app.assets,logo,preset,600,true)
            assertEquals(0,mark.getPixel(0,0))
            val pixels=IntArray(mark.width*mark.height);mark.getPixels(pixels,0,mark.width,0,0,mark.width,mark.height)
            assertTrue(pixels.any{it==LogoPixels.presets[preset][0]})
            assertTrue(pixels.any{it==LogoPixels.presets[preset][2]})
            mark.recycle()
            val mockup=UniformRenderer.render(app.assets,logo,preset,true,0)
            assertEquals(600,mockup.width);mockup.recycle()
        }
    }
}
