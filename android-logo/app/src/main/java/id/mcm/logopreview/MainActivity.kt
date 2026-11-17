package id.mcm.logopreview

import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.graphics.*
import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.view.*
import android.view.inputmethod.InputMethodManager
import android.widget.*
import org.json.JSONArray
import org.json.JSONObject
import java.text.DateFormat
import java.util.Date
import java.util.concurrent.Executors
import kotlin.math.abs
import kotlin.math.min

/** All UI uses Android Views and Canvas. No WebView, HTML or JavaScript runtime. */
class MainActivity : Activity() {
    private val navy = 0xff173257.toInt()
    private val worker = Executors.newSingleThreadExecutor()
    private val prefs by lazy { getSharedPreferences("native-studio", MODE_PRIVATE) }
    private val files = arrayOf("variasi-01-evolusi.png", "variasi-02-diamond-negatif.png", "variasi-03-lipatan-metal.png", "variasi-04-horizontal.png", "variasi-05-monokrom.png")
    private val names = arrayOf("Evolusi", "Diamond", "Lipatan metal", "Horizontal", "Industrial")
    private val sources = mutableMapOf<Int, Triple<Bitmap, IntArray, BooleanArray>>()
    private val rendered = android.util.LruCache<Int, Bitmap>(8)
    private lateinit var content: FrameLayout
    private lateinit var logoView: LogoView
    private lateinit var counter: TextView
    private lateinit var status: TextView
    private lateinit var paletteRow: LinearLayout
    private lateinit var numberRow: LinearLayout
    private lateinit var bottom: LinearLayout
    private var current = 0
    private var page = 0
    private var generation = 0
    private val selections = IntArray(5)
    private var noteType = 0
    private fun dp(n: Int) = (n * resources.displayMetrics.density).toInt()
    private fun column() = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL }
    private fun row() = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER_VERTICAL }
    private fun text(value: String, size: Float = 14f) = TextView(this).apply { text=value; textSize=size; setTextColor(navy); gravity=Gravity.CENTER_VERTICAL }
    private fun button(label: String, description: String = label, action: () -> Unit) = Button(this).apply {
        text=label; textSize=13f; isAllCaps=false; contentDescription=description
        setTextColor(navy); minWidth=0; minimumWidth=0
        setPadding(dp(4),0,dp(4),0); setOnClickListener { action() }
    }
    override fun onCreate(state: Bundle?) {
        super.onCreate(state)
        current=state?.getInt("logo") ?: prefs.getInt("logo",0)
        page=state?.getInt("page") ?: 0
        noteType=prefs.getInt("noteType",0)
        for(i in selections.indices) selections[i]=prefs.getInt("palette$i",0).coerceIn(0,3)
        current=current.coerceIn(0,4);page=page.coerceIn(0,2)
        val root=column().apply { setBackgroundColor(Color.WHITE) }
        // Insets are owned by the root on Android 15 edge-to-edge; no guessed status-bar sizes.
        root.setOnApplyWindowInsetsListener { v, insets ->
            if (android.os.Build.VERSION.SDK_INT >= 30) {
                val bars=insets.getInsets(WindowInsets.Type.systemBars() or WindowInsets.Type.ime())
                v.setPadding(bars.left,bars.top,bars.right,bars.bottom)
            } else {
                @Suppress("DEPRECATION")
                v.setPadding(insets.systemWindowInsetLeft,insets.systemWindowInsetTop,insets.systemWindowInsetRight,insets.systemWindowInsetBottom)
            }
            insets
        }
        val header=row().apply { setBackgroundColor(navy);setPadding(dp(16),0,dp(16),0) }
        header.addView(text("MCM · Logo Studio",18f).apply { setTextColor(Color.WHITE);setTypeface(null,Typeface.BOLD) },LinearLayout.LayoutParams(0,dp(56),1f))
        root.addView(header)
        content=FrameLayout(this);root.addView(content,LinearLayout.LayoutParams(-1,0,1f))
        bottom=row();root.addView(bottom,LinearLayout.LayoutParams(-1,dp(60)))
        setContentView(root);root.requestApplyInsets();showPage()
    }
    private fun showPage() {
        generation++
        content.removeAllViews();bottom.removeAllViews()
        arrayOf("◈ Logo","☰ Menu","✎ Catatan").forEachIndexed { i,label ->
            bottom.addView(button(label) {
                (getSystemService(Context.INPUT_METHOD_SERVICE) as InputMethodManager).hideSoftInputFromWindow(content.windowToken,0)
                page=i;showPage()
            }.apply { isSelected=page==i;setBackgroundColor(if(page==i)0xffeaf0f8.toInt() else Color.WHITE) },LinearLayout.LayoutParams(0,-1,1f))
        }
        when(page) { 0 -> showStudio(); 1 -> showMenu(); else -> showNotes() }
    }
    private fun showStudio() {
        val layout=column().apply { setPadding(dp(12),0,dp(12),0) }
        logoView=LogoView(this) { step -> navigate(step) }
        layout.addView(logoView,LinearLayout.LayoutParams(-1,0,1f))
        status=text("",12f).apply { gravity=Gravity.CENTER }
        layout.addView(status,LinearLayout.LayoutParams(-1,dp(20)))
        val navigation=row()
        navigation.addView(button("❮","Logo sebelumnya"){navigate(-1)},LinearLayout.LayoutParams(dp(64),dp(48)))
        counter=text("").apply { gravity=Gravity.CENTER }
        navigation.addView(counter,LinearLayout.LayoutParams(0,dp(48),1f))
        navigation.addView(button("❯","Logo berikutnya"){navigate(1)},LinearLayout.LayoutParams(dp(64),dp(48)))
        layout.addView(navigation)
        paletteRow=row();layout.addView(paletteRow,LinearLayout.LayoutParams(-1,dp(64)))
        numberRow=row();layout.addView(numberRow,LinearLayout.LayoutParams(-1,dp(48)))
        content.addView(layout,FrameLayout.LayoutParams(-1,-1));updateStudio()
    }
    private fun navigate(step: Int) {current=(current+step+5)%5;prefs.edit().putInt("logo",current).apply();updateStudio()}
    private fun updateStudio() {
        counter.text="${current+1} / 5 · ${names[current]}"
        paletteRow.removeAllViews();numberRow.removeAllViews()
        arrayOf("Swatch 1","Swatch 2","Hitam–Putih","Putih–Hitam").forEachIndexed { i,label ->
            val swatch=SwatchView(this, i, label).apply {
                isSelected=selections[current]==i
                setOnClickListener { selections[current]=i;prefs.edit().putInt("palette$current",i).apply();updateStudio() }
            }
            paletteRow.addView(swatch,LinearLayout.LayoutParams(0,-1,1f))
        }
        for(i in 0..4) numberRow.addView(button("0${i+1}","Logo ${i+1}") {
            current=i;prefs.edit().putInt("logo",i).apply();updateStudio()
        }.apply { setBackgroundColor(if(current==i)0xffeaf0f8.toInt() else Color.WHITE) },LinearLayout.LayoutParams(0,-1,1f))
        val index=current;val preset=selections[index];val token=++generation
        val key=index*4+preset
        val bg=LogoPixels.presets[preset][3]
        logoView.setBackgroundColor(bg);logoView.bitmap=null;logoView.invalidate();status.text="Memuat…"
        worker.execute {
            try {
                val bitmap=rendered.get(key) ?: run {
                    val (original,pixels,mask)=sources.getOrPut(index) {
                        val b=assets.open(files[index]).use { BitmapFactory.decodeStream(it) } ?: error("Gambar tidak tersedia")
                        val p=IntArray(b.width*b.height);b.getPixels(p,0,b.width,0,0,b.width,b.height)
                        Triple(b,p,LogoPixels.mask(p,b.width,b.height,index))
                    }
                    val result=Bitmap.createBitmap(LogoPixels.recolor(pixels,mask,preset),original.width,original.height,Bitmap.Config.ARGB_8888)
                    rendered.put(key,result);result
                }
                runOnUiThread { if(!isDestroyed&&page==0&&token==generation) {logoView.bitmap=bitmap;logoView.invalidate();status.text=""} }
            } catch (_: Exception) { runOnUiThread {if(!isDestroyed&&page==0&&token==generation)status.text="Gagal memuat logo. Coba pilih ulang."} }
        }
    }
    private fun showMenu() {
        val layout=column().apply {setPadding(dp(20),dp(16),dp(20),dp(16))}
        layout.addView(text("Menu",22f))
        layout.addView(button("Reset warna logo aktif") {selections[current]=0;prefs.edit().putInt("palette$current",0).apply();Toast.makeText(this,"Warna direset",Toast.LENGTH_SHORT).show()})
        layout.addView(text("Native Kotlin · Offline\nSigning demo publik · untuk review internal",14f))
        content.addView(layout)
    }
    private fun readNotes(): JSONArray = try {JSONArray(prefs.getString("notes","[]"))} catch (_: Exception) {JSONArray()}
    private fun showNotes() {
        val scroll=ScrollView(this);val layout=column().apply {setPadding(dp(20),dp(16),dp(20),dp(24))}
        layout.addView(text("Catatan",22f))
        layout.addView(text("Tersimpan di perangkat ini. Catatan WebView lama belum dimigrasikan.",12f))
        val type=Spinner(this).apply {
            adapter=ArrayAdapter(this@MainActivity,android.R.layout.simple_spinner_dropdown_item,arrayOf("Bug","Pengembangan"));setSelection(noteType)
            onItemSelectedListener=object:AdapterView.OnItemSelectedListener {
                override fun onItemSelected(parent:AdapterView<*>?,view:View?,position:Int,id:Long){noteType=position;prefs.edit().putInt("noteType",position).apply()}
                override fun onNothingSelected(parent:AdapterView<*>?) {}
            }
        };layout.addView(type,LinearLayout.LayoutParams(-1,dp(48)))
        val input=EditText(this).apply {
            hint="Tulis bug atau ide…";gravity=Gravity.TOP;minLines=4;maxLines=8
            inputType=android.text.InputType.TYPE_CLASS_TEXT or android.text.InputType.TYPE_TEXT_FLAG_MULTI_LINE
            filters=arrayOf(android.text.InputFilter.LengthFilter(4000));setText(prefs.getString("draft",""))
            addTextChangedListener(object:TextWatcher {
                override fun beforeTextChanged(s:CharSequence?,start:Int,count:Int,after:Int){}
                override fun onTextChanged(s:CharSequence?,start:Int,before:Int,count:Int){prefs.edit().putString("draft",s.toString()).apply()}
                override fun afterTextChanged(s:Editable?){}
            })
        };layout.addView(input,LinearLayout.LayoutParams(-1,dp(140)))
        layout.addView(button("＋ Simpan catatan") {
            val value=input.text.toString().trim()
            if(value.isEmpty()){input.error="Isi catatan dahulu"}else{
                val old=readNotes();val next=JSONArray().put(JSONObject().put("text",value).put("type",if(noteType==0)"Bug" else "Pengembangan").put("logo",current+1).put("date",System.currentTimeMillis()))
                for(i in 0 until old.length())next.put(old.get(i))
                if(prefs.edit().putString("notes",next.toString()).remove("draft").commit())showPage()
                else Toast.makeText(this,"Gagal menyimpan; coba lagi",Toast.LENGTH_LONG).show()
            }
        })
        val notes=readNotes()
        if(notes.length()==0)layout.addView(text("Belum ada catatan."))
        for(i in 0 until notes.length()) {
            val note=notes.optJSONObject(i) ?: continue
            val card=column().apply {setPadding(0,dp(16),0,dp(8))}
            card.addView(text("${note.optString("type")} · Logo ${note.optInt("logo")} · ${DateFormat.getDateInstance().format(Date(note.optLong("date")))}",12f))
            card.addView(text(note.optString("text"),16f).apply {setTextIsSelectable(true)})
            card.addView(button("Hapus") {
                AlertDialog.Builder(this).setMessage("Hapus catatan ini?").setNegativeButton("Batal",null).setPositiveButton("Hapus") {_,_ ->
                    val remaining=JSONArray();for(j in 0 until notes.length())if(j!=i)remaining.put(notes.get(j))
                    if(prefs.edit().putString("notes",remaining.toString()).commit())showPage()
                    else Toast.makeText(this,"Gagal menghapus",Toast.LENGTH_LONG).show()
                }.show()
            });layout.addView(card)
        }
        scroll.addView(layout);content.addView(scroll)
    }
    override fun onSaveInstanceState(outState: Bundle) {outState.putInt("logo",current);outState.putInt("page",page);super.onSaveInstanceState(outState)}
    override fun onDestroy() {generation++;worker.shutdownNow();super.onDestroy()}

    private class LogoView(context:Context,val navigate:(Int)->Unit):View(context) {
        var bitmap:Bitmap?=null
        private val paint=Paint(Paint.ANTI_ALIAS_FLAG or Paint.FILTER_BITMAP_FLAG)
        private var x=0f;private var y=0f;private var time=0L
        init {contentDescription="Preview logo, geser kiri atau kanan";isClickable=true}
        override fun onDraw(canvas:Canvas) {
            super.onDraw(canvas)
            bitmap?.let { b -> val margin=16*resources.displayMetrics.density
                val scale=min((width-2*margin)/b.width,(height-2*margin)/b.height).coerceAtLeast(0f)
                val w=b.width*scale;val h=b.height*scale
                canvas.drawBitmap(b,null,RectF((width-w)/2,(height-h)/2,(width+w)/2,(height+h)/2),paint)
            }
        }
        override fun onTouchEvent(event:MotionEvent):Boolean {
            when(event.actionMasked){
                MotionEvent.ACTION_DOWN->{x=event.x;y=event.y;time=event.eventTime;return true}
                MotionEvent.ACTION_UP->{val dx=event.x-x;val dy=event.y-y
                    if(event.eventTime-time<900&&abs(dx)>55*resources.displayMetrics.density&&abs(dx)>abs(dy)*1.5f)navigate(if(dx<0)1 else -1) else performClick()
                    return true}
                MotionEvent.ACTION_CANCEL->return true
            };return true
        }
        override fun performClick():Boolean {super.performClick();return true}
    }
    private inner class SwatchView(context:Context,val preset:Int,val label:String):View(context) {
        private val paint=Paint(Paint.ANTI_ALIAS_FLAG)
        init {contentDescription=label;isClickable=true;isFocusable=true}
        override fun onDraw(canvas:Canvas) {
            super.onDraw(canvas);val density=resources.displayMetrics.density
            if(isSelected){paint.color=navy;paint.style=Paint.Style.STROKE;paint.strokeWidth=2*density;canvas.drawRoundRect(4*density,4*density,width-4*density,height-4*density,10*density,10*density,paint)}
            paint.style=Paint.Style.FILL
            val radius=min(8*density,width/12f)
            for(i in 0..2){paint.color=LogoPixels.presets[preset][i];canvas.drawCircle(width/2f+(i-1)*radius*2.5f,22*density,radius,paint)
                paint.style=Paint.Style.STROKE;paint.strokeWidth=density;paint.color=0xff94a3b8.toInt();canvas.drawCircle(width/2f+(i-1)*radius*2.5f,22*density,radius,paint);paint.style=Paint.Style.FILL}
            paint.color=navy;paint.textSize=10*resources.displayMetrics.scaledDensity;paint.textAlign=Paint.Align.CENTER
            canvas.drawText(label,width/2f,48*density,paint)
        }
        override fun setSelected(selected:Boolean){super.setSelected(selected);invalidate()}
    }
}
