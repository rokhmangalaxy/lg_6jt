package com.emrobinso.cutgridimages.data

import android.content.Context
import org.json.JSONArray
import org.json.JSONObject

/** Gambar sumber (URI dokumen) yang ditambahkan pengguna. */
data class SourceImage(val uri: String, val addedAt: Long)

/** Menyimpan daftar URI gambar sumber agar bertahan setelah aplikasi ditutup. */
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

    fun remove(uri: String) = persist(list().filterNot { it.uri == uri })

    fun clear() {
        prefs.edit().remove(KEY_SOURCES).apply()
    }

    private fun persist(items: List<SourceImage>) {
        val array = JSONArray()
        items.forEach { array.put(JSONObject().put("uri", it.uri).put("addedAt", it.addedAt)) }
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
                    if (uri.isNotBlank()) add(SourceImage(uri, item.optLong("addedAt")))
                }
            }
        }.getOrDefault(emptyList())
    }

    private companion object {
        const val PREFS_NAME = "cutgrid_sources"
        const val KEY_SOURCES = "sources"
    }
}
