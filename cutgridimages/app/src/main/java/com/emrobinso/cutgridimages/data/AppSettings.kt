package com.emrobinso.cutgridimages.data

import android.content.Context
import com.emrobinso.cutgridimages.image.PieceNaming

/** Pengaturan aplikasi yang dapat diubah pengguna. */
data class AppSettings(
    val projectName: String = PieceNaming.DEFAULT_PROJECT,
    val digits: Int = DEFAULT_DIGITS,
    val separator: String = PieceNaming.DEFAULT_SEPARATOR,
    val highlightColor: Int = DEFAULT_HIGHLIGHT,
) {
    companion object {
        const val DEFAULT_DIGITS = 3
        val DIGIT_RANGE = PieceNaming.DIGIT_RANGE

        /** Hijau muda, warna default overlay seleksi. */
        val DEFAULT_HIGHLIGHT: Int = 0xFF8BC34A.toInt()

        val COLOR_CHOICES: IntArray = intArrayOf(
            0xFF8BC34A.toInt(), // hijau muda (default)
            0xFF26A69A.toInt(), // teal
            0xFF1F6FEB.toInt(), // biru
            0xFF8E44AD.toInt(), // ungu
            0xFFEF6C00.toInt(), // oranye
            0xFFDC2626.toInt(), // merah
        )
    }
}

/** Menyimpan [AppSettings] di SharedPreferences. */
class SettingsStore(context: Context) {

    private val prefs = context.applicationContext
        .getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)

    fun load(): AppSettings {
        val project = prefs.getString(KEY_PROJECT, null)
            ?.takeIf { it.isNotBlank() }
            ?: PieceNaming.DEFAULT_PROJECT
        val digits = prefs.getInt(KEY_DIGITS, AppSettings.DEFAULT_DIGITS)
            .coerceIn(AppSettings.DIGIT_RANGE.first, AppSettings.DIGIT_RANGE.last)
        val separator = prefs.getString(KEY_SEPARATOR, null)
            ?.takeIf { it.isNotBlank() }
            ?: PieceNaming.DEFAULT_SEPARATOR
        val color = prefs.getInt(KEY_COLOR, AppSettings.DEFAULT_HIGHLIGHT)
        return AppSettings(project, digits, separator, color)
    }

    fun save(settings: AppSettings) {
        prefs.edit()
            .putString(KEY_PROJECT, PieceNaming.sanitizeProject(settings.projectName))
            .putInt(
                KEY_DIGITS,
                settings.digits.coerceIn(AppSettings.DIGIT_RANGE.first, AppSettings.DIGIT_RANGE.last),
            )
            .putString(
                KEY_SEPARATOR,
                settings.separator.trim().ifEmpty { PieceNaming.DEFAULT_SEPARATOR },
            )
            .putInt(KEY_COLOR, settings.highlightColor)
            .apply()
    }

    private companion object {
        const val PREFS_NAME = "cutgrid_settings"
        const val KEY_PROJECT = "project"
        const val KEY_DIGITS = "digits"
        const val KEY_SEPARATOR = "separator"
        const val KEY_COLOR = "highlight_color"
    }
}
