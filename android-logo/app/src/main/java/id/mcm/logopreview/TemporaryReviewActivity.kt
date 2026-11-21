package id.mcm.logopreview

import android.app.Activity
import android.os.Bundle
import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.graphics.BitmapFactory
import android.graphics.Color
import android.text.Editable
import android.text.TextWatcher
import android.view.Gravity
import android.widget.*
import org.json.JSONArray

/** Removable review screen. All state is isolated from catalog, favorites and development notes. */
class TemporaryReviewActivity : Activity() {
    private val prefs by lazy { getSharedPreferences("temporary-logo-review", Context.MODE_PRIVATE) }
    private lateinit var items: JSONArray
    private var position = 0
    private var dark = true
    private fun dp(n: Int) = (n * resources.displayMetrics.density).toInt()
    override fun onCreate(state: Bundle?) {
        super.onCreate(state)
        items = assets.open("temporary-review/index.json").bufferedReader().use { JSONArray(it.readText()) }
        position = prefs.getInt("position", 0).coerceIn(0, items.length()-1)
        val requested=intent.getStringExtra("logoId")
        if(requested!=null) {
            for(i in 0 until items.length()) if(items.getJSONObject(i).getString("id")==requested) { position=i; break }
        }
        dark = prefs.getBoolean("dark", true)
        showReview()
    }
    private fun showReview() {
        val item = items.getJSONObject(position)
        val id = item.getString("id")
        val source = item.getString("sourceName")
        val catalogIndex=LogoCatalog.files.indexOf("exploration/$id.png")
        val variationName=if(catalogIndex>=0) LogoCatalog.names[catalogIndex] else id
        val foreground = Color.parseColor(if (dark) "#E5E7EB" else "#173257")
        val background = Color.parseColor(if (dark) "#111827" else "#EEF2F7")
        window.statusBarColor = background
        window.navigationBarColor = background
        val scroll = ScrollView(this).apply { setBackgroundColor(background) }
        val body = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(16),dp(16),dp(16),dp(24))
        }
        scroll.addView(body)
        fun label(value: String) = TextView(this).apply {
            text = value; textSize = 16f; setTextColor(foreground); setPadding(0,dp(8),0,dp(8))
        }
        fun action(value: String, run: () -> Unit) = Button(this).apply {
            text=value; setTextColor(foreground)
            backgroundTintList=android.content.res.ColorStateList.valueOf(Color.parseColor(if(dark) "#374151" else "#D1D5DB"))
            setOnClickListener { run() }
        }
        body.addView(action("← Kembali") { finish() })
        body.addView(label("Review sementara · ${position+1}/${items.length()}"))
        body.addView(action("Seluruh catatan") { showAllNotes() })
        body.addView(action("Salin semua catatan") { copyAllNotes() })
        body.addView(Switch(this).apply {
            text="Dark mode"; setTextColor(foreground); isChecked=dark
            setOnCheckedChangeListener { _, checked ->
                dark=checked; prefs.edit().putBoolean("dark",dark).apply(); showReview()
            }
        })
        val jump=EditText(this).apply {
            hint="Nomor logo 1–${items.length()}"; inputType=android.text.InputType.TYPE_CLASS_NUMBER
            setTextColor(foreground); setHintTextColor(Color.GRAY)
        }
        body.addView(jump)
        body.addView(action("Buka nomor") {
            val number=jump.text.toString().toIntOrNull()
            if(number!=null && number in 1..items.length()) { position=number-1; savePosition(); showReview() }
            else Toast.makeText(this,"Nomor tidak valid",Toast.LENGTH_SHORT).show()
        })
        body.addView(label("$variationName · $id\n$source"))
        body.addView(label("Asli (kiri) · Redraw (kanan)"))
        val pair=LinearLayout(this).apply { gravity=Gravity.CENTER_VERTICAL }
        for(kind in listOf("source","redraw")) {
            val bitmap=assets.open("temporary-review/$id-$kind.png").use { BitmapFactory.decodeStream(it) }
            pair.addView(ImageView(this).apply {
                contentDescription=if(kind=="source") "Logo asli $id" else "Redraw $id"
                setImageBitmap(bitmap); scaleType=ImageView.ScaleType.FIT_CENTER
                setBackgroundColor(Color.parseColor(if(dark) "#9CA3AF" else "#FFFFFF"))
            },LinearLayout.LayoutParams(0,dp(200),1f).apply { setMargins(dp(2),0,dp(2),0) })
        }
        body.addView(pair)

        val statuses=listOf("Belum dicek","Perlu perbaikan","Sesuai")
        val statusGroup=RadioGroup(this)
        val saved=prefs.getInt("status:$id",0).coerceIn(0,2)
        statuses.forEachIndexed { index, value ->
            statusGroup.addView(RadioButton(this).apply {
                this.id=index+1; text=value; setTextColor(foreground)
                buttonTintList=android.content.res.ColorStateList.valueOf(foreground)
            })
        }
        statusGroup.check(saved+1)
        statusGroup.setOnCheckedChangeListener { _, checked -> prefs.edit().putInt("status:$id",checked-1).apply() }
        val navigation=LinearLayout(this).apply { gravity=Gravity.CENTER_VERTICAL }
        navigation.addView(action("❮") { move(-1) }.apply { contentDescription="Logo sebelumnya" },LinearLayout.LayoutParams(dp(52),dp(52)))
        navigation.addView(statusGroup,LinearLayout.LayoutParams(0,-2,1f))
        navigation.addView(action("❯") { move(1) }.apply { contentDescription="Logo berikutnya" },LinearLayout.LayoutParams(dp(52),dp(52)))
        body.addView(navigation)
        body.addView(label("Penilaian manual untuk catatan kompleks. Radio dan catatan otomatis tersimpan di perangkat ini."))
        val notes=EditText(this).apply {
            hint="Catatan perbaikan, boleh beberapa poin…"; setTextColor(foreground); setHintTextColor(Color.GRAY)
            gravity=Gravity.TOP; minLines=5
            inputType=android.text.InputType.TYPE_CLASS_TEXT or android.text.InputType.TYPE_TEXT_FLAG_MULTI_LINE or android.text.InputType.TYPE_TEXT_FLAG_CAP_SENTENCES
            setText(prefs.getString("note:$id",""))
            addTextChangedListener(object: TextWatcher {
                override fun beforeTextChanged(s:CharSequence?,start:Int,count:Int,after:Int) {}
                override fun onTextChanged(s:CharSequence?,start:Int,before:Int,count:Int) { prefs.edit().putString("note:$id",s.toString()).apply() }
                override fun afterTextChanged(s:Editable?) {}
            })
        }
        body.addView(notes)
        body.addView(action("Salin catatan") {
            val status=statuses[prefs.getInt("status:$id",0).coerceIn(0,2)]
            val value="$variationName:$status, ${notes.text}"
            (getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager).setPrimaryClip(ClipData.newPlainText("Review logo",value))
            Toast.makeText(this,"Catatan disalin",Toast.LENGTH_SHORT).show()
        })
        setContentView(scroll)
        scroll.setOnApplyWindowInsetsListener { view,insets ->
            view.setPadding(insets.systemWindowInsetLeft,insets.systemWindowInsetTop,insets.systemWindowInsetRight,insets.systemWindowInsetBottom)
            insets
        }
        scroll.requestApplyInsets()
    }
    private fun collectedNotes(): List<String> {
        val statuses=listOf("Belum dicek","Perlu perbaikan","Sesuai")
        // Use catalog order and stable IDs, not the source-filename review ordering.
        return LogoCatalog.files.mapIndexedNotNull { index, asset ->
            val id=asset.substringAfterLast('/').removeSuffix(".png")
            val isReviewItem=(0 until items.length()).any { items.getJSONObject(it).getString("id")==id }
            val note=prefs.getString("note:$id","").orEmpty()
            if(!isReviewItem || (!prefs.contains("status:$id") && note.isBlank())) null
            else "${LogoCatalog.names[index]}:${statuses[prefs.getInt("status:$id",0).coerceIn(0,2)]}, $note"
        }
    }
    private fun copyAllNotes() {
        val notes=collectedNotes()
        if(notes.isEmpty()) {
            Toast.makeText(this,"Belum ada catatan atau penilaian tersimpan",Toast.LENGTH_SHORT).show()
            return
        }
        (getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager).setPrimaryClip(
            ClipData.newPlainText("Seluruh catatan logo",notes.joinToString("\n")))
        Toast.makeText(this,"${notes.size} catatan disalin",Toast.LENGTH_SHORT).show()
    }
    private fun showAllNotes() {
        val foreground=Color.parseColor(if(dark) "#E5E7EB" else "#173257")
        val body=LinearLayout(this).apply {
            orientation=LinearLayout.VERTICAL;setPadding(dp(16),dp(16),dp(16),dp(24))
        }
        fun action(title:String, run:()->Unit)=Button(this).apply {
            text=title;setTextColor(foreground)
            backgroundTintList=android.content.res.ColorStateList.valueOf(Color.parseColor(if(dark) "#374151" else "#D1D5DB"))
            setOnClickListener { run() }
        }
        val notes=collectedNotes()
        body.addView(action("← Kembali ke review") { showReview() })
        body.addView(TextView(this).apply {
            text="Seluruh catatan · ${notes.size} item";textSize=20f;setTextColor(foreground)
        })
        body.addView(action("Salin semua catatan") { copyAllNotes() })
        body.addView(TextView(this).apply {
            text=if(notes.isEmpty()) "Belum ada catatan atau penilaian tersimpan." else notes.joinToString("\n\n")
            textSize=16f;setTextColor(foreground);setTextIsSelectable(true)
            setPadding(0,dp(16),0,0)
        })
        val scroll=ScrollView(this).apply {
            setBackgroundColor(Color.parseColor(if(dark) "#111827" else "#EEF2F7"));addView(body)
        }
        setContentView(scroll)
        scroll.setOnApplyWindowInsetsListener { view,insets ->
            view.setPadding(insets.systemWindowInsetLeft,insets.systemWindowInsetTop,insets.systemWindowInsetRight,insets.systemWindowInsetBottom)
            insets
        }
        scroll.requestApplyInsets()
    }
    private fun savePosition() { prefs.edit().putInt("position",position).apply() }
    private fun move(step:Int) {
        val previousId=items.getJSONObject(position).getString("id")
        val previousValue=prefs.getInt("status:$previousId",0).coerceIn(0,2)
        position=(position+step+items.length())%items.length()
        val nextId=items.getJSONObject(position).getString("id")
        // Inherit only on Next, only if the destination has no saved radio value.
        // Manual notes never carry over to another logo.
        if(step>0 && !prefs.contains("status:$nextId")) {
            prefs.edit().putInt("status:$nextId",previousValue).apply()
        }
        savePosition(); showReview()
    }
}
