# Deterministic Campaign Renderer

**Status:** The renderer is implemented and covered by local FFmpeg/FFprobe integration tests. A separate loopback-only browser workflow now orchestrates a restricted card-only campaign path on top of it. This remains a local pilot, not a deployed multi-user application.

## Purpose and boundaries

The renderer assembles local assets and text cards into a real MP4 without model weights, GPU access, or remote-generation credentials. Its manifest contract supports card, still-image, and video scenes plus optional looped background audio. The browser UI currently submits card scenes only. The renderer does not author factual claims, verify remote evidence, manage user accounts, capture approval signatures, or replace creative review.

A media file that passes technical validation is not automatically approved for publication.

## Requirements

- Python 3.11 or later (standard library only).
- Installed FFmpeg with the drawtext filter, libx264 and AAC encoding.
- FFprobe on PATH, plus fontconfig or a supported system TrueType font.
- Local assets only. Network URLs are not accepted as asset paths.

Set environment variables FFMPEG_BIN and FFPROBE_BIN if the executables are not on PATH.

## Render the included ContribQuest concept

From the repository root, run:

    python tools/render_campaign.py examples/contribquest-campaign.json --output outputs/contribquest-concept.mp4

The example defaults to a 1920x1080 H.264 MP4 at 30 fps and adds a draft watermark. It uses text-card scenes rather than recorded application UI and remains a concept until the owner reviews claims and a live walkthrough is recorded.

The renderer refuses to overwrite an existing output unless --overwrite is passed. It prints a JSON result and writes a sidecar manifest beside the video.

## Run the browser workbench

From the repository root, run:

    python tools/workbench_server.py

Then open http://127.0.0.1:8765/ on the same computer. Keep the terminal open. See [Local Browser Workbench](LOCAL_WORKBENCH.md) for the browser workflow, local storage, security boundary, and limits.

The browser app captures the offering, audience, objective, differentiators, call to action, and a short card storyboard. It saves a versioned Markdown brief and campaign JSON, invokes this renderer for that saved version, and exposes the watermarked MP4 plus the technical/provenance report. Unlike the general CLI, the UI does not accept image/video/audio assets or filesystem paths. It always uses a fixed watermark and does not expose an unwatermarked release action.

## Campaign manifest contract

- schema_version must be 1.
- project.id and project.title identify the campaign.
- output specifies MP4 path, dimensions, frame rate, and review watermark.
- scenes contains 1–24 unique cards, still images, or video clips. A scene is capped at 90 seconds and the campaign at 300 seconds.
- Image/video scenes and optional audio require a source path contained in the campaign directory plus provenance: origin, rights_status, and supporting evidence when the status is licensed, permission-confirmed, or public-domain.
- claims_evidence records claim text, evidence state (documented-source, direct-observation, inference, or unverified), and a reference. The renderer preserves the ledger; it does not independently verify remote sources.
- approval records draft, approved, or rejected, with approver and timezone-aware timestamp for approved status.

A local manifest may contain test/stub outputs, but test and illustrative content must remain distinguishable from genuine captured product footage.

## Technical validation

A successful run must:

1. Execute FFmpeg without shell interpolation.
2. Render to temporary staging storage.
3. Run FFprobe against that exact output.
4. Validate one H.264 video stream, requested dimensions and frame rate, expected duration and exact decoded frame count, and an AAC audio stream when requested (or no audio otherwise).
5. Atomically move the validated file into place and write a JSON sidecar containing the input manifest hash, source hashes/provenance, tool versions, output hash and size, technical validation, claim evidence, approval state, and release blockers.

Missing executables/fonts, invalid assets, unsafe paths, malformed manifests, filesystem errors, failed encoding, or failed media checks produce a non-zero exit and a structured JSON error without a Python traceback. A failed validation must never be reported as a successful render.

## Approval and rights gates

The default output is watermarked INTERNAL REVIEW DRAFT. An unwatermarked CLI output is blocked unless a timezone-aware approval record is present, every claim has evidence marked documented-source or direct-observation, and sourced media does not have unverified rights status.

The browser workflow is stricter by design: it uses a fixed INTERNAL REVIEW DRAFT - NOT FOR PUBLICATION watermark and has no control to remove it. It does not provide authentication, reviewer roles, upload intake, or a publication path.

The sidecar records claims and approval as assertions supplied by the manifest, not as independent legal or factual validation. A human must verify rights, evidence, product behavior, privacy, creative quality, and publication permission.

## Test command

    python -m unittest discover --start-directory tests --pattern "test_*.py" --verbose

The test suite includes actual FFmpeg/FFprobe integration tests for title cards, image/video sources, optional audio, codec, dimensions, duration, frame rate, path safety, provenance, and sidecar output. Local-workbench tests cover brief/manifest generation, validation limits, versioned persistence, release-gate separation, and failure state. These tests do not establish production deployment or live end-to-end behavior in ContribQuest.
