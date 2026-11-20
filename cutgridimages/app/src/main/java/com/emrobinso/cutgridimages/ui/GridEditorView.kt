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
import com.emrobinso.cutgridimages.grid.GridSlicer
import com.emrobinso.cutgridimages.grid.MAX_GRID
import com.emrobinso.cutgridimages.grid.MIN_GRID
import kotlin.math.abs
import kotlin.math.min

/**
 * Menampilkan gambar utama dengan pembagian grid presisi dan overlay seleksi.
 * Ketuk sebuah petak (mode seleksi) untuk menyalakan/mematikan overlay semi transparan.
 */
class GridEditorView @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null,
    defStyleAttr: Int = 0,
) : View(context, attrs, defStyleAttr) {

    private val imageRect = RectF()
    private val bitmapPaint = Paint(Paint.FILTER_BITMAP_FLAG)
    private val fillPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply { style = Paint.Style.FILL }
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
        color = Color.parseColor("#8A8F98")
        textAlign = Paint.Align.CENTER
        textSize = TypedValue.applyDimension(
            TypedValue.COMPLEX_UNIT_SP,
            13f,
            resources.displayMetrics,
        )
    }

    private val selected = LinkedHashSet<Int>()
    private val touchSlop = 14f * resources.displayMetrics.density
    private var downX = 0f
    private var downY = 0f
    private var downAt = 0L

    var bitmap: Bitmap? = null
        private set

    var columns: Int = 3
        set(value) {
            field = value.coerceIn(MIN_GRID, MAX_GRID)
            clearSelection()
            invalidate()
        }

    var rows: Int = 3
        set(value) {
            field = value.coerceIn(MIN_GRID, MAX_GRID)
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

    val selectedCount: Int get() = selected.size

    val selectedTiles: Set<Int> get() = selected.toSet()

    fun setImage(image: Bitmap?) {
        bitmap = image
        clearSelection()
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
        val image = bitmap ?: return
        if (image.width <= 0) return
        selected.clear()
        for (index in 0 until columns * rows) selected += index
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

        val scaleX = imageRect.width() / image.width
        val scaleY = imageRect.height() / image.height
        val tiles = GridSlicer.tileBounds(image.width, image.height, columns, rows)

        val overlay = Color.argb(
            80,
            Color.red(highlightColor),
            Color.green(highlightColor),
            Color.blue(highlightColor),
        )
        fillPaint.color = overlay
        tiles.forEach { tile ->
            if (tile.index !in selected) return@forEach
            canvas.drawRect(
                imageRect.left + tile.left * scaleX,
                imageRect.top + tile.top * scaleY,
                imageRect.left + tile.right * scaleX,
                imageRect.top + tile.bottom * scaleY,
                fillPaint,
            )
        }

        linePaint.color = if (selectionMode) highlightColor else Color.argb(235, 255, 255, 255)
        for (index in 1 until columns) {
            val x = imageRect.left + imageRect.width() / columns * index
            canvas.drawLine(x, imageRect.top, x, imageRect.bottom, lineShadowPaint)
            canvas.drawLine(x, imageRect.top, x, imageRect.bottom, linePaint)
        }
        for (index in 1 until rows) {
            val y = imageRect.top + imageRect.height() / rows * index
            canvas.drawLine(imageRect.left, y, imageRect.right, y, lineShadowPaint)
            canvas.drawLine(imageRect.left, y, imageRect.right, y, linePaint)
        }
    }

    private fun drawHint(canvas: Canvas) {
        val metrics = hintPaint.fontMetrics
        val baseline = height / 2f - (metrics.ascent + metrics.descent) / 2f
        canvas.drawText(context.getString(R.string.editor_hint), width / 2f, baseline, hintPaint)
    }

    override fun onTouchEvent(event: MotionEvent): Boolean {
        when (event.actionMasked) {
            MotionEvent.ACTION_DOWN -> {
                downX = event.x
                downY = event.y
                downAt = SystemClock.uptimeMillis()
                return true
            }

            MotionEvent.ACTION_UP -> {
                val moved = abs(event.x - downX) > touchSlop || abs(event.y - downY) > touchSlop
                val quick = SystemClock.uptimeMillis() - downAt < 400
                if (!moved && quick) {
                    performClick()
                    if (selectionMode) toggleAt(event.x, event.y)
                }
                return true
            }
        }
        return super.onTouchEvent(event)
    }

    override fun performClick(): Boolean {
        super.performClick()
        return true
    }

    private fun toggleAt(x: Float, y: Float) {
        val index = tileIndexAt(x, y) ?: return
        if (!selected.add(index)) selected.remove(index)
        onSelectionChanged?.invoke(selected.size)
        invalidate()
    }

    private fun tileIndexAt(x: Float, y: Float): Int? {
        val image = bitmap ?: return null
        if (imageRect.isEmpty || !imageRect.contains(x, y)) return null
        val bitmapX = ((x - imageRect.left) / imageRect.width() * image.width).toInt()
            .coerceIn(0, image.width - 1)
        val bitmapY = ((y - imageRect.top) / imageRect.height() * image.height).toInt()
            .coerceIn(0, image.height - 1)
        return GridSlicer.tileBounds(image.width, image.height, columns, rows)
            .firstOrNull { bitmapX >= it.left && bitmapX < it.right && bitmapY >= it.top && bitmapY < it.bottom }
            ?.index
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
