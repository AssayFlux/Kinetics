package org.assayflux.kinetics

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

private val Teal = Color(0xFF36D6C3)
private val Ink = Color(0xFF101B2B)
private val Muted = Color(0xFF9AAFC5)
private val LightTeal = Color(0xFF087F78)

internal enum class KineticsTab(val label: String, val glyph: String) {
    Home("Home", "⌂"), Work("Work", "▤"), Explore("Explore", "⌕"), Settings("Settings", "⚙")
}

@Composable
internal fun KineticsAppShell(
    jobs: List<ResearchJob>, notice: String, runtimeReport: String?,
    onImport: () -> Unit, onRefresh: () -> Unit, onRunRuntime: () -> Unit,
    onCancel: (ResearchJob) -> Unit, onResume: (ResearchJob) -> Unit,
    onDelete: (ResearchJob) -> Unit, onExport: (ResearchJob) -> Unit,
) {
    var tab by rememberSaveable { mutableStateOf(KineticsTab.Home) }
    var themeFamily by rememberSaveable { mutableStateOf("dark") }
    val scheme = when (themeFamily) {
        "light" -> lightColorScheme(primary = Color(0xFF315D91), secondary = Color(0xFF6685AD), background = Color(0xFFF7FAFF), surface = Color.White, onSurface = Color(0xFF14253B), onBackground = Color(0xFF14253B), surfaceVariant = Color(0xFFEAF1FA), onSurfaceVariant = Color(0xFF52647A), outline = Color(0xFFCBD7E5))
        "neon" -> darkColorScheme(primary = Color(0xFF00F5FF), onPrimary = Color(0xFF071018), secondary = Color(0xFFFF3DF2), background = Color(0xFF080611), surface = Color(0xFF110D20), onSurface = Color(0xFFF5F1FF), onBackground = Color(0xFFF5F1FF), surfaceVariant = Color(0xFF1C1530), onSurfaceVariant = Color(0xFFB6AFC9), outline = Color(0xFF44305E))
        else -> darkColorScheme(primary = Color(0xFF39D7E8), onPrimary = Color(0xFF071018), secondary = Color(0xFF6B9CFF), background = Color(0xFF070B12), surface = Color(0xFF0E1521), onSurface = Color(0xFFEAF3FF), onBackground = Color(0xFFEAF3FF), surfaceVariant = Color(0xFF151F2E), onSurfaceVariant = Color(0xFF9AADC4), outline = Color(0xFF2A3B50))
    }
    MaterialTheme(colorScheme = scheme) {
        BoxWithConstraints(Modifier.fillMaxSize()) {
            // Classify the app window, not the physical device. These are the
            // current Android adaptive breakpoints recorded in docs/ui/verified-specs.md.
            val compactHeight = maxHeight < 480.dp
            val useDrawer = maxWidth >= 1200.dp
            val useRail = maxWidth >= 600.dp || compactHeight

            @Composable
            fun Screen(modifier: Modifier) {
                when (tab) {
                    KineticsTab.Home -> HomeScreen(jobs, notice, runtimeReport, themeFamily, onImport, onRefresh,
                        onRunRuntime, { tab = KineticsTab.Work }, onCancel, onResume, onDelete, onExport, modifier)
                    KineticsTab.Work -> WorkScreen(jobs, onImport, onCancel, onResume, onDelete, onExport, modifier)
                    KineticsTab.Explore -> ExploreScreen(modifier)
                    KineticsTab.Settings -> SettingsScreen(runtimeReport, onRunRuntime, onRefresh, themeFamily,
                        { themeFamily = it }, modifier)
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
    Column(modifier.fillMaxSize().padding(horizontal = 20.dp), verticalArrangement = Arrangement.spacedBy(16.dp)) {
        Column(Modifier.padding(top = 20.dp), verticalArrangement = Arrangement.spacedBy(5.dp)) {
            Text(eyebrow.uppercase(), color = MaterialTheme.colorScheme.primary, style = MaterialTheme.typography.labelMedium, fontWeight = FontWeight.Bold, letterSpacing = 1.4.sp)
            Text(title, style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold)
            Text(subtitle, color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.bodyMedium)
        }
        Box(Modifier.weight(1f).fillMaxWidth()) { content() }
    }
}

@Composable
private fun HomeScreen(
    jobs: List<ResearchJob>, notice: String, runtime: String?, themeFamily: String, onImport: () -> Unit,
    onRefresh: () -> Unit, onRuntime: () -> Unit, onOpenWork: () -> Unit,
    onCancel: (ResearchJob) -> Unit, onResume: (ResearchJob) -> Unit,
    onDelete: (ResearchJob) -> Unit, onExport: (ResearchJob) -> Unit, modifier: Modifier,
) {
    val active = jobs.count { it.state in listOf("queued", "running", "cancel_requested") }
    val done = jobs.count { it.state == "succeeded" }
    val attention = jobs.count { it.state in listOf("failed", "recovery_required") }
    Frame("Your research workspace", "Good science starts here.", "A private, local-first environment for computational research.", modifier) {
        LazyColumn(verticalArrangement = Arrangement.spacedBy(16.dp), contentPadding = PaddingValues(bottom = 24.dp)) {
            item { HeroCard(onImport, themeFamily) }
            item {
                Row(horizontalArrangement = Arrangement.spacedBy(9.dp), modifier = Modifier.fillMaxWidth()) {
                    Metric("ACTIVE", active.toString(), Modifier.weight(1f))
                    Metric("COMPLETE", done.toString(), Modifier.weight(1f))
                    Metric("ATTENTION", attention.toString(), Modifier.weight(1f))
                }
            }
            item { Section("Recent activity", "View all", onOpenWork) }
            if (jobs.isEmpty()) item { Empty("Your workspace is clear", "Import a research file to create your first job.") }
            else items(jobs.take(4), key = { it.id }) { JobCard(it, onCancel, onResume, onDelete, onExport) }
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
private fun HeroCard(onImport: () -> Unit, themeFamily: String) {
    val dark = themeFamily != "light"
    Card(Modifier.fillMaxWidth(), shape = RoundedCornerShape(28.dp),
        colors = CardDefaults.cardColors(containerColor = if (dark) Color(0xFF0B1724) else Color(0xFFE8F0F8))) {
        Box {
            Image(
                painter = painterResource(R.drawable.kinetics_background),
                contentDescription = null,
                contentScale = ContentScale.Crop,
                modifier = Modifier.matchParentSize().alpha(if (dark) 0.42f else 0.14f),
            )
            Box(
                Modifier.matchParentSize().background(
                    Brush.verticalGradient(
                        listOf(
                            if (dark) Color(0xCC07111E) else Color(0xBFEAF2FA),
                            if (dark) Color(0xF207111E) else Color(0xF2EAF2FA),
                        )
                    )
                )
            )
            Column(Modifier.padding(22.dp), verticalArrangement = Arrangement.spacedBy(13.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Box(Modifier.size(36.dp).clip(RoundedCornerShape(12.dp)).background(if (dark) Teal else LightTeal), contentAlignment = Alignment.Center) {
                    Text("K", color = Color.White, fontWeight = FontWeight.Black, fontSize = 21.sp)
                }
                Spacer(Modifier.width(10.dp))
                Text("KINETICS  /  RESEARCH OS", style = MaterialTheme.typography.labelMedium, fontWeight = FontWeight.Bold, letterSpacing = 1.sp)
                Spacer(Modifier.weight(1f))
                AssistChip(onClick = {}, label = { Text("LOCAL FIRST") })
            }
            Text("Your data. Your science. Your device.", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
            Text("Bring in research data and prepare a reproducible analysis workspace. Files are encrypted locally during import.",
                color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.bodyMedium)
            Button(onClick = onImport, Modifier.fillMaxWidth().height(54.dp), shape = RoundedCornerShape(16.dp),
                colors = ButtonDefaults.buttonColors(containerColor = if (dark) Teal else LightTeal)) {
                Text("+   Import research data", fontWeight = FontWeight.Bold, color = if (dark) Ink else Color.White)
            }
            Text("FASTA  ·  FASTQ  ·  PDB/mmCIF  ·  SDF  ·  Other files",
                style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
    }
}

@Composable
private fun Metric(label: String, value: String, modifier: Modifier) {
    OutlinedCard(modifier, shape = RoundedCornerShape(18.dp)) {
        Column(Modifier.padding(11.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
            Text(label, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = FontWeight.Bold, maxLines = 1)
            Text(value, style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold)
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
    onExport: (ResearchJob) -> Unit, modifier: Modifier,
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
            else items(filtered, key = { it.id }) { JobCard(it, onCancel, onResume, onDelete, onExport) }
        }
    }
}

@Composable
private fun JobCard(job: ResearchJob, onCancel: (ResearchJob) -> Unit, onResume: (ResearchJob) -> Unit,
                    onDelete: (ResearchJob) -> Unit, onExport: (ResearchJob) -> Unit) {
    val active = job.state in listOf("queued", "running", "cancel_requested")
    val success = job.state == "succeeded"
    val issue = job.state in listOf("failed", "recovery_required")
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
            Row(horizontalArrangement = Arrangement.spacedBy(7.dp)) {
                if (active) OutlinedButton(onClick = { onCancel(job) }) { Text("Cancel") }
                if (job.state == "cancelled" || job.state == "failed") OutlinedButton(onClick = { onResume(job) }) { Text("Resume") }
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
    AssistChip(onClick = {}, label = { Text(text, style = MaterialTheme.typography.labelSmall) })
}

@Composable
private fun ExploreScreen(modifier: Modifier) {
    val groups = listOf(
        Triple("Genomics & genetics", "FASTA/FASTQ, variants and gene annotation foundations.", "Parser and selected annotation primitives"),
        Triple("Transcriptomics & omics", "Expression transforms, count-aware statistics and cross-omics exploration.", "Independent reference validation required"),
        Triple("Protein & structure", "PDB/mmCIF parsing, contacts, RMSD and structural descriptors.", "Exploratory geometry; no validated molecular viewer"),
        Triple("Chemistry", "SDF parsing, molecular graphs and descriptor foundations.", "Advanced features depend on optional engines"),
        Triple("Phylogenetics", "Distance matrices, UPGMA, neighbour joining and bootstrap foundations.", "Likelihood/model selection remains future work"),
        Triple("Kinetics & statistics", "Growth models, regression, uncertainty and diagnostics.", "Validation and calibration vary by method"),
        Triple("Pharmacogenomics", "Gene reference data and conservative phased haplotype matching.", "No prescribing or treatment recommendations"),
    )
    Frame("Scientific toolkit", "Explore the science.", "A transparent catalogue of research capabilities and their maturity.", modifier) {
        LazyColumn(verticalArrangement = Arrangement.spacedBy(12.dp), contentPadding = PaddingValues(bottom = 24.dp)) {
            item {
                Card(shape = RoundedCornerShape(20.dp), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)) {
                    Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                        Text("Capability transparency", fontWeight = FontWeight.Bold)
                        Text("A module is not runnable until its Android dispatcher, input contract and result viewer are connected. This catalogue does not claim that all listed methods are validated.",
                            color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.bodySmall)
                    }
                }
            }
            items(groups) { (title, description, maturity) ->
                OutlinedCard(Modifier.fillMaxWidth(), shape = RoundedCornerShape(18.dp)) {
                    Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(7.dp)) {
                        Text(title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                        Text(description, style = MaterialTheme.typography.bodyMedium)
                        HorizontalDivider(color = MaterialTheme.colorScheme.outline.copy(alpha = .5f))
                        Text(maturity, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        AssistChip(onClick = {}, label = { Text("Research foundations") })
                    }
                }
            }
        }
    }
}

@Composable
private fun SettingsScreen(runtime: String?, onRuntime: () -> Unit, onRefresh: () -> Unit, themeFamily: String, onThemeFamilyChange: (String) -> Unit, modifier: Modifier) {
    Frame("Workspace controls", "Settings & diagnostics.", "Understand the device, local data and privacy boundary.", modifier) {
        LazyColumn(verticalArrangement = Arrangement.spacedBy(12.dp), contentPadding = PaddingValues(bottom = 24.dp)) {
            item { SettingGroup("APPEARANCE · THEME FAMILY", "Choose a visual family. Dark is the default; selection survives activity recreation.") {
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    listOf("light" to "Light", "dark" to "Dark", "neon" to "Neon").forEach { (key, label) ->
                        FilterChip(selected = themeFamily == key, onClick = { onThemeFamilyChange(key) }, label = { Text(label) }, modifier = Modifier.weight(1f))
                    }
                }
                Text("26 distinct font families are catalogued; font files remain gated on licence and accessibility review.", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
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
private fun Footer() {
    Text("KINETICS  •  RESEARCH MODE ONLY  •  NOT FOR CLINICAL USE",
        Modifier.fillMaxWidth().padding(vertical = 8.dp), color = MaterialTheme.colorScheme.onSurfaceVariant,
        style = MaterialTheme.typography.labelSmall, letterSpacing = .8.sp)
}
