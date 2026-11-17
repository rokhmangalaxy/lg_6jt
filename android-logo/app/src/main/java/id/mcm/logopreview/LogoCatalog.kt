package id.mcm.logopreview

/** Client selection: extracted no.4, then attachment cells 1, 8 and 9. */
object LogoCatalog {
    val files = arrayOf("client-logo-04.png", "client-attachment-01.png", "client-attachment-08.png", "client-attachment-09.png")
    val names = arrayOf("Logo 04", "Lampiran 01", "Lampiran 08", "Lampiran 09")
    val count get() = files.size
    fun next(index: Int, step: Int): Int = ((index + step) % count + count) % count
    fun background(logo: Int, preset: Int): Int =
        if (logo in 1 until count && preset in 0..1) 0xff000000.toInt() else LogoPixels.presets[preset][3]
}
