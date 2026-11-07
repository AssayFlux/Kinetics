# Android feasibility — not yet assessed

**Status:** BLOCKED / NOT STARTED (R0)

No Android project, SDK/NDK build, emulator run, physical-device run, APK or AAB is present. No claim is made about embedded Python/Biopython arm64 feasibility; Rust app calls; C++ JNI; engine cross-compilation; RDKit; offline Mol*/3Dmol.js; 16 KB alignment; package size; cold start; memory; thermal/battery; background execution; SAF or WebGL.

R1 must test a named arm64 device and emulator, record toolchain versions, commands, raw logs and outcomes, then produce a go/no-go matrix for owner review. Target device decision D-006 remains open. CI's R0 native/Android job reports this blocker; it is not a passing feasibility test.
