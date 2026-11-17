package id.mcm.logopreview

/** Client selection: extracted no.4, then attachment cells 1, 8 and 9. */
object LogoCatalog {
    val files = arrayOf("client-logo-04.png", "client-attachment-01.png", "client-attachment-08.png", "client-attachment-09.png")
    val names = arrayOf("Logo 04", "Lampiran 01", "Lampiran 08", "Lampiran 09")
    val count get() = files.size
    fun next(index: Int, step: Int): Int = ((index + step) % count + count) % count
    fun background(logo: Int, preset: Int): Int =
        0xffd1d5db.toInt() // Light gray for every preset: white initials remain visible, never black.
}
