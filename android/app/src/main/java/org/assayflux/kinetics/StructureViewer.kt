package org.assayflux.kinetics

import android.annotation.SuppressLint
import android.database.Cursor
import android.net.Uri
import android.provider.OpenableColumns
import android.webkit.WebResourceRequest
import android.webkit.WebView
import android.widget.FrameLayout
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.webkit.WebViewAssetLoader
import androidx.webkit.WebViewClientCompat
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.io.ByteArrayOutputStream
import java.nio.ByteBuffer
import java.nio.charset.CodingErrorAction

private const val VIEWER_URL = "https://appassets.androidplatform.net/assets/structure-viewer/structure-viewer.html"
private const val MAX_STRUCTURE_SOURCE_BYTES = 16 * 1024 * 1024

private data class ImportedStructure(
    val payloadJson: String,
    val name: String,
    val sourceHash: String,
    val sessionJson: String,
)

private fun readDisplayName(context: android.content.Context, uri: Uri): String {
    val cursor: Cursor? = context.contentResolver.query(
        uri, arrayOf(OpenableColumns.DISPLAY_NAME), null, null, null,
    )
    return cursor.use {
        if (it != null && it.moveToFirst()) it.getString(0) ?: "structure"
        else uri.lastPathSegment ?: "structure"
    }
}

private fun readBounded(context: android.content.Context, uri: Uri): ByteArray {
    val input = context.contentResolver.openInputStream(uri)
        ?: error("The selected document could not be opened")
    return input.use { stream ->
        val output = ByteArrayOutputStream()
        val buffer = ByteArray(32 * 1024)
        var total = 0
        while (true) {
            val count = stream.read(buffer)
            if (count < 0) break
            total += count
            require(total <= MAX_STRUCTURE_SOURCE_BYTES) {
                "Structure file exceeds the 16 MiB import limit"
            }
            output.write(buffer, 0, count)
        }
        output.toByteArray()
    }
}

/** Offline-first structure viewer with bounded SAF import; no network or generic JS bridge. */
@SuppressLint("SetJavaScriptEnabled")
@Composable
internal fun StructureViewerPreview() {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    var payloadJson by remember { mutableStateOf<String?>(null) }
    var sessionExportJson by remember { mutableStateOf<String?>(null) }
    var sourceLabel by remember { mutableStateOf("Synthetic preview fixture") }
    var importMessage by remember {
        mutableStateOf("Choose a local PDB or mmCIF file to inspect it offline.")
    }
    val exportPicker = rememberLauncherForActivityResult(
        ActivityResultContracts.CreateDocument("application/json"),
    ) { uri ->
        val export = sessionExportJson
        if (uri != null && export != null) {
            scope.launch {
                val result = withContext(Dispatchers.IO) {
                    runCatching {
                        context.contentResolver.openOutputStream(uri, "w")?.use { output ->
                            output.write(export.toByteArray(Charsets.UTF_8))
                        } ?: error("The selected export destination could not be opened")
                    }
                }
                importMessage = result.fold(
                    { "Session exported successfully." },
                    { error -> "Export failed: " + (error.message ?: error.javaClass.simpleName) },
                )
            }
        }
    }
    val picker = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->
        if (uri != null) {
            scope.launch {
                importMessage = "Reading and validating structure..."
                val result = withContext(Dispatchers.IO) {
                    runCatching {
                        val name = readDisplayName(context, uri)
                        val format = when {
                            name.endsWith(".pdb", ignoreCase = true) ||
                                name.endsWith(".ent", ignoreCase = true) -> "pdb"
                            name.endsWith(".cif", ignoreCase = true) ||
                                name.endsWith(".mmcif", ignoreCase = true) -> "mmcif"
                            else -> error(
                                "Unsupported file extension. Select .pdb, .ent, .cif or .mmcif",
                            )
                        }
                        val bytes = readBounded(context, uri)
                        val sourceText = Charsets.UTF_8.newDecoder()
                            .onMalformedInput(CodingErrorAction.REPORT)
                            .onUnmappableCharacter(CodingErrorAction.REPORT)
                            .decode(ByteBuffer.wrap(bytes)).toString()
                        require(!sourceText.contains('\u0000')) {
                            "Structure file is not valid UTF-8 text"
                        }
                        if (!Python.isStarted()) {
                            Python.start(AndroidPlatform(context.applicationContext))
                        }
                        val json = Python.getInstance().getModule("kinetics_probe")
                            .callAttr("prepare_structure_viewer_source", sourceText, format)
                            .toString()
                        val envelope = JSONObject(json)
                        val payload = envelope.getJSONObject("payload")
                        val sourceHash = envelope.getJSONObject("preparation")
                            .getString("source_sha256")
                        val sessionJson = Python.getInstance().getModule("kinetics_probe")
                            .callAttr("export_structure_viewer_session", sourceText, format)
                            .toString()
                        ImportedStructure(payload.toString(), name, sourceHash, sessionJson)
                    }
                }
                result.fold(
                    { imported ->
                        payloadJson = imported.payloadJson
                        sessionExportJson = imported.sessionJson
                        sourceLabel = imported.name
                        importMessage = "Imported ${imported.name} · SHA-256 ${imported.sourceHash.take(16)}…"
                    },
                    { error ->
                        importMessage = "Import failed: " +
                            (error.message ?: error.javaClass.simpleName)
                    },
                )
            }
        }
    }
    val fallbackPayload = remember {
        """{"schema":"kinetics.structure-view.v1","source_format":"pdb","coordinate_unit":"angstrom","atom_count":8,"atoms":[{"serial":1,"name":"N","residue":"GLY","chain":"A","residue_number":1,"element":"N","xyz":[0.0,0.0,0.0]},{"serial":2,"name":"CA","residue":"GLY","chain":"A","residue_number":1,"element":"C","xyz":[1.45,0.1,0.0]},{"serial":3,"name":"C","residue":"GLY","chain":"A","residue_number":1,"element":"C","xyz":[2.0,1.48,0.1]},{"serial":4,"name":"O","residue":"GLY","chain":"A","residue_number":1,"element":"O","xyz":[1.35,2.45,0.1]},{"serial":5,"name":"N","residue":"ALA","chain":"A","residue_number":2,"element":"N","xyz":[3.25,1.55,0.0]},{"serial":6,"name":"CA","residue":"ALA","chain":"A","residue_number":2,"element":"C","xyz":[4.0,2.8,0.2]},{"serial":7,"name":"C","residue":"ALA","chain":"A","residue_number":2,"element":"C","xyz":[5.45,2.55,0.0]},{"serial":8,"name":"O","residue":"ALA","chain":"A","residue_number":2,"element":"O","xyz":[6.1,3.5,0.1]}],"limitations":["Synthetic UI preview fixture only; not experimental structure data.","Coordinates and annotations only; no inferred bonds or biological interpretation."]}"""
    }
    val activePayload = payloadJson ?: fallbackPayload
    val assetLoader = remember(context) {
        WebViewAssetLoader.Builder()
            .addPathHandler("/assets/", WebViewAssetLoader.AssetsPathHandler(context))
            .build()
    }
    val webView = remember(context, activePayload) {
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

                override fun shouldOverrideUrlLoading(
                    view: WebView, request: WebResourceRequest,
                ): Boolean = true

                override fun onPageFinished(view: WebView, url: String) {
                    if (url == VIEWER_URL) {
                        val encoded = JSONObject.quote(activePayload)
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
    Card {
        Column(
            modifier = Modifier.fillMaxWidth().padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            Text(
                "Offline-first structure viewer",
                style = MaterialTheme.typography.titleSmall,
                color = MaterialTheme.colorScheme.onSurface,
            )
            Text(sourceLabel, style = MaterialTheme.typography.labelMedium)
            Text(importMessage, style = MaterialTheme.typography.bodySmall)
            Button(onClick = { picker.launch(arrayOf("*/*")) }) {
                Text("Import PDB / mmCIF")
            }
            Button(
                onClick = {
                    val baseName = sourceLabel.substringBeforeLast('.', sourceLabel)
                    exportPicker.launch("$baseName.kinetics-session.json")
                },
                enabled = sessionExportJson != null,
            ) {
                Text("Export session JSON")
            }
            AndroidView(
                factory = { FrameLayout(it).apply { addView(webView) } },
                update = { frame ->
                    if (frame.childCount != 1 || frame.getChildAt(0) !== webView) {
                        frame.removeAllViews()
                        frame.addView(webView)
                    }
                },
                modifier = Modifier.fillMaxWidth().height(440.dp),
            )
        }
    }
}
