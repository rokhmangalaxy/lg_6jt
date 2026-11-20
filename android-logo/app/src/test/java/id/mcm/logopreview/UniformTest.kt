package id.mcm.logopreview

import android.app.Application
import android.widget.Button
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[34])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class UniformTest {
    @Test fun transparentMarksAndAllMockupPlacementsRender(){
        val app:Application=RuntimeEnvironment.getApplication()
        for(logo in 0..3)for(preset in 0..3){
            val mark=LogoVectorRenderer.render(app.assets,logo,preset,400,true)
            assertEquals(0,mark.getPixel(0,0));mark.recycle()
            val mockup=UniformRenderer.render(app.assets,logo,preset,true,0)
            assertEquals(600,mockup.width);assertEquals(600,mockup.height);mockup.recycle()
        }
        for(cap in listOf(false,true))for(angle in 0..3){
            val image=UniformRenderer.render(app.assets,2,1,cap,angle)
            assertEquals(if(angle==3)1200 else 600,image.width);assertTrue(image.height>0);image.recycle()
        }
    }
    private fun all(v:View):List<View> = listOf(v)+if(v is ViewGroup)(0 until v.childCount).flatMap{all(v.getChildAt(it))}else emptyList()
    @Test fun uniformTabUsesCurrentLogoAndLastSwatchAndRestoresOnRotation(){
        val app:Application=RuntimeEnvironment.getApplication()
        app.getSharedPreferences("native-studio",0).edit().clear().putInt("clientSetLogo",2).putInt("clientSetPalette2",1).commit()
        val controller=Robolectric.buildActivity(MainActivity::class.java).setup()
        fun tap(label:String){all(controller.get().window.decorView).filterIsInstance<Button>().first{it.text.toString()==label}.performClick()}
        val decor=controller.get().window.decorView
        decor.measure(View.MeasureSpec.makeMeasureSpec(1080,View.MeasureSpec.EXACTLY),View.MeasureSpec.makeMeasureSpec(1920,View.MeasureSpec.EXACTLY))
        decor.layout(0,0,1080,1920)
        val preview=all(decor).first{it.contentDescription=="Preview logo, geser kiri atau kanan"}
        assertTrue(preview.width>0);assertEquals(preview.width,preview.height)
        assertEquals(11,all(decor).filterIsInstance<Button>().count{it.text.toString().matches(Regex("0[1-9]|1[01]"))})
        assertFalse(all(decor).filterIsInstance<Button>().any{it.text=="Pilihan Klien"||it.text=="Eksplorasi"})
        tap("Seragam")
        assertTrue(all(controller.get().window.decorView).filterIsInstance<TextView>().any{it.text.toString()=="Variasi 03 · Swatch 2"})
        controller.recreate()
        assertTrue(all(controller.get().window.decorView).filterIsInstance<TextView>().any{it.text.toString()=="Variasi 03 · Swatch 2"})
        tap("Logo");tap("04");tap("Seragam")
        assertTrue(all(controller.get().window.decorView).filterIsInstance<TextView>().any{it.text.toString()=="Variasi 04 · Swatch 1"})
        tap("Logo");tap("05");tap("Seragam")
        assertTrue(all(controller.get().window.decorView).filterIsInstance<TextView>().any{it.text.toString()=="Variasi 05 · Swatch 1"})
        controller.pause().stop().destroy()
    }
}
