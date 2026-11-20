package com.emrobinso.cutgridimages.image

/**
 * Aturan penamaan berkas potongan gambar: `<proyek><pemisah><nomor berdigit>`.
 *
 * Contoh: proyek `mcm`, pemisah `_`, nomor 1, digit 3 → `mcm_001`.
 * Fungsi di sini murni (tanpa Android) supaya bisa diuji di JVM.
 */
object PieceNaming {

    const val DEFAULT_PROJECT = "cutgrid"
    const val DEFAULT_SEPARATOR = "_"
    val DIGIT_RANGE = 1..6

    /** Nama dasar berkas tanpa ekstensi, mis. `mcm_001`. */
    fun buildFileName(project: String, separator: String, index: Int, digits: Int): String {
        val safeProject = sanitizeProject(project)
        val safeSeparator = separator.trim().ifEmpty { DEFAULT_SEPARATOR }
        val safeDigits = digits.coerceIn(DIGIT_RANGE.first, DIGIT_RANGE.last)
        val number = index.coerceAtLeast(1).toString().padStart(safeDigits, '0')
        return "$safeProject$safeSeparator$number"
    }

    /** Membuang karakter yang tidak sah untuk nama berkas; spasi diganti tanda hubung. */
    fun sanitizeProject(raw: String): String {
        val cleaned = raw.trim()
            .replace(Regex("[\\\\/:*?\"<>|]"), "-")
            .replace(Regex("\\s+"), "-")
            .trim('-')
        return cleaned.ifEmpty { DEFAULT_PROJECT }
    }

    /** Contoh nama lengkap untuk pratinjau di Pengaturan. */
    fun previewName(project: String, separator: String, digits: Int): String =
        buildFileName(project, separator, 1, digits) + ".png"
}
