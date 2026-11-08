# Kinetics Android UI/UX specification

**Status:** Design baseline — implementation and usability validation still required.
**Product boundary:** Research Mode only. This interface is not for diagnosis, treatment, patient management or clinical decision support.

## Product principles

1. Scientific work is the primary task; navigation and decoration must not obscure it.
2. Large local datasets are first-class: show file identity, byte progress, resumability, integrity and storage state.
3. No silent state changes. Explain permissions, encryption, cancellation, recovery and export outcomes in plain language.
4. Offline-first. Never imply cloud upload or remote execution when work is local.
5. Accessible by default: scalable text, high contrast, semantic labels, touch targets, keyboard/switch navigation and non-colour status cues.
6. Distinguish capability implementation from scientific validation. Unvalidated methods carry an explicit experimental label and link to method notes.

## Information architecture

Bottom navigation (four destinations):
- **Home** — research workspace summary, primary import action, recent jobs and runtime health.
- **Work** — all jobs, filters by state, job detail, progress, provenance, cancel/resume/delete/export.
- **Explore** — analysis families and supported input formats. Each tool card states required input, engine, maturity and limitations. Disabled/unavailable capabilities are not presented as ready-to-run.
- **Settings** — runtime diagnostics, data packs and licenses, storage/recovery, privacy/security, accessibility and app version.

## Home screen

- Compact app bar with Kinetics identity, Research Mode chip and settings shortcut.
- Welcome/summary panel with counts of active and completed jobs.
- Prominent **Import data** action with accepted-format guidance and large-file note.
- Recent activity list with state text, progress where available, last update and a clear action to open details.
- Runtime status panel for Python/native probes; probe execution is user initiated and results are timestamped.
- Persistent, dismissible notice area for actionable errors and recovery requirements.

## Work and job detail

- Filterable job list: All, Active, Completed, Needs attention.
- Job detail includes original filename, format, byte count, SHA-256, created/updated timestamps, selected engine/version, parameter snapshot and provenance.
- State presentation uses icon + text, never colour alone.
- Queued/running jobs expose cancellation; failed/cancelled jobs expose retry only when source permission and retained data make retry possible.
- Recovery-required jobs explain that ciphertext is preserved and that a lost Android Keystore key cannot be recreated from ciphertext.
- Export uses Android Storage Access Framework and confirms destination/result; partial export failures are explicit.
- Destructive deletion uses a clear confirmation and describes limits of flash storage erasure.

## Explore

- Group tools by Genomics, Transcriptomics/Omics, Protein & Structure, Chemistry, Phylogenetics, Kinetics/Statistics and Pharmacogenomics.
- Every tool descriptor must show: input types, output types, engine/dependency, online/offline requirements, validation maturity, known limitations and provenance emitted.
- Do not show a Run action for capabilities without an executable Android dispatcher.
- Experimental/reference-only methods are visibly marked and cannot be mistaken for validated clinical methods.

## Settings

- Runtime diagnostics: Python, native C++/Rust, ABI, dependency and probe results.
- Data packs: version, source, checksum, license, install/update/remove state.
- Storage: encrypted input count/size, recovery-needed jobs, export behavior and clear-storage actions with warnings.
- Privacy: local processing boundary and permissions.
- Accessibility: system font scaling and theme/high-contrast behavior.
- About: app version, source revision, licenses, research-only disclaimer.

## Visual language

- Material 3 foundations with a restrained scientific-workbench feel.
- Deep ink/navy surfaces, teal/blue action accents, neutral cards and restrained amber/red status accents.
- Rounded cards, clear section hierarchy, generous whitespace, compact but readable data rows.
- No decorative charts without data; all scientific plots must include units, axes, method and provenance.
- Light and dark themes; respect system setting.

## Delivery sequence

1. Extract import, job, export and diagnostics behavior into state holders/view models without changing storage/security semantics.
2. Build shared theme, app shell, bottom navigation, Home, Work/job detail, Explore and Settings.
3. Add progress and state mapping from WorkManager/ResearchStore; keep all existing SAF and crypto guarantees.
4. Add Compose previews and unit/UI tests for navigation, state rendering, accessibility semantics, large font and empty/error/loading states.
5. Run JVM tests and arm64 APK/AAB build; then manual device verification for touch, layout, file picker, background import, process death and accessibility.

## Exit criteria

- All four destinations work and are reachable with consistent navigation.
- Existing import, cancellation, retry, export, deletion, key-loss and runtime-probe behavior is preserved.
- No capability is shown as executable unless its Android dispatcher is wired.
- Empty, loading, success, partial, failed and recovery-required states are designed and tested.
- Compose tests cover navigation and critical workflows; accessibility checks and real-device review are recorded.
