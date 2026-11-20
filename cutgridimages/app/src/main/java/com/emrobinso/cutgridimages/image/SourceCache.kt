package com.emrobinso.cutgridimages.image

import android.content.Context
import android.graphics.Bitmap
import java.io.File
import java.io.FileOutputStream
import java.io.IOException

/**
 * Salinan lokal gambar yang dipilih pengguna.
 *
 * Izin baca URI dokumen bisa dicabut (misalnya setelah aplikasi ditutup, berkas dihapus dari
 * penyedia, atau URI berasal dari "Buka dengan"/"Bagikan" yang izinnya sementara). Karena itu
 * setiap gambar yang berhasil dibaca langsung disalin ke penyimpanan aplikasi, lalu semua
 * pemuatan berikutnya memakai berkas lokal ini.
 */
object SourceCache {

    private const val DIRECTORY = "sources"
    private const val JPEG_QUALITY = 92

    fun directory(context: Context): File = File(context.filesDir, DIRECTORY)

    /** Nama berkas deterministik dari URI, aman dipakai di semua jenis URI. */
    fun fileNameFor(uri: String): String {
        val marker = Integer.toHexString(uri.hashCode())
        return "src_" + uri.length.toString(16) + "_" + marker + ".img"
    }

    fun fileFor(context: Context, uri: String): File = File(directory(context), fileNameFor(uri))

    fun hasCache(context: Context, uri: String): Boolean = fileFor(context, uri).isFile

    /** Menulis [bitmap] sebagai PNG (bila beralfa) atau JPEG, lalu mengembalikan berkasnya. */
    fun write(context: Context, uri: String, bitmap: Bitmap): File? {
        if (bitmap.width <= 0 || bitmap.height <= 0) return null
        val target = fileFor(context, uri)
        val format = if (bitmap.hasAlpha()) Bitmap.CompressFormat.PNG else Bitmap.CompressFormat.JPEG
        return runCatching {
            target.parentFile?.mkdirs()
            val temp = File(target.parentFile, target.name + ".tmp")
            FileOutputStream(temp).use { output ->
                if (!bitmap.compress(format, JPEG_QUALITY, output)) {
                    throw IOException("Gagal menulis salinan gambar")
                }
            }
            if (target.exists() && !target.delete()) throw IOException("Gagal mengganti salinan lama")
            if (!temp.renameTo(target)) throw IOException("Gagal menyimpan salinan gambar")
            target
        }.getOrNull()
    }

    fun delete(context: Context, uri: String) {
        runCatching { fileFor(context, uri).delete() }
    }

    fun clear(context: Context) {
        runCatching { directory(context).listFiles()?.forEach { it.delete() } }
    }
}
