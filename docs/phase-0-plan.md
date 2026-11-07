# Phase 0 plan — audit, safe migration foundation and registry

## Scope
1. Record the remote repository baseline and constraints in AUDIT.md.
2. Preserve all 160 domain definitions and convert them into individual small YAML-compatible files.
3. Add a machine-readable capability registry and CI consistency checker.
4. Rewrite README to accurately describe the Android-first target and current implementation status.
5. Record Android feasibility as untested; do not infer device capability.
6. Keep all science source paths unchanged in this slice. Migrate only after import/test path plans exist.

## Safety
- Work directly on main; do not create a branch.
- Never change LICENSE.
- No destructive removals until the archive tag exists and candidate paths have been reviewed.
- Do not claim local working-tree status from remote GitHub data.

## Exit checks
- Exactly 160 unique domain YAML definitions.
- Registry checker passes and is wired into CI.
- Existing source modules and tests remain unchanged.
- README claims match the registry and audit.
- Existing CI remains green.
- No Android/device/16 KB/Play-policy claims without evidence.

## Deferred
- Archive tag creation is blocked by current connector capabilities; deletion/archive cleanup is deferred.
- Full source migration and Kotlin/Compose skeleton are deferred until the base registry is stable.
- LICENSE selection remains exclusively the project owner's decision.
