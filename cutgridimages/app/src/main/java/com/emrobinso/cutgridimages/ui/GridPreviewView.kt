package com.emrobinso.cutgridimages.ui

import android.content.Context
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.RectF
import android.util.AttributeSet
import android.util.TypedValue
import android.view.View
import com.emrobinso.cutgridimages.R
import com.emrobinso.cutgridimages.grid.MAX_GRID
import com.emrobinso.cutgridimages.grid.MIN_GRID
import kotlin.math.min

/**
 * Menampilkan bitmap dengan rasio asli (fit center) sekaligus garis grid.
 * Garis digambar tepat di atas area gambar, bukan di atas seluruh View.
 */
class GridPreviewView @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null,
    defStyleAttr: Int = 0,
) : View(context, attrs, defStyleAttr) {

    private val imageRect = RectF()
    private val bitmapPaint = Paint(Paint.FILTER_BITMAP_FLAG)
    private val density = resources.displayMetrics.density

    private val gridShadowPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        style = Paint.Style.STROKE
        strokeWidth = 3.5f * density
        color = Color.argb(80, 0, 0, 0)
    }
    private val gridPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        style = Paint.Style.STROKE
        strokeWidth = 1.5f * density
        color = Color.WHITE
    }
    private val hintPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        color = Color.parseColor("#8A8F98")
        textSize = TypedValue.applyDimension(
            TypedValue.COMPLEX_UNIT_SP,
            14f,
            resources.displayMetrics,
        )
        textAlign = Paint.Align.CENTER
    }

    var bitmap: Bitmap? = null
        set(value) {
            field = value
            invalidate()
        }

    var columns: Int = 3
        set(value) {
            field = value.coerceIn(MIN_GRID, MAX_GRID)
            invalidate()
        }

    var rows: Int = 3
        set(value) {
            field = value.coerceIn(MIN_GRID, MAX_GRID)
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
        drawGrid(canvas)
    }

    private fun drawHint(canvas: Canvas) {
        val metrics = hintPaint.fontMetrics
        val baseline = height / 2f - (metrics.ascent + metrics.descent) / 2f
        canvas.drawText(context.getString(R.string.no_image), width / 2f, baseline, hintPaint)
    }

    private fun drawGrid(canvas: Canvas) {
        if (imageRect.isEmpty) return
        val stepX = imageRect.width() / columns
        val stepY = imageRect.height() / rows
        for (column in 1 until columns) {
            val x = imageRect.left + stepX * column
            canvas.drawLine(x, imageRect.top, x, imageRect.bottom, gridShadowPaint)
            canvas.drawLine(x, imageRect.top, x, imageRect.bottom, gridPaint)
        }
        for (row in 1 until rows) {
            val y = imageRect.top + stepY * row
            canvas.drawLine(imageRect.left, y, imageRect.right, y, gridShadowPaint)
            canvas.drawLine(imageRect.left, y, imageRect.right, y, gridPaint)
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
