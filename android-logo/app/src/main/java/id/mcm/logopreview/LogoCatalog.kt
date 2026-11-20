package id.mcm.logopreview

/** One undecided collection. Stable asset IDs preserve saved swatches. */
object LogoCatalog {
    val files = arrayOf("client-logo-04.png", "client-attachment-01.png", "client-attachment-08.png", "client-attachment-09.png",
        "exploration/exp-001-01.png", "exploration/exp-001-08.png")
    val names = arrayOf("Variasi 01", "Variasi 02", "Variasi 03", "Variasi 04", "Variasi 05", "Variasi 06")
    const val clientCount = 4
    val count get() = files.size
    fun isExploration(index: Int) = index >= clientCount
    fun collection(index: Int): IntRange = 0 until count
    fun next(index: Int, step: Int): Int = ((index+step)%count+count)%count
    fun background(logo: Int, preset: Int): Int = 0xffd1d5db.toInt()
}
