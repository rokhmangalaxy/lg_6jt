package com.emrobinso.cutgridimages.image

import android.annotation.SuppressLint
import android.annotation.TargetApi
import android.content.ContentValues
import android.content.Context
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Color
import android.media.MediaScannerConnection
import android.os.Build
import android.os.Environment
import android.provider.MediaStore
import com.emrobinso.cutgridimages.grid.GridTile
import java.io.File
import java.io.FileOutputStream
import java.io.IOException
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

/** Format berkas keluaran. */
enum class OutputFormat(val extension: String, val mimeType: String) {
    PNG("png", "image/png"),
    JPEG("jpg", "image/jpeg"),
}

/**
 * Menyimpan setiap petak sebagai berkas gambar di folder galeri `Pictures/CutGridImages`.
 *
 * Android 10+ memakai MediaStore (tanpa izin). Android 8–9 menulis ke penyimpanan publik
 * dan memindai ulang lewat MediaScanner; pemanggil wajib memegang izin tulis di sana.
 */
class TileExporter(private val context: Context) {

    /** Ringkasan hasil ekspor. */
    data class Summary(val count: Int, val locationLabel: String)

    /**
     * @param source bitmap sumber yang sudah berorientasi benar
     * @param tiles petak yang akan disimpan; petak kosong sebaiknya sudah disaring
     * @param format PNG (mempertahankan transparansi) atau JPEG (latar putih)
     * @param quality kualitas JPEG 0..100; diabaikan untuk PNG
     */
    fun export(
        source: Bitmap,
        tiles: List<GridTile>,
        format: OutputFormat,
        quality: Int = 95,
    ): Summary {
        require(tiles.isNotEmpty()) { "Tidak ada petak untuk disimpan" }
        val stamp = SimpleDateFormat("yyyyMMdd_HHmmss", Locale.US).format(Date())
        var saved = 0
        for (tile in tiles) {
            val tileBitmap = renderTile(source, tile, format)
            try {
                val name = "cutgrid_${stamp}_r${tile.row + 1}c${tile.column + 1}.${format.extension}"
                writeBitmap(tileBitmap, name, format, quality)
                saved++
            } finally {
                if (tileBitmap !== source) tileBitmap.recycle()
            }
        }
        return Summary(saved, "Pictures/$ALBUM")
    }

    private fun renderTile(source: Bitmap, tile: GridTile, format: OutputFormat): Bitmap {
        val cropped = Bitmap.createBitmap(source, tile.left, tile.top, tile.width, tile.height)
        if (format != OutputFormat.JPEG || !cropped.hasAlpha()) return cropped

        // JPEG tidak mendukung transparansi: ratakan ke latar putih, bukan hitam.
        val flattened = Bitmap.createBitmap(cropped.width, cropped.height, Bitmap.Config.ARGB_8888)
        Canvas(flattened).apply {
            drawColor(Color.WHITE)
            drawBitmap(cropped, 0f, 0f, null)
        }
        if (cropped !== source) cropped.recycle()
        return flattened
    }

    private fun writeBitmap(bitmap: Bitmap, name: String, format: OutputFormat, quality: Int) {
        val compressFormat = when (format) {
            OutputFormat.PNG -> Bitmap.CompressFormat.PNG
            OutputFormat.JPEG -> Bitmap.CompressFormat.JPEG
        }
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            writeToMediaStore(bitmap, name, format, compressFormat, quality)
        } else {
            writeToLegacyPictures(bitmap, name, format, compressFormat, quality)
        }
    }

    @TargetApi(Build.VERSION_CODES.Q)
    private fun writeToMediaStore(
        bitmap: Bitmap,
        name: String,
        format: OutputFormat,
        compressFormat: Bitmap.CompressFormat,
        quality: Int,
    ) {
        val resolver = context.contentResolver
        val collection = MediaStore.Images.Media.getContentUri(MediaStore.VOLUME_EXTERNAL_PRIMARY)
        val values = ContentValues().apply {
            put(MediaStore.Images.Media.DISPLAY_NAME, name)
            put(MediaStore.Images.Media.MIME_TYPE, format.mimeType)
            put(MediaStore.Images.Media.RELATIVE_PATH, "${Environment.DIRECTORY_PICTURES}/$ALBUM")
            put(MediaStore.Images.Media.IS_PENDING, 1)
        }
        val uri = resolver.insert(collection, values)
            ?: throw IOException("MediaStore menolak membuat entri $name")

        try {
            val stream = resolver.openOutputStream(uri)
                ?: throw IOException("Tidak bisa menulis ke $uri")
            stream.use { output ->
                require(bitmap.compress(compressFormat, quality, output)) {
                    "Kompresi gambar gagal"
                }
            }
            val ready = ContentValues().apply { put(MediaStore.Images.Media.IS_PENDING, 0) }
            resolver.update(uri, ready, null, null)
        } catch (error: Exception) {
            // Jangan tinggalkan entri setengah jadi di galeri.
            runCatching { resolver.delete(uri, null, null) }
            throw error
        }
    }

    @SuppressLint("MissingPermission") // Izin tulis diminta di MainActivity sebelum ekspor.
    @TargetApi(Build.VERSION_CODES.P)
    @Suppress("DEPRECATION")
    private fun writeToLegacyPictures(
        bitmap: Bitmap,
        name: String,
        format: OutputFormat,
        compressFormat: Bitmap.CompressFormat,
        quality: Int,
    ) {
        val directory = File(
            Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_PICTURES),
            ALBUM,
        )
        if (!directory.isDirectory && !directory.mkdirs()) {
            throw IOException("Tidak bisa membuat folder ${directory.absolutePath}")
        }
        val file = File(directory, name)
        FileOutputStream(file).use { output ->
            require(bitmap.compress(compressFormat, quality, output)) {
                "Kompresi gambar gagal"
            }
        }
        MediaScannerConnection.scanFile(context, arrayOf(file.absolutePath), arrayOf(format.mimeType), null)
    }

    companion object {
        /** Nama folder album di galeri. */
        const val ALBUM = "CutGridImages"
    }
}
