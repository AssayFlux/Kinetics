package org.assayflux.kinetics

import android.annotation.SuppressLint
import android.webkit.WebResourceRequest
import android.webkit.WebView
import android.widget.FrameLayout
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.webkit.WebViewAssetLoader
import androidx.webkit.WebViewClientCompat
import org.json.JSONObject

private const val VIEWER_URL = "https://appassets.androidplatform.net/assets/structure-viewer/structure-viewer.html"

/** Offline-first renderer smoke preview. Production file import is a separate S1 gate. */
@SuppressLint("SetJavaScriptEnabled")
@Composable
internal fun StructureViewerPreview() {
    val context = LocalContext.current
    val payload = remember {
        """{"schema":"kinetics.structure-view.v1","source_format":"pdb","coordinate_unit":"angstrom","atom_count":8,"atoms":[{"serial":1,"name":"N","residue":"GLY","chain":"A","residue_number":1,"element":"N","xyz":[0.0,0.0,0.0]},{"serial":2,"name":"CA","residue":"GLY","chain":"A","residue_number":1,"element":"C","xyz":[1.45,0.1,0.0]},{"serial":3,"name":"C","residue":"GLY","chain":"A","residue_number":1,"element":"C","xyz":[2.0,1.48,0.1]},{"serial":4,"name":"O","residue":"GLY","chain":"A","residue_number":1,"element":"O","xyz":[1.35,2.45,0.1]},{"serial":5,"name":"N","residue":"ALA","chain":"A","residue_number":2,"element":"N","xyz":[3.25,1.55,0.0]},{"serial":6,"name":"CA","residue":"ALA","chain":"A","residue_number":2,"element":"C","xyz":[4.0,2.8,0.2]},{"serial":7,"name":"C","residue":"ALA","chain":"A","residue_number":2,"element":"C","xyz":[5.45,2.55,0.0]},{"serial":8,"name":"O","residue":"ALA","chain":"A","residue_number":2,"element":"O","xyz":[6.1,3.5,0.1]}],"limitations":["Synthetic UI preview fixture only; not experimental structure data.","Coordinates and annotations only; no inferred bonds or biological interpretation."]}"""
    }
    val assetLoader = remember(context) {
        WebViewAssetLoader.Builder()
            .addPathHandler("/assets/", WebViewAssetLoader.AssetsPathHandler(context))
            .build()
    }
    val webView = remember(context) {
        WebView(context).apply {
            settings.javaScriptEnabled = true
            settings.allowFileAccess = false
            settings.allowContentAccess = false
            settings.domStorageEnabled = false
            settings.javaScriptCanOpenWindowsAutomatically = false
            settings.setSupportMultipleWindows(false)
            settings.mixedContentMode = android.webkit.WebSettings.MIXED_CONTENT_NEVER_ALLOW
            settings.loadsImagesAutomatically = false
            settings.blockNetworkLoads = true
            webViewClient = object : WebViewClientCompat() {
                override fun shouldInterceptRequest(view: WebView, request: WebResourceRequest) =
                    assetLoader.shouldInterceptRequest(request.url)
                override fun shouldOverrideUrlLoading(view: WebView, request: WebResourceRequest): Boolean = true
                override fun onPageFinished(view: WebView, url: String) {
                    if (url == VIEWER_URL) {
                        val encoded = JSONObject.quote(payload)
                        view.evaluateJavascript(
                            "window.KineticsStructureViewer.load(JSON.parse($encoded));",
                            null,
                        )
                    }
                }
            }
            loadUrl(VIEWER_URL)
        }
    }
    DisposableEffect(webView) {
        onDispose {
            webView.stopLoading()
            webView.loadUrl("about:blank")
            webView.destroy()
        }
    }
    androidx.compose.material3.Card {
        androidx.compose.foundation.layout.Column(
            modifier = Modifier.fillMaxWidth(),
        ) {
            Text(
                "Offline-first structure viewer · preview fixture",
                modifier = Modifier.fillMaxWidth().then(Modifier),
                style = MaterialTheme.typography.titleSmall,
                color = MaterialTheme.colorScheme.onSurface,
            )
            AndroidView(
                factory = { FrameLayout(it).apply { addView(webView) } },
                modifier = Modifier.fillMaxWidth().height(440.dp),
            )
        }
    }
}
