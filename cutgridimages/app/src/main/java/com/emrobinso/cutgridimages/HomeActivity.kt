package com.emrobinso.cutgridimages

import android.app.Activity
import android.app.AlertDialog
import android.content.Intent
import android.content.res.ColorStateList
import android.graphics.Bitmap
import android.graphics.Typeface
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.provider.MediaStore
import android.view.Gravity
import android.view.View
import android.widget.Button
import android.widget.FrameLayout
import android.widget.GridLayout
import android.widget.ImageButton
import android.widget.ImageView
import android.widget.ScrollView
import android.widget.TextView
import com.emrobinso.cutgridimages.data.AppSettings
import com.emrobinso.cutgridimages.data.ImageSourceStore
import com.emrobinso.cutgridimages.data.PieceStore
import com.emrobinso.cutgridimages.data.SettingsStore
import com.emrobinso.cutgridimages.data.SourceImage
import com.emrobinso.cutgridimages.grid.ContentGridDetector
import com.emrobinso.cutgridimages.grid.MAX_GRID
import com.emrobinso.cutgridimages.grid.MIN_GRID
import com.emrobinso.cutgridimages.image.ImageLoader
import com.emrobinso.cutgridimages.image.SourceCache
import com.emrobinso.cutgridimages.image.Thumbnails
import com.emrobinso.cutgridimages.ui.GridEditorView
import com.emrobinso.cutgridimages.ui.dp
import com.emrobinso.cutgridimages.ui.roundedBackground
import java.io.File
import java.util.concurrent.Executors

/**
 * Beranda: input gambar dari galeri, strip 5 kolom yang bisa di-scroll, gambar utama dengan
 * grid yang bisa digeser, tombol pindah gambar, dan mode seleksi untuk menyimpan potongan.
 *
 * Bitmap yang sudah dibaca disimpan di cache memori supaya pindah gambar terasa instan, dan
 * setiap gambar juga disalin ke penyimpanan aplikasi agar tidak bergantung izin URI penyedia.
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
    private lateinit var resetGridButton: Button
    private lateinit var autoGridButton: Button
    private lateinit var selectAllButton: Button
    private lateinit var clearSelectionButton: Button
    private lateinit var saveSelectedButton: Button
    private lateinit var saveAllButton: Button
    private lateinit var statusText: TextView
    private lateinit var navHome: Button
    private lateinit var navGallery: Button
    private lateinit var navSettings: Button
    private lateinit var prevImageButton: ImageButton
    private lateinit var nextImageButton: ImageButton
    private lateinit var imageCounter: TextView

    private lateinit var settingsStore: SettingsStore
    private lateinit var sourceStore: ImageSourceStore
    private lateinit var pieceStore: PieceStore

    private val executor = Executors.newSingleThreadExecutor()
    private val handler = Handler(Looper.getMainLooper())

    /** Bitmap pratinjau terakhir (paling banyak 2) agar pindah gambar tidak memuat ulang. */
    private val previewCache = object : LinkedHashMap<String, Bitmap>(2, 0.75f, true) {
        override fun removeEldestEntry(eldest: MutableMap.MutableEntry<String, Bitmap>?): Boolean =
            size > PREVIEW_CACHE_SIZE
    }

    /** Thumbnail hasil dekode, dipakai ulang saat strip digambar ulang. */
    private val thumbnailCache = HashMap<String, Bitmap>()

    /** Bingkai thumbnail per URI, supaya hanya sorotan yang diperbarui saat ganti gambar. */
    private val thumbnailFrames = HashMap<String, View>()

    private var settings = AppSettings()
    private var sources: List<SourceImage> = emptyList()
    private var mainUri: String? = null
    private var mainBitmap: Bitmap? = null
    private var busy = false
    private var loadToken = 0

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
        editor.clipToOutline = true
        editor.highlightColor = settings.highlightColor
        editor.columns = savedInstanceState?.getInt(STATE_COLUMNS) ?: 3
        editor.rows = savedInstanceState?.getInt(STATE_ROWS) ?: 3
        editor.onSelectionChanged = { updateSelectionUi() }
        editor.onGridChanged = { updateSelectionUi() }

        modeGridButton.setOnClickListener { setMode(Mode.GRID) }
        modeSelectButton.setOnClickListener { setMode(Mode.SELECT) }
        columnsMinus.setOnClickListener { adjustGrid(columnsDelta = -1) }
        columnsPlus.setOnClickListener { adjustGrid(columnsDelta = 1) }
        rowsMinus.setOnClickListener { adjustGrid(rowsDelta = -1) }
        rowsPlus.setOnClickListener { adjustGrid(rowsDelta = 1) }
        resetGridButton.setOnClickListener {
            editor.resetGrid()
            setStatus(getString(R.string.grid_reset))
        }
        autoGridButton.setOnClickListener { detectGrid() }
        selectAllButton.setOnClickListener { editor.selectAll() }
        clearSelectionButton.setOnClickListener { editor.clearSelection() }
        saveSelectedButton.setOnClickListener { savePieces(onlySelected = true) }
        saveAllButton.setOnClickListener { savePieces(onlySelected = false) }
        emptyPlaceholder.setOnClickListener { pickImages() }
        prevImageButton.setOnClickListener { stepImage(-1) }
        nextImageButton.setOnClickListener { stepImage(1) }
        navHome.setOnClickListener { updateNavHighlight(0) }
        navGallery.setOnClickListener { navigate(GalleryActivity::class.java) }
        navSettings.setOnClickListener { navigate(SettingsActivity::class.java) }

        sources = sourceStore.list()
        renderThumbnails()
        setMode(Mode.GRID)
        updateGridLabels()

        val restoredMain = savedInstanceState?.getString(STATE_MAIN_URI)
        val preferred = restoredMain?.let { uri -> sources.firstOrNull { it.uri == uri } }
            ?: sources.firstOrNull()
        when {
            handleLaunchIntent(intent) -> Unit
            preferred != null -> selectMain(preferred)
            else -> updateImageNav()
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
        resetGridButton = findViewById(R.id.resetGridButton)
        autoGridButton = findViewById(R.id.autoGridButton)
        selectAllButton = findViewById(R.id.selectAllButton)
        clearSelectionButton = findViewById(R.id.clearSelectionButton)
        saveSelectedButton = findViewById(R.id.saveSelectedButton)
        saveAllButton = findViewById(R.id.saveAllButton)
        statusText = findViewById(R.id.statusText)
        navHome = findViewById(R.id.navHome)
        navGallery = findViewById(R.id.navGallery)
        navSettings = findViewById(R.id.navSettings)
        prevImageButton = findViewById(R.id.prevImageButton)
        nextImageButton = findViewById(R.id.nextImageButton)
        imageCounter = findViewById(R.id.imageCounter)
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
                sources.firstOrNull()?.let { selectMain(it) }
            }
            renderThumbnails()
        }
        updateSelectionUi()
    }

    // --- Memilih gambar ------------------------------------------------------------------

    /**
     * Android 13+ memakai **photo picker** sistem (grid galeri, multi pilih, tanpa izin).
     * Versi lama memakai pemilih konten bergambar yang biasanya diarahkan ke aplikasi galeri,
     * dan pemilih dokumen hanya dipakai sebagai jalan terakhir.
     */
    @Suppress("DEPRECATION")
    private fun pickImages() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            val picker = Intent(MediaStore.ACTION_PICK_IMAGES).apply {
                type = "image/*"
                putExtra(MediaStore.EXTRA_PICK_IMAGES_MAX, PICK_LIMIT)
            }
            if (picker.resolveActivity(packageManager) != null) {
                startActivityForResult(picker, REQUEST_PICK_IMAGES)
                return
            }
        }

        val contentPicker = Intent(Intent.ACTION_GET_CONTENT).apply {
            addCategory(Intent.CATEGORY_OPENABLE)
            type = "image/*"
            putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true)
        }
        if (contentPicker.resolveActivity(packageManager) != null) {
            startActivityForResult(contentPicker, REQUEST_PICK_IMAGES)
            return
        }

        val galleryPicker = Intent(Intent.ACTION_PICK, MediaStore.Images.Media.EXTERNAL_CONTENT_URI).apply {
            type = "image/*"
        }
        if (galleryPicker.resolveActivity(packageManager) != null) {
            startActivityForResult(galleryPicker, REQUEST_PICK_IMAGES)
            return
        }

        val documents = Intent(Intent.ACTION_OPEN_DOCUMENT).apply {
            addCategory(Intent.CATEGORY_OPENABLE)
            type = "image/*"
            putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true)
            addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
        }
        startActivityForResult(documents, REQUEST_PICK_IMAGES)
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

        val firstUri = picked.first().toString()
        sources.firstOrNull { it.uri == firstUri }?.let { selectMain(it) }
    }

    private fun handleLaunchIntent(intent: Intent?): Boolean {
        if (intent == null) return false
        val uri = when (intent.action) {
            Intent.ACTION_VIEW -> intent.data
            Intent.ACTION_SEND -> sharedImageUri(intent)
            else -> null
        } ?: return false
        val uriString = uri.toString()
        sources = sourceStore.add(listOf(uriString))
        renderThumbnails()
        sources.firstOrNull { it.uri == uriString }?.let { selectMain(it) }
        return true
    }

    override fun onNewIntent(intent: Intent?) {
        super.onNewIntent(intent)
        setIntent(intent)
        if (busy) return
        handleLaunchIntent(intent)
    }

    @Suppress("DEPRECATION")
    private fun sharedImageUri(intent: Intent): Uri? =
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            intent.getParcelableExtra(Intent.EXTRA_STREAM, Uri::class.java)
        } else {
            intent.getParcelableExtra<Uri>(Intent.EXTRA_STREAM)
        }

    // --- Strip thumbnail -----------------------------------------------------------------

    private fun renderThumbnails() {
        thumbnailGrid.removeAllViews()
        thumbnailFrames.clear()
        val hasSources = sources.isNotEmpty()
        thumbnailScroll.visibility = if (hasSources) View.VISIBLE else View.GONE
        emptyPlaceholder.visibility = if (hasSources) View.GONE else View.VISIBLE
        if (!hasSources) {
            updateImageNav()
            return
        }

        val tileSize = dp(56)
        val margin = dp(4)
        sources.forEach { source ->
            val frame = FrameLayout(this)
            frame.layoutParams = GridLayout.LayoutParams().apply {
                width = tileSize
                height = tileSize
                setMargins(margin, margin, margin, margin)
            }
            val image = ImageView(this)
            image.layoutParams = FrameLayout.LayoutParams(
                FrameLayout.LayoutParams.MATCH_PARENT,
                FrameLayout.LayoutParams.MATCH_PARENT,
            ).apply { setMargins(dp(3), dp(3), dp(3), dp(3)) }
            image.scaleType = ImageView.ScaleType.CENTER_CROP
            frame.addView(image)
            frame.setOnClickListener { selectMain(source) }
            frame.setOnLongClickListener {
                confirmRemoveSource(source)
                true
            }
            thumbnailGrid.addView(frame)
            thumbnailFrames[source.uri] = frame
            loadThumbnail(source, image)
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
        addTile.background = roundedBackground(getColor(R.color.chip), radiusDp = 14)
        addTile.contentDescription = getString(R.string.add_image)
        addTile.setOnClickListener { pickImages() }
        thumbnailGrid.addView(addTile)

        updateThumbnailSelection()
        updateImageNav()
    }

    private fun loadThumbnail(source: SourceImage, target: ImageView) {
        val uriString = source.uri
        target.tag = uriString
        val ready = thumbnailCache[uriString]
        if (ready != null && !ready.isRecycled) {
            target.setImageBitmap(ready)
            return
        }
        val cachedFile = source.cachedPath?.let { File(it) }?.takeIf { it.isFile }
        executor.execute {
            val bitmap = if (cachedFile != null) {
                Thumbnails.decodeFile(cachedFile, THUMBNAIL_DIMENSION)
            } else {
                runCatching {
                    Thumbnails.decode(contentResolver, Uri.parse(uriString), THUMBNAIL_DIMENSION)
                }.getOrNull()
            }
            handler.post {
                if (bitmap == null || isFinishing || isDestroyed) return@post
                if (thumbnailCache.size > THUMBNAIL_CACHE_LIMIT) thumbnailCache.clear()
                thumbnailCache[uriString] = bitmap
                if (target.tag == uriString) target.setImageBitmap(bitmap)
            }
        }
    }

    /** Hanya menyorot ulang bingkai terpilih; strip tidak dibangun ulang. */
    private fun updateThumbnailSelection() {
        thumbnailFrames.forEach { (uri, frame) ->
            frame.background = roundedBackground(
                fillColor = getColor(R.color.surface),
                strokeColor = getColor(
                    if (uri == mainUri) R.color.selected_outline else R.color.line,
                ),
                radiusDp = 14,
            )
        }
    }

    // --- Gambar utama --------------------------------------------------------------------

    private fun selectMain(source: SourceImage) {
        if (busy) return
        mainUri = source.uri
        updateThumbnailSelection()
        updateImageNav()

        val cachedBitmap = previewCache[source.uri]
        if (cachedBitmap != null && !cachedBitmap.isRecycled) {
            showMain(cachedBitmap)
            setStatus("")
            return
        }

        // Tampilkan thumbnail lebih dulu supaya perpindahan terasa instan,
        // lalu ganti dengan resolusi penuh ketika selesai dibaca.
        thumbnailCache[source.uri]?.takeIf { !it.isRecycled }?.let { showMain(it) }
        setStatus(getString(R.string.loading_image))

        val token = ++loadToken
        executor.execute {
            val loaded = runCatching { loadSourceBitmap(source) }
            handler.post {
                if (isFinishing || isDestroyed || token != loadToken) return@post
                loaded.onSuccess { bitmap ->
                    previewCache[source.uri] = bitmap
                    showMain(bitmap)
                    setStatus("")
                }.onFailure { error ->
                    if (mainBitmap == null) showMain(null)
                    setStatus(getString(R.string.load_failed_hint, error.readableMessage()))
                }
            }
        }
    }

    /**
     * Memuat gambar utama: pakai salinan lokal bila ada, jika tidak baca dari URI lalu
     * simpan salinannya supaya pemuatan berikutnya tidak bergantung pada izin penyedia.
     */
    private fun loadSourceBitmap(source: SourceImage): Bitmap {
        val cached = source.cachedPath?.let { File(it) }?.takeIf { it.isFile }
        if (cached != null) {
            val fromCache = runCatching { ImageLoader.loadFile(cached, PREVIEW_MAX_DIMENSION) }
            if (fromCache.isSuccess) return fromCache.getOrThrow()
            runCatching { cached.delete() }
        }

        val bitmap = ImageLoader.load(this, Uri.parse(source.uri), PREVIEW_MAX_DIMENSION)
        val file = SourceCache.write(this, source.uri, bitmap)
        if (file != null) {
            val updated = sourceStore.setCached(source.uri, file.absolutePath)
            handler.post {
                if (!isFinishing && !isDestroyed) sources = updated
            }
        }
        return bitmap
    }

    private fun showMain(bitmap: Bitmap?) {
        if (bitmap === mainBitmap) {
            updateSelectionUi()
            return
        }
        mainBitmap = bitmap
        editor.setImage(bitmap)
        editor.setDetectedCells(null)
        updateSelectionUi()
    }

    /**
     * Menjalankan deteksi kotak isi pada gambar utama (dipakai untuk lembar logo berlatar polos).
     * Gambar dikecilkan lebih dulu supaya pemindaian piksel tetap ringan.
     */
    private fun detectGrid() {
        val bitmap = mainBitmap
        if (bitmap == null) {
            setStatus(getString(R.string.pick_first))
            return
        }
        if (busy) return
        val expectedColumns = editor.columns
        val expectedRows = editor.rows
        setStatus(getString(R.string.auto_grid_running))

        executor.execute {
            val detected = runCatching {
                val longest = maxOf(bitmap.width, bitmap.height)
                val scale = (DETECTION_MAX_DIMENSION / longest).coerceAtMost(1f)
                val width = (bitmap.width * scale).toInt().coerceAtLeast(1)
                val height = (bitmap.height * scale).toInt().coerceAtLeast(1)
                val scaled = Bitmap.createScaledBitmap(bitmap, width, height, true)
                val pixels = IntArray(width * height)
                scaled.getPixels(pixels, 0, width, 0, 0, width, height)
                if (scaled !== bitmap) scaled.recycle()
                ContentGridDetector.detect(
                    pixels = pixels,
                    width = width,
                    height = height,
                    expectedColumns = expectedColumns,
                    expectedRows = expectedRows,
                )
            }.getOrNull()

            handler.post {
                if (isFinishing || isDestroyed) return@post
                if (detected == null || detected.cells.size < 2) {
                    setStatus(getString(R.string.auto_grid_failed))
                    return@post
                }
                editor.setDetectedCells(detected.cells)
                setStatus(getString(R.string.auto_grid_done, detected.cells.size))
            }
        }
    }

    private fun confirmRemoveSource(source: SourceImage) {
        AlertDialog.Builder(this)
            .setTitle(R.string.remove_source_title)
            .setMessage(R.string.remove_source_message)
            .setPositiveButton(R.string.delete) { _, _ -> removeSource(source) }
            .setNegativeButton(R.string.cancel, null)
            .show()
    }

    private fun removeSource(source: SourceImage) {
        SourceCache.delete(this, source.uri)
        previewCache.remove(source.uri)?.let { if (it !== mainBitmap) it.recycle() }
        thumbnailCache.remove(source.uri)
        sources = sourceStore.remove(source.uri)
        if (mainUri == source.uri) {
            mainUri = null
            showMain(null)
            sources.firstOrNull()?.let { selectMain(it) }
        }
        renderThumbnails()
        setStatus(getString(R.string.source_removed))
    }

    // --- Pindah gambar dalam koleksi -----------------------------------------------------

    /** Memperbarui tombol prev/next dan penunjuk posisi `2 / 5`. */
    private fun updateImageNav() {
        val total = sources.size
        val index = sources.indexOfFirst { it.uri == mainUri }
        val canStep = total > 1 && index >= 0 && !busy
        listOf(prevImageButton, nextImageButton).forEach { button ->
            button.isEnabled = canStep
            button.alpha = if (canStep) 1f else 0.35f
        }
        if (index >= 0) {
            imageCounter.text = getString(R.string.image_counter, index + 1, total)
            imageCounter.visibility = View.VISIBLE
        } else {
            imageCounter.visibility = View.GONE
        }
    }

    /** Pindah ke gambar sebelum/berikutnya dalam urutan koleksi (memutar di ujung). */
    private fun stepImage(delta: Int) {
        if (sources.size < 2 || busy) return
        val current = sources.indexOfFirst { it.uri == mainUri }
        val base = if (current >= 0) current else 0
        val target = ((base + delta) % sources.size + sources.size) % sources.size
        selectMain(sources[target])
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
            getColor(if (selecting) R.color.ink else R.color.surface),
        )
        modeSelectButton.backgroundTintList =
            ColorStateList.valueOf(getColor(if (selecting) R.color.accent else R.color.chip))
        modeSelectButton.setTextColor(
            getColor(if (selecting) R.color.surface else R.color.ink),
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
        updateImageNav()
    }

    private fun savePieces(onlySelected: Boolean) {
        val bitmap = mainBitmap
        if (bitmap == null) {
            setStatus(getString(R.string.pick_first))
            return
        }
        if (busy) return

        val tiles = editor.currentTiles()
        if (tiles.isEmpty()) {
            setStatus(getString(R.string.pick_first))
            return
        }
        val indexes: Set<Int> =
            if (onlySelected) {
                editor.selectedTiles
            } else {
                tiles.filterNot { it.isEmpty }.mapTo(LinkedHashSet()) { it.index }
            }
        if (indexes.isEmpty()) {
            setStatus(getString(R.string.selection_empty))
            return
        }

        val settingsSnapshot = settings
        val sourceLabel = mainUri?.let { Uri.parse(it).lastPathSegment }
            ?: settingsSnapshot.projectName

        setBusy(true, getString(R.string.saving_pieces))
        executor.execute {
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
        resetGridButton.isEnabled = !value
        autoGridButton.isEnabled = !value
        selectAllButton.isEnabled = !value && mainBitmap != null
        clearSelectionButton.isEnabled = !value && editor.selectedCount > 0
        saveSelectedButton.isEnabled = !value && mode == Mode.SELECT && editor.selectedCount > 0
        saveAllButton.isEnabled = !value && mainBitmap != null
        updateImageNav()
        if (message != null) setStatus(message)
    }

    private fun setStatus(message: String) {
        statusText.text = message
    }

    /** Pindah tab tanpa terasa seperti membuka halaman baru, dan tanpa menumpuk back stack. */
    private fun navigate(target: Class<*>) {
        startActivity(
            Intent(this, target).addFlags(
                Intent.FLAG_ACTIVITY_REORDER_TO_FRONT or Intent.FLAG_ACTIVITY_NO_ANIMATION,
            ),
        )
        @Suppress("DEPRECATION")
        overridePendingTransition(0, 0)
        finish()
    }

    private fun updateNavHighlight(index: Int) {
        val buttons = listOf(navHome, navGallery, navSettings)
        buttons.forEachIndexed { position, button ->
            val active = position == index
            button.backgroundTintList = ColorStateList.valueOf(
                if (active) getColor(R.color.accent) else android.graphics.Color.TRANSPARENT,
            )
            button.setTextColor(getColor(if (active) R.color.surface else R.color.ink_muted))
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
        mainBitmap = null
        previewCache.values.forEach { runCatching { it.recycle() } }
        previewCache.clear()
        thumbnailCache.values.forEach { runCatching { it.recycle() } }
        thumbnailCache.clear()
        thumbnailFrames.clear()
        super.onDestroy()
    }

    private companion object {
        const val REQUEST_PICK_IMAGES = 1001
        const val PREVIEW_MAX_DIMENSION = 2560
        const val THUMBNAIL_DIMENSION = 256
        const val PREVIEW_CACHE_SIZE = 2
        const val THUMBNAIL_CACHE_LIMIT = 80
        const val PICK_LIMIT = 20
        const val DETECTION_MAX_DIMENSION = 640f
        const val STATE_MAIN_URI = "state_main_uri"
        const val STATE_COLUMNS = "state_columns"
        const val STATE_ROWS = "state_rows"
    }
}
