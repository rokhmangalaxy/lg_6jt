package id.mcm.logopreview

/** Client indices never change. Exploration IDs are stable and source names stay in manifest. */
object LogoCatalog {
    val files = arrayOf("client-logo-04.png", "client-attachment-01.png", "client-attachment-08.png", "client-attachment-09.png",
        "exploration/exp-001-01.png", "exploration/exp-001-08.png")
    val names = arrayOf("Logo 04", "Lampiran 01", "Lampiran 08", "Lampiran 09", "Eksplorasi 01–01", "Eksplorasi 01–08")
    const val clientCount = 4
    val count get() = files.size
    fun isExploration(index: Int) = index >= clientCount
    fun collection(index: Int): IntRange = if(isExploration(index)) clientCount until count else 0 until clientCount
    fun next(index: Int, step: Int): Int {
        val range=collection(index);val size=range.count()
        return range.first+((index-range.first+step)%size+size)%size
    }
    fun background(logo: Int, preset: Int): Int = 0xffd1d5db.toInt()
}
