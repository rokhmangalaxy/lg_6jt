package id.mcm.logopreview

import android.app.Application
import android.view.View
import android.view.ViewGroup
import android.widget.Button
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
class FavoriteTest{
    private fun all(v:View):List<View> = listOf(v)+if(v is ViewGroup)(0 until v.childCount).flatMap{all(v.getChildAt(it))}else emptyList()
    @Test fun stableFavoritesPersistAndPaginationHasNoDuplicates(){
        val app:Application=RuntimeEnvironment.getApplication()
        val prefs=app.getSharedPreferences("favorite-test",0);prefs.edit().clear().commit()
        val store=FavoriteStore(prefs)
        for(i in 0..7)assertTrue(store.toggle(i))
        assertEquals(8,FavoriteStore(prefs).indices().size)
        assertEquals(2,FavoriteStore.pageCount(8,3));assertEquals(1,FavoriteStore.pageCount(8,5))
        assertEquals((0..7).toList(),FavoriteStore.page(store.indices(),3,0)+FavoriteStore.page(store.indices(),3,1))
        assertFalse(store.toggle(7));assertEquals(7,store.indices().size)
        assertEquals(6,FavoriteStore.page(store.indices(),3,99).first())
    }
    @Test fun heartToggleCenterTabGridAndRemovalWork(){
        val app:Application=RuntimeEnvironment.getApplication()
        app.getSharedPreferences("native-studio",0).edit().clear().commit()
        val controller=Robolectric.buildActivity(MainActivity::class.java).setup()
        fun views()=all(controller.get().window.decorView)
        fun tap(description:String){views().first{it.contentDescription==description}.performClick()}
        tap("Tambahkan ke favorit");tap("Menu ♥ Favorit")
        assertTrue(views().filterIsInstance<TextView>().any{it.text=="♥ Favorit · 1 logo"})
        views().filterIsInstance<Button>().first{it.text=="5 kolom"}.performClick()
        controller.recreate()
        assertTrue(views().filterIsInstance<Button>().first{it.text=="5 kolom"}.isSelected)
        tap("Hapus Variasi 01 dari favorit")
        assertTrue(views().filterIsInstance<TextView>().any{it.text.toString().startsWith("Belum ada favorit")})
        controller.pause().stop().destroy()
    }
}
