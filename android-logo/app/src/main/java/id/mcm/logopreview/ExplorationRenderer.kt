package id.mcm.logopreview

import android.content.res.AssetManager
import android.graphics.*
import kotlin.math.roundToInt

/** Raster exploration preview. Not a vector master: enlargement cannot invent source detail. */
object ExplorationRenderer {
    fun render(assets:AssetManager,logo:Int,preset:Int,maxEdge:Int,transparent:Boolean):Bitmap{
        val source=assets.open(LogoCatalog.files[logo]).use{BitmapFactory.decodeStream(it,null,BitmapFactory.Options().apply{inMutable=true;inPreferredConfig=Bitmap.Config.ARGB_8888;inScaled=false})}
        val pixels=IntArray(source.width*source.height)
        source.getPixels(pixels,0,source.width,0,0,source.width,source.height)
        val colors=LogoPixels.presets[preset]
        for(i in pixels.indices){
            val pixel=pixels[i];val alpha=pixel ushr 24
            if(alpha==0)continue
            val r=(pixel ushr 16)and 255;val g=(pixel ushr 8)and 255;val b=pixel and 255
            // Prepared, reviewed sources: classify material roles, not background gray.
            val role=if(r>g*1.35&&r>b*1.35)0 else if(b>r*1.12&&b>g*1.05)1 else 2
            pixels[i]=(colors[role] and 0x00ffffff) or (alpha shl 24)
        }
        source.setPixels(pixels,0,source.width,0,0,source.width,source.height)
        val scale=maxEdge.toFloat()/maxOf(source.width,source.height)
        val output=Bitmap.createBitmap((source.width*scale).roundToInt().coerceAtLeast(1),(source.height*scale).roundToInt().coerceAtLeast(1),Bitmap.Config.ARGB_8888)
        val canvas=Canvas(output)
        if(!transparent)canvas.drawColor(LogoCatalog.background(logo,preset))
        canvas.drawBitmap(source,null,Rect(0,0,output.width,output.height),Paint(3))
        source.recycle();return output
    }
}
