package com.emrobinso.cutgridimages.data

import android.content.Context
import android.graphics.Bitmap
import com.emrobinso.cutgridimages.grid.GridTile
import com.emrobinso.cutgridimages.image.PieceNaming
import java.io.File
import java.io.FileOutputStream
import java.util.UUID
import kotlin.math.max

/** Satu potongan gambar yang tersimpan di galeri aplikasi. */
data class Piece(
    val id: String,
    val displayName: String,
    val project: String,
    val createdAt: Long,
    val sourceLabel: String,
    val file: File,
)

/**
 * Menyimpan potongan sebagai PNG di penyimpanan internal aplikasi (`files/pieces`),
 * dengan indeks JSON (`files/pieces.json`) berisi nama tampilan dan nomor urut berikutnya.
 * Tidak memerlukan izin penyimpanan.
 */
class PieceStore(context: Context) {

    private val appContext = context.applicationContext
    private val directory = File(appContext.filesDir, DIRECTORY)
    private val indexFile = File(appContext.filesDir, INDEX_FILE)

    /** Isi indeks: potongan terbaru lebih dulu, plus nomor urut berikutnya. */
    data class Index(val pieces: List<Piece>, val nextIndex: Int)

    @Synchronized
    fun load(): Index {
        val raw = runCatching { indexFile.readText() }.getOrNull()
        if (raw.isNullOrBlank()) return Index(emptyList(), 1)
        return runCatching {
            val json = org.json.JSONObject(raw)
            val array = json.optJSONArray("pieces") ?: org.json.JSONArray()
            val pieces = buildList {
                for (position in 0 until array.length()) {
                    val item = array.optJSONObject(position) ?: continue
                    val id = item.optString("id")
                    val name = item.optString("name")
                    if (id.isBlank() || name.isBlank()) continue
                    val file = File(directory, "$id.png")
                    if (!file.isFile) continue
                    add(
                        Piece(
                            id = id,
                            displayName = name,
                            project = item.optString("project"),
                            createdAt = item.optLong("createdAt"),
                            sourceLabel = item.optString("source"),
                            file = file,
                        ),
                    )
                }
            }.sortedByDescending { it.createdAt }
            val next = max(1, json.optInt("nextIndex", pieces.size + 1))
            Index(pieces, next)
        }.getOrElse { Index(emptyList(), 1) }
    }

    /** Memotong [tile] dari [bitmap] dan menyimpannya sebagai potongan baru. */
    @Synchronized
    fun save(
        bitmap: Bitmap,
        tile: GridTile,
        settings: AppSettings,
        sourceLabel: String,
    ): Piece? {
        if (tile.isEmpty) return null
        val index = load()
        if (!directory.isDirectory && !directory.mkdirs()) return null

        val displayName = PieceNaming.buildFileName(
            project = settings.projectName,
            separator = settings.separator,
            index = index.nextIndex,
            digits = settings.digits,
        )
        val id = UUID.randomUUID().toString()
        val file = File(directory, "$id.png")
        val cropped = Bitmap.createBitmap(bitmap, tile.left, tile.top, tile.width, tile.height)
        try {
            FileOutputStream(file).use { output ->
                if (!cropped.compress(Bitmap.CompressFormat.PNG, 100, output)) {
                    file.delete()
                    return null
                }
            }
        } finally {
            if (cropped !== bitmap) cropped.recycle()
        }

        val piece = Piece(
            id = id,
            displayName = displayName,
            project = settings.projectName,
            createdAt = System.currentTimeMillis(),
            sourceLabel = sourceLabel,
            file = file,
        )
        writeIndex(index.copy(pieces = index.pieces + piece, nextIndex = index.nextIndex + 1))
        return piece
    }

    @Synchronized
    fun delete(pieces: Collection<Piece>) {
        val ids = pieces.mapTo(HashSet()) { it.id }
        pieces.forEach { runCatching { it.file.delete() } }
        val index = load()
        writeIndex(index.copy(pieces = index.pieces.filterNot { it.id in ids }))
    }

    @Synchronized
    fun clear() {
        directory.listFiles()?.forEach { runCatching { it.delete() } }
        indexFile.delete()
    }

    fun count(): Int = load().pieces.size

    private fun writeIndex(index: Index) {
        val array = org.json.JSONArray()
        index.pieces.forEach { piece ->
            array.put(
                org.json.JSONObject()
                    .put("id", piece.id)
                    .put("name", piece.displayName)
                    .put("project", piece.project)
                    .put("createdAt", piece.createdAt)
                    .put("source", piece.sourceLabel),
            )
        }
        val json = org.json.JSONObject()
            .put("nextIndex", index.nextIndex)
            .put("pieces", array)
        runCatching { indexFile.writeText(json.toString()) }
    }

    private companion object {
        const val DIRECTORY = "pieces"
        const val INDEX_FILE = "pieces.json"
    }
}
