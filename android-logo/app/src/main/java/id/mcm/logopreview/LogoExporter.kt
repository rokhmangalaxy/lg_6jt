package id.mcm.logopreview

import android.graphics.Bitmap
import java.io.OutputStream

/** Exports the original-resolution rendered bitmap, never a screenshot or UI capture. */
object LogoExporter {
    fun write(bitmap: Bitmap, output: OutputStream) {
        check(bitmap.compress(Bitmap.CompressFormat.PNG,100,output)) { "PNG encoding failed" }
        output.flush()
    }
}
