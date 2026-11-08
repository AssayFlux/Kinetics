package org.assayflux.designsystem

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.FilterChip
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

/** Development catalogue for design review; never shown in the production navigation. */
@Composable
fun KineticsComponentGallery() {
    val palettes = listOf(
        "Kinetics Light Classic" to (KineticsTokens.KineticsLightClassic to false),
        "Kinetics Dark Classic" to (KineticsTokens.KineticsDarkClassic to true),
    )
    LazyColumn(
        modifier = Modifier.fillMaxWidth(),
        verticalArrangement = Arrangement.spacedBy(16.dp),
    ) {
        item {
            Text(
                "Kinetics design system",
                modifier = Modifier.padding(16.dp),
                style = MaterialTheme.typography.headlineMedium,
            )
        }
        items(palettes, key = { it.first }) { (name, entry) ->
            val (palette, isDark) = entry
            val scheme = if (!isDark) {
                lightColorScheme(
                    primary = palette.primary, secondary = palette.secondary,
                    background = palette.background, surface = palette.surface,
                    onSurface = palette.text, onBackground = palette.text,
                    surfaceVariant = palette.surfaceAlt, onSurfaceVariant = palette.muted,
                    outline = palette.outline,
                )
            } else {
                darkColorScheme(
                    primary = palette.primary, onPrimary = palette.background,
                    secondary = palette.secondary, background = palette.background,
                    surface = palette.surface, onSurface = palette.text,
                    onBackground = palette.text, surfaceVariant = palette.surfaceAlt,
                    onSurfaceVariant = palette.muted, outline = palette.outline,
                )
            }
            MaterialTheme(colorScheme = scheme, typography = KineticsTypography) {
                Card(
                    modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp),
                    shape = RoundedCornerShape(20.dp),
                    colors = CardDefaults.cardColors(containerColor = palette.surface),
                ) {
                    Column(
                        modifier = Modifier.padding(16.dp),
                        verticalArrangement = Arrangement.spacedBy(12.dp),
                    ) {
                        Text(name, style = MaterialTheme.typography.titleLarge, color = palette.text)
                        Text("Semantic surface, type, outline and action preview", color = palette.muted)
                        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            Surface(Modifier.weight(1f).background(palette.primary), shape = RoundedCornerShape(8.dp)) {
                                Text("Primary", Modifier.padding(10.dp), color = palette.background)
                            }
                            Surface(Modifier.weight(1f).background(palette.secondary), shape = RoundedCornerShape(8.dp)) {
                                Text("Secondary", Modifier.padding(10.dp), color = palette.background)
                            }
                        }
                        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            Button(onClick = {}) { Text("Primary action") }
                            val (selected, setSelected) = remember(name) { mutableStateOf(false) }
                            FilterChip(selected, { setSelected(!selected) }, label = { Text("Filter chip") })
                        }
                        Text("Research Mode · Implemented · On-device", color = palette.muted)
                    }
                }
            }
        }
    }
}
