package org.assayflux.designsystem

import androidx.compose.material3.Typography
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp

/**
 * D-015 role-based typography.
 *
 * System serif/sans/monospace families are deliberate fallbacks while the
 * requested Cormorant Garamond, IBM Plex Sans and IBM Plex Mono binaries
 * undergo exact-version, licence, Indic-glyph and offline-size review.
 * Great Vibes is not used until the owner logo's wordmark is visually audited.
 */
private val BaseTypography = Typography()

val KineticsTypography = BaseTypography.copy(
    displayLarge = BaseTypography.displayLarge.copy(
        fontFamily = FontFamily.Serif,
        fontWeight = FontWeight.Normal,
        letterSpacing = (-0.4).sp,
    ),
    displayMedium = BaseTypography.displayMedium.copy(
        fontFamily = FontFamily.Serif,
        fontWeight = FontWeight.Normal,
    ),
    displaySmall = BaseTypography.displaySmall.copy(
        fontFamily = FontFamily.Serif,
        fontWeight = FontWeight.Normal,
    ),
    headlineLarge = BaseTypography.headlineLarge.copy(
        fontFamily = FontFamily.Serif,
        fontWeight = FontWeight.SemiBold,
    ),
    headlineMedium = BaseTypography.headlineMedium.copy(
        fontFamily = FontFamily.Serif,
        fontWeight = FontWeight.SemiBold,
    ),
    headlineSmall = BaseTypography.headlineSmall.copy(
        fontFamily = FontFamily.Serif,
        fontWeight = FontWeight.SemiBold,
    ),
    titleLarge = BaseTypography.titleLarge.copy(fontFamily = FontFamily.SansSerif),
    titleMedium = BaseTypography.titleMedium.copy(fontFamily = FontFamily.SansSerif),
    titleSmall = BaseTypography.titleSmall.copy(fontFamily = FontFamily.SansSerif),
    bodyLarge = BaseTypography.bodyLarge.copy(fontFamily = FontFamily.SansSerif),
    bodyMedium = BaseTypography.bodyMedium.copy(fontFamily = FontFamily.SansSerif),
    bodySmall = BaseTypography.bodySmall.copy(fontFamily = FontFamily.SansSerif),
    labelLarge = BaseTypography.labelLarge.copy(fontFamily = FontFamily.SansSerif),
    labelMedium = BaseTypography.labelMedium.copy(fontFamily = FontFamily.SansSerif),
    labelSmall = BaseTypography.labelSmall.copy(fontFamily = FontFamily.SansSerif),
)

/** Scientific identifiers and numeric summaries use a stable monospaced fallback. */
val KineticsScientificTextStyle = BaseTypography.bodyMedium.copy(
    fontFamily = FontFamily.Monospace,
    letterSpacing = 0.sp,
)
