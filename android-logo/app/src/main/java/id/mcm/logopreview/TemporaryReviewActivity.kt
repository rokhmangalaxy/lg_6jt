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
        body.addView(Switch(this).apply {
            text="Dark mode"; setTextColor(foreground); isChecked=dark
            setOnCheckedChangeListener { _, checked ->
                dark=checked; prefs.edit().putBoolean("dark",dark).apply(); showReview()
            }
        })
        val navigation=LinearLayout(this)
        navigation.addView(action("❮ Sebelumnya") { move(-1) }, LinearLayout.LayoutParams(0,dp(52),1f))
        navigation.addView(action("Berikutnya ❯") { move(1) }, LinearLayout.LayoutParams(0,dp(52),1f))
        body.addView(navigation)
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
        body.addView(label("$id\n$source"))
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
        body.addView(label("Penilaian manual; bukan skor otomatis. Catatan tersimpan otomatis di perangkat ini."))
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
        body.addView(statusGroup)
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
            val value="$id — $status\nSumber: $source\n${notes.text}"
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
    private fun savePosition() { prefs.edit().putInt("position",position).apply() }
    private fun move(step:Int) { position=(position+step+items.length())%items.length(); savePosition(); showReview() }
}
