package id.mcm.logopreview

import android.annotation.SuppressLint
import android.app.Activity
import android.graphics.Color
import android.os.Bundle
import android.webkit.WebResourceRequest
import android.webkit.WebView
import android.webkit.WebViewClient

/** Offline Kotlin shell for the same canvas-based logo studio. No JS/native bridge. */
class MainActivity : Activity() {
    private lateinit var webView: WebView

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        webView = WebView(this)
        webView.setBackgroundColor(Color.WHITE)
        webView.settings.apply {
            javaScriptEnabled = true
            allowFileAccess = false
            allowContentAccess = false
            blockNetworkLoads = true
            domStorageEnabled = false
        }
        webView.webViewClient = object : WebViewClient() {
            override fun shouldOverrideUrlLoading(view: WebView, request: WebResourceRequest): Boolean = true
        }
        setContentView(webView)
        // Read only the packaged asset; base64 images require neither file access nor internet.
        val html = assets.open("index.html").bufferedReader().use { it.readText() }
        webView.loadDataWithBaseURL("https://mcm.invalid/?android=1", html, "text/html", "UTF-8", null)
    }

    override fun onDestroy() {
        webView.destroy()
        super.onDestroy()
    }
}
