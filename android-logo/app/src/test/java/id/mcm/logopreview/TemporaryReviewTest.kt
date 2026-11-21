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
    @Test fun reviewIsReachableFromLauncherAndCatalogExpanded() {
        val controller=Robolectric.buildActivity(MainActivity::class.java).setup()
        val activity=controller.get()
        val button=descendants(activity.findViewById<View>(android.R.id.content)).filterIsInstance<Button>().single { it.text=="☾ Review asli · Catatan · Dark mode" }
        button.performClick()
        val launched=org.robolectric.Shadows.shadowOf(activity).nextStartedActivity
        assertEquals(TemporaryReviewActivity::class.java.name,launched.component?.className)
        assertEquals(330,LogoCatalog.count)
        controller.pause().stop().destroy()
    }
    @Test fun nextInheritsOnlyMissingStatusAndCopyUsesVariationName() {
        val controller=Robolectric.buildActivity(TemporaryReviewActivity::class.java).setup()
        val activity=controller.get()
        val prefs=activity.getSharedPreferences("temporary-logo-review",Context.MODE_PRIVATE)
        val items=org.json.JSONArray(activity.assets.open("temporary-review/index.json").bufferedReader().use { it.readText() })
        val start=prefs.getInt("position",0)
        val currentId=items.getJSONObject(start).getString("id")
        val nextId=items.getJSONObject((start+1)%items.length()).getString("id")
        prefs.edit().remove("status:$nextId").remove("note:$nextId").apply()
        fun views()=descendants(activity.findViewById<View>(android.R.id.content))
        views().filterIsInstance<RadioButton>().first { it.text=="Perlu perbaikan" }.performClick()
        views().filterIsInstance<EditText>().last().setText("Perbaiki rail")
        views().filterIsInstance<Button>().first { it.text=="Salin catatan" }.performClick()
        val clipboard=activity.getSystemService(Context.CLIPBOARD_SERVICE) as android.content.ClipboardManager
        val name=LogoCatalog.names[LogoCatalog.files.indexOf("exploration/$currentId.png")]
        assertEquals("$name:Perlu perbaikan, Perbaiki rail",clipboard.primaryClip!!.getItemAt(0).text.toString())
        views().filterIsInstance<Button>().first { it.text=="❯" }.performClick()
        assertEquals(1,prefs.getInt("status:$nextId",-1))
        assertEquals("",views().filterIsInstance<EditText>().last().text.toString())
        views().filterIsInstance<RadioButton>().first { it.text=="Sesuai" }.performClick()
        views().filterIsInstance<Button>().first { it.text=="❮" }.performClick()
        views().filterIsInstance<Button>().first { it.text=="❯" }.performClick()
        assertEquals(2,prefs.getInt("status:$nextId",-1))
        assertTrue(views().filterIsInstance<RadioButton>().first { it.text=="Sesuai" }.isChecked)
        controller.pause().stop().destroy()
    }
    @Test fun allNotesShowsAndCopiesEverySavedItemIncludingRatingOnly() {
        val controller=Robolectric.buildActivity(TemporaryReviewActivity::class.java).setup()
        val activity=controller.get()
        val prefs=activity.getSharedPreferences("temporary-logo-review",Context.MODE_PRIVATE)
        prefs.edit().clear().putInt("status:exp-001-01",1).putString("note:exp-001-01","Perbaiki rail")
            .putInt("status:exp-001-08",2).putString("note:exp-001-02","Catatan saja").apply()
        fun views()=descendants(activity.findViewById<View>(android.R.id.content))
        views().filterIsInstance<Button>().first { it.text=="Seluruh catatan" }.performClick()
        val text=views().filterIsInstance<TextView>().map { it.text.toString() }.joinToString("\n")
        assertTrue(text.contains("Variasi 05:Perlu perbaikan, Perbaiki rail"))
        assertTrue(text.contains("Variasi 06:Sesuai, "))
        assertTrue(text.contains("Variasi 09:Belum dicek, Catatan saja"))
        assertFalse(text.contains("Variasi 10:"))
        views().filterIsInstance<Button>().first { it.text=="Salin semua catatan" }.performClick()
        val clipboard=activity.getSystemService(Context.CLIPBOARD_SERVICE) as android.content.ClipboardManager
        assertEquals("Variasi 05:Perlu perbaikan, Perbaiki rail\nVariasi 06:Sesuai, \nVariasi 09:Belum dicek, Catatan saja",clipboard.primaryClip!!.getItemAt(0).text.toString())
        views().filterIsInstance<Button>().first { it.text=="← Kembali ke review" }.performClick()
        assertTrue(views().filterIsInstance<Button>().any { it.text=="❯" })
        controller.pause().stop().destroy()
    }
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
        views().filterIsInstance<Button>().first { it.text=="❯" }.performClick()
        views().filterIsInstance<Button>().first { it.text=="❮" }.performClick()
        assertEquals("Rail perlu diperbaiki",views().filterIsInstance<EditText>().last().text.toString())
        assertTrue(views().filterIsInstance<RadioButton>().first { it.text=="Perlu perbaikan" }.isChecked)
        controller.recreate()
        assertEquals(start,prefs.getInt("position",-1))
        assertFalse(views().filterIsInstance<Switch>().single().isChecked)
        assertEquals("Rail perlu diperbaiki",views().filterIsInstance<EditText>().last().text.toString())
        controller.pause().stop().destroy()
    }
}
