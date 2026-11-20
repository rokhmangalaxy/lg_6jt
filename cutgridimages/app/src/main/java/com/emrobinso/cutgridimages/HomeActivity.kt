package com.emrobinso.cutgridimages

import android.app.Activity
import android.content.Intent
import android.content.res.ColorStateList
import android.graphics.Bitmap
import android.graphics.Typeface
import android.net.Uri
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.Gravity
import android.view.View
import android.widget.Button
import android.widget.FrameLayout
import android.widget.GridLayout
import android.widget.ImageView
import android.widget.ScrollView
import android.widget.TextView
import com.emrobinso.cutgridimages.data.AppSettings
import com.emrobinso.cutgridimages.data.ImageSourceStore
import com.emrobinso.cutgridimages.data.PieceStore
import com.emrobinso.cutgridimages.data.SettingsStore
import com.emrobinso.cutgridimages.data.SourceImage
import com.emrobinso.cutgridimages.grid.GridSlicer
import com.emrobinso.cutgridimages.grid.MAX_GRID
import com.emrobinso.cutgridimages.grid.MIN_GRID
import com.emrobinso.cutgridimages.image.ImageLoader
import com.emrobinso.cutgridimages.image.Thumbnails
import com.emrobinso.cutgridimages.ui.GridEditorView
import com.emrobinso.cutgridimages.ui.dp
import com.emrobinso.cutgridimages.ui.roundedBackground
import java.util.concurrent.Executors

/**
 * Beranda: placeholder input gambar (multi seleksi), strip 5 kolom yang bisa di-scroll,
 * gambar utama dengan pengaturan kolom/baris, dan mode seleksi untuk menyimpan potongan.
 */
class HomeActivity : Activity() {

    private lateinit var editor: GridEditorView
    private lateinit var projectSubtitle: TextView
    private lateinit var thumbnailScroll: ScrollView
    private lateinit var thumbnailGrid: GridLayout
    private lateinit var emptyPlaceholder: View
    private lateinit var gridControls: View
    private lateinit var selectPanel: View
    private lateinit var modeGridButton: Button
    private lateinit var modeSelectButton: Button
    private lateinit var columnsValue: TextView
    private lateinit var rowsValue: TextView
    private lateinit var columnsMinus: Button
    private lateinit var columnsPlus: Button
    private lateinit var rowsMinus: Button
    private lateinit var rowsPlus: Button
    private lateinit var selectAllButton: Button
    private lateinit var clearSelectionButton: Button
    private lateinit var saveSelectedButton: Button
    private lateinit var saveAllButton: Button
    private lateinit var statusText: TextView
    private lateinit var navHome: Button
    private lateinit var navGallery: Button
    private lateinit var navSettings: Button

    private lateinit var settingsStore: SettingsStore
    private lateinit var sourceStore: ImageSourceStore
    private lateinit var pieceStore: PieceStore

    private val executor = Executors.newSingleThreadExecutor()
    private val handler = Handler(Looper.getMainLooper())

    private var settings = AppSettings()
    private var sources: List<SourceImage> = emptyList()
    private var mainUri: String? = null
    private var mainBitmap: Bitmap? = null
    private var busy = false

    private enum class Mode { GRID, SELECT }

    private var mode = Mode.GRID

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_home)

        settingsStore = SettingsStore(this)
        sourceStore = ImageSourceStore(this)
        pieceStore = PieceStore(this)
        settings = settingsStore.load()

        bindViews()
        editor.highlightColor = settings.highlightColor
        editor.columns = savedInstanceState?.getInt(STATE_COLUMNS) ?: 3
        editor.rows = savedInstanceState?.getInt(STATE_ROWS) ?: 3
        editor.onSelectionChanged = { updateSelectionUi() }

        modeGridButton.setOnClickListener { setMode(Mode.GRID) }
        modeSelectButton.setOnClickListener { setMode(Mode.SELECT) }
        columnsMinus.setOnClickListener { adjustGrid(columnsDelta = -1) }
        columnsPlus.setOnClickListener { adjustGrid(columnsDelta = 1) }
        rowsMinus.setOnClickListener { adjustGrid(rowsDelta = -1) }
        rowsPlus.setOnClickListener { adjustGrid(rowsDelta = 1) }
        selectAllButton.setOnClickListener { editor.selectAll() }
        clearSelectionButton.setOnClickListener { editor.clearSelection() }
        saveSelectedButton.setOnClickListener { savePieces(onlySelected = true) }
        saveAllButton.setOnClickListener { savePieces(onlySelected = false) }
        emptyPlaceholder.setOnClickListener { pickImages() }
        navHome.setOnClickListener { updateNavHighlight(0) }
        navGallery.setOnClickListener { navigate(GalleryActivity::class.java) }
        navSettings.setOnClickListener { navigate(SettingsActivity::class.java) }

        sources = sourceStore.list()
        renderThumbnails()
        setMode(Mode.GRID)
        updateGridLabels()

        val restoredMain = savedInstanceState?.getString(STATE_MAIN_URI)
        if (restoredMain != null) {
            selectMain(restoredMain)
        } else if (sources.isNotEmpty()) {
            selectMain(sources.first().uri)
        } else {
            handleLaunchIntent(intent)
        }
    }

    private fun bindViews() {
        editor = findViewById(R.id.editor)
        projectSubtitle = findViewById(R.id.projectSubtitle)
        thumbnailScroll = findViewById(R.id.thumbnailScroll)
        thumbnailGrid = findViewById(R.id.thumbnailGrid)
        emptyPlaceholder = findViewById(R.id.emptyPlaceholder)
        gridControls = findViewById(R.id.gridControls)
        selectPanel = findViewById(R.id.selectPanel)
        modeGridButton = findViewById(R.id.modeGridButton)
        modeSelectButton = findViewById(R.id.modeSelectButton)
        columnsValue = findViewById(R.id.columnsValue)
        rowsValue = findViewById(R.id.rowsValue)
        columnsMinus = findViewById(R.id.columnsMinus)
        columnsPlus = findViewById(R.id.columnsPlus)
        rowsMinus = findViewById(R.id.rowsMinus)
        rowsPlus = findViewById(R.id.rowsPlus)
        selectAllButton = findViewById(R.id.selectAllButton)
        clearSelectionButton = findViewById(R.id.clearSelectionButton)
        saveSelectedButton = findViewById(R.id.saveSelectedButton)
        saveAllButton = findViewById(R.id.saveAllButton)
        statusText = findViewById(R.id.statusText)
        navHome = findViewById(R.id.navHome)
        navGallery = findViewById(R.id.navGallery)
        navSettings = findViewById(R.id.navSettings)
    }

    override fun onResume() {
        super.onResume()
        settings = settingsStore.load()
        editor.highlightColor = settings.highlightColor
        projectSubtitle.text = getString(R.string.home_project, settings.projectName)
        updateNavHighlight(0)

        val latest = sourceStore.list()
        if (latest != sources) {
            sources = latest
            if (sources.none { it.uri == mainUri }) {
                mainUri = null
                showMain(null)
                if (sources.isNotEmpty()) selectMain(sources.first().uri)
            }
            renderThumbnails()
        }
        updateSelectionUi()
    }

    // --- Gambar sumber ------------------------------------------------------------------

    @Suppress("DEPRECATION")
    private fun pickImages() {
        val intent = Intent(Intent.ACTION_OPEN_DOCUMENT).apply {
            addCategory(Intent.CATEGORY_OPENABLE)
            type = "image/*"
            putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true)
            addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
        }
        startActivityForResult(intent, REQUEST_PICK_IMAGES)
    }

    @Suppress("DEPRECATION")
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode != REQUEST_PICK_IMAGES || resultCode != RESULT_OK) return

        val picked = mutableListOf<Uri>()
        val clip = data?.clipData
        if (clip != null) {
            for (position in 0 until clip.itemCount) {
                clip.getItemAt(position).uri?.let { picked += it }
            }
        } else {
            data?.data?.let { picked += it }
        }
        if (picked.isEmpty()) return

        picked.forEach { uri ->
            runCatching {
                contentResolver.takePersistableUriPermission(
                    uri,
                    Intent.FLAG_GRANT_READ_URI_PERMISSION,
                )
            }
        }
        sources = sourceStore.add(picked.map { it.toString() })
        renderThumbnails()
        selectMain(picked.first().toString())
    }

    private fun handleLaunchIntent(intent: Intent?) {
        if (intent == null) return
        val uri = when (intent.action) {
            Intent.ACTION_VIEW -> intent.data
            Intent.ACTION_SEND -> sharedImageUri(intent)
            else -> null
        } ?: return
        sources = sourceStore.add(listOf(uri.toString()))
        renderThumbnails()
        selectMain(uri.toString())
    }

    @Suppress("DEPRECATION")
    private fun sharedImageUri(intent: Intent): Uri? =
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.TIRAMISU) {
            intent.getParcelableExtra(Intent.EXTRA_STREAM, Uri::class.java)
        } else {
            intent.getParcelableExtra<Uri>(Intent.EXTRA_STREAM)
        }

    private fun renderThumbnails() {
        thumbnailGrid.removeAllViews()
        val hasSources = sources.isNotEmpty()
        thumbnailScroll.visibility = if (hasSources) View.VISIBLE else View.GONE
        emptyPlaceholder.visibility = if (hasSources) View.GONE else View.VISIBLE
        if (!hasSources) return

        val tileSize = dp(56)
        val margin = dp(4)
        sources.forEach { source ->
            val frame = FrameLayout(this)
            frame.layoutParams = GridLayout.LayoutParams().apply {
                width = tileSize
                height = tileSize
                setMargins(margin, margin, margin, margin)
            }
            frame.background = roundedBackground(
                fillColor = getColor(R.color.surface),
                strokeColor = getColor(
                    if (source.uri == mainUri) R.color.selected_outline else R.color.line,
                ),
                radiusDp = 10,
            )
            val image = ImageView(this)
            image.layoutParams = FrameLayout.LayoutParams(
                FrameLayout.LayoutParams.MATCH_PARENT,
                FrameLayout.LayoutParams.MATCH_PARENT,
            ).apply { setMargins(dp(3), dp(3), dp(3), dp(3)) }
            image.scaleType = ImageView.ScaleType.CENTER_CROP
            frame.addView(image)
            frame.setOnClickListener { selectMain(source.uri) }
            thumbnailGrid.addView(frame)
            loadThumbnail(source.uri, image)
        }

        val addTile = TextView(this)
        addTile.layoutParams = GridLayout.LayoutParams().apply {
            width = tileSize
            height = tileSize
            setMargins(margin, margin, margin, margin)
        }
        addTile.text = "+"
        addTile.gravity = Gravity.CENTER
        addTile.setTextColor(getColor(R.color.accent))
        addTile.textSize = 22f
        addTile.background = roundedBackground(getColor(R.color.chip), radiusDp = 10)
        addTile.contentDescription = getString(R.string.add_image)
        addTile.setOnClickListener { pickImages() }
        thumbnailGrid.addView(addTile)
    }

    private fun loadThumbnail(uriString: String, target: ImageView) {
        target.tag = uriString
        executor.execute {
            val bitmap = runCatching {
                Thumbnails.decode(contentResolver, Uri.parse(uriString), THUMBNAIL_DIMENSION)
            }.getOrNull()
            handler.post {
                if (target.tag == uriString && bitmap != null) target.setImageBitmap(bitmap)
            }
        }
    }

    private fun selectMain(uriString: String) {
        if (busy) return
        mainUri = uriString
        renderThumbnails()
        setStatus(getString(R.string.loading_image))
        executor.execute {
            val loaded = runCatching {
                ImageLoader.load(this, Uri.parse(uriString), PREVIEW_MAX_DIMENSION)
            }
            handler.post {
                if (isFinishing || isDestroyed) {
                    loaded.getOrNull()?.recycle()
                    return@post
                }
                loaded.onSuccess { bitmap ->
                    showMain(bitmap)
                    setStatus("")
                }.onFailure { error ->
                    showMain(null)
                    setStatus(getString(R.string.load_failed, error.readableMessage()))
                }
            }
        }
    }

    private fun showMain(bitmap: Bitmap?) {
        editor.setImage(null)
        mainBitmap?.recycle()
        mainBitmap = bitmap
        editor.setImage(bitmap)
        updateSelectionUi()
    }

    // --- Mode, grid, dan seleksi ---------------------------------------------------------

    private fun setMode(newMode: Mode) {
        mode = newMode
        val selecting = newMode == Mode.SELECT
        gridControls.visibility = if (selecting) View.GONE else View.VISIBLE
        selectPanel.visibility = if (selecting) View.VISIBLE else View.GONE
        editor.selectionMode = selecting

        modeGridButton.backgroundTintList =
            ColorStateList.valueOf(getColor(if (selecting) R.color.chip else R.color.accent))
        modeGridButton.setTextColor(
            getColor(if (selecting) R.color.ink else android.R.color.white),
        )
        modeSelectButton.backgroundTintList =
            ColorStateList.valueOf(getColor(if (selecting) R.color.accent else R.color.chip))
        modeSelectButton.setTextColor(
            getColor(if (selecting) android.R.color.white else R.color.ink),
        )
        updateSelectionUi()
    }

    private fun adjustGrid(columnsDelta: Int = 0, rowsDelta: Int = 0) {
        val newColumns = (editor.columns + columnsDelta).coerceIn(MIN_GRID, MAX_GRID)
        val newRows = (editor.rows + rowsDelta).coerceIn(MIN_GRID, MAX_GRID)
        if (newColumns != editor.columns) editor.columns = newColumns
        if (newRows != editor.rows) editor.rows = newRows
        updateGridLabels()
        updateSelectionUi()
    }

    private fun updateGridLabels() {
        columnsValue.text = editor.columns.toString()
        rowsValue.text = editor.rows.toString()
    }

    private fun updateSelectionUi() {
        val count = editor.selectedCount
        saveSelectedButton.text = getString(R.string.save_selected_count, count)
        saveSelectedButton.isEnabled = !busy && mode == Mode.SELECT && count > 0
        saveAllButton.isEnabled = !busy && mainBitmap != null
        clearSelectionButton.isEnabled = !busy && count > 0
        selectAllButton.isEnabled = !busy && mainBitmap != null
        if (mode == Mode.SELECT && count > 0) setStatus(getString(R.string.selected_count, count))
    }

    private fun savePieces(onlySelected: Boolean) {
        val bitmap = mainBitmap
        if (bitmap == null) {
            setStatus(getString(R.string.pick_first))
            return
        }
        if (busy) return

        val columns = editor.columns
        val rows = editor.rows
        val indexes: Set<Int> =
            if (onlySelected) editor.selectedTiles else (0 until columns * rows).toSet()
        if (indexes.isEmpty()) {
            setStatus(getString(R.string.selection_empty))
            return
        }

        val settingsSnapshot = settings
        val sourceLabel = mainUri?.let { Uri.parse(it).lastPathSegment }
            ?: settingsSnapshot.projectName

        setBusy(true, getString(R.string.saving_pieces))
        executor.execute {
            val tiles = GridSlicer.tileBounds(bitmap.width, bitmap.height, columns, rows)
            var saved = 0
            indexes.sorted().forEach { index ->
                val tile = tiles.getOrNull(index) ?: return@forEach
                if (tile.isEmpty) return@forEach
                if (pieceStore.save(bitmap, tile, settingsSnapshot, sourceLabel) != null) saved++
            }
            handler.post {
                if (isFinishing || isDestroyed) return@post
                setBusy(false, null)
                editor.clearSelection()
                setStatus(
                    if (saved > 0) {
                        getString(R.string.saved_pieces, saved)
                    } else {
                        getString(R.string.unpickable_tile)
                    },
                )
            }
        }
    }

    // --- Bantu ---------------------------------------------------------------------------

    private fun setBusy(value: Boolean, message: String?) {
        busy = value
        modeGridButton.isEnabled = !value
        modeSelectButton.isEnabled = !value
        columnsMinus.isEnabled = !value
        columnsPlus.isEnabled = !value
        rowsMinus.isEnabled = !value
        rowsPlus.isEnabled = !value
        selectAllButton.isEnabled = !value && mainBitmap != null
        clearSelectionButton.isEnabled = !value && editor.selectedCount > 0
        saveSelectedButton.isEnabled = !value && mode == Mode.SELECT && editor.selectedCount > 0
        saveAllButton.isEnabled = !value && mainBitmap != null
        if (message != null) setStatus(message)
    }

    private fun setStatus(message: String) {
        statusText.text = message
    }

    private fun navigate(target: Class<*>) {
        startActivity(Intent(this, target).addFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT))
    }

    private fun updateNavHighlight(index: Int) {
        val buttons = listOf(navHome, navGallery, navSettings)
        buttons.forEachIndexed { position, button ->
            val active = position == index
            button.setTextColor(getColor(if (active) R.color.accent else R.color.ink_muted))
            button.typeface = if (active) Typeface.DEFAULT_BOLD else Typeface.DEFAULT
        }
    }

    private fun Throwable.readableMessage(): String =
        message?.takeIf { it.isNotBlank() } ?: javaClass.simpleName

    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        outState.putString(STATE_MAIN_URI, mainUri)
        outState.putInt(STATE_COLUMNS, editor.columns)
        outState.putInt(STATE_ROWS, editor.rows)
    }

    override fun onDestroy() {
        handler.removeCallbacksAndMessages(null)
        executor.shutdownNow()
        editor.setImage(null)
        mainBitmap?.recycle()
        mainBitmap = null
        super.onDestroy()
    }

    private companion object {
        const val REQUEST_PICK_IMAGES = 1001
        const val PREVIEW_MAX_DIMENSION = 3072
        const val THUMBNAIL_DIMENSION = 256
        const val STATE_MAIN_URI = "state_main_uri"
        const val STATE_COLUMNS = "state_columns"
        const val STATE_ROWS = "state_rows"
    }
}
