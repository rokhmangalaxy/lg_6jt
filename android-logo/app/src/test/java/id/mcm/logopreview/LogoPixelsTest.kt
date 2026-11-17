package id.mcm.logopreview

import org.junit.Assert.*
import org.junit.Test

class LogoPixelsTest {
    private val white = -1
    private val red = 0xffdc2626.toInt()
    private fun fixture(): IntArray = IntArray(100) { white }.apply {
        for (y in 2..5) for(x in 2..5) if(y==2||y==5||x==2||x==5)this[y*10+x]=red
    }
    @Test fun exteriorAndEnclosedWhiteAreSeparate() {
        val pixels=fixture();val mask=LogoPixels.mask(pixels,10,10,-1)
        assertTrue(mask[0]);assertFalse(mask[33])
        for(preset in 0..3){
            val output=LogoPixels.recolor(pixels,mask,preset)
            assertEquals(LogoPixels.presets[preset][3],output[0])
            assertEquals(LogoPixels.presets[preset][2],output[33])
        }
    }
    @Test fun nameplateCounterUsesBackground() {
        // Closed white hole in the bottom nameplate of logo 05.
        val pixels=IntArray(100){white}
        for(y in 7..9)for(x in 2..4)if(y!=8||x!=3)pixels[y*10+x]=red
        val mask=LogoPixels.mask(pixels,10,10,4)
        assertTrue(mask[83])
        for(preset in 0..3)assertEquals(LogoPixels.presets[preset][3],LogoPixels.recolor(pixels,mask,preset)[83])
    }
    @Test fun recolorDoesNotMutateOriginalAndCanReset() {
        val source=fixture();val before=source.copyOf();val mask=LogoPixels.mask(source,10,10,-1)
        LogoPixels.recolor(source,mask,1)
        assertArrayEquals(before,source)
        assertArrayEquals(before,LogoPixels.recolor(source,mask,0))
    }
    @Test fun swappingOnlySwapsBrandColors() {
        val source=intArrayOf(red,0xff173257.toInt(),white)
        val result=LogoPixels.recolor(source,booleanArrayOf(false,false,true),1)
        assertArrayEquals(intArrayOf(0xff173257.toInt(),red,white),result)
    }
}
