package com.emrobinso.cutgridimages.ui

import android.content.Context
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.RectF
import android.os.SystemClock
import android.util.AttributeSet
import android.util.TypedValue
import android.view.MotionEvent
import android.view.View
import com.emrobinso.cutgridimages.R
import com.emrobinso.cutgridimages.data.AppSettings
import com.emrobinso.cutgridimages.grid.FractionRect
import com.emrobinso.cutgridimages.grid.GridSlicer
import com.emrobinso.cutgridimages.grid.GridTile
import com.emrobinso.cutgridimages.grid.MAX_GRID
import com.emrobinso.cutgridimages.grid.MIN_GRID
import kotlin.math.abs
import kotlin.math.min

/**
 * Menampilkan gambar utama dengan pembagian grid presisi.
 *
 * Garis grid bisa **digeser**: garis kolom digeser horizontal, garis baris digeser vertikal,
 * sehingga potongan tidak harus simetris. Mode seleksi memakai ketukan pada petak untuk
 * menyalakan overlay semi transparan.
 */
class GridEditorView @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null,
    defStyleAttr: Int = 0,
) : View(context, attrs, defStyleAttr) {

    private val imageRect = RectF()
    private val bitmapPaint = Paint(Paint.FILTER_BITMAP_FLAG)
    private val fillPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply { style = Paint.Style.FILL }
    private val handlePaint = Paint(Paint.ANTI_ALIAS_FLAG).apply { style = Paint.Style.FILL }
    private val lineShadowPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        style = Paint.Style.STROKE
        strokeWidth = 3.5f * resources.displayMetrics.density
        color = Color.argb(90, 0, 0, 0)
    }
    private val linePaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        style = Paint.Style.STROKE
        strokeWidth = 1.6f * resources.displayMetrics.density
    }
    private val hintPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        color = Color.parseColor("#6E5A96")
        textAlign = Paint.Align.CENTER
        textSize = TypedValue.applyDimension(
            TypedValue.COMPLEX_UNIT_SP,
            13f,
            resources.displayMetrics,
        )
    }

    private val selected = LinkedHashSet<Int>()
    private val touchSlop = 14f * resources.displayMetrics.density
    private val grabRadius = 22f * resources.displayMetrics.density
    private val minTilePx = 28f * resources.displayMetrics.density
    private var downX = 0f
    private var downY = 0f
    private var downAt = 0L

    private enum class DragAxis { NONE, COLUMN, ROW }

    private var dragAxis = DragAxis.NONE
    private var dragIndex = -1

    /** Sel hasil deteksi otomatis; bila ada, grid manual diabaikan sampai direset. */
    private var detectedCells: List<FractionRect>? = null

    /** Posisi garis kolom dalam fraksi 0..1 (ukuran `columns + 1`). */
    private var columnCuts: FloatArray = GridSlicer.uniformCuts(3)

    /** Posisi garis baris dalam fraksi 0..1 (ukuran `rows + 1`). */
    private var rowCuts: FloatArray = GridSlicer.uniformCuts(3)

    var bitmap: Bitmap? = null
        private set

    var columns: Int = 3
        set(value) {
            field = value.coerceIn(MIN_GRID, MAX_GRID)
            columnCuts = GridSlicer.uniformCuts(field)
            detectedCells = null
            clearSelection()
            invalidate()
        }

    var rows: Int = 3
        set(value) {
            field = value.coerceIn(MIN_GRID, MAX_GRID)
            rowCuts = GridSlicer.uniformCuts(field)
            detectedCells = null
            clearSelection()
            invalidate()
        }

    /** Saat aktif, ketukan pada petak menyalakan/mematikan overlay seleksi. */
    var selectionMode: Boolean = false
        set(value) {
            field = value
            if (!value) clearSelection() else invalidate()
        }

    var highlightColor: Int = AppSettings.DEFAULT_HIGHLIGHT
        set(value) {
            field = value
            invalidate()
        }

    /** Dipanggil setiap kali jumlah potongan terpilih berubah. */
    var onSelectionChanged: ((Int) -> Unit)? = null

    /** Dipanggil setelah garis grid selesai digeser atau direset. */
    var onGridChanged: (() -> Unit)? = null

    val selectedCount: Int get() = selected.size

    val selectedTiles: Set<Int> get() = selected.toSet()

    fun setImage(image: Bitmap?) {
        bitmap = image
        clearSelection()
        invalidate()
    }

    /** Petak sesuai posisi garis saat ini; dipakai juga saat menyimpan potongan. */
    fun currentTiles(): List<GridTile> {
        val image = bitmap ?: return emptyList()
        if (image.width <= 0 || image.height <= 0) return emptyList()
        val cells = detectedCells
        if (cells != null) return GridSlicer.tilesFrom(cells, image.width, image.height)
        return GridSlicer.tilesFor(image.width, image.height, columnCuts, rowCuts)
    }

    val hasDetectedCells: Boolean get() = detectedCells != null

    /** Mengaktifkan sel hasil deteksi otomatis (null untuk kembali ke grid manual). */
    fun setDetectedCells(cells: List<FractionRect>?) {
        detectedCells = cells
        clearSelection()
        onGridChanged?.invoke()
        invalidate()
    }

    /** Mengembalikan semua garis ke posisi seragam. */
    fun resetGrid() {
        detectedCells = null
        columnCuts = GridSlicer.uniformCuts(columns)
        rowCuts = GridSlicer.uniformCuts(rows)
        onGridChanged?.invoke()
        invalidate()
    }

    fun clearSelection() {
        if (selected.isEmpty()) {
            invalidate()
            return
        }
        selected.clear()
        onSelectionChanged?.invoke(0)
        invalidate()
    }

    fun selectAll() {
        selected.clear()
        currentTiles().filterNot { it.isEmpty }.forEach { selected += it.index }
        onSelectionChanged?.invoke(selected.size)
        invalidate()
    }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        val image = bitmap
        if (image == null) {
            drawHint(canvas)
            return
        }
        computeImageRect(image.width, image.height, imageRect)
        canvas.drawBitmap(image, null, imageRect, bitmapPaint)
        if (imageRect.isEmpty) return

        val tiles = GridSlicer.tilesFor(image.width, image.height, columnCuts, rowCuts)
        val scaleX = imageRect.width() / image.width
        val scaleY = imageRect.height() / image.height

        val overlay = Color.argb(
            80,
            Color.red(highlightColor),
            Color.green(highlightColor),
            Color.blue(highlightColor),
        )
        fillPaint.color = overlay
        tiles.forEach { tile ->
            if (tile.index !in selected || tile.isEmpty) return@forEach
            canvas.drawRect(
                imageRect.left + tile.left * scaleX,
                imageRect.top + tile.top * scaleY,
                imageRect.left + tile.right * scaleX,
                imageRect.top + tile.bottom * scaleY,
                fillPaint,
            )
        }

        linePaint.color = if (selectionMode) highlightColor else Color.argb(235, 255, 255, 255)
        if (detectedCells != null) {
            // Outline tiap sel hasil deteksi, mengikuti batas konten masing-masing.
            tiles.forEach { tile ->
                val left = imageRect.left + tile.left * scaleX
                val top = imageRect.top + tile.top * scaleY
                val right = imageRect.left + tile.right * scaleX
                val bottom = imageRect.top + tile.bottom * scaleY
                canvas.drawRect(left, top, right, bottom, lineShadowPaint)
                canvas.drawRect(left, top, right, bottom, linePaint)
            }
        } else {
            for (position in 1 until columnCuts.size - 1) {
                val x = imageRect.left + columnCuts[position] * imageRect.width()
                canvas.drawLine(x, imageRect.top, x, imageRect.bottom, lineShadowPaint)
                canvas.drawLine(x, imageRect.top, x, imageRect.bottom, linePaint)
            }
            for (position in 1 until rowCuts.size - 1) {
                val y = imageRect.top + rowCuts[position] * imageRect.height()
                canvas.drawLine(imageRect.left, y, imageRect.right, y, lineShadowPaint)
                canvas.drawLine(imageRect.left, y, imageRect.right, y, linePaint)
            }
            if (!selectionMode) drawHandles(canvas)
        }
    }

    /** Titik kecil di tengah tiap garis sebagai penanda bahwa garis bisa digeser. */
    private fun drawHandles(canvas: Canvas) {
        handlePaint.color = Color.argb(235, 255, 255, 255)
        val radius = 3.5f * resources.displayMetrics.density
        for (position in 1 until columnCuts.size - 1) {
            val x = imageRect.left + columnCuts[position] * imageRect.width()
            canvas.drawCircle(x, imageRect.centerY(), radius, handlePaint)
        }
        for (position in 1 until rowCuts.size - 1) {
            val y = imageRect.top + rowCuts[position] * imageRect.height()
            canvas.drawCircle(imageRect.centerX(), y, radius, handlePaint)
        }
    }

    private fun drawHint(canvas: Canvas) {
        val metrics = hintPaint.fontMetrics
        val baseline = height / 2f - (metrics.ascent + metrics.descent) / 2f
        canvas.drawText(context.getString(R.string.editor_hint), width / 2f, baseline, hintPaint)
    }

    override fun onTouchEvent(event: MotionEvent): Boolean {
        if (bitmap == null || imageRect.isEmpty) return super.onTouchEvent(event)
        when (event.actionMasked) {
            MotionEvent.ACTION_DOWN -> {
                downX = event.x
                downY = event.y
                downAt = SystemClock.uptimeMillis()
                val hit = if (detectedCells != null) null else findCut(event.x, event.y)
                dragAxis = hit?.first ?: DragAxis.NONE
                dragIndex = hit?.second ?: -1
                return true
            }

            MotionEvent.ACTION_MOVE -> {
                if (dragAxis != DragAxis.NONE) {
                    moveCut(dragAxis, dragIndex, event.x, event.y)
                    return true
                }
                return true
            }

            MotionEvent.ACTION_UP -> {
                if (dragAxis != DragAxis.NONE) {
                    dragAxis = DragAxis.NONE
                    dragIndex = -1
                    onGridChanged?.invoke()
                    return true
                }
                val moved = abs(event.x - downX) > touchSlop || abs(event.y - downY) > touchSlop
                val quick = SystemClock.uptimeMillis() - downAt < 400
                if (!moved && quick) {
                    performClick()
                    if (selectionMode) toggleAt(event.x, event.y)
                }
                return true
            }

            MotionEvent.ACTION_CANCEL -> {
                dragAxis = DragAxis.NONE
                dragIndex = -1
                return true
            }
        }
        return super.onTouchEvent(event)
    }

    override fun performClick(): Boolean {
        super.performClick()
        return true
    }

    /** Mencari garis terdekat dari titik sentuh; hanya garis dalam (bukan tepi gambar). */
    private fun findCut(x: Float, y: Float): Pair<DragAxis, Int>? {
        if (x < imageRect.left - grabRadius || x > imageRect.right + grabRadius) return null
        if (y < imageRect.top - grabRadius || y > imageRect.bottom + grabRadius) return null

        var best: Pair<DragAxis, Int>? = null
        var bestDistance = grabRadius
        for (position in 1 until columnCuts.size - 1) {
            val lineX = imageRect.left + columnCuts[position] * imageRect.width()
            val distance = abs(x - lineX)
            if (distance <= bestDistance) {
                bestDistance = distance
                best = DragAxis.COLUMN to position
            }
        }
        for (position in 1 until rowCuts.size - 1) {
            val lineY = imageRect.top + rowCuts[position] * imageRect.height()
            val distance = abs(y - lineY)
            if (distance <= bestDistance) {
                bestDistance = distance
                best = DragAxis.ROW to position
            }
        }
        return best
    }

    private fun moveCut(axis: DragAxis, position: Int, x: Float, y: Float) {
        if (position <= 0) return
        when (axis) {
            DragAxis.COLUMN -> {
                if (imageRect.width() <= 0f) return
                val cuts = columnCuts
                if (position >= cuts.size - 1) return
                val gap = (minTilePx / imageRect.width()).coerceAtMost(0.25f)
                val lower = cuts[position - 1] + gap
                val upper = cuts[position + 1] - gap
                val fraction = ((x - imageRect.left) / imageRect.width()).coerceIn(0f, 1f)
                cuts[position] = if (lower <= upper) fraction.coerceIn(lower, upper) else (lower + upper) / 2f
                invalidate()
            }

            DragAxis.ROW -> {
                if (imageRect.height() <= 0f) return
                val cuts = rowCuts
                if (position >= cuts.size - 1) return
                val gap = (minTilePx / imageRect.height()).coerceAtMost(0.25f)
                val lower = cuts[position - 1] + gap
                val upper = cuts[position + 1] - gap
                val fraction = ((y - imageRect.top) / imageRect.height()).coerceIn(0f, 1f)
                cuts[position] = if (lower <= upper) fraction.coerceIn(lower, upper) else (lower + upper) / 2f
                invalidate()
            }

            DragAxis.NONE -> Unit
        }
    }

    private fun toggleAt(x: Float, y: Float) {
        val tile = tileAt(x, y) ?: return
        if (tile.isEmpty) return
        val index = tile.index
        val added = selected.add(index)
        if (!added) selected.remove(index)
        performHapticFeedback(android.view.HapticFeedbackConstants.KEYBOARD_TAP)
        onSelectionChanged?.invoke(selected.size)
        invalidate()
    }

    private fun tileAt(x: Float, y: Float): GridTile? {
        val image = bitmap ?: return null
        if (imageRect.isEmpty || !imageRect.contains(x, y)) return null
        val bitmapX = ((x - imageRect.left) / imageRect.width() * image.width).toInt()
            .coerceIn(0, image.width - 1)
        val bitmapY = ((y - imageRect.top) / imageRect.height() * image.height).toInt()
            .coerceIn(0, image.height - 1)
        return currentTiles().firstOrNull {
            bitmapX >= it.left && bitmapX < it.right && bitmapY >= it.top && bitmapY < it.bottom
        }
    }

    private fun computeImageRect(imageWidth: Int, imageHeight: Int, out: RectF) {
        if (imageWidth <= 0 || imageHeight <= 0) {
            out.setEmpty()
            return
        }
        val availableWidth = (width - paddingLeft - paddingRight).coerceAtLeast(1).toFloat()
        val availableHeight = (height - paddingTop - paddingBottom).coerceAtLeast(1).toFloat()
        val scale = min(availableWidth / imageWidth, availableHeight / imageHeight)
        val drawWidth = imageWidth * scale
        val drawHeight = imageHeight * scale
        val left = paddingLeft + (availableWidth - drawWidth) / 2f
        val top = paddingTop + (availableHeight - drawHeight) / 2f
        out.set(left, top, left + drawWidth, top + drawHeight)
    }
}
