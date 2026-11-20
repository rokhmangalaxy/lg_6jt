package id.mcm.logopreview

import android.content.res.AssetManager
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Paint
import android.graphics.Path
import org.json.JSONObject
import kotlin.math.max
import kotlin.math.roundToInt

/** Native antialiased path rendering. Does not scale/quantize the small PNG preview. */
object LogoVectorRenderer {
    fun render(assets: AssetManager, logo: Int, preset: Int, maxEdge: Int = 1600, transparent: Boolean = false): Bitmap {
        require(logo in 0 until LogoCatalog.count && preset in 0..3 && maxEdge > 0)
        val file=LogoCatalog.files[logo].removeSuffix(".png")+".json"
        val json=JSONObject(assets.open(file).bufferedReader().use {it.readText()})
        val sourceWidth=json.getInt("width");val sourceHeight=json.getInt("height")
        require(sourceWidth>0&&sourceHeight>0)
        val scale=maxEdge.toFloat()/max(sourceWidth,sourceHeight)
        val width=(sourceWidth*scale).roundToInt().coerceAtLeast(1)
        val height=(sourceHeight*scale).roundToInt().coerceAtLeast(1)
        val bitmap=Bitmap.createBitmap(width,height,Bitmap.Config.ARGB_8888)
        val canvas=Canvas(bitmap);if (!transparent) canvas.drawColor(LogoCatalog.background(logo,preset))
        canvas.scale(width.toFloat()/sourceWidth,height.toFloat()/sourceHeight)
        val paint=Paint(Paint.ANTI_ALIAS_FLAG or Paint.DITHER_FLAG).apply {style=Paint.Style.FILL}
        val layers=json.getJSONArray("layers")
        for(i in 0 until layers.length()){
            val layer=layers.getJSONObject(i);val commands=layer.getJSONArray("commands")
            val p=Path().apply {fillType=Path.FillType.EVEN_ODD}
            for(j in 0 until commands.length()){
                val command=commands.getJSONArray(j)
                fun n(index:Int)=command.getDouble(index).toFloat()
                when(command.getString(0)){
                    "M"->p.moveTo(n(1),n(2))
                    "L"->p.lineTo(n(1),n(2))
                    "Q"->p.quadTo(n(1),n(2),n(3),n(4))
                    "Z"->p.close()
                    else->error("Invalid logo path command")
                }
            }
            paint.color=LogoPixels.presets[preset][layer.getInt("color")]
            canvas.drawPath(p,paint)
        }
        return bitmap
    }
}
