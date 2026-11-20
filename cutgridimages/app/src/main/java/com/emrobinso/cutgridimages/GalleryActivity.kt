package com.emrobinso.cutgridimages

import android.Manifest
import android.app.Activity
import android.app.AlertDialog
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.graphics.Typeface
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.text.TextUtils
import android.view.Gravity
import android.view.View
import android.widget.Button
import android.widget.GridLayout
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import com.emrobinso.cutgridimages.data.Piece
import com.emrobinso.cutgridimages.data.PieceStore
import com.emrobinso.cutgridimages.image.PieceExporter
import com.emrobinso.cutgridimages.image.Thumbnails
import com.emrobinso.cutgridimages.ui.dp
import com.emrobinso.cutgridimages.ui.roundedBackground
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.concurrent.Executors
import kotlin.math.ceil
import kotlin.math.max

/** Galeri potongan: mode list/grid 3/grid 5, paginasi, multi seleksi hapus, dan simpan ke galeri perangkat. */
class GalleryActivity : Activity() {

    private enum class ViewMode(val columns: Int, val pageSize: Int) {
        LIST(1, 10),
        GRID3(3, 9),
        GRID5(5, 15),
    }

    private lateinit var galleryCount: TextView
    private lateinit var viewListButton: Button
    private lateinit var viewGrid3Button: Button
    private lateinit var viewGrid5Button: Button
    private lateinit var selectToggleButton: Button
    private lateinit var galleryGrid: GridLayout
    private lateinit var galleryScroll: ScrollView
    private lateinit var galleryEmpty: View
    private lateinit var prevPageButton: Button
    private lateinit var nextPageButton: Button
    private lateinit var pageInfoText: TextView
    private lateinit var selectionPanel: View
    private lateinit var cancelSelectionButton: Button
    private lateinit var deleteSelectedButton: Button
    private lateinit var exportSelectedButton: Button
    private lateinit var exportAllButton: Button
    private lateinit var galleryStatus: TextView
    private lateinit var navHome: Button
    private lateinit var navGallery: Button
    private lateinit var navSettings: Button

    private lateinit var store: PieceStore
    private val executor = Executors.newSingleThreadExecutor()
    private val handler = Handler(Looper.getMainLooper())
    private val thumbnailCache = HashMap<String, Bitmap>()
    private val dateFormat = SimpleDateFormat("dd/MM/yyyy HH:mm", Locale.getDefault())

    private var pieces: List<Piece> = emptyList()
    private var mode = ViewMode.LIST
    private var page = 0
    private var selectionMode = false
    private var busy = false
    private val selected = LinkedHashSet<String>()
    private var pendingExport: List<Piece>? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_gallery)
        store = PieceStore(this)
        bindViews()

        viewListButton.setOnClickListener { changeMode(ViewMode.LIST) }
        viewGrid3Button.setOnClickListener { changeMode(ViewMode.GRID3) }
        viewGrid5Button.setOnClickListener { changeMode(ViewMode.GRID5) }
        selectToggleButton.setOnClickListener {
            selectionMode = !selectionMode
            if (!selectionMode) selected.clear()
            render()
        }
        prevPageButton.setOnClickListener {
            if (page > 0) {
                page--
                render()
            }
        }
        nextPageButton.setOnClickListener {
            page++
            render()
        }
        cancelSelectionButton.setOnClickListener {
            selected.clear()
            selectionMode = false
            render()
        }
        deleteSelectedButton.setOnClickListener { confirmDelete() }
        exportSelectedButton.setOnClickListener { exportPieces(onlySelected = true) }
        exportAllButton.setOnClickListener { exportPieces(onlySelected = false) }
        navHome.setOnClickListener { navigate(HomeActivity::class.java) }
        navGallery.setOnClickListener { updateNavHighlight(1) }
        navSettings.setOnClickListener { navigate(SettingsActivity::class.java) }
    }

    private fun bindViews() {
        galleryCount = findViewById(R.id.galleryCount)
        viewListButton = findViewById(R.id.viewListButton)
        viewGrid3Button = findViewById(R.id.viewGrid3Button)
        viewGrid5Button = findViewById(R.id.viewGrid5Button)
        selectToggleButton = findViewById(R.id.selectToggleButton)
        galleryGrid = findViewById(R.id.galleryGrid)
        galleryScroll = findViewById(R.id.galleryScroll)
        galleryEmpty = findViewById(R.id.galleryEmpty)
        prevPageButton = findViewById(R.id.prevPageButton)
        nextPageButton = findViewById(R.id.nextPageButton)
        pageInfoText = findViewById(R.id.pageInfoText)
        selectionPanel = findViewById(R.id.selectionPanel)
        cancelSelectionButton = findViewById(R.id.cancelSelectionButton)
        deleteSelectedButton = findViewById(R.id.deleteSelectedButton)
        exportSelectedButton = findViewById(R.id.exportSelectedButton)
        exportAllButton = findViewById(R.id.exportAllButton)
        galleryStatus = findViewById(R.id.galleryStatus)
        navHome = findViewById(R.id.navHome)
        navGallery = findViewById(R.id.navGallery)
        navSettings = findViewById(R.id.navSettings)
    }

    override fun onResume() {
        super.onResume()
        updateNavHighlight(1)
        reloadPieces()
    }

    private fun reloadPieces() {
        pieces = store.load().pieces
        selected.retainAll(pieces.mapTo(HashSet()) { it.id })
        if (pieces.isEmpty()) selectionMode = false
        render()
    }

    private fun changeMode(newMode: ViewMode) {
        if (mode == newMode) return
        mode = newMode
        page = 0
        render()
    }

    private fun render() {
        galleryCount.text = getString(R.string.gallery_count, pieces.size)
        galleryEmpty.visibility = if (pieces.isEmpty()) View.VISIBLE else View.GONE
        galleryScroll.visibility = if (pieces.isEmpty()) View.GONE else View.VISIBLE

        val pageCount = max(1, ceil(pieces.size / mode.pageSize.toDouble()).toInt())
        page = page.coerceIn(0, pageCount - 1)
        val start = page * mode.pageSize
        val pageItems = pieces.drop(start).take(mode.pageSize)

        galleryGrid.removeAllViews()
        galleryGrid.columnCount = mode.columns
        val itemWidth = itemWidth()
        pageItems.forEach { piece -> galleryGrid.addView(buildItem(piece, itemWidth)) }

        pageInfoText.text = getString(R.string.page_info, page + 1, pageCount)
        prevPageButton.isEnabled = page > 0
        nextPageButton.isEnabled = page < pageCount - 1

        selectionPanel.visibility = if (selectionMode) View.VISIBLE else View.GONE
        selectToggleButton.text = getString(if (selectionMode) R.string.cancel else R.string.select_mode)
        selectToggleButton.backgroundTintList = android.content.res.ColorStateList.valueOf(
            getColor(if (selectionMode) R.color.accent else R.color.chip),
        )
        selectToggleButton.setTextColor(
            getColor(if (selectionMode) android.R.color.white else R.color.ink),
        )
        deleteSelectedButton.text = getString(R.string.delete_selected, selected.size)
        deleteSelectedButton.isEnabled = !busy && selected.isNotEmpty()
        cancelSelectionButton.isEnabled = !busy
        exportSelectedButton.text = getString(R.string.export_selected, selected.size)
        exportSelectedButton.isEnabled = !busy && selected.isNotEmpty()
        exportAllButton.isEnabled = !busy && pieces.isNotEmpty()
        highlightModeButtons()
        if (selectionMode && selected.isEmpty()) {
            galleryStatus.text = getString(R.string.selection_mode_hint)
        }
    }

    private fun highlightModeButtons() {
        val buttons = mapOf(
            viewListButton to ViewMode.LIST,
            viewGrid3Button to ViewMode.GRID3,
            viewGrid5Button to ViewMode.GRID5,
        )
        buttons.forEach { (button, candidate) ->
            val active = candidate == mode
            button.backgroundTintList = android.content.res.ColorStateList.valueOf(
                getColor(if (active) R.color.accent else R.color.chip),
            )
            button.setTextColor(getColor(if (active) android.R.color.white else R.color.ink))
        }
    }

    private fun itemWidth(): Int {
        val available = resources.displayMetrics.widthPixels - dp(32)
        val spacing = dp(6) * (mode.columns - 1)
        return ((available - spacing) / mode.columns).coerceAtLeast(dp(48))
    }

    private fun buildItem(piece: Piece, widthPx: Int): View {
        val isSelected = piece.id in selected
        val strokeColor = getColor(if (isSelected) R.color.selected_outline else R.color.line)
        return if (mode == ViewMode.LIST) {
            buildListItem(piece, widthPx, strokeColor)
        } else {
            buildGridItem(piece, widthPx, strokeColor)
        }
    }

    private fun buildListItem(piece: Piece, widthPx: Int, strokeColor: Int): View {
        val row = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
            setPadding(dp(8), dp(8), dp(8), dp(8))
            background = roundedBackground(getColor(R.color.surface), strokeColor, 10)
        }
        row.layoutParams = GridLayout.LayoutParams().apply {
            width = widthPx
            height = GridLayout.LayoutParams.WRAP_CONTENT
            setMargins(dp(3), dp(3), dp(3), dp(3))
        }

        val thumb = ImageView(this)
        thumb.scaleType = ImageView.ScaleType.CENTER_CROP
        row.addView(thumb, LinearLayout.LayoutParams(dp(52), dp(52)))
        thumbnailFor(piece, thumb)

        val texts = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(10), 0, 0, 0)
        }
        val name = TextView(this).apply {
            text = "${piece.displayName}.png"
            textSize = 13f
            setTextColor(getColor(R.color.ink))
            typeface = Typeface.DEFAULT_BOLD
        }
        val meta = TextView(this).apply {
            text = "${piece.project} · ${formatDate(piece.createdAt)}"
            textSize = 11f
            setTextColor(getColor(R.color.ink_muted))
        }
        texts.addView(name)
        texts.addView(meta)
        row.addView(texts, LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.WRAP_CONTENT, 1f))

        row.setOnClickListener { toggleSelection(piece) }
        row.setOnLongClickListener {
            if (!selectionMode) selectionMode = true
            selected.add(piece.id)
            render()
            true
        }
        return row
    }

    private fun buildGridItem(piece: Piece, widthPx: Int, strokeColor: Int): View {
        val column = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            background = roundedBackground(getColor(R.color.surface), strokeColor, 10)
            setPadding(dp(3), dp(3), dp(3), dp(4))
        }
        column.layoutParams = GridLayout.LayoutParams().apply {
            width = widthPx
            height = GridLayout.LayoutParams.WRAP_CONTENT
            setMargins(dp(3), dp(3), dp(3), dp(3))
        }

        val thumb = ImageView(this)
        thumb.scaleType = ImageView.ScaleType.CENTER_CROP
        val thumbHeight = (widthPx - dp(6)).coerceAtLeast(dp(40))
        column.addView(thumb, LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, thumbHeight))
        thumbnailFor(piece, thumb)

        val name = TextView(this).apply {
            text = "${piece.displayName}.png"
            textSize = 9f
            gravity = Gravity.CENTER
            maxLines = 1
            ellipsize = TextUtils.TruncateAt.END
            setTextColor(getColor(R.color.ink_muted))
            setPadding(0, dp(3), 0, 0)
        }
        column.addView(name)

        column.setOnClickListener { toggleSelection(piece) }
        column.setOnLongClickListener {
            if (!selectionMode) selectionMode = true
            selected.add(piece.id)
            render()
            true
        }
        return column
    }

    private fun thumbnailFor(piece: Piece, target: ImageView) {
        val cached = thumbnailCache[piece.id]
        if (cached != null && !cached.isRecycled) {
            target.setImageBitmap(cached)
            return
        }
        target.tag = piece.id
        executor.execute {
            val bitmap = Thumbnails.decodeFile(piece.file, 320)
            handler.post {
                if (target.tag == piece.id && bitmap != null) {
                    if (thumbnailCache.size > 80) thumbnailCache.clear()
                    thumbnailCache[piece.id] = bitmap
                    target.setImageBitmap(bitmap)
                }
            }
        }
    }

    private fun toggleSelection(piece: Piece) {
        if (busy) return
        if (!selectionMode) selectionMode = true
        if (!selected.add(piece.id)) selected.remove(piece.id)
        if (selected.isEmpty()) galleryStatus.text = ""
        render()
    }

    private fun confirmDelete() {
        if (selected.isEmpty()) return
        AlertDialog.Builder(this)
            .setTitle(R.string.delete_title)
            .setMessage(getString(R.string.delete_message, selected.size))
            .setPositiveButton(R.string.delete) { _, _ -> deleteSelected() }
            .setNegativeButton(R.string.cancel, null)
            .show()
    }

    private fun deleteSelected() {
        val targets = pieces.filter { it.id in selected }
        if (targets.isEmpty()) return
        setBusy(true, null)
        executor.execute {
            store.delete(targets)
            handler.post {
                if (isFinishing || isDestroyed) return@post
                selected.clear()
                selectionMode = false
                setBusy(false, null)
                reloadPieces()
                galleryStatus.text = getString(R.string.delete_done, targets.size)
            }
        }
    }

    private fun exportPieces(onlySelected: Boolean) {
        if (busy) return
        val targets = if (onlySelected) pieces.filter { it.id in selected } else pieces
        if (targets.isEmpty()) {
            galleryStatus.text = getString(R.string.export_empty)
            return
        }
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.Q &&
            checkSelfPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED
        ) {
            pendingExport = targets
            requestPermissions(arrayOf(Manifest.permission.WRITE_EXTERNAL_STORAGE), REQUEST_STORAGE)
            return
        }
        runExport(targets)
    }

    private fun runExport(targets: List<Piece>) {
        setBusy(true, getString(R.string.exporting))
        executor.execute {
            val result = runCatching { PieceExporter(this).export(targets) }
            handler.post {
                if (isFinishing || isDestroyed) return@post
                setBusy(false, null)
                result.onSuccess { summary ->
                    galleryStatus.text = getString(R.string.export_done, summary.saved, summary.location)
                }.onFailure { error ->
                    galleryStatus.text = getString(R.string.export_failed, error.readableMessage())
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
        if (requestCode != REQUEST_STORAGE) return
        val granted = grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED
        val targets = pendingExport
        pendingExport = null
        if (granted && targets != null) {
            runExport(targets)
        } else {
            galleryStatus.text = getString(R.string.permission_needed)
        }
    }

    private fun setBusy(value: Boolean, message: String?) {
        busy = value
        selectionPanel.isEnabled = !value
        selectToggleButton.isEnabled = !value
        viewListButton.isEnabled = !value
        viewGrid3Button.isEnabled = !value
        viewGrid5Button.isEnabled = !value
        exportAllButton.isEnabled = !value && pieces.isNotEmpty()
        exportSelectedButton.isEnabled = !value && selected.isNotEmpty()
        deleteSelectedButton.isEnabled = !value && selected.isNotEmpty()
        prevPageButton.isEnabled = !value && page > 0
        if (message != null) galleryStatus.text = message
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

    private fun formatDate(millis: Long): String = dateFormat.format(Date(millis))

    private fun Throwable.readableMessage(): String =
        message?.takeIf { it.isNotBlank() } ?: javaClass.simpleName

    override fun onDestroy() {
        handler.removeCallbacksAndMessages(null)
        executor.shutdownNow()
        thumbnailCache.clear()
        super.onDestroy()
    }

    private companion object {
        const val REQUEST_STORAGE = 2001
    }
}
