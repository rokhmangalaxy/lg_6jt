package com.emrobinso.cutgridimages

import android.Manifest
import android.app.Activity
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.widget.Button
import android.widget.RadioGroup
import android.widget.SeekBar
import android.widget.TextView
import com.emrobinso.cutgridimages.grid.GridSlicer
import com.emrobinso.cutgridimages.grid.MAX_GRID
import com.emrobinso.cutgridimages.grid.MIN_GRID
import com.emrobinso.cutgridimages.image.ImageLoader
import com.emrobinso.cutgridimages.image.OutputFormat
import com.emrobinso.cutgridimages.image.TileExporter
import com.emrobinso.cutgridimages.ui.GridPreviewView
import java.util.concurrent.Executors

/**
 * Satu layar: pilih gambar, atur jumlah kolom/baris, lihat pratinjau, lalu simpan tiap petak.
 *
 * Hanya memakai API platform Android (tanpa AndroidX) supaya build ringan dan tidak
 * menambah dependensi runtime.
 */
class MainActivity : Activity() {

    private lateinit var preview: GridPreviewView
    private lateinit var pickButton: Button
    private lateinit var exportButton: Button
    private lateinit var columnsBar: SeekBar
    private lateinit var rowsBar: SeekBar
    private lateinit var columnsValue: TextView
    private lateinit var rowsValue: TextView
    private lateinit var formatGroup: RadioGroup
    private lateinit var statusText: TextView

    private val ioExecutor = Executors.newSingleThreadExecutor()
    private val mainHandler = Handler(Looper.getMainLooper())

    private var sourceBitmap: Bitmap? = null
    private var sourceUri: Uri? = null
    private var busy = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        bindViews()

        columnsBar.max = MAX_GRID - MIN_GRID
        rowsBar.max = MAX_GRID - MIN_GRID
        columnsBar.progress = 2 // 3 kolom
        rowsBar.progress = 2 // 3 baris

        val gridListener = object : SeekBar.OnSeekBarChangeListener {
            override fun onProgressChanged(seekBar: SeekBar?, progress: Int, fromUser: Boolean) {
                updateGrid()
            }

            override fun onStartTrackingTouch(seekBar: SeekBar?) = Unit

            override fun onStopTrackingTouch(seekBar: SeekBar?) = Unit
        }
        columnsBar.setOnSeekBarChangeListener(gridListener)
        rowsBar.setOnSeekBarChangeListener(gridListener)

        pickButton.setOnClickListener { pickImage() }
        exportButton.setOnClickListener { requestExport() }

        updateGrid()

        val restoredUri = savedInstanceState?.getString(STATE_URI)
        if (restoredUri != null) {
            loadImage(Uri.parse(restoredUri))
        } else {
            handleLaunchIntent(intent)
        }
    }

    private fun bindViews() {
        preview = findViewById(R.id.preview)
        pickButton = findViewById(R.id.pickButton)
        exportButton = findViewById(R.id.exportButton)
        columnsBar = findViewById(R.id.columnsBar)
        rowsBar = findViewById(R.id.rowsBar)
        columnsValue = findViewById(R.id.columnsValue)
        rowsValue = findViewById(R.id.rowsValue)
        formatGroup = findViewById(R.id.formatGroup)
        statusText = findViewById(R.id.statusText)
    }

    // --- Pilih dan muat gambar -------------------------------------------------------------

    @Suppress("DEPRECATION")
    private fun pickImage() {
        val intent = Intent(Intent.ACTION_OPEN_DOCUMENT).apply {
            addCategory(Intent.CATEGORY_OPENABLE)
            type = "image/*"
            addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
        }
        startActivityForResult(intent, REQUEST_PICK_IMAGE)
    }

    @Deprecated("API platform; penggantinya butuh AndroidX Activity Result")
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode != REQUEST_PICK_IMAGE || resultCode != RESULT_OK) return
        val uri = data?.data ?: return
        try {
            contentResolver.takePersistableUriPermission(uri, Intent.FLAG_GRANT_READ_URI_PERMISSION)
        } catch (error: SecurityException) {
            // Penyedia tidak memberi izin persisten; muat sekali saja.
        }
        loadImage(uri)
    }

    private fun handleLaunchIntent(intent: Intent?) {
        if (intent == null) return
        val uri = when (intent.action) {
            Intent.ACTION_VIEW -> intent.data
            Intent.ACTION_SEND -> sharedImageUri(intent)
            else -> null
        }
        if (uri != null) loadImage(uri)
    }

    @Suppress("DEPRECATION")
    private fun sharedImageUri(intent: Intent): Uri? =
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            intent.getParcelableExtra(Intent.EXTRA_STREAM, Uri::class.java)
        } else {
            intent.getParcelableExtra<Uri>(Intent.EXTRA_STREAM)
        }

    private fun loadImage(uri: Uri) {
        if (busy) return
        sourceUri = uri
        setBusy(true, getString(R.string.loading_image))
        ioExecutor.execute {
            val loaded = runCatching { ImageLoader.load(this, uri) }
            mainHandler.post {
                if (isFinishing || isDestroyed) {
                    loaded.getOrNull()?.recycle()
                    return@post
                }
                setBusy(false, null)
                loaded.onSuccess { bitmap ->
                    preview.bitmap = null
                    sourceBitmap?.recycle()
                    sourceBitmap = bitmap
                    preview.bitmap = bitmap
                    exportButton.isEnabled = true
                    showStatus(gridSummary())
                }.onFailure { error ->
                    preview.bitmap = null
                    sourceBitmap?.recycle()
                    sourceBitmap = null
                    exportButton.isEnabled = false
                    showStatus(getString(R.string.load_failed, error.readableMessage()))
                }
            }
        }
    }

    // --- Pengaturan grid -------------------------------------------------------------------

    private fun updateGrid() {
        val columns = columnsBar.progress + MIN_GRID
        val rows = rowsBar.progress + MIN_GRID
        preview.columns = columns
        preview.rows = rows
        columnsValue.text = columns.toString()
        rowsValue.text = rows.toString()
        if (!busy) {
            exportButton.isEnabled = sourceBitmap != null
            if (sourceBitmap != null) showStatus(gridSummary())
        }
    }

    private fun gridSummary(): String {
        val bitmap = sourceBitmap
        val columns = columnsBar.progress + MIN_GRID
        val rows = rowsBar.progress + MIN_GRID
        return if (bitmap == null) {
            getString(R.string.hint_start)
        } else {
            getString(R.string.grid_summary, columns, rows, columns * rows, bitmap.width, bitmap.height)
        }
    }

    // --- Ekspor ----------------------------------------------------------------------------

    private fun requestExport() {
        val bitmap = sourceBitmap
        if (bitmap == null) {
            showStatus(getString(R.string.pick_first))
            return
        }
        if (busy) return
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.Q &&
            checkSelfPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED
        ) {
            requestPermissions(arrayOf(Manifest.permission.WRITE_EXTERNAL_STORAGE), REQUEST_STORAGE_PERMISSION)
            return
        }
        exportTiles(bitmap)
    }

    private fun exportTiles(bitmap: Bitmap) {
        val columns = preview.columns
        val rows = preview.rows
        val format = if (formatGroup.checkedRadioButtonId == R.id.formatJpeg) {
            OutputFormat.JPEG
        } else {
            OutputFormat.PNG
        }
        setBusy(true, getString(R.string.exporting))
        ioExecutor.execute {
            val result = runCatching {
                val tiles = GridSlicer.tileBounds(bitmap.width, bitmap.height, columns, rows)
                    .filterNot { it.isEmpty }
                TileExporter(this).export(bitmap, tiles, format)
            }
            mainHandler.post {
                if (isFinishing || isDestroyed) return@post
                setBusy(false, null)
                result.onSuccess { summary ->
                    showStatus(getString(R.string.saved, summary.count, summary.locationLabel))
                }.onFailure { error ->
                    showStatus(getString(R.string.export_failed, error.readableMessage()))
                }
            }
        }
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray,
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode != REQUEST_STORAGE_PERMISSION) return
        val granted = grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED
        val bitmap = sourceBitmap
        if (granted && bitmap != null) {
            exportTiles(bitmap)
        } else {
            showStatus(getString(R.string.permission_needed))
        }
    }

    // --- Status dan siklus hidup -----------------------------------------------------------

    private fun setBusy(value: Boolean, message: String?) {
        busy = value
        pickButton.isEnabled = !value
        exportButton.isEnabled = !value && sourceBitmap != null
        columnsBar.isEnabled = !value
        rowsBar.isEnabled = !value
        for (index in 0 until formatGroup.childCount) {
            formatGroup.getChildAt(index).isEnabled = !value
        }
        if (message != null) showStatus(message)
    }

    private fun showStatus(message: String) {
        statusText.text = message
    }

    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        outState.putString(STATE_URI, sourceUri?.toString())
    }

    override fun onDestroy() {
        mainHandler.removeCallbacksAndMessages(null)
        ioExecutor.shutdownNow()
        preview.bitmap = null
        super.onDestroy()
    }

    private fun Throwable.readableMessage(): String =
        message?.takeIf { it.isNotBlank() } ?: javaClass.simpleName

    private companion object {
        const val REQUEST_PICK_IMAGE = 1001
        const val REQUEST_STORAGE_PERMISSION = 1002
        const val STATE_URI = "state_source_uri"
    }
}
