package id.mcm.logopreview

import android.graphics.*
import android.graphics.drawable.Drawable

/** Small native drawable: light upper-left and dark lower-right soft relief. */
class NeoSurface(private val density: Float, private val inset: Boolean = false): Drawable() {
    private val paint = Paint(Paint.ANTI_ALIAS_FLAG)
    override fun draw(canvas: Canvas) {
        val d = density
        val rect = RectF(bounds.left+7*d,bounds.top+7*d,bounds.right-7*d,bounds.bottom-7*d)
        val radius=13*d
        if(inset){
            paint.shader=LinearGradient(rect.left,rect.top,rect.right,rect.bottom,0xffccd7e4.toInt(),0xfff4f7fb.toInt(),Shader.TileMode.CLAMP)
            canvas.drawRoundRect(rect,radius,radius,paint);paint.shader=null
            paint.color=0xff9cacc0.toInt();paint.style=Paint.Style.STROKE;paint.strokeWidth=d
            canvas.drawRoundRect(rect,radius,radius,paint);paint.style=Paint.Style.FILL
        } else {
            paint.color=BASE;paint.setShadowLayer(5*d,3*d,3*d,0xffb8c5d5.toInt())
            canvas.drawRoundRect(rect,radius,radius,paint)
            paint.setShadowLayer(5*d,-3*d,-3*d,Color.WHITE)
            canvas.drawRoundRect(rect,radius,radius,paint);paint.clearShadowLayer()
            canvas.drawRoundRect(rect,radius,radius,paint)
        }
    }
    override fun setAlpha(alpha:Int){paint.alpha=alpha;invalidateSelf()}
    override fun setColorFilter(colorFilter:ColorFilter?){paint.colorFilter=colorFilter;invalidateSelf()}
    @Suppress("DEPRECATION") override fun getOpacity():Int=PixelFormat.TRANSLUCENT
    companion object { val BASE=0xffe9eef5.toInt() }
}
