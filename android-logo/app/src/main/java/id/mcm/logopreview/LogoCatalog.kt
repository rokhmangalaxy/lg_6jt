package id.mcm.logopreview

/** One undecided collection. Stable asset IDs preserve saved swatches. */
object LogoCatalog {
    val files = arrayOf("client-logo-04.png", "client-attachment-01.png", "client-attachment-08.png", "client-attachment-09.png",
        "exploration/exp-001-01.png", "exploration/exp-001-08.png", "exploration/geo-007.png", "exploration/geo-008.png",
        "exploration/exp-001-02.png", "exploration/exp-001-03.png", "exploration/exp-001-04.png")
    val names = arrayOf("Variasi 01", "Variasi 02", "Variasi 03", "Variasi 04", "Variasi 05", "Variasi 06", "Variasi 07", "Variasi 08", "Variasi 09", "Variasi 10", "Variasi 11")
    const val clientCount = 4
    val count get() = files.size
    fun isExploration(index: Int) = index >= clientCount
    fun collection(index: Int): IntRange = 0 until count
    fun next(index: Int, step: Int): Int = ((index+step)%count+count)%count
    fun background(logo: Int, preset: Int): Int = 0xffd1d5db.toInt()
}
