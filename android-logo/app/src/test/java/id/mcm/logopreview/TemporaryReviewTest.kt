package id.mcm.logopreview

import android.content.Context
import android.widget.*
import android.view.View
import android.view.ViewGroup
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[34])
class TemporaryReviewTest {
    private fun descendants(view: View): List<View> = listOf(view) +
        if(view is ViewGroup) (0 until view.childCount).flatMap { descendants(view.getChildAt(it)) } else emptyList()
    @Test fun notesStatusAndDarkModePersistAcrossNavigationAndRecreation() {
        val controller=Robolectric.buildActivity(TemporaryReviewActivity::class.java).setup()
        val activity=controller.get()
        val prefs=activity.getSharedPreferences("temporary-logo-review",Context.MODE_PRIVATE)
        fun views()=descendants(activity.findViewById<View>(android.R.id.content))
        val start=prefs.getInt("position",0)
        views().filterIsInstance<EditText>().last().setText("Rail perlu diperbaiki")
        views().filterIsInstance<RadioButton>().first { it.text=="Perlu perbaikan" }.performClick()
        val toggle=views().filterIsInstance<Switch>().single()
        toggle.isChecked=false
        assertFalse(prefs.getBoolean("dark",true))
        views().filterIsInstance<Button>().first { it.text=="Berikutnya ❯" }.performClick()
        views().filterIsInstance<Button>().first { it.text=="❮ Sebelumnya" }.performClick()
        assertEquals("Rail perlu diperbaiki",views().filterIsInstance<EditText>().last().text.toString())
        assertTrue(views().filterIsInstance<RadioButton>().first { it.text=="Perlu perbaikan" }.isChecked)
        controller.recreate()
        assertEquals(start,prefs.getInt("position",-1))
        assertFalse(views().filterIsInstance<Switch>().single().isChecked)
        assertEquals("Rail perlu diperbaiki",views().filterIsInstance<EditText>().last().text.toString())
        controller.pause().stop().destroy()
    }
}
