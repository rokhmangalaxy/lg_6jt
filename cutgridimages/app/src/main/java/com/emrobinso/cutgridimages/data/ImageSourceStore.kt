package com.emrobinso.cutgridimages.data

import android.content.Context
import org.json.JSONArray
import org.json.JSONObject

/**
 * Gambar sumber yang ditambahkan pengguna.
 *
 * [cachedPath] menunjuk salinan lokal di penyimpanan aplikasi (lihat `image.SourceCache`).
 * Bila salinan ada, gambar tidak lagi bergantung pada izin URI penyedia dokumen.
 */
data class SourceImage(
    val uri: String,
    val addedAt: Long,
    val cachedPath: String? = null,
)

/** Menyimpan daftar gambar sumber agar bertahan setelah aplikasi ditutup. */
class ImageSourceStore(context: Context) {

    private val prefs = context.applicationContext
        .getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)

    fun list(): List<SourceImage> = parse(prefs.getString(KEY_SOURCES, null))

    /** Menambahkan URI baru (duplikat diabaikan) dan mengembalikan daftar terbaru. */
    fun add(uris: Collection<String>): List<SourceImage> {
        val current = list().toMutableList()
        val known = current.mapTo(HashSet()) { it.uri }
        val now = System.currentTimeMillis()
        uris.forEach { uri ->
            if (uri.isNotBlank() && known.add(uri)) current += SourceImage(uri, now)
        }
        persist(current)
        return current
    }

    /** Mencatat lokasi salinan lokal untuk [uri] (atau menghapus catatannya bila null). */
    fun setCached(uri: String, path: String?): List<SourceImage> {
        val updated = list().map { item ->
            if (item.uri == uri) item.copy(cachedPath = path) else item
        }
        persist(updated)
        return updated
    }

    fun remove(uri: String): List<SourceImage> {
        val updated = list().filterNot { it.uri == uri }
        persist(updated)
        return updated
    }

    fun clear() {
        prefs.edit().remove(KEY_SOURCES).apply()
    }

    private fun persist(items: List<SourceImage>) {
        val array = JSONArray()
        items.forEach { item ->
            array.put(
                JSONObject()
                    .put("uri", item.uri)
                    .put("addedAt", item.addedAt)
                    .put("cache", item.cachedPath ?: ""),
            )
        }
        prefs.edit().putString(KEY_SOURCES, array.toString()).apply()
    }

    private fun parse(raw: String?): List<SourceImage> {
        if (raw.isNullOrBlank()) return emptyList()
        return runCatching {
            val array = JSONArray(raw)
            buildList {
                for (index in 0 until array.length()) {
                    val item = array.optJSONObject(index) ?: continue
                    val uri = item.optString("uri")
                    if (uri.isBlank()) continue
                    val cache = item.optString("cache").takeIf { it.isNotBlank() }
                    add(SourceImage(uri, item.optLong("addedAt"), cache))
                }
            }
        }.getOrDefault(emptyList())
    }

    private companion object {
        const val PREFS_NAME = "cutgrid_sources"
        const val KEY_SOURCES = "sources"
    }
}
