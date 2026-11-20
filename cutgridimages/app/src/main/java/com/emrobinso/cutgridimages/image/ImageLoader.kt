package com.emrobinso.cutgridimages.image

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Matrix
import android.media.ExifInterface
import android.net.Uri
import java.io.IOException

/**
 * Memuat gambar dari [Uri] tanpa memakai library tambahan.
 *
 * Dua tahap: baca dimensi saja, lalu dekode dengan `inSampleSize` agar sisi terpanjang
 * tidak melebihi [MAX_DIMENSION]. Orientasi EXIF diterapkan supaya hasil potongan tegak.
 */
object ImageLoader {

    /** Batas sisi terpanjang bitmap sumber; menjaga pemakaian memori tetap wajar. */
    const val MAX_DIMENSION = 4096

    fun load(context: Context, uri: Uri, maxDimension: Int = MAX_DIMENSION): Bitmap {
        val resolver = context.contentResolver

        val bounds = BitmapFactory.Options().apply { inJustDecodeBounds = true }
        resolver.openInputStream(uri)?.use { BitmapFactory.decodeStream(it, null, bounds) }
            ?: throw IOException("Tidak bisa membuka $uri")
        if (bounds.outWidth <= 0 || bounds.outHeight <= 0) {
            throw IOException("Berkas bukan gambar yang dikenali")
        }

        val options = BitmapFactory.Options().apply {
            inSampleSize = ImageSizing.sampleSizeFor(bounds.outWidth, bounds.outHeight, maxDimension)
            inPreferredConfig = Bitmap.Config.ARGB_8888
        }
        val decoded = resolver.openInputStream(uri)?.use { BitmapFactory.decodeStream(it, null, options) }
            ?: throw IOException("Gagal membaca gambar")

        return applyExifOrientation(context, uri, decoded)
    }

    private fun applyExifOrientation(context: Context, uri: Uri, decoded: Bitmap): Bitmap {
        val orientation = try {
            context.contentResolver.openInputStream(uri)?.use { stream ->
                ExifInterface(stream).getAttributeInt(
                    ExifInterface.TAG_ORIENTATION,
                    ExifInterface.ORIENTATION_NORMAL,
                )
            } ?: ExifInterface.ORIENTATION_NORMAL
        } catch (error: IOException) {
            ExifInterface.ORIENTATION_NORMAL
        } catch (error: RuntimeException) {
            // Sebagian penyedia dokumen mengembalikan stream aneh; abaikan saja.
            ExifInterface.ORIENTATION_NORMAL
        }

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

        val oriented = Bitmap.createBitmap(decoded, 0, 0, decoded.width, decoded.height, matrix, true)
        if (oriented !== decoded) decoded.recycle()
        return oriented
    }
}
