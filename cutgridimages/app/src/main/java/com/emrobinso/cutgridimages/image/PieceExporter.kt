package com.emrobinso.cutgridimages.image

import android.annotation.SuppressLint
import android.annotation.TargetApi
import android.content.ContentValues
import android.content.Context
import android.media.MediaScannerConnection
import android.os.Build
import android.os.Environment
import android.provider.MediaStore
import com.emrobinso.cutgridimages.data.Piece
import java.io.File
import java.io.FileOutputStream
import java.io.IOException

/**
 * Menyalin potongan dari galeri aplikasi ke galeri perangkat (`Pictures/CutGridImages`).
 * Android 10+ memakai MediaStore tanpa izin; Android 8–9 menulis ke penyimpanan publik.
 */
class PieceExporter(private val context: Context) {

    data class Summary(val saved: Int, val location: String)

    fun export(pieces: List<Piece>): Summary {
        require(pieces.isNotEmpty()) { "Tidak ada gambar untuk disimpan" }
        var saved = 0
        var lastError: String? = null
        pieces.forEach { piece ->
            if (!piece.file.isFile) {
                lastError = "Berkas ${piece.displayName} tidak ditemukan"
                return@forEach
            }
            runCatching {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                    writeToMediaStore(piece)
                } else {
                    writeToLegacyPictures(piece)
                }
            }.onSuccess { saved++ }
                .onFailure { lastError = it.message ?: it.javaClass.simpleName }
        }
        if (saved == 0) {
            throw IOException(lastError ?: "Tidak ada potongan yang bisa disimpan")
        }
        return Summary(saved, "Pictures/$ALBUM")
    }

    @TargetApi(Build.VERSION_CODES.Q)
    private fun writeToMediaStore(piece: Piece) {
        val resolver = context.contentResolver
        val collection = MediaStore.Images.Media.getContentUri(MediaStore.VOLUME_EXTERNAL_PRIMARY)
        val values = ContentValues().apply {
            put(MediaStore.Images.Media.DISPLAY_NAME, "${piece.displayName}.png")
            put(MediaStore.Images.Media.MIME_TYPE, MIME_TYPE)
            put(MediaStore.Images.Media.RELATIVE_PATH, "${Environment.DIRECTORY_PICTURES}/$ALBUM")
            put(MediaStore.Images.Media.IS_PENDING, 1)
        }
        val uri = resolver.insert(collection, values)
            ?: throw IOException("MediaStore menolak ${piece.displayName}")

        try {
            val output = resolver.openOutputStream(uri)
                ?: throw IOException("Tidak bisa menulis ke $uri")
            output.use { stream -> piece.file.inputStream().use { it.copyTo(stream) } }
            val ready = ContentValues().apply { put(MediaStore.Images.Media.IS_PENDING, 0) }
            resolver.update(uri, ready, null, null)
        } catch (error: Exception) {
            runCatching { resolver.delete(uri, null, null) }
            throw error
        }
    }

    @SuppressLint("MissingPermission") // Izin tulis diminta pemanggil sebelum ekspor di Android 8–9.
    @TargetApi(Build.VERSION_CODES.P)
    @Suppress("DEPRECATION")
    private fun writeToLegacyPictures(piece: Piece) {
        val directory = File(
            Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_PICTURES),
            ALBUM,
        )
        if (!directory.isDirectory && !directory.mkdirs()) {
            throw IOException("Tidak bisa membuat folder ${directory.absolutePath}")
        }
        val target = File(directory, "${piece.displayName}.png")
        piece.file.inputStream().use { input ->
            FileOutputStream(target).use { output -> input.copyTo(output) }
        }
        MediaScannerConnection.scanFile(context, arrayOf(target.absolutePath), arrayOf(MIME_TYPE), null)
    }

    companion object {
        const val ALBUM = "CutGridImages"
        private const val MIME_TYPE = "image/png"
    }
}
