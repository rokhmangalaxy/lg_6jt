package id.mcm.logopreview

import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.content.Intent
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
    private val files = LogoCatalog.files
    private val names = LogoCatalog.names
    private val rendered = object : android.util.LruCache<Int, Bitmap>(32*1024) {
        override fun sizeOf(key: Int, value: Bitmap): Int = (value.allocationByteCount/1024).coerceAtLeast(1)
    }
    private lateinit var content: FrameLayout
    private lateinit var logoView: LogoView
    private lateinit var counter: TextView
    private lateinit var status: TextView
    private lateinit var paletteRow: LinearLayout
    private lateinit var numberRow: GridLayout
    private lateinit var numberScroll: ScrollView
    private lateinit var downloadButton: Button
    private var pendingExportLogo = -1
    private var pendingExportPreset = 0
    private var current = 0
    private var page = 0
    private val favorites by lazy { FavoriteStore(prefs) }
    private var favoritesPage=0
    private var favoriteColumns=3
    private lateinit var favoriteButton:Button
    private lateinit var bottomNav: LinearLayout
    private var uniformCap = true
    private var uniformAngle = 0
    private var uniformExport: IntArray? = null
    @Volatile private var generation = 0
    private val selections = IntArray(LogoCatalog.count)
    private var noteType = 0
    private fun dp(n: Int) = (n * resources.displayMetrics.density).toInt()
    private fun column() = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL }
    private fun row() = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER_VERTICAL }
    private fun text(value: String, size: Float = 14f) = TextView(this).apply { text=value; textSize=size; setTextColor(navy); gravity=Gravity.CENTER_VERTICAL }
    private fun button(label: String, description: String = label, action: () -> Unit) = Button(this).apply {
        text=label; textSize=13f; isAllCaps=false; contentDescription=description
        setTextColor(navy); minWidth=0; minimumWidth=0
        setPadding(dp(8),0,dp(8),0)
        setLayerType(View.LAYER_TYPE_SOFTWARE,null)
        val density=resources.displayMetrics.density
        background=android.graphics.drawable.StateListDrawable().apply {
            addState(intArrayOf(android.R.attr.state_pressed),NeoSurface(density,true))
            addState(intArrayOf(android.R.attr.state_selected),NeoSurface(density,true))
            addState(intArrayOf(),NeoSurface(density))
        }
        setOnClickListener { action() }
    }
    override fun onCreate(state: Bundle?) {
        super.onCreate(state)
        current=state?.getInt("clientSetLogo") ?: prefs.getInt("clientSetLogo",0)
        page=state?.getInt("activeTab") ?: 0
        uniformCap=state?.getBoolean("uniformCap") ?: prefs.getBoolean("uniformCap",true)
        uniformAngle=(state?.getInt("uniformAngle") ?: prefs.getInt("uniformAngle",0)).coerceIn(0,3)
        uniformExport=state?.getIntArray("uniformExport")
        pendingExportLogo=state?.getInt("exportLogo",-1) ?: -1
        pendingExportPreset=state?.getInt("exportPreset",0) ?: 0
        favoritesPage=state?.getInt("favoritesPage")?:0
        favoriteColumns=prefs.getInt("favoriteColumns",3).let{if(it==5)5 else 3}
        noteType=prefs.getInt("noteType",0)
        for(i in selections.indices) selections[i]=prefs.getInt("clientSetPalette$i",0).coerceIn(0,3)
        current=current.coerceIn(0,LogoCatalog.count-1);page=page.coerceIn(0,2)
        val root=column().apply { setBackgroundColor(NeoSurface.BASE) }
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
        val header=row().apply { setBackgroundColor(NeoSurface.BASE);setPadding(dp(16),0,dp(16),0) }
        header.addView(text("MCM · Logo Studio",18f).apply { setTextColor(navy);setTypeface(null,Typeface.BOLD) },LinearLayout.LayoutParams(0,dp(56),1f))
        downloadButton=button("↓","Download gambar") { if(page==1)beginUniformExport() else if(page==0)beginExport() }.apply {
            textSize=24f;isEnabled=false
        }
        header.addView(downloadButton,LinearLayout.LayoutParams(dp(56),dp(56)))
        root.addView(header)
        content=FrameLayout(this);root.addView(content,LinearLayout.LayoutParams(-1,0,1f))
        bottomNav=row().apply {
            setPadding(dp(8),dp(6),dp(8),dp(6))
            setBackgroundColor(0xffe1e7ef.toInt());elevation=dp(6).toFloat()
        }
        arrayOf("Logo","♥ Favorit","Seragam").forEachIndexed { index,label ->
            val target=intArrayOf(0,2,1)[index]
            bottomNav.addView(Button(this).apply{
                text=label;isAllCaps=false;textSize=13f;contentDescription="Menu $label"
                minWidth=0;minimumWidth=0;setPadding(0,0,0,0)
                setOnClickListener{page=target;showPage()}
            },LinearLayout.LayoutParams(0,dp(52),1f).apply{setMargins(dp(3),0,dp(3),0)})
        }
        root.addView(bottomNav)
        setContentView(root);root.requestApplyInsets();showPage()
    }
    private fun showPage() {
        generation++
        content.removeAllViews()
        for(i in 0..2){
            val selected=page==intArrayOf(0,2,1)[i]
            (bottomNav.getChildAt(i) as Button).apply{
                isSelected=selected;setTextColor(if(selected)Color.WHITE else navy)
                backgroundTintList=null
                background=android.graphics.drawable.GradientDrawable().apply{setColor(if(selected)navy else Color.TRANSPARENT);cornerRadius=dp(18).toFloat()}
            }
        }
        downloadButton.isEnabled=false
        if(page==1)showUniform() else if(page==2)showFavorites() else showStudio()
    }
    private fun refreshFavoriteButton(){
        val liked=favorites.contains(current)
        favoriteButton.text=if(liked)"♥" else "♡"
        favoriteButton.contentDescription=if(liked)"Hapus dari favorit" else "Tambahkan ke favorit"
        favoriteButton.setTextColor(if(liked)0xffdc2626.toInt() else navy)
    }
    private fun toggleCurrentFavorite(){favorites.toggle(current);refreshFavoriteButton()}
    private fun showFavorites(){
        val layout=column().apply{setPadding(dp(12),dp(8),dp(12),0)}
        val items=favorites.indices()
        favoritesPage=favoritesPage.coerceIn(0,FavoriteStore.pageCount(items.size,favoriteColumns)-1)
        layout.addView(text("♥ Favorit · ${items.size} logo",20f))
        layout.addView(button("Copy nama favorit","Salin semua nama logo favorit"){
            val allNames=favorites.indices().joinToString("\n"){names[it]}
            if(allNames.isNotEmpty()){
                val clipboard=getSystemService(Context.CLIPBOARD_SERVICE) as android.content.ClipboardManager
                clipboard.setPrimaryClip(android.content.ClipData.newPlainText("Nama logo favorit",allNames))
                Toast.makeText(this,"${favorites.indices().size} nama favorit disalin",Toast.LENGTH_SHORT).show()
            }
        }.apply{isEnabled=items.isNotEmpty()},LinearLayout.LayoutParams(-1,dp(48)))
        val controls=row()
        for(columns in listOf(3,5))controls.addView(button("$columns kolom"){
            favoriteColumns=columns;favoritesPage=0;prefs.edit().putInt("favoriteColumns",columns).apply();showPage()
        }.apply{isSelected=columns==favoriteColumns},LinearLayout.LayoutParams(0,dp(48),1f))
        layout.addView(controls)
        val grid=GridLayout(this).apply{columnCount=favoriteColumns}
        val scroll=ScrollView(this).apply{addView(grid)}
        layout.addView(scroll,LinearLayout.LayoutParams(-1,0,1f))
        if(items.isEmpty())grid.addView(text("Belum ada favorit. Ketuk ♡ di pojok preview logo.",14f))
        val token=++generation
        for((position,id) in FavoriteStore.page(items,favoriteColumns,favoritesPage).withIndex()){
            val tile=column().apply{setPadding(dp(3),dp(4),dp(3),dp(4))}
            val image=ImageView(this).apply{
                scaleType=ImageView.ScaleType.FIT_CENTER;contentDescription="Buka ${names[id]}"
                setOnClickListener{current=id;prefs.edit().putInt("clientSetLogo",id).apply();page=0;showPage()}
            }
            tile.addView(image,LinearLayout.LayoutParams(-1,dp(if(favoriteColumns==3)96 else 64)))
            tile.addView(button("${id+1} ♥","Hapus ${names[id]} dari favorit"){favorites.toggle(id);showPage()},LinearLayout.LayoutParams(-1,dp(48)))
            grid.addView(tile,GridLayout.LayoutParams(GridLayout.spec(GridLayout.UNDEFINED),GridLayout.spec(position%favoriteColumns,1f)).apply{width=0;height=-2})
            worker.execute{
                try{
                    val thumbnail=LogoVectorRenderer.render(assets,id,selections[id],240)
                    runOnUiThread{if(!isDestroyed&&page==2&&generation==token)image.setImageBitmap(thumbnail)else thumbnail.recycle()}
                }catch(_:Exception){runOnUiThread{if(!isDestroyed&&generation==token)image.contentDescription="Thumbnail gagal dimuat: ${names[id]}"}}
            }
        }
        val pager=row()
        pager.addView(button("❮","Halaman favorit sebelumnya"){favoritesPage--;showPage()}.apply{isEnabled=favoritesPage>0},LinearLayout.LayoutParams(dp(56),dp(48)))
        pager.addView(text("${favoritesPage+1} / ${FavoriteStore.pageCount(items.size,favoriteColumns)}").apply{gravity=Gravity.CENTER},LinearLayout.LayoutParams(0,dp(48),1f))
        pager.addView(button("❯","Halaman favorit berikutnya"){favoritesPage++;showPage()}.apply{isEnabled=favoritesPage+1<FavoriteStore.pageCount(items.size,favoriteColumns)},LinearLayout.LayoutParams(dp(56),dp(48)))
        layout.addView(pager);content.addView(layout)
    }
    private fun showUniform() {
        val layout=column().apply { setPadding(dp(12),0,dp(12),0) }
        val swatches=arrayOf("Swatch 1","Swatch 2","Hitam–Putih","Putih–Hitam")
        layout.addView(text("${names[current]} · ${swatches[selections[current]]}",14f))
        val image=ImageView(this).apply { scaleType=ImageView.ScaleType.FIT_CENTER;contentDescription="Mockup seragam dengan logo aktif" }
        layout.addView(image,LinearLayout.LayoutParams(-1,0,1f))
        val types=row()
        arrayOf("Topi","Kemeja").forEachIndexed { i,label ->
            types.addView(button(label) { uniformCap=i==0;uniformAngle=0;saveUniform();showPage() }.apply {isSelected=uniformCap==(i==0)},LinearLayout.LayoutParams(0,dp(48),1f))
        }
        layout.addView(types)
        val angles=row()
        val labels=if(uniformCap)arrayOf("Depan","Serong kiri","Samping kiri","Kolase")else arrayOf("Depan","Serong depan","Belakang","Kolase")
        labels.forEachIndexed { i,label ->angles.addView(button(label){uniformAngle=i;saveUniform();showPage()}.apply{isSelected=uniformAngle==i},LinearLayout.LayoutParams(0,dp(48),1f)) }
        layout.addView(angles)
        layout.addView(text("Simulasi penempatan 2D · bukan pola bordir produksi.\nUbah logo dan swatch melalui tab Logo.",12f))
        content.addView(layout)
        val token=++generation;val index=current;val preset=selections[index];val cap=uniformCap;val angle=uniformAngle
        worker.execute {
            try {
                val bitmap=UniformRenderer.render(assets,index,preset,cap,angle)
                runOnUiThread {
                    if(!isDestroyed&&page==1&&token==generation){image.setImageBitmap(bitmap);downloadButton.isEnabled=uniformExport==null}
                    else bitmap.recycle()
                }
            }catch(error:Exception){runOnUiThread {if(!isDestroyed&&page==1&&token==generation)Toast.makeText(this,"Mockup gagal dimuat",Toast.LENGTH_LONG).show()}}
        }
    }
    private fun saveUniform(){prefs.edit().putBoolean("uniformCap",uniformCap).putInt("uniformAngle",uniformAngle).apply()}
    @Suppress("DEPRECATION")
    private fun beginUniformExport(){
        if(uniformExport!=null)return
        uniformExport=intArrayOf(current,selections[current],if(uniformCap)1 else 0,uniformAngle)
        val intent=Intent(Intent.ACTION_CREATE_DOCUMENT).apply{
            addCategory(Intent.CATEGORY_OPENABLE);type="image/jpeg"
            putExtra(Intent.EXTRA_TITLE,"MCM-seragam-${current+1}-swatch-${selections[current]+1}.jpg")
        }
        try{startActivityForResult(intent,1002)}catch(_:android.content.ActivityNotFoundException){uniformExport=null;Toast.makeText(this,"Aplikasi penyimpan tidak tersedia",Toast.LENGTH_LONG).show()}
    }
    private fun showStudio() {
        val layout=column().apply { setPadding(dp(12),0,dp(12),0) }
        logoView=LogoView(this) { step -> navigate(step) }
        val square=object:FrameLayout(this){
            override fun onMeasure(widthSpec:Int,heightSpec:Int){
                val w=View.MeasureSpec.getSize(widthSpec)
                val side=minOf(w,(resources.displayMetrics.heightPixels*.36f).toInt())
                logoView.measure(View.MeasureSpec.makeMeasureSpec(side,View.MeasureSpec.EXACTLY),View.MeasureSpec.makeMeasureSpec(side,View.MeasureSpec.EXACTLY))
                if(childCount>1)getChildAt(1).measure(View.MeasureSpec.makeMeasureSpec(dp(48),View.MeasureSpec.EXACTLY),View.MeasureSpec.makeMeasureSpec(dp(48),View.MeasureSpec.EXACTLY))
                setMeasuredDimension(w,side)
            }
            override fun onLayout(changed:Boolean,l:Int,t:Int,r:Int,b:Int){
                super.onLayout(changed,l,t,r,b)
                if(childCount>1){
                    val right=(width+logoView.measuredWidth)/2-dp(12)
                    getChildAt(1).layout(right-dp(48),height-dp(60),right,height-dp(12))
                }
            }
        }
        square.addView(logoView,FrameLayout.LayoutParams(-2,-2,Gravity.CENTER))
        favoriteButton=button("♡","Tambahkan ke favorit"){toggleCurrentFavorite()}.apply{textSize=25f}
        square.addView(favoriteButton,FrameLayout.LayoutParams(dp(48),dp(48),Gravity.BOTTOM or Gravity.END).apply{setMargins(0,0,dp(12),dp(12))})
        layout.addView(square,LinearLayout.LayoutParams(-1,-2))
        status=text("",12f).apply { gravity=Gravity.CENTER }
        layout.addView(status,LinearLayout.LayoutParams(-1,dp(20)))
        val navigation=row()
        navigation.addView(button("❮","Logo sebelumnya"){navigate(-1)},LinearLayout.LayoutParams(dp(64),dp(48)))
        counter=text("").apply { gravity=Gravity.CENTER }
        navigation.addView(counter,LinearLayout.LayoutParams(0,dp(48),1f))
        navigation.addView(button("❯","Logo berikutnya"){navigate(1)},LinearLayout.LayoutParams(dp(64),dp(48)))
        layout.addView(navigation)
        paletteRow=row();layout.addView(paletteRow,LinearLayout.LayoutParams(-1,dp(64)))
        layout.addView(text("Semua variasi · ketuk thumbnail untuk memilih",12f))
        numberRow=GridLayout(this).apply {columnCount=3;alignmentMode=GridLayout.ALIGN_BOUNDS}
        numberScroll=ScrollView(this).apply {isFillViewport=false;addView(numberRow,android.view.ViewGroup.LayoutParams(-1,-2))}
        layout.addView(numberScroll,LinearLayout.LayoutParams(-1,0,1f))
        content.addView(layout,FrameLayout.LayoutParams(-1,-1));updateStudio()
    }
    private fun selectLogo(index:Int){
        current=index;prefs.edit().putInt("clientSetLogo",index).apply();updateStudio()
    }
    private fun navigate(step: Int) {current=LogoCatalog.next(current,step);prefs.edit().putInt("clientSetLogo",current).apply();updateStudio()}
    private fun updateStudio() {
        val collection=LogoCatalog.collection(current)
        refreshFavoriteButton()
        counter.text="${current-collection.first+1} / ${collection.count()} · ${names[current]}"
        paletteRow.removeAllViews();numberRow.removeAllViews()
        arrayOf("Swatch 1","Swatch 2","Hitam–Putih","Putih–Hitam").forEachIndexed { i,label ->
            val swatch=SwatchView(this, i, label).apply {
                isSelected=selections[current]==i
                setOnClickListener { selections[current]=i;prefs.edit().putInt("clientSetPalette$current",i).apply();updateStudio() }
            }
            paletteRow.addView(swatch,LinearLayout.LayoutParams(0,-1,1f))
        }
        val thumbnails=mutableListOf<Pair<Int,ImageView>>()
        for(i in files.indices){
            val tile=column().apply {setPadding(dp(4),dp(4),dp(4),dp(4))}
            val thumb=ImageView(this).apply {
                scaleType=ImageView.ScaleType.FIT_CENTER
                contentDescription="Pilih ${names[i]}";setBackgroundColor(LogoCatalog.background(i,selections[i]))
                setOnClickListener {selectLogo(i)}
            }
            tile.addView(thumb,LinearLayout.LayoutParams(-1,dp(84)))
            tile.addView(button(String.format(java.util.Locale.ROOT,"%02d",i+1),"Pilih ${names[i]}"){selectLogo(i)}.apply {isSelected=current==i},LinearLayout.LayoutParams(-1,dp(40)))
            numberRow.addView(tile,GridLayout.LayoutParams(GridLayout.spec(GridLayout.UNDEFINED),GridLayout.spec(i%3,1f)).apply{width=0;height=-2})
            thumbnails.add(i to thumb)
        }
        val index=current;val preset=selections[index];val token=++generation
        val bg=LogoCatalog.background(index,preset)
        logoView.canvasBackground=bg;logoView.bitmap=null;logoView.invalidate();status.text="Memuat…";downloadButton.isEnabled=false
        worker.execute {
            if(token!=generation)return@execute
            try {
                val bitmap=renderLogo(index,preset)
                runOnUiThread { if(!isDestroyed&&page==0&&token==generation) {logoView.bitmap=bitmap;logoView.invalidate();status.text="";downloadButton.isEnabled=pendingExportLogo<0} }
                for((id,view) in thumbnails){
                    if(token!=generation)break
                    val thumbnail=LogoVectorRenderer.render(assets,id,selections[id],240)
                    runOnUiThread {
                        if(!isDestroyed&&page==0&&token==generation)view.setImageBitmap(thumbnail) else thumbnail.recycle()
                    }
                }
            } catch (error: Exception) {
                android.util.Log.e("MCMLogo", "Preview failed: ${files[index]}, preset=$preset", error)
                runOnUiThread {if(!isDestroyed&&page==0&&token==generation)status.text="Logo ${index+1} gagal dimuat. Coba pilih ulang."}
            }
        }
    }
    // Called only on the single background executor, shared by preview and export.
    private fun renderLogo(index:Int,preset:Int):Bitmap {
        val key=index*4+preset
        return rendered.get(key) ?: LogoVectorRenderer.render(assets,index,preset).also {rendered.put(key,it)}
    }

    @Suppress("DEPRECATION")
    private fun beginExport() {
        if(pendingExportLogo>=0||logoView.bitmap==null)return
        pendingExportLogo=current;pendingExportPreset=selections[current];downloadButton.isEnabled=false
        val name="MCM-${files[current].substringAfterLast("/").removeSuffix(".png")}-swatch-${pendingExportPreset+1}.png"
        val intent=Intent(Intent.ACTION_CREATE_DOCUMENT).apply {
            addCategory(Intent.CATEGORY_OPENABLE);type="image/png";putExtra(Intent.EXTRA_TITLE,name)
        }
        try {startActivityForResult(intent,1001)}catch(_:android.content.ActivityNotFoundException){
            pendingExportLogo=-1;downloadButton.isEnabled=true
            Toast.makeText(this,"Aplikasi penyimpan berkas tidak tersedia",Toast.LENGTH_LONG).show()
        }
    }
    @Deprecated("Platform result API retained for SDK-only native app")
    override fun onActivityResult(requestCode:Int,resultCode:Int,data:Intent?) {
        super.onActivityResult(requestCode,resultCode,data)
        if(requestCode==1002){
            val config=uniformExport;uniformExport=null
            val uri=data?.data
            if(resultCode==RESULT_OK&&uri!=null&&config!=null)worker.execute{
                try{
                    val bitmap=UniformRenderer.render(assets,config[0],config[1],config[2]==1,config[3])
                    try{contentResolver.openOutputStream(uri,"wt").use{stream->checkNotNull(stream);check(bitmap.compress(Bitmap.CompressFormat.JPEG,94,stream))}}finally{bitmap.recycle()}
                    runOnUiThread{if(!isDestroyed)Toast.makeText(this,"Mockup JPG tersimpan",Toast.LENGTH_SHORT).show()}
                }catch(_:Exception){runOnUiThread{if(!isDestroyed)Toast.makeText(this,"Gagal menyimpan mockup",Toast.LENGTH_LONG).show()}}
            }
            if(page==1)showPage()
            return
        }
        if(requestCode!=1001)return
        val index=pendingExportLogo;val preset=pendingExportPreset;val uri=data?.data
        pendingExportLogo=-1
        if(resultCode!=RESULT_OK||uri==null||index !in files.indices){downloadButton.isEnabled=logoView.bitmap!=null;return}
        status.text="Menyimpan PNG…"
        worker.execute {
            try {
                val bitmap=renderLogo(index,preset)
                contentResolver.openOutputStream(uri,"wt").use { stream ->
                    checkNotNull(stream){"Tujuan penyimpanan tidak dapat dibuka"}
                    LogoExporter.write(bitmap,stream)
                }
                runOnUiThread {if(!isDestroyed){status.text="PNG tersimpan";downloadButton.isEnabled=logoView.bitmap!=null;Toast.makeText(this,"Logo PNG tersimpan",Toast.LENGTH_SHORT).show()}}
            }catch(error:Exception){
                android.util.Log.e("MCMLogo","PNG export failed",error)
                runOnUiThread {if(!isDestroyed){status.text="Gagal menyimpan PNG. Coba lagi.";downloadButton.isEnabled=logoView.bitmap!=null}}
            }
        }
    }
    private fun showMenu() {
        val layout=column().apply {setPadding(dp(20),dp(16),dp(20),dp(16))}
        layout.addView(text("Menu",22f))
        layout.addView(button("Reset warna logo aktif") {selections[current]=0;prefs.edit().putInt("clientSetPalette$current",0).apply();Toast.makeText(this,"Warna direset",Toast.LENGTH_SHORT).show()})
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
    override fun onSaveInstanceState(outState: Bundle) {outState.putInt("favoritesPage",favoritesPage);outState.putInt("activeTab",page);outState.putBoolean("uniformCap",uniformCap);outState.putInt("uniformAngle",uniformAngle);outState.putIntArray("uniformExport",uniformExport);outState.putInt("clientSetLogo",current);outState.putInt("exportLogo",pendingExportLogo);outState.putInt("exportPreset",pendingExportPreset);super.onSaveInstanceState(outState)}
    override fun onDestroy() {generation++;worker.shutdown();super.onDestroy()}

    private class LogoView(context:Context,val navigate:(Int)->Unit):View(context) {
        var bitmap:Bitmap?=null
        var canvasBackground=Color.WHITE
        private val paint=Paint(Paint.ANTI_ALIAS_FLAG or Paint.FILTER_BITMAP_FLAG)
        private var x=0f;private var y=0f;private var time=0L
        init {contentDescription="Preview logo, geser kiri atau kanan";isClickable=true;setLayerType(LAYER_TYPE_SOFTWARE,null)}
        override fun onDraw(canvas:Canvas) {
            super.onDraw(canvas)
            val d=resources.displayMetrics.density
            val card=RectF(10*d,10*d,width-10*d,height-10*d)
            paint.color=NeoSurface.BASE;paint.setShadowLayer(7*d,4*d,4*d,0xffb8c5d5.toInt());canvas.drawRoundRect(card,20*d,20*d,paint)
            paint.setShadowLayer(7*d,-4*d,-4*d,Color.WHITE);canvas.drawRoundRect(card,20*d,20*d,paint);paint.clearShadowLayer()
            paint.color=canvasBackground;canvas.drawRoundRect(card,20*d,20*d,paint)
            bitmap?.let { b -> val margin=24*resources.displayMetrics.density
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
        init {contentDescription=label;isClickable=true;isFocusable=true;setLayerType(LAYER_TYPE_SOFTWARE,null)}
        override fun onDraw(canvas:Canvas) {
            super.onDraw(canvas);val density=resources.displayMetrics.density
            NeoSurface(density,isSelected||isPressed).apply {setBounds(0,0,width,height);draw(canvas)}
            if(isSelected){paint.color=navy;paint.style=Paint.Style.STROKE;paint.strokeWidth=density;canvas.drawRoundRect(7*density,7*density,width-7*density,height-7*density,12*density,12*density,paint)}
            paint.style=Paint.Style.FILL
            val radius=min(8*density,width/12f)
            for(i in 0..2){paint.color=LogoPixels.presets[preset][i];canvas.drawCircle(width/2f+(i-1)*radius*2.5f,22*density,radius,paint)
                paint.style=Paint.Style.STROKE;paint.strokeWidth=density;paint.color=0xff94a3b8.toInt();canvas.drawCircle(width/2f+(i-1)*radius*2.5f,22*density,radius,paint);paint.style=Paint.Style.FILL}
            paint.color=navy;paint.textSize=10*resources.displayMetrics.scaledDensity;paint.textAlign=Paint.Align.CENTER
            canvas.drawText(label,width/2f,48*density,paint)
        }
        override fun drawableStateChanged(){super.drawableStateChanged();invalidate()}
        override fun setSelected(selected:Boolean){super.setSelected(selected);invalidate()}
    }
}
