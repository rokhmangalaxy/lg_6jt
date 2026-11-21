package id.mcm.logopreview

/** Platform-independent source-color mapping; original pixels are never mutated. */
object LogoPixels {
    private const val WHITE = -1
    val presets = arrayOf(
        intArrayOf(0xffdc2626.toInt(),0xff173257.toInt(),WHITE,WHITE),
        intArrayOf(0xff173257.toInt(),0xffdc2626.toInt(),WHITE,WHITE),
        intArrayOf(0xff000000.toInt(),0xff000000.toInt(),WHITE,0xffd1d5db.toInt()),
        intArrayOf(WHITE,WHITE,0xff000000.toInt(),0xffd1d5db.toInt())
    )
    /** Android may color-convert PNG profiles by a few levels. Quantize known solid assets. */
    fun normalize(source: IntArray): IntArray {
        val palette = presets[0]
        return IntArray(source.size) { i ->
            val pixel=source[i]
            if ((pixel ushr 24) == 0) return@IntArray 0
            val r=(pixel ushr 16) and 255;val g=(pixel ushr 8) and 255;val b=pixel and 255
            var best=WHITE;var distance=Int.MAX_VALUE
            for(j in 0..2){
                val c=palette[j]
                val dr=r-((c ushr 16) and 255);val dg=g-((c ushr 8) and 255);val db=b-(c and 255)
                val d=dr*dr+dg*dg+db*db
                if(d<distance){distance=d;best=c}
            }
            best
        }
    }
    fun mask(pixels: IntArray, width: Int, height: Int, logo: Int): BooleanArray {
        require(pixels.size == width * height && width > 0 && height > 0)
        // All selected sources have explicit alpha: includes enclosed black counters.
        val mask = BooleanArray(pixels.size) { i -> (pixels[i] ushr 24) == 0 }
        return mask
    }
    fun recolor(source: IntArray, mask: BooleanArray, preset: Int, background: Int = presets[preset][3]): IntArray {
        require(source.size == mask.size)
        val colors = presets[preset]
        return IntArray(source.size) { i ->
            if (mask[i]) background else when (source[i]) {
                0xffdc2626.toInt() -> colors[0]
                0xff173257.toInt() -> colors[1]
                else -> colors[2]
            }
        }
    }
}
