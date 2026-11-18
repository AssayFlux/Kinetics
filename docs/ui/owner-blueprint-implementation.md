# Owner UI Blueprint — Login and Dashboard

**Authority:** Owner-approved reference images supplied on 2026-11-18.  
**Platform:** Native Android / Jetpack Compose.  
**Visual authority:** D-024 Premium Minimal Monochrome Design System V1 remains authoritative for final colours, typography, spacing, iconography, accessibility and light/dark behavior. The colours in the reference drawings are structural placeholders unless separately approved.

## 1. Reference assets

The source images are preserved in the repository:
- `Assets/App UI - Login Page Design.jpg`
- `Assets/App UI - Dashboard Design.jpg`

Do not move, rename, duplicate or delete these assets during implementation.

## 2. Login / unlock screen

The first reference establishes:
- A quiet, uncluttered canvas framed by a thin rounded outline.
- One large, centrally positioned rounded panel.
- Four vertically stacked, full-width rounded controls.
- A fingerprint action centered in the lowest control.
- No dashboard, service carousel or primary navigation on this screen.

The drawing does not label the four controls. Their labels and behavior must not be invented. The current Android implementation provides a device-local biometric/device-credential app lock only. That lock is not an online account sign-in. Until a real identity provider and account backend are implemented, the screen must identify itself accurately as a local unlock flow; it must not fabricate usernames, user IDs, password reset or cloud-account behavior. Biometric templates remain managed by Android.

## 3. Dashboard structure

The second reference defines the Home screen's hierarchy:

### 3.1 Header
- Hamburger/menu control at the upper left.
- User avatar/profile control at the upper right.
- No persistent bottom navigation.
- The hamburger drawer contains Home, Work and Settings (and any other implemented global destinations).
- The avatar opens the account/profile area. Display only identity data actually available. Local device security and account authentication must remain clearly distinguished.

### 3.2 Primary service carousel
- A large horizontal pager directly below the header, containing one card per registered service capability (68 catalogue entries at the current audit baseline) plus the Public Reference Databases service.
- The active/central card is prominent; neighboring cards remain partially visible to communicate horizontal navigation.
- Pagination indicators sit immediately below the cards.
- Each card represents a real service present in the repository's capability catalogue.
- Every card is an actionable control. Selecting one opens a dedicated service destination.
- The catalogue and implementation status are the source of truth; do not invent capabilities. Each card is keyed by its stable capability ID and opens the corresponding dedicated service detail destination.
- A destination may report that a capability is registered but not yet available through an Android execution path. Never imply that registration alone means it can run on-device.
- Do not place a second, duplicate service catalogue below the carousel.

### 3.3 Four dashboard panels
Four full-width, vertically stacked rounded panels follow the carousel. Their exact geometry and order are structural requirements. Their contents should be concise, live summaries derived from real application state, such as:
1. Runtime / engine readiness.
2. Active and queued research work.
3. Recent research activity.
4. Local storage and public-reference retrieval status.

These are summaries, not additional service launchers. Do not fabricate counts, health states, progress, ETAs or results. When a value is unavailable, show an honest not-checked/unknown state.

## 4. Service destinations

Move service-specific workflows and controls out of Home and into the relevant dedicated destination. This includes the public database retrieval workflow, structure viewer/preview, chemistry/ligand tools, FASTA/FASTQ QC, genetic-code inference, and genomics/VCF tools where their current implementations exist. Keep each existing engine, privacy boundary, provenance behavior and evidence limitation intact.

Where a service is not yet implemented or lacks a real Android dispatcher, its page must clearly state that status and must not offer a fake run action. Service destinations must be individually addressable from carousel cards and support system back navigation.

## 5. Navigation and account behavior

- Remove the persistent Home / Work / Settings bottom bar on all phone layouts.
- Do not replace it with a persistent navigation rail on larger layouts; use the requested drawer navigation consistently.
- Drawer entries: Home, Work, Settings; add destinations only when they are real and useful.
- The top-right avatar opens a profile/account destination.
- Profile may show only locally available and user-provided profile data. No synthetic identity or ID.
- Password reset, remote login, registration and sign-out require a real account service. Until one exists, label them unavailable/not configured rather than simulating success.
- Existing biometric unlock remains a local device lock, not a user account.

## 6. Visual and interaction rules

- D-024 monochrome visual language wins over placeholder colours in the reference images.
- Semantic decision/status colours may be used only for meaningful states and must not dominate the monochrome interface.
- Preserve the reference hierarchy, rounded panel/card language, alignment, whitespace and carousel composition.
- Respect Android safe drawing insets, system appearance, font scaling, accessibility semantics and back behavior.
- All visible controls must work; no decorative/dead carousel cards.
- Keep native Jetpack Compose and existing design-system tokens/components.
- Preserve scientific and privacy behavior; do not move patient data into public network requests, CI fixtures or repository content.

## 7. Acceptance checklist

- [ ] Login/local-unlock screen follows the first reference structure.
- [ ] Four controls are not assigned invented semantics.
- [ ] Biometric action is connected to Android's actual biometric/device-credential flow.
- [ ] Home header has working hamburger and profile controls.
- [ ] No persistent bottom navigation or rail.
- [x] Service carousel uses repository-backed catalogue entries, one card per capability plus Public Reference Databases.
- [x] Carousel pagination presents a five-indicator window while supporting the full service list.
- [x] Each capability card opens its own ID-addressed service detail destination.
- [x] Cards are clickable and open dedicated service destinations.
- [ ] Pagination reflects the actual carousel page.
- [ ] Service workflows are removed from the Home content column and placed in their relevant destinations.
- [ ] Four dashboard panels show only persisted/runtime-derived information.
- [ ] No duplicate service list remains on Home.
- [ ] Profile does not claim remote account/password features without a backend.
- [ ] Light/dark/system themes, safe insets and accessibility are retained.
- [ ] Android unit tests and CI build pass.
- [ ] Device screenshots and interaction tests are recorded before declaring visual/device acceptance.

## 8. Evidence and completion policy

Track implementation, automated build/test evidence, and physical-device acceptance separately. A green CI build does not establish visual fidelity or device testing. A registered scientific capability does not establish scientific validation or clinical suitability. Clinical diagnosis, treatment and dosing remain outside the app's validated scope unless separately governed and validated.
