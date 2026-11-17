package id.mcm.logopreview

/** Platform-independent source-color mapping; original pixels are never mutated. */
object LogoPixels {
    private const val WHITE = -1
    private val regions = arrayOf(
        floatArrayOf(0f,.89f,1f,1f), floatArrayOf(0f,.66f,1f,1f),
        floatArrayOf(0f,.86f,1f,1f), floatArrayOf(.28f,.34f,1f,.69f),
        floatArrayOf(0f,.69f,1f,1f)
    )
    val presets = arrayOf(
        intArrayOf(0xffdc2626.toInt(),0xff173257.toInt(),WHITE,WHITE),
        intArrayOf(0xff173257.toInt(),0xffdc2626.toInt(),WHITE,WHITE),
        intArrayOf(0xff000000.toInt(),0xff000000.toInt(),WHITE,0xffd1d5db.toInt()),
        intArrayOf(WHITE,WHITE,0xff000000.toInt(),0xffd1d5db.toInt())
    )
    fun mask(pixels: IntArray, width: Int, height: Int, logo: Int): BooleanArray {
        require(pixels.size == width * height && width > 0 && height > 0)
        val mask = BooleanArray(pixels.size)
        val queue = IntArray(pixels.size)
        var head = 0; var tail = 0
        fun add(p: Int) {
            if (!mask[p] && pixels[p] == WHITE) { mask[p] = true; queue[tail++] = p }
        }
        for (x in 0 until width) { add(x); add((height-1)*width+x) }
        for (y in 0 until height) { add(y*width); add(y*width+width-1) }
        while (head < tail) {
            val p = queue[head++]; val x = p % width
            if (x > 0) add(p-1)
            if (x+1 < width) add(p+1)
            if (p >= width) add(p-width)
            if (p+width < pixels.size) add(p+width)
        }
        fun nameplate(r: FloatArray) {
            for (y in (r[1]*height).toInt() until kotlin.math.ceil((r[3]*height).toDouble()).toInt().coerceAtMost(height)) {
                for (x in (r[0]*width).toInt() until kotlin.math.ceil((r[2]*width).toDouble()).toInt().coerceAtMost(width)) {
                    val p = y*width+x
                    if (pixels[p] == WHITE) mask[p] = true
                }
            }
        }
        if (logo in regions.indices) nameplate(regions[logo])
        if (logo in 5 until LogoCatalog.count) nameplate(floatArrayOf(0f,.8f,1f,1f))
        if (logo == 3) nameplate(floatArrayOf(.23f,.36f,.285f,.44f))
        return mask
    }
    fun recolor(source: IntArray, mask: BooleanArray, preset: Int): IntArray {
        require(source.size == mask.size)
        val colors = presets[preset]
        return IntArray(source.size) { i ->
            if (mask[i]) colors[3] else when (source[i]) {
                0xffdc2626.toInt() -> colors[0]
                0xff173257.toInt() -> colors[1]
                else -> colors[2]
            }
        }
    }
}
