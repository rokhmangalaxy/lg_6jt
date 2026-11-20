package id.mcm.logopreview

import android.content.res.AssetManager
import android.graphics.*

/** Fixed photo mockups, not 3D or production embroidery. No gray preview background on marks. */
object UniformRenderer {
    val capPhotos = arrayOf("cap-front", "cap-corner", "cap-left")
    // rear-angle is a duplicate front asset in the supplied prototype; do not offer it.
    val shirtPhotos = arrayOf("front", "angle", "back")
    fun render(assets: AssetManager, logo: Int, preset: Int, cap: Boolean, angle: Int): Bitmap {
        if(angle==3){
            val result=Bitmap.createBitmap(1200,1200,Bitmap.Config.ARGB_8888)
            val canvas=Canvas(result);canvas.drawColor(0xffedefed.toInt())
            for(i in 0..2){
                val image=render(assets,logo,preset,cap,i)
                val box=if(i==0)RectF(0f,0f,800f,1200f)else RectF(812f,if(i==1)0f else 606f,1200f,if(i==1)594f else 1200f)
                val scale=minOf(box.width()/image.width,box.height()/image.height)
                val w=image.width*scale;val h=image.height*scale
                canvas.drawBitmap(image,null,RectF(box.centerX()-w/2,box.centerY()-h/2,box.centerX()+w/2,box.centerY()+h/2),Paint(3));image.recycle()
            }
            return result
        }
        val photos=if(cap) capPhotos else shirtPhotos
        require(angle in photos.indices)
        val photo=assets.open("uniform/${photos[angle]}.webp").use { BitmapFactory.decodeStream(it) }
        val output=Bitmap.createBitmap(600,photo.height,Bitmap.Config.ARGB_8888)
        val canvas=Canvas(output);canvas.drawBitmap(photo,null,Rect(0,0,600,photo.height),Paint(3))
        val mark=LogoVectorRenderer.render(assets,logo,preset,600,true)
        // Fit visible artwork, excluding each source's padding, to a calibrated placement.
        var left=mark.width;var top=mark.height;var right=0;var bottom=0
        val pixels=IntArray(mark.width*mark.height);mark.getPixels(pixels,0,mark.width,0,0,mark.width,mark.height)
        for(y in 0 until mark.height)for(x in 0 until mark.width)if((pixels[y*mark.width+x] ushr 24)>8){
            left=minOf(left,x);top=minOf(top,y);right=maxOf(right,x+1);bottom=maxOf(bottom,y+1)
        }
        fun stamp(x:Float,y:Float,w:Float,h:Float,rotation:Float=0f){
            if(right<=left||bottom<=top)return
            val fit=minOf(w/(right-left),h/(bottom-top))
            val dw=(right-left)*fit;val dh=(bottom-top)*fit
            canvas.save();canvas.rotate(rotation,x,y)
            canvas.drawBitmap(mark,Rect(left,top,right,bottom),RectF(x-dw/2,y-dh/2,x+dw/2,y+dh/2),Paint(3));canvas.restore()
        }
        if(cap)when(angle){
            0->stamp(300f,299f,120f,90f)
            1->{stamp(335f,300f,96f,84f,-6f);stamp(133f,352f,36f,36f,8f)}
            2->stamp(222f,360f,60f,48f)
        }else when(angle){
            0->stamp(386f,168f,48f,42f)
            1->stamp(304f,165f,42f,42f,3f)
            2->stamp(300f,108f,120f,90f)
        }
        photo.recycle();mark.recycle();return output
    }
}
