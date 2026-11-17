package id.mcm.logopreview

object LogoCatalog {
    val files = arrayOf(
        "variasi-01-evolusi.png", "variasi-02-diamond-negatif.png",
        "variasi-03-lipatan-metal.png", "variasi-04-horizontal.png", "variasi-05-monokrom.png",
        "variasi-06-native.png", "variasi-07-native.png", "variasi-08-native.png",
        "variasi-09-native.png", "variasi-10-native.png"
    )
    val names = arrayOf("Evolusi", "Diamond", "Lipatan metal", "Horizontal", "Industrial",
        "Hexa Frame", "Folded MCM", "Shield", "Interlock", "Precision Cut")
    val count get() = files.size
    fun next(index: Int, step: Int): Int = ((index + step) % count + count) % count
}
