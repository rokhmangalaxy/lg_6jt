package com.emrobinso.cutgridimages

import android.app.Activity
import android.app.AlertDialog
import android.content.Intent
import android.graphics.Typeface
import android.graphics.drawable.GradientDrawable
import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.GridLayout
import android.widget.TextView
import com.emrobinso.cutgridimages.data.AppSettings
import com.emrobinso.cutgridimages.data.ImageSourceStore
import com.emrobinso.cutgridimages.data.PieceStore
import com.emrobinso.cutgridimages.data.SettingsStore
import com.emrobinso.cutgridimages.image.PieceNaming
import com.emrobinso.cutgridimages.image.SourceCache
import com.emrobinso.cutgridimages.ui.dp

/** Pengaturan: nama proyek, digit nomor, pemisah, warna seleksi, dan pembersihan data. */
class SettingsActivity : Activity() {

    private lateinit var projectInput: EditText
    private lateinit var digitsInput: EditText
    private lateinit var separatorInput: EditText
    private lateinit var colorGrid: GridLayout
    private lateinit var namingPreview: TextView
    private lateinit var saveButton: Button
    private lateinit var clearButton: Button
    private lateinit var statusText: TextView
    private lateinit var navHome: Button
    private lateinit var navGallery: Button
    private lateinit var navSettings: Button

    private lateinit var settingsStore: SettingsStore
    private lateinit var pieceStore: PieceStore
    private lateinit var sourceStore: ImageSourceStore

    private var selectedColor = AppSettings.DEFAULT_HIGHLIGHT

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_settings)

        settingsStore = SettingsStore(this)
        pieceStore = PieceStore(this)
        sourceStore = ImageSourceStore(this)

        bindViews()
        fillFromSettings()

        val watcher = object : TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) = Unit

            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) = Unit

            override fun afterTextChanged(s: Editable?) = updatePreview()
        }
        projectInput.addTextChangedListener(watcher)
        digitsInput.addTextChangedListener(watcher)
        separatorInput.addTextChangedListener(watcher)

        saveButton.setOnClickListener { saveSettings() }
        clearButton.setOnClickListener { confirmClear() }
        navHome.setOnClickListener { navigate(HomeActivity::class.java) }
        navGallery.setOnClickListener { navigate(GalleryActivity::class.java) }
        navSettings.setOnClickListener { updateNavHighlight(2) }
    }

    private fun bindViews() {
        projectInput = findViewById(R.id.projectNameInput)
        digitsInput = findViewById(R.id.digitsInput)
        separatorInput = findViewById(R.id.separatorInput)
        colorGrid = findViewById(R.id.colorGrid)
        namingPreview = findViewById(R.id.namingPreview)
        saveButton = findViewById(R.id.saveSettingsButton)
        clearButton = findViewById(R.id.clearDataButton)
        statusText = findViewById(R.id.settingsStatus)
        navHome = findViewById(R.id.navHome)
        navGallery = findViewById(R.id.navGallery)
        navSettings = findViewById(R.id.navSettings)
    }

    private fun fillFromSettings() {
        val settings = settingsStore.load()
        projectInput.setText(settings.projectName)
        digitsInput.setText(settings.digits.toString())
        separatorInput.setText(settings.separator)
        selectedColor = settings.highlightColor
        buildColorSwatches()
        updatePreview()
        updateNavHighlight(2)
    }

    private fun buildColorSwatches() {
        colorGrid.removeAllViews()
        val size = dp(40)
        AppSettings.COLOR_CHOICES.forEach { color ->
            val swatch = View(this)
            swatch.layoutParams = GridLayout.LayoutParams().apply {
                width = size
                height = size
                setMargins(dp(4), dp(4), dp(4), dp(4))
            }
            swatch.background = GradientDrawable().apply {
                shape = GradientDrawable.OVAL
                setColor(color)
                if (color == selectedColor) setStroke(dp(3), getColor(R.color.ink))
            }
            swatch.contentDescription = String.format("#%06X", 0xFFFFFF and color)
            swatch.setOnClickListener {
                selectedColor = color
                buildColorSwatches()
            }
            colorGrid.addView(swatch)
        }
    }

    private fun updatePreview() {
        val digits = digitsInput.text.toString().toIntOrNull()
            ?.coerceIn(AppSettings.DIGIT_RANGE.first, AppSettings.DIGIT_RANGE.last)
            ?: AppSettings.DEFAULT_DIGITS
        namingPreview.text = getString(
            R.string.settings_preview,
            PieceNaming.previewName(
                project = projectInput.text.toString(),
                separator = separatorInput.text.toString(),
                digits = digits,
            ),
        )
    }

    private fun saveSettings() {
        val digits = digitsInput.text.toString().toIntOrNull()
        if (digits == null || digits !in AppSettings.DIGIT_RANGE) {
            statusText.text = getString(R.string.invalid_digits)
            return
        }
        val settings = AppSettings(
            projectName = projectInput.text.toString(),
            digits = digits,
            separator = separatorInput.text.toString(),
            highlightColor = selectedColor,
        )
        settingsStore.save(settings)
        projectInput.setText(PieceNaming.sanitizeProject(settings.projectName))
        separatorInput.setText(
            settings.separator.trim().ifEmpty { PieceNaming.DEFAULT_SEPARATOR },
        )
        updatePreview()
        statusText.text = getString(R.string.settings_saved)
    }

    private fun confirmClear() {
        AlertDialog.Builder(this)
            .setTitle(R.string.clear_title)
            .setMessage(R.string.clear_message)
            .setPositiveButton(R.string.delete) { _, _ ->
                pieceStore.clear()
                sourceStore.clear()
                SourceCache.clear(this)
                statusText.text = getString(R.string.clear_done)
            }
            .setNegativeButton(R.string.cancel, null)
            .show()
    }

    private fun navigate(target: Class<*>) {
        startActivity(Intent(this, target).addFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT))
    }

    private fun updateNavHighlight(index: Int) {
        val buttons = listOf(navHome, navGallery, navSettings)
        buttons.forEachIndexed { position, button ->
            val active = position == index
            button.backgroundTintList = android.content.res.ColorStateList.valueOf(
                if (active) getColor(R.color.accent) else android.graphics.Color.TRANSPARENT,
            )
            button.setTextColor(getColor(if (active) R.color.surface else R.color.ink_muted))
            button.typeface = if (active) Typeface.DEFAULT_BOLD else Typeface.DEFAULT
        }
    }
}
