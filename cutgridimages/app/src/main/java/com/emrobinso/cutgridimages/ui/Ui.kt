package com.emrobinso.cutgridimages.ui

import android.content.Context
import android.graphics.drawable.GradientDrawable
import android.util.TypedValue
import kotlin.math.roundToInt

/** Konversi dp ke piksel. */
fun Context.dp(value: Int): Int =
    (value * resources.displayMetrics.density).roundToInt()

/** Ukuran sp ke piksel. */
fun Context.sp(value: Float): Float =
    TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_SP, value, resources.displayMetrics)

/** Latar membulat dengan warna isi dan garis tepi opsional. */
fun roundedBackground(fillColor: Int, strokeColor: Int? = null, radiusDp: Int = 10): GradientDrawable =
    GradientDrawable().apply {
        shape = GradientDrawable.RECTANGLE
        cornerRadius = radiusDp.toFloat()
        setColor(fillColor)
        if (strokeColor != null) setStroke(1, strokeColor)
    }
