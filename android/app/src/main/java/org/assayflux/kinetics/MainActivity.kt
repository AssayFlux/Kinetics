package org.assayflux.kinetics

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent { FeasibilityScreen(this) }
    }
}

@Composable
private fun FeasibilityScreen(context: android.content.Context) {
    var report by remember { mutableStateOf("Running on-device Python and scientific package smoke tests…") }
    val nativeReport = remember {
        runCatching {
            val probe = NativeProbe()
            val rust = probe.rustSumSquares(3.0, 4.0)
            val cpp = probe.cppSumSquares(3.0, 4.0)
            check(kotlin.math.abs(rust - 25.0) < 1e-9)
            check(kotlin.math.abs(cpp - 25.0) < 1e-9)
            "Rust FFI: $rust; C++17 JNI: $cpp"
        }.fold(
            onSuccess = { it },
            onFailure = { "Native smoke test failed: ${it.stackTraceToString()}" },
        )
    }

    LaunchedEffect(Unit) {
        report = withContext(Dispatchers.IO) {
            runCatching { PythonProbe.report(context) }
                .getOrElse { error -> "R1 probe failed: ${error.stackTraceToString()}" }
        }
    }

    MaterialTheme {
        Surface(modifier = Modifier.fillMaxSize()) {
            Column(
                modifier = Modifier.fillMaxSize().padding(24.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center,
            ) {
                Text("Kinetics — R1 feasibility")
                Text("Research Mode only. No scientific capability is validated.")
                Text(nativeReport)
                Text(report)
            }
        }
    }
}
