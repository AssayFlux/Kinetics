package org.assayflux.designsystem

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

/** Development-only live gallery for the owner V1 semantic system and reusable controls. */
@Composable
fun KineticsComponentGallery() {
    val palettes = listOf(
        "Light" to (KineticsTokens.KineticsLightClassic to false),
        "Dark" to (KineticsTokens.KineticsDarkClassic to true),
    )
    LazyColumn(
        modifier = Modifier.fillMaxWidth(),
        contentPadding = androidx.compose.foundation.layout.PaddingValues(20.dp),
        verticalArrangement = Arrangement.spacedBy(24.dp),
    ) {
        item {
            Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                Text("KINETICS", style = MaterialTheme.typography.labelMedium)
                Text("Component gallery", style = MaterialTheme.typography.headlineMedium)
                Text(
                    "Owner V1 · monochrome · native Compose",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
        }
        items(palettes, key = { it.first }) { (name, entry) ->
            val (palette, isDark) = entry
            val scheme = if (!isDark) {
                lightColorScheme(
                    primary = palette.primary, onPrimary = palette.background,
                    secondary = palette.secondary, tertiary = palette.tertiary,
                    background = palette.background, surface = palette.surface,
                    onSurface = palette.text, onBackground = palette.text,
                    surfaceVariant = palette.surfaceAlt, onSurfaceVariant = palette.muted,
                    outline = palette.outline,
                )
            } else {
                darkColorScheme(
                    primary = palette.primary, onPrimary = palette.background,
                    secondary = palette.secondary, tertiary = palette.tertiary,
                    background = palette.background, surface = palette.surface,
                    onSurface = palette.text, onBackground = palette.text,
                    surfaceVariant = palette.surfaceAlt, onSurfaceVariant = palette.muted,
                    outline = palette.outline,
                )
            }
            MaterialTheme(colorScheme = scheme, typography = KineticsTypography) {
                var field by remember(name) { mutableStateOf("") }
                var pressed by remember(name) { mutableStateOf(false) }
                Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                    Text("$name appearance", style = MaterialTheme.typography.titleLarge)
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        Surface(
                            modifier = Modifier.weight(1f),
                            color = palette.primary,
                            shape = androidx.compose.foundation.shape.RoundedCornerShape(8.dp),
                        ) {
                            Text("Primary", Modifier.padding(12.dp), color = palette.background)
                        }
                        Surface(
                            modifier = Modifier.weight(1f),
                            color = palette.surfaceAlt,
                            shape = androidx.compose.foundation.shape.RoundedCornerShape(8.dp),
                        ) {
                            Text("Secondary", Modifier.padding(12.dp), color = palette.text)
                        }
                    }
                    KineticsPrimaryButton(
                        label = if (pressed) "Action acknowledged" else "Primary action",
                        onClick = { pressed = !pressed },
                        modifier = Modifier.fillMaxWidth(),
                    )
                    KineticsSecondaryButton(
                        label = "Secondary action",
                        onClick = { field = "Secondary action selected" },
                        modifier = Modifier.fillMaxWidth(),
                    )
                    KineticsField(
                        value = field,
                        onValueChange = { field = it },
                        label = "Example input",
                        supportingText = "52 dp target · 10 dp radius",
                    )
                    KineticsStatus(label = "Research Mode · local")
                }
            }
        }
    }
}
