package id.mcm.logopreview

import android.content.SharedPreferences

/** Persist stable asset IDs, never grid positions or display names. */
class FavoriteStore(private val prefs:SharedPreferences){
    fun ids():Set<String> = prefs.getStringSet("favoriteLogoIds",emptySet())!!.toSet()
    fun contains(index:Int)=LogoCatalog.files[index] in ids()
    fun toggle(index:Int):Boolean{
        val values=ids().toMutableSet();val id=LogoCatalog.files[index]
        val added=if(id in values){values.remove(id);false}else{values.add(id);true}
        prefs.edit().putStringSet("favoriteLogoIds",values).apply();return added
    }
    fun indices()=LogoCatalog.files.indices.filter{contains(it)}
    companion object{
        fun pageCount(size:Int,columns:Int)=maxOf(1,(size+columns*2-1)/(columns*2))
        fun page(items:List<Int>,columns:Int,page:Int):List<Int>{
            require(columns==3||columns==5)
            val safe=page.coerceIn(0,pageCount(items.size,columns)-1)
            return items.drop(safe*columns*2).take(columns*2)
        }
    }
}
