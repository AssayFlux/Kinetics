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
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Home
import androidx.compose.material.icons.outlined.Menu
import androidx.compose.material.icons.outlined.Search
import androidx.compose.material.icons.outlined.ArrowBack
import androidx.compose.material.icons.outlined.AccountCircle
import androidx.compose.material.icons.outlined.Settings
import androidx.compose.material.icons.outlined.WorkOutline
import androidx.compose.runtime.*
import androidx.activity.compose.BackHandler
import androidx.compose.runtime.saveable.rememberSaveable
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.luminance
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
import org.assayflux.designsystem.KineticsAppBar
import org.assayflux.designsystem.KineticsField
import org.assayflux.designsystem.KineticsListRow
import org.assayflux.designsystem.KineticsComponentGallery
import org.json.JSONArray
import org.json.JSONObject

internal enum class KineticsTab(val label: String) {
    Home("Home"), Work("Work"), Settings("Settings")
}

@Composable
private fun KineticsTabIcon(tab: KineticsTab) {
    val image = when (tab) {
        KineticsTab.Home -> Icons.Outlined.Home
        KineticsTab.Work -> Icons.Outlined.WorkOutline
        KineticsTab.Settings -> Icons.Outlined.Settings
    }
    Icon(image, contentDescription = null)
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
    onAnalyzeFastq: (ResearchJob, Int) -> Unit,
    themeFamily: String, onThemeFamilyChange: (String) -> Unit,
    biometricEnabled: Boolean, biometricAvailable: Boolean,
    onBiometricChange: (Boolean) -> Unit,
    debugBuild: Boolean,
) {
    var tab by rememberSaveable { mutableStateOf(KineticsTab.Home) }
    var showSearch by rememberSaveable { mutableStateOf(false) }
    var searchQuery by rememberSaveable { mutableStateOf("") }
    var workSearchQuery by rememberSaveable { mutableStateOf("") }
    var showComponentGallery by rememberSaveable { mutableStateOf(false) }
    var showProfile by rememberSaveable { mutableStateOf(false) }
    var selectedServiceDomain by rememberSaveable { mutableStateOf<String?>(null) }
    val context = LocalContext.current
    val capabilities = remember(context) {
        runCatching { loadCapabilityCatalogue(context) }.getOrDefault(emptyList())
    }
    BackHandler(enabled = showSearch || showComponentGallery || showProfile || selectedServiceDomain != null) {
        when {
            showComponentGallery -> showComponentGallery = false
            showSearch -> showSearch = false
            showProfile -> showProfile = false
            else -> selectedServiceDomain = null
        }
    }
    val resolvedTheme = when (themeFamily) {
        "system" -> if (isSystemInDarkTheme()) "dark" else "light"
        else -> themeFamily
    }
    val palette = if (resolvedTheme == "dark") KineticsTokens.KineticsDarkClassic else KineticsTokens.KineticsLightClassic
    val decisionColors = if (resolvedTheme == "dark") KineticsTokens.StatusDark else KineticsTokens.StatusLight
    val scheme = if (resolvedTheme == "light") {
        lightColorScheme(
            primary = palette.primary, secondary = palette.secondary, tertiary = palette.tertiary,
            background = palette.background, surface = palette.surface, onSurface = palette.text,
            onBackground = palette.text, surfaceVariant = palette.surfaceAlt,
            onSurfaceVariant = palette.muted, outline = palette.outline, error = decisionColors.error,
        )
    } else {
        darkColorScheme(
            primary = palette.primary, onPrimary = palette.background,
            secondary = palette.secondary, tertiary = palette.tertiary,
            background = palette.background, surface = palette.surface, onSurface = palette.text,
            onBackground = palette.text, surfaceVariant = palette.surfaceAlt,
            onSurfaceVariant = palette.muted, outline = palette.outline, error = decisionColors.error,
        )
    }
    MaterialTheme(colorScheme = scheme, typography = KineticsTypography) {
      BoxWithConstraints(Modifier.fillMaxSize().windowInsetsPadding(WindowInsets.safeDrawing)) {
        val drawerState = rememberDrawerState(DrawerValue.Closed)
        val drawerScope = rememberCoroutineScope()
        ModalNavigationDrawer(
            drawerState = drawerState,
            gesturesEnabled = true,
            drawerContent = {
                ModalDrawerSheet(
                    modifier = Modifier.fillMaxHeight().widthIn(max = 340.dp),
                    drawerContainerColor = MaterialTheme.colorScheme.surface,
                ) {
                    Column(
                        Modifier.fillMaxWidth().height(160.dp).padding(horizontal = 24.dp, vertical = 20.dp),
                        verticalArrangement = Arrangement.Bottom,
                    ) {
                        Text("KINETICS", style = MaterialTheme.typography.headlineSmall,
                            fontWeight = FontWeight.SemiBold, letterSpacing = 1.4.sp)
                        Spacer(Modifier.height(6.dp))
                        Text("COMPUTATIONAL RESEARCH", style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant, letterSpacing = 1.sp)
                    }
                    HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant)
                    Spacer(Modifier.height(12.dp))
                    KineticsTab.entries.forEach { item ->
                        NavigationDrawerItem(
                            selected = tab == item && selectedServiceDomain == null && !showProfile,
                            onClick = {
                                tab = item
                                selectedServiceDomain = null
                                showProfile = false
                                drawerScope.launch { drawerState.close() }
                            },
                            icon = { KineticsTabIcon(item) },
                            label = { Text(item.label) },
                            modifier = Modifier.padding(horizontal = 12.dp, vertical = 2.dp),
                        )
                    }
                    Spacer(Modifier.weight(1f))
                    HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant)
                    Text("RESEARCH MODE", modifier = Modifier.padding(horizontal = 24.dp, vertical = 18.dp),
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            },
        ) {
            Scaffold(
                containerColor = MaterialTheme.colorScheme.background,
                topBar = {
                    KineticsAppBar(
                        title = when {
                            showSearch -> "Search"
                            showComponentGallery -> "Design system"
                            showProfile -> "Profile"
                            selectedServiceDomain != null -> selectedServiceDomain!!
                            tab == KineticsTab.Home -> ""
                            else -> "KINETICS"
                        },
                        subtitle = when {
                            showSearch -> "Jobs and registered capabilities"
                            showComponentGallery -> "Developer component preview"
                            showProfile -> "Local profile and device security"
                            selectedServiceDomain != null -> "Scientific service workspace"
                            tab == KineticsTab.Home -> ""
                            else -> tab.label
                        },
                        navigation = {
                            if (showSearch || showComponentGallery || showProfile || selectedServiceDomain != null) {
                                IconButton(
                                    onClick = {
                                        when {
                                            showSearch -> showSearch = false
                                            showComponentGallery -> showComponentGallery = false
                                            showProfile -> showProfile = false
                                            else -> selectedServiceDomain = null
                                        }
                                    },
                                    modifier = Modifier.size(48.dp),
                                ) { Icon(Icons.Outlined.ArrowBack, contentDescription = "Back") }
                            } else {
                                IconButton(
                                    onClick = { drawerScope.launch { drawerState.open() } },
                                    modifier = Modifier.size(48.dp),
                                ) { Icon(Icons.Outlined.Menu, contentDescription = "Open navigation menu") }
                            }
                        },
                        actions = {
                            if (!showSearch && !showComponentGallery && !showProfile && selectedServiceDomain == null) {
                                IconButton(onClick = { showSearch = true }, modifier = Modifier.size(48.dp)) {
                                    Icon(Icons.Outlined.Search, contentDescription = "Search jobs and capabilities")
                                }
                                IconButton(onClick = { showProfile = true }, modifier = Modifier.size(48.dp)) {
                                    Icon(Icons.Outlined.AccountCircle, contentDescription = "Open profile")
                                }
                            }
                        },
                    )
                },
            ) { padding ->
                val contentModifier = Modifier.padding(padding)
                when {
                    showComponentGallery -> KineticsComponentGallery()
                    showProfile -> ProfileScreen(biometricEnabled, biometricAvailable)
                    showSearch -> GlobalSearchScreen(
                        query = searchQuery,
                        onQueryChange = { searchQuery = it },
                        jobs = jobs,
                        onSelectJob = { result ->
                            workSearchQuery = result.title
                            showSearch = false
                            tab = KineticsTab.Work
                        },
                        onSelectCapability = { result ->
                            val entry = capabilities.firstOrNull { it.id == result.id.removePrefix("capability:") }
                            selectedServiceDomain = entry?.domain
                            showSearch = false
                        },
                        modifier = contentModifier,
                    )
                    selectedServiceDomain != null -> ServiceDomainScreen(
                        domain = selectedServiceDomain!!,
                        capabilities = capabilities.filter { it.domain == selectedServiceDomain },
                        onImport = onImport,
                        modifier = contentModifier,
                    )
                    else -> when (tab) {
                        KineticsTab.Home -> HomeScreen(
                            jobs, notice, runtimeReport, resolvedTheme, onImport, onRunRuntime,
                            { tab = KineticsTab.Work }, { selectedServiceDomain = it },
                            onCancel, onResume, onDelete, onExport, onExportProvenance,
                            onExportProvenanceSummary, onAnalyzeImported, onExportAnalysis,
                            onAnalyzeFastq, contentModifier,
                        )
                        KineticsTab.Work -> WorkScreen(
                            jobs, workSearchQuery, onImport, onCancel, onResume, onDelete, onExport,
                            onExportProvenance, onExportProvenanceSummary, onAnalyzeImported,
                            onExportAnalysis, onAnalyzeFastq, contentModifier,
                        )
                        KineticsTab.Settings -> SettingsScreen(
                            runtimeReport, onRunRuntime, onRefresh, themeFamily, onThemeFamilyChange,
                            biometricEnabled, biometricAvailable, onBiometricChange,
                            debugBuild, { showComponentGallery = true }, contentModifier,
                        )
                    }
                }
            }
      }
    }
}

@Composable
private fun ProfileScreen(biometricEnabled: Boolean, biometricAvailable: Boolean) {
    Frame("ACCOUNT", "Local profile", "Account services are not configured in this build.", Modifier) {
        Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
            OutlinedCard(Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp)) {
                Column(Modifier.padding(18.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Icon(Icons.Outlined.AccountCircle, contentDescription = null, modifier = Modifier.size(44.dp))
                    Text("No signed-in account", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
                    Text("Kinetics currently has no remote identity provider. A username, account ID, profile image, password reset and cloud sign-out cannot be shown or performed until account services are implemented.",
                        style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
            SettingGroup("DEVICE SECURITY", "The existing biometric option is a local app lock, not account authentication.") {
                Text(
                    when {
                        biometricEnabled && biometricAvailable -> "Biometric/device credential unlock is enabled on this device."
                        biometricAvailable -> "Biometric/device credential unlock is available but not enabled."
                        else -> "No supported biometric/device credential is currently enrolled."
                    },
                    style = MaterialTheme.typography.bodySmall,
                )
                Text("Manage the local app lock in Settings.", style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
    }
}

@Composable
private fun ServiceDomainScreen(
    domain: String,
    capabilities: List<CapabilityEntry>,
    onImport: () -> Unit,
    modifier: Modifier,
) {
    var publicRecord by remember { mutableStateOf<PublicScientificRecord?>(null) }
    Frame("SCIENTIFIC SERVICE", domain, "Capabilities and workflows currently registered for this service area.", modifier) {
        LazyColumn(verticalArrangement = Arrangement.spacedBy(12.dp), contentPadding = PaddingValues(bottom = 24.dp)) {
            if (domain == "Public reference databases") {
                item { PublicDatabaseCard(onStructureFetched = { publicRecord = it }) }
                item { StructureViewerPreview(publicRecord = publicRecord) }
            }
            if (domain == "Sequence analysis") {
                item { FastaQcCard() }
                item { FastqQcCard() }
                item { GeneticCodeInferenceCard() }
            }
            if (domain == "Structural biology") {
                item { StructureViewerPreview(publicRecord = publicRecord) }
                item { StructureSiteAnalysisCard() }
            }
            if (domain == "Computational chemistry") {
                item { LigandGraphPreviewCard() }
            }
            if (domain == "Genomics") {
                item { GenomicsVcfQcCard() }
                item { U5ResearchGateCard() }
            }
            item {
                Text("REGISTERED CAPABILITIES", style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = FontWeight.Bold)
            }
            if (capabilities.isEmpty()) {
                item { Empty("No catalogue entries", "This service area has no registered capability entries yet.") }
            } else {
                items(capabilities, key = { it.id }) { capability ->
                    OutlinedCard(Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp)) {
                        Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(5.dp)) {
                            Text(capability.name, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold)
                            Text(capability.id, style = MaterialTheme.typography.labelSmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant)
                            Text(
                                if (capability.status == "implemented") "Engine registered · Android execution path must be verified per workflow"
                                else "Not implemented",
                                style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                            )
                        }
                    }
                }
            }
            item {
                OutlinedButton(onClick = onImport, modifier = Modifier.fillMaxWidth()) {
                    Text("Import research input")
                }
            }
            item { Footer() }
        }
    }
}

@Composable
private fun GlobalSearchScreen(
    query: String,
    onQueryChange: (String) -> Unit,
    jobs: List<ResearchJob>,
    onSelectJob: (SearchDocument) -> Unit,
    onSelectCapability: (SearchDocument) -> Unit,
    modifier: Modifier,
) {
    val context = LocalContext.current
    val capabilities = remember(context) {
        runCatching { loadCapabilityCatalogue(context) }.getOrDefault(emptyList())
    }
    val documents = remember(jobs, capabilities) {
        jobs.map { job ->
            SearchDocument(
                id = "job:${job.id}",
                title = job.inputName,
                subtitle = "Research job · ${job.state}",
                searchableText = listOfNotNull(job.id, job.sha256, job.message, job.provenanceToolId).joinToString(" "),
                kind = SearchDocument.Kind.JOB,
            )
        } + capabilities.map { capability ->
            SearchDocument(
                id = "capability:${capability.id}",
                title = capability.name,
                subtitle = "${capability.domain} · ${capability.status.replace('_', ' ')}",
                searchableText = "${capability.id} ${capability.implementation} ${capability.evidenceLevel}",
                kind = SearchDocument.Kind.CAPABILITY,
            )
        }
    }
    val results = remember(query, documents) { filterSearchDocuments(query, documents) }
    Frame("Find in Kinetics", "Search your workspace.", "Searches only saved local jobs and the bundled capability catalogue. No network search is performed.", modifier) {
        LazyColumn(verticalArrangement = Arrangement.spacedBy(8.dp), contentPadding = PaddingValues(bottom = 24.dp)) {
            item {
                KineticsField(
                    value = query,
                    onValueChange = onQueryChange,
                    label = "Search jobs and capabilities",
                    supportingText = "Names, job state, capability IDs and implementation metadata",
                )
            }
            if (query.isBlank()) {
                item { Empty("Start with a keyword", "Search a file name, tool name, domain or capability identifier.") }
            } else if (results.isEmpty()) {
                item { Empty("No matching results", "Try a different term. Search is limited to data currently stored on this device and the bundled catalogue.") }
            } else {
                item {
                    Text("${results.size} matching result${if (results.size == 1) "" else "s"}",
                        style = MaterialTheme.typography.labelMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
                items(results, key = { it.id }) { result ->
                    OutlinedCard(Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp)) {
                        KineticsListRow(
                            title = result.title,
                            supportingText = result.subtitle,
                            trailing = { Text("OPEN", style = MaterialTheme.typography.labelSmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant) },
                            onClick = {
                                if (result.kind == SearchDocument.Kind.JOB) onSelectJob(result) else onSelectCapability(result)
                            },
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun Frame(eyebrow: String, title: String, subtitle: String, modifier: Modifier = Modifier, content: @Composable () -> Unit) {
    BoxWithConstraints(modifier.fillMaxSize(), contentAlignment = Alignment.TopCenter) {
      val horizontalPadding = when {
          maxWidth < 390.dp -> 16.dp
          maxWidth < 600.dp -> 20.dp
          else -> 24.dp
      }
      val sectionGap = if (maxWidth < 390.dp) 16.dp else 24.dp
      Column(Modifier.fillMaxWidth().widthIn(max = 840.dp).padding(horizontal = horizontalPadding),
        verticalArrangement = Arrangement.spacedBy(sectionGap)) {
        Column(Modifier.padding(top = 20.dp), verticalArrangement = Arrangement.spacedBy(5.dp)) {
            Text(eyebrow, color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.labelMedium)
            Text(title, style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold)
            Text(subtitle, color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.bodyMedium)
        }
        Box(Modifier.weight(1f).fillMaxWidth()) { content() }
      }
    }
}

@Composable
private fun RuntimeStatusCard(label: String, status: String, modifier: Modifier = Modifier) {
    val colors = if (MaterialTheme.colorScheme.background.luminance() < 0.5f) KineticsTokens.StatusDark else KineticsTokens.StatusLight
    val tint = when (status) { "OK" -> colors.success; "Not working" -> colors.error; else -> colors.warning }
    OutlinedCard(modifier, shape = RoundedCornerShape(10.dp)) {
        Column(Modifier.padding(9.dp), verticalArrangement = Arrangement.spacedBy(5.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(5.dp)) {
                Box(Modifier.size(8.dp).clip(CircleShape).background(tint))
                Text(status, style = MaterialTheme.typography.labelSmall, color = tint, fontWeight = FontWeight.Bold)
            }
            Text(label, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurface,
                maxLines = 2, overflow = TextOverflow.Ellipsis)
        }
    }
}

@Composable
private fun HomeScreen(
    jobs: List<ResearchJob>, notice: String, runtime: String?, themeFamily: String, onImport: () -> Unit,
    onRuntime: () -> Unit, onOpenWork: () -> Unit, onOpenService: (String) -> Unit,
    onCancel: (ResearchJob) -> Unit, onResume: (ResearchJob) -> Unit,
    onDelete: (ResearchJob) -> Unit, onExport: (ResearchJob) -> Unit,
    onExportProvenance: (ResearchJob) -> Unit,
    onExportProvenanceSummary: (ResearchJob) -> Unit, onAnalyzeImported: (ResearchJob) -> Unit,
    onExportAnalysis: (ResearchJob) -> Unit, onAnalyzeFastq: (ResearchJob, Int) -> Unit, modifier: Modifier,
) {
    val context = LocalContext.current
    val services = remember(context) { runCatching { loadCapabilityCatalogue(context) }.getOrDefault(emptyList()) }
    val active = jobs.count { it.state in listOf("queued", "running", "cancel_requested") }
    val done = jobs.count { it.state == "succeeded" }
    val attention = jobs.count { it.state in listOf("failed", "recovery_required") }
    val pythonPart = runtime?.substringAfter("Python probe:", "")?.substringBefore("Native probe:")?.trim()
    val nativePart = runtime?.substringAfter("Native probe:", "")?.trim()
    val pythonState = when { runtime == null -> "Not checked"; pythonPart.isNullOrBlank() -> "Partial"; pythonPart.contains("FAILED", true) -> "Not working"; pythonPart.contains("WARNING", true) || pythonPart.contains("PARTIAL", true) -> "Partial"; else -> "OK" }
    val nativeState = when { runtime == null -> "Not checked"; nativePart.isNullOrBlank() -> "Partial"; nativePart.contains("FAILED", true) -> "Not working"; nativePart.contains("WARNING", true) || nativePart.contains("PARTIAL", true) -> "Partial"; else -> "OK" }
    val storageState = when { runtime == null -> "Not checked"; runtime.contains("Keystore AES-GCM + versioned file roundtrip: passed") -> "OK"; runtime.contains("Keystore AES-GCM + versioned file roundtrip: FAILED") -> "Not working"; else -> "Partial" }
    BoxWithConstraints(modifier.fillMaxSize()) {
        LazyColumn(Modifier.fillMaxSize(), verticalArrangement = Arrangement.spacedBy(14.dp), contentPadding = PaddingValues(bottom = 24.dp)) {
            item { WorkspaceCarousel(services = services, onOpenService = onOpenService) }
            item {
                DashboardPanel("SYSTEM READINESS", "Runtime and protected storage", "Sequence engine: $pythonState  ·  Native engine: $nativeState  ·  Private storage: $storageState", "Run diagnostics", onRuntime)
            }
            item {
                DashboardPanel("RESEARCH WORK", "$active active · $done complete · $attention need attention", "Your locally stored research jobs and their current lifecycle state.", "Open Work", onOpenWork)
            }
            item {
                val latest = jobs.firstOrNull()
                DashboardPanel("RECENT ACTIVITY", latest?.inputName ?: "No research activity yet",
                    latest?.let { "Latest job: ${it.state} · timestamp ${it.analysisCreatedAt ?: it.provenanceCreatedAt ?: "unavailable"}" } ?: "Import a research input to begin your first local job.",
                    if (latest == null) "Import input" else "View Work", if (latest == null) onImport else onOpenWork)
            }
            item {
                DashboardPanel("LOCAL DATA & REFERENCES", "Private research storage", "Imported files remain in app-private storage. Public reference retrieval is available as a dedicated service.", "Open databases", { onOpenService("Public reference databases") })
            }
            if (notice.isNotBlank()) item { Notice(notice) }
            item { Footer() }
        }
    }
}

@Composable
private fun DashboardPanel(
    eyebrow: String,
    title: String,
    detail: String,
    actionLabel: String,
    onAction: () -> Unit,
) {
    OutlinedCard(Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp)) {
        Column(Modifier.fillMaxWidth().padding(16.dp), verticalArrangement = Arrangement.spacedBy(7.dp)) {
            Text(eyebrow, style = MaterialTheme.typography.labelSmall, letterSpacing = 1.sp,
                color = MaterialTheme.colorScheme.onSurfaceVariant)
            Text(title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
            Text(detail, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            TextButton(onClick = onAction, contentPadding = PaddingValues(0.dp)) { Text(actionLabel) }
        }
    }
}

@Composable
private fun WorkspaceCarousel(
    services: List<CapabilityEntry>,
    onOpenService: (String) -> Unit,
) {
    val domains = remember(services) { services.map { it.domain }.distinct().sorted() + "Public reference databases" }
    val pager = rememberPagerState(pageCount = { domains.size })
    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
        HorizontalPager(
            state = pager,
            contentPadding = PaddingValues(horizontal = 42.dp),
            pageSpacing = 12.dp,
            modifier = Modifier.fillMaxWidth(),
        ) { page ->
            val domain = domains[page]
            val count = services.count { it.domain == domain }
            Card(
                onClick = { onOpenService(domain) },
                modifier = Modifier.fillMaxWidth().height(218.dp),
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant),
            ) {
                Column(Modifier.fillMaxSize().padding(18.dp), verticalArrangement = Arrangement.SpaceBetween) {
                    Column(verticalArrangement = Arrangement.spacedBy(9.dp)) {
                        Text(if (domain == "Public reference databases") "REFERENCE DATA" else "SCIENTIFIC SERVICE",
                            style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant,
                            letterSpacing = 1.1.sp)
                        Text(domain, style = MaterialTheme.typography.headlineSmall,
                            color = MaterialTheme.colorScheme.onSurface, fontWeight = FontWeight.SemiBold)
                        Text(if (domain == "Public reference databases") "Search and retrieve public records directly inside Kinetics."
                            else "$count registered capabilities in this service area.",
                            style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                    Text("OPEN SERVICE  →", style = MaterialTheme.typography.labelLarge,
                        color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                }
            }
        }
        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.Center, verticalAlignment = Alignment.CenterVertically) {
            repeat(domains.size) { index ->
                val selected = pager.currentPage == index
                Box(
                    Modifier.padding(horizontal = 3.dp)
                        .size(width = if (selected) 20.dp else 7.dp, height = 7.dp)
                        .clip(RoundedCornerShape(50))
                        .background(if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.outline),
                )
            }
        }
    }
}

@Composable
private fun Metric(label: String, value: String, modifier: Modifier) {
    OutlinedCard(modifier, shape = RoundedCornerShape(12.dp)) {
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
    jobs: List<ResearchJob>, initialQuery: String, onImport: () -> Unit, onCancel: (ResearchJob) -> Unit,
    onResume: (ResearchJob) -> Unit, onDelete: (ResearchJob) -> Unit,
    onExport: (ResearchJob) -> Unit, onExportProvenance: (ResearchJob) -> Unit,
    onExportProvenanceSummary: (ResearchJob) -> Unit, onAnalyzeImported: (ResearchJob) -> Unit,
    onExportAnalysis: (ResearchJob) -> Unit, onAnalyzeFastq: (ResearchJob, Int) -> Unit, modifier: Modifier,
) {
    var query by rememberSaveable(initialQuery) { mutableStateOf(initialQuery) }
    var filter by rememberSaveable { mutableStateOf("All") }
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
                    shape = RoundedCornerShape(10.dp), label = { Text("Search research jobs") })
            }
            item {
                Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                    listOf("All", "Active", "Complete", "Attention").forEach {
                        FilterChip(filter == it, { filter = it }, label = { Text(it) })
                    }
                }
            }
            item { Button(onClick = onImport, Modifier.fillMaxWidth(), shape = RoundedCornerShape(10.dp)) { Text("Import new data") } }
            if (filtered.isEmpty()) item { Empty("No matching research jobs", "Try another search or import a dataset to begin.") }
            else items(filtered, key = { it.id }) { JobCard(it, onCancel, onResume, onDelete, onExport, onExportProvenance, onExportProvenanceSummary, onAnalyzeImported, onExportAnalysis, onAnalyzeFastq) }
        }
    }
}

@Composable
private fun JobCard(job: ResearchJob, onCancel: (ResearchJob) -> Unit, onResume: (ResearchJob) -> Unit,
                    onDelete: (ResearchJob) -> Unit, onExport: (ResearchJob) -> Unit,
                    onExportProvenance: (ResearchJob) -> Unit,
                    onExportProvenanceSummary: (ResearchJob) -> Unit,
                    onAnalyzeImported: (ResearchJob) -> Unit,
                    onExportAnalysis: (ResearchJob) -> Unit,
    onAnalyzeFastq: (ResearchJob, Int) -> Unit) {
    val active = job.state in listOf("queued", "running", "cancel_requested")
    val success = job.state == "succeeded"
    val issue = job.state in listOf("failed", "recovery_required")
    var provenanceExpanded by rememberSaveable(job.id) { mutableStateOf(false) }
    var showPhredDialog by rememberSaveable(job.id) { mutableStateOf(false) }
    var selectedPhredOffset by rememberSaveable(job.id) { mutableIntStateOf(33) }
    OutlinedCard(Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp)) {
        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(9.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Box(Modifier.size(40.dp).clip(RoundedCornerShape(12.dp)).background(MaterialTheme.colorScheme.surfaceVariant), contentAlignment = Alignment.Center) {
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
                        shape = RoundedCornerShape(12.dp),
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
                    val result = remember(job.id, job.analysisResultJson) {
                        runCatching { JSONObject(job.analysisResultJson) }.getOrNull()
                    }
                    Text("Method: ${job.analysisToolId ?: "unknown"} · Version: ${job.analysisToolVersion ?: "unknown"}",
                        style = MaterialTheme.typography.labelSmall)
                    job.analysisCreatedAt?.let { created ->
                        Text("Saved: ${java.time.format.DateTimeFormatter.ISO_INSTANT.format(java.time.Instant.ofEpochMilli(created))}",
                            style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                    Text("Input SHA-256: ${job.sha256 ?: "not recorded"}",
                        style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    job.analysisParametersJson?.let {
                        Text("Parameters: $it", style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                    if (result != null) {
                        Text("Records: ${result.optInt("record_count")} · Total bases: ${result.optLong("total_bases")}",
                            style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.SemiBold)
                        if (result.has("phred_offset")) Text(
                            "Encoding: Phred+${result.optInt("phred_offset")} · Mean quality: ${result.optDouble("mean_phred")}",
                            style = MaterialTheme.typography.bodySmall)
                        if (result.has("q20_fraction")) Text(
                            "Q20: ${"%.1f".format(result.optDouble("q20_fraction") * 100)}% · Q30: ${"%.1f".format(result.optDouble("q30_fraction") * 100)}%",
                            style = MaterialTheme.typography.bodySmall)
                        val records = result.optJSONArray("records") ?: result.optJSONArray("reads")
                        if (records != null) {
                            Text("RECORD PREVIEW", style = MaterialTheme.typography.labelSmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant)
                            for (index in 0 until minOf(records.length(), 5)) {
                                val item = records.optJSONObject(index) ?: continue
                                val summary = buildString {
                                    append(item.optString("identifier", "record ${index + 1}"))
                                    append(" · ${item.optInt("length")} bases")
                                    if (item.has("gc_percent")) append(" · GC ${item.optDouble("gc_percent")}%")
                                    if (item.has("mean_phred")) append(" · mean Q ${item.optDouble("mean_phred")}")
                                }
                                Text(summary, style = MaterialTheme.typography.bodySmall)
                            }
                            if (records.length() > 5) Text("Showing first 5 of ${records.length()} records. Export the full result for all records.",
                                style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                        val limitations = result.optJSONArray("limitations")
                        if (limitations != null) {
                            Text("LIMITATIONS", style = MaterialTheme.typography.labelSmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant)
                            for (index in 0 until limitations.length()) {
                                Text("• ${limitations.optString(index)}", style = MaterialTheme.typography.bodySmall)
                            }
                        }
                    } else {
                        Text("Saved result is not valid JSON and cannot be rendered as a structured preview. The original stored record remains exportable.",
                            style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.error)
                    }
                    TextButton(onClick = { onExportAnalysis(job) }) { Text("Export complete analysis JSON") }
                }
            }
            Row(horizontalArrangement = Arrangement.spacedBy(7.dp)) {
                if (active) OutlinedButton(onClick = { onCancel(job) }) { Text("Cancel") }
                if (job.state == "cancelled" || job.state == "failed") OutlinedButton(onClick = { onResume(job) }) { Text("Resume") }
                if (success && job.analysisResultJson == null && job.inputName.lowercase().removeSuffix(".gz").substringAfterLast('.') in setOf("fa", "fasta", "fna")) OutlinedButton(onClick = { onAnalyzeImported(job) }) { Text("Run FASTA QC") }
                if (success && job.inputName.lowercase().removeSuffix(".gz").substringAfterLast('.') in setOf("fastq", "fq")) OutlinedButton(onClick = { showPhredDialog = true }) { Text("Run FASTQ QC") }
                if (success) Button(onClick = { onExport(job) }) { Text("Export") }
                if (success || issue || job.state == "cancelled") OutlinedButton(onClick = { onDelete(job) }) { Text("Delete") }
            }
        }
    }
    if (showPhredDialog) AlertDialog(
        onDismissRequest = { showPhredDialog = false },
        title = { Text("Choose FASTQ quality encoding") },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text("Kinetics never guesses the Phred offset. Select the encoding used by this file.")
                listOf(33, 64).forEach { offset ->
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        RadioButton(selected = selectedPhredOffset == offset, onClick = { selectedPhredOffset = offset })
                        Column {
                            Text("Phred+$offset", style = MaterialTheme.typography.bodyMedium)
                            Text(if (offset == 33) "Sanger / modern Illumina" else "Legacy Illumina 1.3–1.7",
                                style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }
                }
            }
        },
        confirmButton = { TextButton(onClick = { showPhredDialog = false; onAnalyzeFastq(job, selectedPhredOffset) }) { Text("Run QC") } },
        dismissButton = { TextButton(onClick = { showPhredDialog = false }) { Text("Cancel") } },
    )
}

@Composable
private fun StatePill(state: String) {
    val text = when (state) {
        "succeeded" -> "COMPLETE"; "queued" -> "QUEUED"; "running" -> "RUNNING"
        "cancel_requested" -> "STOPPING"; "failed" -> "FAILED"; "cancelled" -> "CANCELLED"
        "recovery_required" -> "RECOVERY"; else -> state.uppercase()
    }
    val statusColors = if (MaterialTheme.colorScheme.background.luminance() < 0.5f) {
        KineticsTokens.StatusDark
    } else {
        KineticsTokens.StatusLight
    }
    val statusColor = when (state) {
        "succeeded" -> statusColors.success
        "failed" -> statusColors.error
        "recovery_required" -> statusColors.warning
        "queued", "running", "cancel_requested" -> statusColors.information
        else -> MaterialTheme.colorScheme.onSurfaceVariant
    }
    Surface(
        color = MaterialTheme.colorScheme.surfaceVariant,
        shape = RoundedCornerShape(6.dp),
        modifier = Modifier.semantics { contentDescription = "Job status: $text" },
    ) {
        Text(text, Modifier.padding(horizontal = 10.dp, vertical = 6.dp),
            style = MaterialTheme.typography.labelSmall,
            color = statusColor)
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
private fun FastaQcCard() {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    var fastaText by rememberSaveable {
        mutableStateOf(">example_sequence\nACGTACGTGCGTNNACGT\n")
    }
    var running by remember { mutableStateOf(false) }
    var result by remember { mutableStateOf<SequenceQcResult?>(null) }
    var error by remember { mutableStateOf<String?>(null) }

    OutlinedCard(Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp)) {
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
    OutlinedCard(Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp)) {
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
    debugBuild: Boolean, onOpenComponentGallery: () -> Unit,
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
                Text("System sans-serif typography is used. Additional font files require licence and glyph review.", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
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
            item { SettingGroup("DEVICE RUNTIME", "Scientific processing and storage checks run locally on this device.") {
                Button(onRuntime, Modifier.fillMaxWidth()) { Text("Run runtime diagnostics") }
                val pythonPart = runtime?.substringAfter("Python probe:", "")?.substringBefore("Native probe:")?.trim()
                val nativePart = runtime?.substringAfter("Native probe:", "")?.trim()
                val pythonState = when {
                    runtime == null -> "Not checked"
                    pythonPart.isNullOrBlank() -> "Partial"
                    pythonPart.contains("FAILED", true) -> "Not working"
                    pythonPart.contains("WARNING", true) || pythonPart.contains("PARTIAL", true) -> "Partial"
                    else -> "OK"
                }
                val nativeState = when {
                    runtime == null -> "Not checked"
                    nativePart.isNullOrBlank() -> "Partial"
                    nativePart.contains("FAILED", true) -> "Not working"
                    nativePart.contains("WARNING", true) || nativePart.contains("PARTIAL", true) -> "Partial"
                    else -> "OK"
                }
                val storageState = when {
                    runtime == null -> "Not checked"
                    runtime.contains("Keystore AES-GCM + versioned file roundtrip: passed") -> "OK"
                    runtime.contains("FAILED", true) -> "Not working"
                    else -> "Partial"
                }
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    RuntimeStatusCard("Sequence engine", pythonState, Modifier.weight(1f))
                    RuntimeStatusCard("Native engine", nativeState, Modifier.weight(1f))
                    RuntimeStatusCard("Private storage", storageState, Modifier.weight(1f))
                }
            } }
            item { SettingGroup("LOCAL STORAGE", "Research inputs use Keystore-backed AES-GCM and app-private storage.") {
                OutlinedButton(onRefresh, Modifier.fillMaxWidth()) { Text("Refresh local job state") }
            } }
            item { SettingGroup(
                "PRIVACY · LOCAL DATA INVENTORY",
                "This app has no cloud account or remote compute service. Public reference searches send only the chosen public query/accession to approved database endpoints; imported research files stay local. The following information is stored locally:",
            ) {
                Text("• Imported inputs: AES-256-GCM encrypted chunks in the app's no-backup private directory. Plaintext is materialized temporarily in app-private cache for analysis/export and is removed on normal completion; stale prefixed cache files older than 24 hours are cleaned at store startup.",
                    style = MaterialTheme.typography.bodySmall)
                Text("• Job database: input display name, selected content URI, job state, byte count, SHA-256, timestamps, storage path and import provenance are stored in the app-private SQLite database. This metadata database is not separately encrypted by the current implementation.",
                    style = MaterialTheme.typography.bodySmall)
                Text("• Analysis results: FASTA/FASTQ result JSON and method parameters are currently stored in that SQLite database. Treat the device's app-private storage and OS account protection as part of the security boundary.",
                    style = MaterialTheme.typography.bodySmall)
                Text("• Public reference records: raw FASTA/mmCIF payloads are encrypted with Android Keystore AES-GCM in app-private no-backup storage. Source metadata and public FASTA QC JSON are stored in a separate app-private SQLite database and are not separately encrypted.",
                    style = MaterialTheme.typography.bodySmall)
                Text("• Public network requests: only user-entered public names/accessions are sent to NCBI, UniProtKB or RCSB. Raw sequences, VCFs, patient/sample identifiers and private research files are not submitted. Retrieved data are parsed and analysed locally.",
                    style = MaterialTheme.typography.bodySmall)
                Text("• Preferences: appearance, onboarding acknowledgement and the optional local app-lock setting are stored in private SharedPreferences.",
                    style = MaterialTheme.typography.bodySmall)
                Text("• Exports: only created after you select a destination in Android's document picker. Copies at that destination are outside Kinetics' control.",
                    style = MaterialTheme.typography.bodySmall)
                Text("Deletion removes the app-managed files and database rows where operations succeed. Flash-storage secure erasure and deletion of exported copies cannot be guaranteed. Android backup is disabled in the app manifest; merged-manifest and device verification remain pending.",
                    style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                Text("Screenshot/Recents protection is not enabled pending explicit threat review and owner approval. Do not treat the optional app lock as protection against a compromised or rooted device.",
                    style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            } }
            item { SettingGroup("DATA PACKS & LICENCES", "Reference packs require version, source, checksum and licence metadata. Third-party engines retain their own terms.") }
            item { SettingGroup("ACCESSIBILITY", "System light/dark mode and font scaling are respected. Status is conveyed with text, not colour alone.") }
            item { SettingGroup("ABOUT KINETICS", "Research Mode · Version 0.0.1 · Apache-2.0 project code. Not for clinical use.") }
            if (debugBuild) item {
                SettingGroup("DESIGN SYSTEM · DEVELOPER", "Open the live V1 component gallery. This route is available only in debug builds.") {
                    OutlinedButton(onClick = onOpenComponentGallery, modifier = Modifier.fillMaxWidth()) {
                        Text("Open component gallery")
                    }
                }
            }
            item { Footer() }
        }
    }
}

@Composable
private fun SettingGroup(title: String, description: String, content: @Composable () -> Unit = {}) {
    OutlinedCard(Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp)) {
        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(9.dp)) {
            Text(title, color = MaterialTheme.colorScheme.onSurface, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold)
            Text(description, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
            content()
        }
    }
}


@Composable
private fun InfoPill(label: String) {
    Surface(color = MaterialTheme.colorScheme.surfaceVariant, shape = RoundedCornerShape(6.dp)) {
        Text(label, Modifier.padding(horizontal = 8.dp, vertical = 4.dp),
            style = MaterialTheme.typography.labelSmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant)
    }
}

@Composable
private fun Empty(title: String, detail: String) {
    OutlinedCard(Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp)) {
        Column(Modifier.fillMaxWidth().padding(22.dp), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(8.dp)) {
            Text("No recent items", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 13.sp)
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
                    shape = RoundedCornerShape(16.dp),
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
                                shape = RoundedCornerShape(6.dp),
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
                            shape = RoundedCornerShape(10.dp),
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
    Text("KINETICS · Research Mode only · Not for clinical use",
        Modifier.fillMaxWidth().padding(vertical = 8.dp), color = MaterialTheme.colorScheme.onSurfaceVariant,
        style = MaterialTheme.typography.labelSmall, letterSpacing = .8.sp)
}
