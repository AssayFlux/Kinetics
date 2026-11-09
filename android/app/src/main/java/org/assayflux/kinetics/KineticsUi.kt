package org.assayflux.kinetics

import android.content.Context
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.pager.HorizontalPager
import androidx.compose.foundation.pager.rememberPagerState
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import org.assayflux.designsystem.KineticsTokens
import org.assayflux.designsystem.KineticsTypography
import org.assayflux.designsystem.KineticsScientificTextStyle
import org.json.JSONArray

internal enum class KineticsTab(val label: String, val glyph: String) {
    Home("Home", "⌂"), Work("Work", "▤"), Explore("Explore", "⌕"), Settings("Settings", "⚙")
}

@Composable
internal fun KineticsAppShell(
    jobs: List<ResearchJob>, notice: String, runtimeReport: String?,
    onImport: () -> Unit, onRefresh: () -> Unit, onRunRuntime: () -> Unit,
    onCancel: (ResearchJob) -> Unit, onResume: (ResearchJob) -> Unit,
    onDelete: (ResearchJob) -> Unit, onExport: (ResearchJob) -> Unit,
    onExportProvenance: (ResearchJob) -> Unit,
    onExportProvenanceSummary: (ResearchJob) -> Unit,
    onAnalyzeImported: (ResearchJob) -> Unit, onExportAnalysis: (ResearchJob) -> Unit,
    themeFamily: String, onThemeFamilyChange: (String) -> Unit,
    biometricEnabled: Boolean, biometricAvailable: Boolean,
    onBiometricChange: (Boolean) -> Unit,
) {
    var tab by rememberSaveable { mutableStateOf(KineticsTab.Home) }
    val resolvedTheme = when (themeFamily) {
        "system" -> if (isSystemInDarkTheme()) "dark" else "light"
        else -> themeFamily
    }
    val palette = if (resolvedTheme == "dark") KineticsTokens.KineticsDarkClassic else KineticsTokens.KineticsLightClassic
    val scheme = if (resolvedTheme == "light") {
        lightColorScheme(
            primary = palette.primary, secondary = palette.secondary, tertiary = palette.tertiary,
            background = palette.background, surface = palette.surface, onSurface = palette.text,
            onBackground = palette.text, surfaceVariant = palette.surfaceAlt,
            onSurfaceVariant = palette.muted, outline = palette.outline,
        )
    } else {
        darkColorScheme(
            primary = palette.primary, onPrimary = palette.background,
            secondary = palette.secondary, tertiary = palette.tertiary,
            background = palette.background, surface = palette.surface, onSurface = palette.text,
            onBackground = palette.text, surfaceVariant = palette.surfaceAlt,
            onSurfaceVariant = palette.muted, outline = palette.outline,
        )
    }
    MaterialTheme(colorScheme = scheme, typography = KineticsTypography) {
        BoxWithConstraints(Modifier.fillMaxSize()) {
            // Classify the app window, not the physical device. These are the
            // current Android adaptive breakpoints recorded in docs/ui/verified-specs.md.
            val navigationMode = classifyNavigationMode(maxWidth.value, maxHeight.value)
            val useDrawer = navigationMode == NavigationMode.Drawer
            val useRail = navigationMode == NavigationMode.Rail

            @Composable
            fun Screen(modifier: Modifier) {
                when (tab) {
                    KineticsTab.Home -> HomeScreen(jobs, notice, runtimeReport, resolvedTheme, onImport,
                        onRunRuntime, { tab = KineticsTab.Work }, onCancel, onResume, onDelete, onExport, onExportProvenance, onExportProvenanceSummary, onAnalyzeImported, onExportAnalysis, modifier)
                    KineticsTab.Work -> WorkScreen(jobs, onImport, onCancel, onResume, onDelete, onExport, onExportProvenance, onExportProvenanceSummary, onAnalyzeImported, onExportAnalysis, modifier)
                    KineticsTab.Explore -> ExploreScreen(modifier)
                    KineticsTab.Settings -> SettingsScreen(
                        runtimeReport, onRunRuntime, onRefresh, themeFamily, onThemeFamilyChange,
                        biometricEnabled, biometricAvailable, onBiometricChange, modifier,
                    )
                }
            }

            @Composable
            fun NavigationItems() {
                KineticsTab.entries.forEach { item ->
                    NavigationDrawerItem(
                        selected = tab == item,
                        onClick = { tab = item },
                        icon = { Text(item.glyph, fontSize = 20.sp) },
                        label = { Text(item.label) },
                        modifier = Modifier.padding(NavigationDrawerItemDefaults.ItemPadding),
                    )
                }
            }

            when {
                useDrawer -> PermanentNavigationDrawer(
                    drawerContent = {
                        PermanentDrawerSheet(Modifier.width(280.dp)) {
                            Spacer(Modifier.height(24.dp))
                            Text("KINETICS", modifier = Modifier.padding(horizontal = 24.dp, vertical = 12.dp),
                                color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                            NavigationItems()
                        }
                    },
                ) {
                    Scaffold(containerColor = MaterialTheme.colorScheme.background) { padding ->
                        Screen(Modifier.padding(padding))
                    }
                }
                useRail -> Row(Modifier.fillMaxSize()) {
                    NavigationRail {
                        Spacer(Modifier.height(12.dp))
                        KineticsTab.entries.forEach { item ->
                            NavigationRailItem(
                                selected = tab == item,
                                onClick = { tab = item },
                                icon = { Text(item.glyph, fontSize = 20.sp) },
                                label = { Text(item.label) },
                                alwaysShowLabel = true,
                            )
                        }
                    }
                    Scaffold(
                        modifier = Modifier.weight(1f),
                        containerColor = MaterialTheme.colorScheme.background,
                    ) { padding -> Screen(Modifier.padding(padding)) }
                }
                else -> Scaffold(
                    containerColor = MaterialTheme.colorScheme.background,
                    bottomBar = {
                        NavigationBar(containerColor = MaterialTheme.colorScheme.surface) {
                            KineticsTab.entries.forEach { item ->
                                NavigationBarItem(
                                    selected = tab == item, onClick = { tab = item },
                                    icon = { Text(item.glyph, fontSize = 20.sp, modifier = Modifier.semantics { contentDescription = item.label }) },
                                    label = { Text(item.label) },
                                )
                            }
                        }
                    },
                ) { padding -> Screen(Modifier.padding(padding)) }
            }
        }
    }
}

@Composable
private fun Frame(eyebrow: String, title: String, subtitle: String, modifier: Modifier = Modifier, content: @Composable () -> Unit) {
    Box(modifier.fillMaxSize(), contentAlignment = Alignment.TopCenter) {
      Column(Modifier.fillMaxWidth().widthIn(max = 840.dp).padding(horizontal = 20.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)) {
        Column(Modifier.padding(top = 20.dp), verticalArrangement = Arrangement.spacedBy(5.dp)) {
            Text(eyebrow.uppercase(), color = MaterialTheme.colorScheme.primary, style = MaterialTheme.typography.labelMedium, fontWeight = FontWeight.Bold, letterSpacing = 1.4.sp)
            Text(title, style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold)
            Text(subtitle, color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.bodyMedium)
        }
        Box(Modifier.weight(1f).fillMaxWidth()) { content() }
      }
    }
}

@Composable
private fun HomeScreen(
    jobs: List<ResearchJob>, notice: String, runtime: String?, themeFamily: String, onImport: () -> Unit,
    onRuntime: () -> Unit, onOpenWork: () -> Unit,
    onCancel: (ResearchJob) -> Unit, onResume: (ResearchJob) -> Unit,
    onDelete: (ResearchJob) -> Unit, onExport: (ResearchJob) -> Unit,
    onExportProvenance: (ResearchJob) -> Unit,
    onExportProvenanceSummary: (ResearchJob) -> Unit, onAnalyzeImported: (ResearchJob) -> Unit,
    onExportAnalysis: (ResearchJob) -> Unit, modifier: Modifier,
) {
    val active = jobs.count { it.state in listOf("queued", "running", "cancel_requested") }
    val done = jobs.count { it.state == "succeeded" }
    val attention = jobs.count { it.state in listOf("failed", "recovery_required") }
    Frame("Your research workspace", "Good science starts here.", "A private, local-first environment for computational research.", modifier) {
        LazyColumn(verticalArrangement = Arrangement.spacedBy(16.dp), contentPadding = PaddingValues(bottom = 24.dp)) {
            item {
                WorkspaceCarousel(
                    isDark = themeFamily == "dark",
                    active = active,
                    complete = done,
                    attention = attention,
                    runtime = runtime,
                    onImport = onImport,
                    onOpenWork = onOpenWork,
                    onRuntime = onRuntime,
                )
            }
            item {
                Row(horizontalArrangement = Arrangement.spacedBy(9.dp), modifier = Modifier.fillMaxWidth()) {
                    Metric("ACTIVE", active.toString(), Modifier.weight(1f))
                    Metric("COMPLETE", done.toString(), Modifier.weight(1f))
                    Metric("ATTENTION", attention.toString(), Modifier.weight(1f))
                }
            }
            item { Section("Recent activity", "View all", onOpenWork) }
            if (jobs.isEmpty()) item { Empty("Your workspace is clear", "Import a research file to create your first job.") }
            else items(jobs.take(4), key = { it.id }) { JobCard(it, onCancel, onResume, onDelete, onExport, onExportProvenance, onExportProvenanceSummary, onAnalyzeImported, onExportAnalysis) }
            item {
                Section("Device health", "Run checks", onRuntime)
                OutlinedCard(Modifier.fillMaxWidth(), shape = RoundedCornerShape(20.dp)) {
                    Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(7.dp)) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Dot(MaterialTheme.colorScheme.primary)
                            Spacer(Modifier.width(8.dp))
                            Text("On-device runtime", fontWeight = FontWeight.SemiBold)
                            Spacer(Modifier.weight(1f))
                            Text("Diagnostics", color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.labelSmall)
                        }
                        Text("Check embedded Python, native engines and encrypted storage.", color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.bodySmall)
                        runtime?.let { Text(it, style = MaterialTheme.typography.bodySmall) }
                    }
                }
            }
            item { Notice(notice) }
            item { Footer() }
        }
    }
}

@Composable
private fun WorkspaceCarousel(
    isDark: Boolean,
    active: Int,
    complete: Int,
    attention: Int,
    runtime: String?,
    onImport: () -> Unit,
    onOpenWork: () -> Unit,
    onRuntime: () -> Unit,
) {
    val pager = rememberPagerState(pageCount = { 3 })
    val heroContainer = if (isDark) MaterialTheme.colorScheme.surfaceVariant else MaterialTheme.colorScheme.primary
    val heroForeground = if (isDark) MaterialTheme.colorScheme.onSurface else MaterialTheme.colorScheme.onPrimary
    val heroAction = if (isDark) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onPrimary
    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
        HorizontalPager(
            state = pager,
            contentPadding = PaddingValues(horizontal = 30.dp),
            pageSpacing = 12.dp,
            modifier = Modifier.fillMaxWidth(),
        ) { page ->
            when (page) {
                0 -> Card(
                    onClick = onImport,
                    modifier = Modifier.fillMaxWidth().height(218.dp),
                    shape = RoundedCornerShape(26.dp),
                    colors = CardDefaults.cardColors(containerColor = heroContainer),
                ) {
                    Column(
                        Modifier.fillMaxSize().padding(22.dp),
                        verticalArrangement = Arrangement.SpaceBetween,
                    ) {
                        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                            Text("KINETICS  /  RESEARCH WORKSPACE", style = MaterialTheme.typography.labelSmall,
                                color = heroForeground.copy(alpha = .78f), letterSpacing = 1.1.sp)
                            Text("Make room for discovery.", style = MaterialTheme.typography.headlineSmall,
                                color = heroForeground, fontWeight = FontWeight.SemiBold)
                            Text("Import a research input and create a protected local work item.",
                                style = MaterialTheme.typography.bodyMedium, color = heroForeground.copy(alpha = .88f))
                        }
                        Text("IMPORT RESEARCH INPUT  →", style = MaterialTheme.typography.labelLarge,
                            color = heroAction, fontWeight = FontWeight.Bold)
                    }
                }
                1 -> Card(
                    onClick = onOpenWork,
                    modifier = Modifier.fillMaxWidth().height(218.dp),
                    shape = RoundedCornerShape(26.dp),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant),
                ) {
                    Column(
                        Modifier.fillMaxSize().padding(22.dp),
                        verticalArrangement = Arrangement.SpaceBetween,
                    ) {
                        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                            Text("YOUR WORK", style = MaterialTheme.typography.labelSmall,
                                color = MaterialTheme.colorScheme.primary, letterSpacing = 1.1.sp)
                            Text("Research, in motion.", style = MaterialTheme.typography.headlineSmall,
                                color = MaterialTheme.colorScheme.onSurface, fontWeight = FontWeight.SemiBold)
                            Text("$active active  ·  $complete complete  ·  $attention need attention",
                                style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                        Text("OPEN WORKSPACE  →", style = MaterialTheme.typography.labelLarge,
                            color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                    }
                }
                else -> Card(
                    onClick = onRuntime,
                    modifier = Modifier.fillMaxWidth().height(218.dp),
                    shape = RoundedCornerShape(26.dp),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
                ) {
                    Column(
                        Modifier.fillMaxSize().padding(22.dp),
                        verticalArrangement = Arrangement.SpaceBetween,
                    ) {
                        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                            Text("DEVICE READINESS", style = MaterialTheme.typography.labelSmall,
                                color = MaterialTheme.colorScheme.secondary, letterSpacing = 1.1.sp)
                            Text("Know your instruments.", style = MaterialTheme.typography.headlineSmall,
                                color = MaterialTheme.colorScheme.onSurface, fontWeight = FontWeight.SemiBold)
                            Text(runtime ?: "Run local checks for embedded Python, native engines and encrypted storage.",
                                style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant,
                                maxLines = 3, overflow = TextOverflow.Ellipsis)
                        }
                        Text("RUN RUNTIME CHECKS  →", style = MaterialTheme.typography.labelLarge,
                            color = MaterialTheme.colorScheme.secondary, fontWeight = FontWeight.Bold)
                    }
                }
            }
        }
        Row(
            Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.Center,
            verticalAlignment = Alignment.CenterVertically,
        ) {
            repeat(3) { index ->
                val selected = pager.currentPage == index
                Box(
                    Modifier.padding(horizontal = 4.dp).size(width = if (selected) 22.dp else 7.dp, height = 7.dp)
                        .clip(RoundedCornerShape(50))
                        .background(if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.outline),
                )
            }
        }
    }
}

@Composable
private fun Metric(label: String, value: String, modifier: Modifier) {
    OutlinedCard(modifier, shape = RoundedCornerShape(18.dp)) {
        Column(Modifier.padding(11.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
            Text(label, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = FontWeight.Bold, maxLines = 1)
            Text(value, style = KineticsScientificTextStyle.copy(fontSize = MaterialTheme.typography.headlineMedium.fontSize, fontWeight = FontWeight.Bold))
            Text("Research jobs", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant, maxLines = 1)
        }
    }
}

@Composable
private fun Section(title: String, action: String, onClick: () -> Unit) {
    Row(verticalAlignment = Alignment.CenterVertically) {
        Text(title, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
        Spacer(Modifier.weight(1f))
        TextButton(onClick = onClick) { Text(action) }
    }
}

@Composable
private fun WorkScreen(
    jobs: List<ResearchJob>, onImport: () -> Unit, onCancel: (ResearchJob) -> Unit,
    onResume: (ResearchJob) -> Unit, onDelete: (ResearchJob) -> Unit,
    onExport: (ResearchJob) -> Unit, onExportProvenance: (ResearchJob) -> Unit,
    onExportProvenanceSummary: (ResearchJob) -> Unit, onAnalyzeImported: (ResearchJob) -> Unit,
    onExportAnalysis: (ResearchJob) -> Unit, modifier: Modifier,
) {
    var query by remember { mutableStateOf("") }
    var filter by remember { mutableStateOf("All") }
    val filtered = jobs.filter { job ->
        (query.isBlank() || job.inputName.contains(query, true)) && when (filter) {
            "Active" -> job.state in listOf("queued", "running", "cancel_requested")
            "Complete" -> job.state == "succeeded"
            "Attention" -> job.state in listOf("failed", "recovery_required")
            else -> true
        }
    }
    Frame("Research activity", "Your work, organized.", "Track imports, inspect integrity and manage local files.", modifier) {
        LazyColumn(verticalArrangement = Arrangement.spacedBy(12.dp), contentPadding = PaddingValues(bottom = 24.dp)) {
            item {
                OutlinedTextField(query, { query = it }, Modifier.fillMaxWidth(), singleLine = true,
                    shape = RoundedCornerShape(16.dp), label = { Text("Search research jobs") })
            }
            item {
                Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                    listOf("All", "Active", "Complete", "Attention").forEach {
                        FilterChip(filter == it, { filter = it }, label = { Text(it) })
                    }
                }
            }
            item { Button(onClick = onImport, Modifier.fillMaxWidth(), shape = RoundedCornerShape(14.dp)) { Text("+  Import new data") } }
            if (filtered.isEmpty()) item { Empty("No matching research jobs", "Try another search or import a dataset to begin.") }
            else items(filtered, key = { it.id }) { JobCard(it, onCancel, onResume, onDelete, onExport, onExportProvenance, onExportProvenanceSummary, onAnalyzeImported) }
        }
    }
}

@Composable
private fun JobCard(job: ResearchJob, onCancel: (ResearchJob) -> Unit, onResume: (ResearchJob) -> Unit,
                    onDelete: (ResearchJob) -> Unit, onExport: (ResearchJob) -> Unit,
                    onExportProvenance: (ResearchJob) -> Unit,
                    onExportProvenanceSummary: (ResearchJob) -> Unit,
                    onAnalyzeImported: (ResearchJob) -> Unit,
                    onExportAnalysis: (ResearchJob) -> Unit) {
    val active = job.state in listOf("queued", "running", "cancel_requested")
    val success = job.state == "succeeded"
    val issue = job.state in listOf("failed", "recovery_required")
    var provenanceExpanded by rememberSaveable(job.id) { mutableStateOf(false) }
    OutlinedCard(Modifier.fillMaxWidth(), shape = RoundedCornerShape(20.dp)) {
        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(9.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Box(Modifier.size(40.dp).clip(RoundedCornerShape(13.dp)).background(MaterialTheme.colorScheme.surfaceVariant), contentAlignment = Alignment.Center) {
                    Text(if (success) "✓" else if (issue) "!" else "▤", fontSize = 19.sp,
                        color = if (issue) MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                }
                Spacer(Modifier.width(12.dp))
                Column(Modifier.weight(1f)) {
                    Text(job.inputName, fontWeight = FontWeight.SemiBold, maxLines = 1, overflow = TextOverflow.Ellipsis)
                    Text("Research import", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
                StatePill(job.state)
            }
            if (active) {
                LinearProgressIndicator(Modifier.fillMaxWidth())
                Text("Processed in the background.", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
            job.sha256?.let { Text("SHA-256  ${it.take(12)}…", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant) }
            job.message?.let { Text(it, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant) }
            if (job.state == "recovery_required") Text(
                "Encrypted data is preserved. If its original Keystore key is lost, creating a replacement key cannot decrypt it.",
                style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.error)
            if (job.provenanceToolId != null) {
                TextButton(
                    onClick = { provenanceExpanded = !provenanceExpanded },
                    modifier = Modifier.semantics {
                        contentDescription = if (provenanceExpanded) {
                            "Hide import provenance"
                        } else {
                            "Inspect import provenance"
                        }
                    },
                ) {
                    Text(if (provenanceExpanded) "Hide provenance" else "Inspect provenance")
                }
                if (provenanceExpanded) {
                    Surface(
                        modifier = Modifier.fillMaxWidth(),
                        color = MaterialTheme.colorScheme.surfaceVariant,
                        shape = RoundedCornerShape(14.dp),
                    ) {
                        Column(Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                            Text("IMPORT PROVENANCE", style = MaterialTheme.typography.labelMedium,
                                color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                            Text("Tool: ${job.provenanceToolId}", style = MaterialTheme.typography.bodySmall)
                            Text("Version: ${job.provenanceToolVersion ?: "unknown"}",
                                style = MaterialTheme.typography.bodySmall)
                            job.provenanceCreatedAt?.let {
                                val recorded = java.time.format.DateTimeFormatter.ISO_INSTANT
                                    .format(java.time.Instant.ofEpochMilli(it))
                                Text("Recorded: $recorded", style = MaterialTheme.typography.bodySmall)
                            }
                            job.sha256?.let {
                                Text("Input SHA-256: $it", style = MaterialTheme.typography.labelSmall)
                            }
                            job.provenanceParametersJson?.let {
                                Text("Parameters: $it", style = MaterialTheme.typography.labelSmall,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant)
                            }
                            TextButton(
                                onClick = { onExportProvenance(job) },
                                modifier = Modifier.semantics {
                                    contentDescription = "Export import provenance as JSON"
                                },
                            ) {
                                Text("Export provenance JSON")
                            }
                            TextButton(
                                onClick = { onExportProvenanceSummary(job) },
                                modifier = Modifier.semantics {
                                    contentDescription = "Export human-readable import provenance summary"
                                },
                            ) {
                                Text("Export provenance summary")
                            }
                        }
                    }
                }
            }
            if (job.analysisResultJson != null) {
                var analysisExpanded by rememberSaveable(job.id) { mutableStateOf(false) }
                TextButton(onClick = { analysisExpanded = !analysisExpanded }) {
                    Text(if (analysisExpanded) "Hide analysis result" else "View saved analysis result")
                }
                if (analysisExpanded) {
                    Text("Analysis method: ${job.analysisToolId ?: "unknown"}", style = MaterialTheme.typography.labelSmall)
                    Text(job.analysisResultJson, style = MaterialTheme.typography.bodySmall)
                    TextButton(onClick = { onExportAnalysis(job) }) { Text("Export analysis JSON") }
                }
            }
            Row(horizontalArrangement = Arrangement.spacedBy(7.dp)) {
                if (active) OutlinedButton(onClick = { onCancel(job) }) { Text("Cancel") }
                if (job.state == "cancelled" || job.state == "failed") OutlinedButton(onClick = { onResume(job) }) { Text("Resume") }
                if (success && job.analysisResultJson == null && job.inputName.substringAfterLast('.').lowercase() in setOf("fa", "fasta", "fna")) OutlinedButton(onClick = { onAnalyzeImported(job) }) { Text("Run FASTA QC") }
                if (success) Button(onClick = { onExport(job) }) { Text("Export") }
                if (success || issue || job.state == "cancelled") OutlinedButton(onClick = { onDelete(job) }) { Text("Delete") }
            }
        }
    }
}

@Composable
private fun StatePill(state: String) {
    val text = when (state) {
        "succeeded" -> "COMPLETE"; "queued" -> "QUEUED"; "running" -> "RUNNING"
        "cancel_requested" -> "STOPPING"; "failed" -> "FAILED"; "cancelled" -> "CANCELLED"
        "recovery_required" -> "RECOVERY"; else -> state.uppercase()
    }
    Surface(
        color = MaterialTheme.colorScheme.surfaceVariant,
        shape = RoundedCornerShape(50),
        modifier = Modifier.semantics { contentDescription = "Job status: $text" },
    ) {
        Text(text, Modifier.padding(horizontal = 10.dp, vertical = 6.dp),
            style = MaterialTheme.typography.labelSmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant)
    }
}

private data class CapabilityEntry(
    val id: String,
    val name: String,
    val status: String,
    val implementation: String,
    val evidenceLevel: String,
    val domain: String,
)

private fun loadCapabilityCatalogue(context: Context): List<CapabilityEntry> {
    val source = context.assets.open("capability-catalog.json")
        .bufferedReader(Charsets.UTF_8).use { it.readText() }
    val tools = JSONArray(source)
    return buildList {
        for (index in 0 until tools.length()) {
            val item = tools.getJSONObject(index)
            add(
                CapabilityEntry(
                    id = item.getString("id"),
                    name = item.getString("name"),
                    status = item.getString("status"),
                    implementation = item.getString("implementation"),
                    evidenceLevel = item.getString("evidence_level"),
                    domain = item.getString("domain"),
                ),
            )
        }
    }
}

@Composable
fun ExploreScreen(modifier: Modifier) {
    val context = LocalContext.current
    val catalogue = remember(context) { runCatching { loadCapabilityCatalogue(context) } }
    val entries = catalogue.getOrNull().orEmpty()
    val groups = entries.groupBy { it.domain }.toList()
    Frame(
        "Scientific toolkit",
        "Explore the science.",
        "A live view of the repository capability registry and its evidence maturity.",
        modifier,
    ) {
        LazyColumn(
            verticalArrangement = Arrangement.spacedBy(12.dp),
            contentPadding = PaddingValues(bottom = 24.dp),
        ) {
            item {
                Card(
                    shape = RoundedCornerShape(20.dp),
                    colors = CardDefaults.cardColors(
                        containerColor = MaterialTheme.colorScheme.surfaceVariant,
                    ),
                ) {
                    Column(
                        Modifier.padding(16.dp),
                        verticalArrangement = Arrangement.spacedBy(6.dp),
                    ) {
                        Text("Capability transparency", fontWeight = FontWeight.Bold)
                        Text(
                            if (catalogue.isSuccess) {
                                "${entries.size} registered source capabilities across ${groups.size} research areas. Registry status describes source implementation only; it does not imply an Android execution path or scientific validation."
                            } else {
                                "The capability catalogue could not be loaded. No capabilities are being presented as available."
                            },
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            style = MaterialTheme.typography.bodySmall,
                        )
                    }
                }
            }
            if (entries.any { it.id == "sequence.fasta" && it.status == "implemented" }) {
                item { FastaQcCard() }
            }
            if (entries.any { it.id == "sequence.fastq" && it.status == "implemented" }) {
                item { FastqQcCard() }
            }
            if (catalogue.isFailure) {
                item {
                    OutlinedCard(Modifier.fillMaxWidth()) {
                        Text(
                            "Catalogue unavailable: ${catalogue.exceptionOrNull()?.message ?: "asset read failed"}",
                            Modifier.padding(16.dp),
                            color = MaterialTheme.colorScheme.error,
                        )
                    }
                }
            }
            items(groups, key = { it.first }) { (domain, tools) ->
                OutlinedCard(Modifier.fillMaxWidth(), shape = RoundedCornerShape(18.dp)) {
                    Column(
                        Modifier.padding(16.dp),
                        verticalArrangement = Arrangement.spacedBy(10.dp),
                    ) {
                        Row(
                            Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically,
                        ) {
                            Text(
                                domain,
                                style = MaterialTheme.typography.titleMedium,
                                fontWeight = FontWeight.Bold,
                            )
                            InfoPill("${tools.size} modules")
                        }
                        tools.forEachIndexed { index, tool ->
                            if (index > 0) {
                                HorizontalDivider(
                                    color = MaterialTheme.colorScheme.outline.copy(alpha = .35f),
                                )
                            }
                            Column(verticalArrangement = Arrangement.spacedBy(5.dp)) {
                                Text(tool.name, style = MaterialTheme.typography.bodyMedium)
                                Text(
                                    tool.id,
                                    style = MaterialTheme.typography.labelSmall,
                                    color = MaterialTheme.colorScheme.primary,
                                )
                                Row(
                                    horizontalArrangement = Arrangement.spacedBy(7.dp),
                                    verticalAlignment = Alignment.CenterVertically,
                                ) {
                                    InfoPill(
                                        if (tool.status == "implemented") "Source implemented"
                                        else tool.status.replaceFirstChar { it.uppercase() },
                                    )
                                    InfoPill(
                                        if (tool.evidenceLevel == "none") "Not validated"
                                        else tool.evidenceLevel,
                                    )
                                }
                                Text(
                                    tool.implementation,
                                    style = MaterialTheme.typography.labelSmall,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                                    maxLines = 1,
                                    overflow = TextOverflow.Ellipsis,
                                )
                            }
                        }
                    }
                }
            }
        }
    }
}


@Composable
private fun FastaQcCard() {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    var fastaText by rememberSaveable {
        mutableStateOf(">example_sequence\nACGTACGTGCGTNNACGT\n")
    }
    var running by remember { mutableStateOf(false) }
    var result by remember { mutableStateOf<SequenceQcResult?>(null) }
    var error by remember { mutableStateOf<String?>(null) }

    OutlinedCard(Modifier.fillMaxWidth(), shape = RoundedCornerShape(20.dp)) {
        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Text("FASTA quick quality check", style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold)
            Text("Run the registered local FASTA parser and basic sequence statistics. Input stays on this device.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant)
            OutlinedTextField(
                value = fastaText,
                onValueChange = {
                    if (it.length <= SequenceQcRunner.MAX_INPUT_CHARS) {
                        fastaText = it
                        error = null
                    }
                },
                modifier = Modifier.fillMaxWidth(),
                label = { Text("FASTA input") },
                minLines = 4,
                maxLines = 8,
                supportingText = { Text("Up to 1,000,000 characters · multiple records supported") },
            )
            Button(
                onClick = {
                    running = true
                    error = null
                    result = null
                    scope.launch {
                        val outcome = withContext(Dispatchers.IO) {
                            runCatching { SequenceQcRunner.analyze(context, fastaText) }
                        }
                        outcome.onSuccess { result = it }
                            .onFailure { error = it.message ?: "FASTA analysis failed" }
                        running = false
                    }
                },
                enabled = !running && fastaText.isNotBlank(),
                modifier = Modifier.fillMaxWidth(),
            ) {
                Text(if (running) "Analysing…" else "Analyse FASTA")
            }
            error?.let {
                Text(it, color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodySmall)
            }
            result?.let { summary ->
                HorizontalDivider()
                Text("${summary.recordCount} records · ${summary.totalBases} total bases",
                    fontWeight = FontWeight.SemiBold)
                summary.records.forEach { record ->
                    Column(verticalArrangement = Arrangement.spacedBy(2.dp)) {
                        Text(record.identifier, style = MaterialTheme.typography.labelLarge,
                            maxLines = 1, overflow = TextOverflow.Ellipsis)
                        Text("${record.length} bases · ${String.format(java.util.Locale.ROOT, "%.2f", record.gcPercent)}% GC (all symbols) · ${record.ambiguousCount} non-ACGT symbols",
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
                Text("Basic QC only. No sequence identity, function, pathogenicity or clinical interpretation is inferred. Independent biological validation is not claimed.",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
    }
}


@Composable
private fun FastqQcCard() {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    var input by rememberSaveable { mutableStateOf("@read_1\nACGTACGT\n+\nIIII!!!!\n") }
    var offset by rememberSaveable { mutableIntStateOf(33) }
    var running by remember { mutableStateOf(false) }
    var result by remember { mutableStateOf<FastqQcResult?>(null) }
    var error by remember { mutableStateOf<String?>(null) }
    OutlinedCard(Modifier.fillMaxWidth(), shape = RoundedCornerShape(20.dp)) {
        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Text("FASTQ read-quality check", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
            Text("Wrapped FASTQ parsing. Quality encoding must be selected explicitly; it is never guessed.",
                style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            OutlinedTextField(value = input, onValueChange = {
                if (it.length <= SequenceQcRunner.MAX_INPUT_CHARS) { input = it; error = null }
            }, modifier = Modifier.fillMaxWidth(), label = { Text("FASTQ input") },
                minLines = 4, maxLines = 8,
                supportingText = { Text("Up to 1,000,000 characters · wrapped reads supported") })
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                FilterChip(selected = offset == 33, onClick = { offset = 33; result = null }, label = { Text("Phred+33") })
                FilterChip(selected = offset == 64, onClick = { offset = 64; result = null }, label = { Text("Phred+64") })
            }
            Button(onClick = {
                running = true; error = null; result = null
                scope.launch {
                    val outcome = withContext(Dispatchers.IO) {
                        runCatching { SequenceQcRunner.analyzeFastq(context, input, offset) }
                    }
                    outcome.onSuccess { result = it }.onFailure { error = it.message ?: "FASTQ analysis failed" }
                    running = false
                }
            }, enabled = !running && input.isNotBlank(), modifier = Modifier.fillMaxWidth()) {
                Text(if (running) "Analysing…" else "Analyse FASTQ")
            }
            error?.let { Text(it, color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodySmall) }
            result?.let { summary ->
                HorizontalDivider()
                Text("${summary.recordCount} reads · ${summary.totalBases} bases · Phred+${summary.phredOffset}",
                    fontWeight = FontWeight.SemiBold)
                Text("Mean Q ${String.format(java.util.Locale.ROOT, "%.2f", summary.meanPhred)} · Q20 ${String.format(java.util.Locale.ROOT, "%.1f", summary.q20Fraction * 100)}% · Q30 ${String.format(java.util.Locale.ROOT, "%.1f", summary.q30Fraction * 100)}%",
                    style = MaterialTheme.typography.bodySmall)
                summary.reads.take(20).forEach { read ->
                    Text("${read.identifier}: ${read.length} bases · mean Q ${String.format(java.util.Locale.ROOT, "%.2f", read.meanPhred)}",
                        style = MaterialTheme.typography.labelSmall, maxLines = 1, overflow = TextOverflow.Ellipsis)
                }
                if (summary.reads.size > 20) Text("${summary.reads.size - 20} additional reads omitted from this preview.",
                    style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                Text("Quality summary only. No adapter detection/trimming, variant calling or clinical conclusions.",
                    style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
    }
}

@Composable
private fun SettingsScreen(
    runtime: String?, onRuntime: () -> Unit, onRefresh: () -> Unit,
    themeFamily: String, onThemeFamilyChange: (String) -> Unit,
    biometricEnabled: Boolean, biometricAvailable: Boolean, onBiometricChange: (Boolean) -> Unit,
    modifier: Modifier,
) {
    Frame("Workspace controls", "Settings & diagnostics.", "Understand the device, local data and privacy boundary.", modifier) {
        LazyColumn(verticalArrangement = Arrangement.spacedBy(12.dp), contentPadding = PaddingValues(bottom = 24.dp)) {
            item { SettingGroup("APPEARANCE · THEME", "Choose Light Classic, Dark Classic or follow your Android system appearance. Your choice is saved on this device.") {
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    listOf("light" to "Light", "dark" to "Dark", "system" to "System").forEach { (key, label) ->
                        FilterChip(selected = themeFamily == key, onClick = { onThemeFamilyChange(key) }, label = { Text(label) }, modifier = Modifier.weight(1f))
                    }
                }
                Text("Calligraphic brand accent, editorial display, clear sans-serif UI and monospaced scientific data. Font files remain gated on licence and glyph review.", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            } }
            item { SettingGroup(
                "SECURITY · BIOMETRIC APP UNLOCK",
                "Optional device-local app lock. This is not an online account login. Android manages biometric templates; Kinetics never receives or stores them. Research files remain encrypted at rest independently of this screen lock.",
            ) {
                Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                    Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(3.dp)) {
                        Text("Unlock with biometrics or device credential", style = MaterialTheme.typography.bodyMedium)
                        Text(
                            if (biometricAvailable) "Available on this device" else "No supported biometric or device credential is currently enrolled",
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                        )
                    }
                    Switch(
                        checked = biometricEnabled,
                        onCheckedChange = onBiometricChange,
                        enabled = biometricAvailable || biometricEnabled,
                    )
                }
            } }
            item { SettingGroup("DEVICE RUNTIME", "Python 3.11 and native runtime probes execute locally.") {
                Button(onRuntime, Modifier.fillMaxWidth()) { Text("Run runtime diagnostics") }
                runtime?.let { Text(it, style = MaterialTheme.typography.bodySmall) }
            } }
            item { SettingGroup("LOCAL STORAGE", "Research inputs use Keystore-backed AES-GCM and app-private storage.") {
                OutlinedButton(onRefresh, Modifier.fillMaxWidth()) { Text("Refresh local job state") }
            } }
            item { SettingGroup("PRIVACY", "No cloud account or remote compute service is implied. Imported data stays on this device unless explicitly exported.") }
            item { SettingGroup("DATA PACKS & LICENCES", "Reference packs require version, source, checksum and licence metadata. Third-party engines retain their own terms.") }
            item { SettingGroup("ACCESSIBILITY", "System light/dark mode and font scaling are respected. Status is conveyed with text, not colour alone.") }
            item { SettingGroup("ABOUT KINETICS", "Research Mode · Version 0.0.1 · Apache-2.0 project code. Not for clinical use.") }
            item { Footer() }
        }
    }
}

@Composable
private fun SettingGroup(title: String, description: String, content: @Composable () -> Unit = {}) {
    OutlinedCard(Modifier.fillMaxWidth(), shape = RoundedCornerShape(18.dp)) {
        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(9.dp)) {
            Text(title, color = MaterialTheme.colorScheme.primary, style = MaterialTheme.typography.labelMedium, fontWeight = FontWeight.Bold, letterSpacing = 1.sp)
            Text(description, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
            content()
        }
    }
}


@Composable
private fun InfoPill(label: String) {
    Surface(color = MaterialTheme.colorScheme.surfaceVariant, shape = RoundedCornerShape(50)) {
        Text(label, Modifier.padding(horizontal = 10.dp, vertical = 6.dp),
            style = MaterialTheme.typography.labelSmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant)
    }
}

@Composable
private fun Empty(title: String, detail: String) {
    OutlinedCard(Modifier.fillMaxWidth(), shape = RoundedCornerShape(18.dp)) {
        Column(Modifier.fillMaxWidth().padding(22.dp), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(8.dp)) {
            Text("✧", color = MaterialTheme.colorScheme.primary, fontSize = 30.sp)
            Text(title, fontWeight = FontWeight.Bold)
            Text(detail, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
    }
}

@Composable
private fun Notice(message: String) {
    OutlinedCard(Modifier.fillMaxWidth(), shape = RoundedCornerShape(16.dp)) {
        Row(Modifier.padding(14.dp), verticalAlignment = Alignment.Top, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            Dot(MaterialTheme.colorScheme.secondary)
            Column(verticalArrangement = Arrangement.spacedBy(3.dp)) {
                Text("Workspace notice", fontWeight = FontWeight.SemiBold, style = MaterialTheme.typography.labelMedium)
                Text(message, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
    }
}

@Composable
private fun Dot(color: Color) {
    Box(Modifier.padding(top = 4.dp).size(9.dp).clip(CircleShape).background(color)
        .semantics { contentDescription = "Status indicator" })
}

@Composable
internal fun BiometricLockScreen(
    error: String?,
    themeFamily: String,
    onRetry: () -> Unit,
) {
    val resolvedTheme = when (themeFamily) {
        "system" -> if (isSystemInDarkTheme()) "dark" else "light"
        else -> themeFamily
    }
    val isDark = resolvedTheme == "dark"
    val palette = if (isDark) KineticsTokens.KineticsDarkClassic else KineticsTokens.KineticsLightClassic
    val scheme = if (isDark) {
        darkColorScheme(
            primary = palette.primary,
            onPrimary = palette.background,
            secondary = palette.secondary,
            tertiary = palette.tertiary,
            background = palette.background,
            surface = palette.surface,
            onSurface = palette.text,
            onBackground = palette.text,
            surfaceVariant = palette.surfaceAlt,
            onSurfaceVariant = palette.muted,
            outline = palette.outline,
        )
    } else {
        lightColorScheme(
            primary = palette.primary,
            secondary = palette.secondary,
            tertiary = palette.tertiary,
            background = palette.background,
            surface = palette.surface,
            onSurface = palette.text,
            onBackground = palette.text,
            surfaceVariant = palette.surfaceAlt,
            onSurfaceVariant = palette.muted,
            outline = palette.outline,
        )
    }
    MaterialTheme(colorScheme = scheme, typography = KineticsTypography) {
        Surface(Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.background) {
            Column(
                Modifier
                    .fillMaxSize()
                    .verticalScroll(rememberScrollState())
                    .padding(24.dp),
                verticalArrangement = Arrangement.Center,
                horizontalAlignment = Alignment.CenterHorizontally,
            ) {
                Card(
                    modifier = Modifier.fillMaxWidth().widthIn(max = 480.dp),
                    shape = RoundedCornerShape(28.dp),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
                    border = androidx.compose.foundation.BorderStroke(
                        1.dp, MaterialTheme.colorScheme.outline,
                    ),
                ) {
                    Column(
                        Modifier.fillMaxWidth().padding(28.dp),
                        verticalArrangement = Arrangement.spacedBy(16.dp),
                    ) {
                        Text(
                            "DEVICE SECURITY",
                            color = MaterialTheme.colorScheme.primary,
                            style = MaterialTheme.typography.labelLarge,
                            fontWeight = FontWeight.Bold,
                            letterSpacing = 1.6.sp,
                        )
                        Text(
                            "Welcome back",
                            style = MaterialTheme.typography.headlineLarge,
                            color = MaterialTheme.colorScheme.onSurface,
                        )
                        Text(
                            "Unlock your local Kinetics research workspace.",
                            style = MaterialTheme.typography.bodyLarge,
                            color = MaterialTheme.colorScheme.onSurface,
                        )
                        Text(
                            "Use your enrolled biometric or your device screen credential to continue.",
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                        )
                        if (error != null) {
                            Surface(
                                color = MaterialTheme.colorScheme.errorContainer,
                                shape = RoundedCornerShape(14.dp),
                                modifier = Modifier.fillMaxWidth(),
                            ) {
                                Text(
                                    error,
                                    Modifier.padding(14.dp),
                                    color = MaterialTheme.colorScheme.onErrorContainer,
                                    style = MaterialTheme.typography.bodySmall,
                                )
                            }
                        }
                        Button(
                            onClick = onRetry,
                            modifier = Modifier.fillMaxWidth().heightIn(min = 52.dp),
                            shape = RoundedCornerShape(16.dp),
                        ) {
                            Text("Try again")
                        }
                        Text(
                            "This is a device-local app lock, not an online account sign-in. Android handles biometric data; Kinetics does not receive or store biometric templates.",
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun Footer() {
    Text("KINETICS  •  RESEARCH MODE ONLY  •  NOT FOR CLINICAL USE",
        Modifier.fillMaxWidth().padding(vertical = 8.dp), color = MaterialTheme.colorScheme.onSurfaceVariant,
        style = MaterialTheme.typography.labelSmall, letterSpacing = .8.sp)
}
