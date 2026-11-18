package org.assayflux.kinetics

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Card
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

/** Visible dependency boundary: unavailable PGx and host-only engines are not fake launch actions. */
@Composable
internal fun U5ResearchGateCard() {
    Card(Modifier.fillMaxWidth()) {
        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            Text("PGx · NOT ENABLED", style = MaterialTheme.typography.titleSmall)
            Text(
                "P2 parsers and phased-definition matching are research software foundations only. No licensed release-pinned allele pack, broad biological concordance or qualified review is approved for this app. Individual genotype interpretation, star-allele/diplotype/phenotype assignment and guideline recommendations remain unavailable while P0 is NOT APPROVED.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Text("IN-SILICO ENGINES · HOST ONLY", style = MaterialTheme.typography.titleSmall)
            Text(
                "Docking and OpenMM adapters remain host-side research tools. No secured compute node is deployed, no validated force-field package is selected, and no ADMET model or dataset is approved. These engines are not bundled or presented as runnable on Android.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Text(
                "P0 GATE · BLOCKED / NOT APPROVED",
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.error,
            )
            Text(
                "No patient data, human-subject data, clinical reports, diagnosis, treatment or dosing workflows are permitted. The VCF panel above is restricted to synthetic or authorized public non-patient data and returns aggregate syntax/QC counts only.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
    }
}
