package id.mcm.logopreview

import org.junit.Assert.*
import org.junit.Test

class LogoPixelsTest {
    private val white = -1
    private val red = 0xffdc2626.toInt()
    private val blue = 0xff173257.toInt()
    @Test fun alphaSeparatesWhiteInitialsFromBackgroundIncludingClosedHoles() {
        val source=intArrayOf(0,red,white,blue,0)
        val mask=LogoPixels.mask(source,5,1,0)
        assertArrayEquals(booleanArrayOf(true,false,false,false,true),mask)
        for(logo in 0 until LogoCatalog.count)for(preset in 0..3){
            val bg=LogoCatalog.background(logo,preset)
            val output=LogoPixels.recolor(source,mask,preset,bg)
            assertEquals(bg,output[0]);assertEquals(bg,output[4])
            assertEquals(LogoPixels.presets[preset][2],output[2])
        }
    }
    @Test fun recolorDoesNotMutateOriginalAndCanReset() {
        val source=intArrayOf(0,red,blue,white);val before=source.copyOf()
        val mask=LogoPixels.mask(source,4,1,0)
        LogoPixels.recolor(source,mask,1)
        assertArrayEquals(before,source)
        assertArrayEquals(intArrayOf(white,red,blue,white),LogoPixels.recolor(source,mask,0))
    }
    @Test fun catalogHasExactlyTheFourClientSelectionsAndWraps() {
        assertEquals(105,LogoCatalog.count)
        assertArrayEquals(arrayOf("client-logo-04.png","client-attachment-01.png","client-attachment-08.png","client-attachment-09.png"),LogoCatalog.files.take(4).toTypedArray())
        assertEquals(LogoCatalog.files.size,LogoCatalog.names.size)
        assertEquals(105,LogoCatalog.files.toSet().size)
        assertEquals(4,LogoCatalog.next(3,1))
        assertEquals(104,LogoCatalog.next(0,-1))
    }
    @Test fun everyLogoAndSwatchUseLightGrayNeverBlack() {
        for(logo in 0..3)for(preset in 0..3)assertEquals(0xffd1d5db.toInt(),LogoCatalog.background(logo,preset))
    }
    @Test fun normalizePreservesTransparencyAndRoundsBrandColors() {
        val source=intArrayOf(0,0x00101010,0xffdd2727.toInt(),0xff183358.toInt(),0xfffefefe.toInt())
        val before=source.copyOf()
        assertArrayEquals(intArrayOf(0,0,red,blue,white),LogoPixels.normalize(source))
        assertArrayEquals(before,source)
    }
}
