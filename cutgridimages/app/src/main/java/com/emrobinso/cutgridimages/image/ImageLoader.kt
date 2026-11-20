package com.emrobinso.cutgridimages.image

import android.content.ContentResolver
import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Matrix
import android.media.ExifInterface
import android.net.Uri
import android.os.ParcelFileDescriptor
import java.io.File
import java.io.IOException
import java.io.InputStream

/**
 * Memuat gambar dari [Uri] tanpa memakai library tambahan.
 *
 * Dua tahap: baca dimensi saja, lalu dekode dengan `inSampleSize` agar sisi terpanjang
 * tidak melebihi [MAX_DIMENSION]. Orientasi EXIF diterapkan supaya hasil potongan tegak.
 *
 * Sebagian penyedia dokumen (Downloads, Drive, Files) menolak `openInputStream` biasa atau
 * mengembalikan `null`; karena itu ada beberapa jalur cadangan sebelum menyerah.
 */
object ImageLoader {

    /** Batas sisi terpanjang bitmap sumber; menjaga pemakaian memori tetap wajar. */
    const val MAX_DIMENSION = 4096

    fun load(context: Context, uri: Uri, maxDimension: Int = MAX_DIMENSION): Bitmap {
        val resolver = context.contentResolver

        val bounds = BitmapFactory.Options().apply { inJustDecodeBounds = true }
        openStream(resolver, uri).use { BitmapFactory.decodeStream(it, null, bounds) }
        if (bounds.outWidth <= 0 || bounds.outHeight <= 0) {
            throw IOException("Berkas bukan gambar yang dikenali")
        }

        val options = BitmapFactory.Options().apply {
            inSampleSize = ImageSizing.sampleSizeFor(bounds.outWidth, bounds.outHeight, maxDimension)
            inPreferredConfig = Bitmap.Config.ARGB_8888
        }
        val decoded = openStream(resolver, uri).use { BitmapFactory.decodeStream(it, null, options) }
            ?: throw IOException("Isi berkas tidak bisa dibaca sebagai gambar")

        return orient(decoded, readOrientation(resolver, uri))
    }

    /** Memuat berkas salinan lokal; orientasi sudah diterapkan saat salinan dibuat. */
    fun loadFile(file: File, maxDimension: Int = MAX_DIMENSION): Bitmap {
        if (!file.isFile) throw IOException("Salinan gambar tidak ditemukan, pilih ulang gambarnya")
        val bounds = BitmapFactory.Options().apply { inJustDecodeBounds = true }
        BitmapFactory.decodeFile(file.absolutePath, bounds)
        if (bounds.outWidth <= 0 || bounds.outHeight <= 0) {
            throw IOException("Salinan gambar rusak, pilih ulang gambarnya")
        }
        val options = BitmapFactory.Options().apply {
            inSampleSize = ImageSizing.sampleSizeFor(bounds.outWidth, bounds.outHeight, maxDimension)
            inPreferredConfig = Bitmap.Config.ARGB_8888
        }
        val decoded = BitmapFactory.decodeFile(file.absolutePath, options)
            ?: throw IOException("Salinan gambar tidak bisa dibaca")
        return orient(decoded, readFileOrientation(file))
    }

    /**
     * Jalur baca berlapis: `openInputStream` → `openTypedAssetFileDescriptor` →
     * `openFileDescriptor`. Penyedia yang menolak jalur pertama sering berhasil di jalur lain.
     */
    private fun openStream(resolver: ContentResolver, uri: Uri): InputStream {
        runCatching { resolver.openInputStream(uri) }.getOrNull()?.let { return it }
        runCatching {
            resolver.openTypedAssetFileDescriptor(uri, "image/*", null)?.createInputStream()
        }.getOrNull()?.let { return it }
        runCatching {
            val descriptor = resolver.openFileDescriptor(uri, "r")
            descriptor?.let { ParcelFileDescriptor.AutoCloseInputStream(it) }
        }.getOrNull()?.let { return it }
        throw IOException(
            "Penyedia dokumen menolak membuka berkas ini. Pilih ulang gambarnya dari galeri.",
        )
    }

    private fun readOrientation(resolver: ContentResolver, uri: Uri): Int = runCatching {
        openStream(resolver, uri).use { stream ->
            ExifInterface(stream).getAttributeInt(
                ExifInterface.TAG_ORIENTATION,
                ExifInterface.ORIENTATION_NORMAL,
            )
        }
    }.getOrDefault(ExifInterface.ORIENTATION_NORMAL)

    private fun readFileOrientation(file: File): Int = runCatching {
        ExifInterface(file.absolutePath).getAttributeInt(
            ExifInterface.TAG_ORIENTATION,
            ExifInterface.ORIENTATION_NORMAL,
        )
    }.getOrDefault(ExifInterface.ORIENTATION_NORMAL)

    private fun orient(decoded: Bitmap, orientation: Int): Bitmap {
        val matrix = Matrix()
        when (orientation) {
            ExifInterface.ORIENTATION_ROTATE_90 -> matrix.postRotate(90f)
            ExifInterface.ORIENTATION_ROTATE_180 -> matrix.postRotate(180f)
            ExifInterface.ORIENTATION_ROTATE_270 -> matrix.postRotate(270f)
            ExifInterface.ORIENTATION_FLIP_HORIZONTAL -> matrix.postScale(-1f, 1f)
            ExifInterface.ORIENTATION_FLIP_VERTICAL -> matrix.postScale(1f, -1f)
            ExifInterface.ORIENTATION_TRANSPOSE -> {
                matrix.postScale(-1f, 1f)
                matrix.postRotate(270f)
            }
            ExifInterface.ORIENTATION_TRANSVERSE -> {
                matrix.postScale(-1f, 1f)
                matrix.postRotate(90f)
            }
            else -> return decoded
        }
        return runCatching {
            val oriented = Bitmap.createBitmap(decoded, 0, 0, decoded.width, decoded.height, matrix, true)
            if (oriented !== decoded) decoded.recycle()
            oriented
        }.getOrDefault(decoded)
    }
}
