# Local Browser Workbench

**Status:** Local pilot implementation. This is not a deployed multi-user application.

## What the workflow does

The browser workflow supports one focused path: capture a business offering, target audience, objective, differentiators, and call to action; edit a short card storyboard; save a versioned campaign brief and JSON manifest; render a watermarked H.264 MP4; and inspect or download the brief, manifest, MP4, and renderer provenance sidecar.

It is intentionally limited to title cards. The UI does not accept local file paths or upload image, video, audio, logo, or model assets. The existing CLI renderer supports sourced media separately.

## Prerequisites

- Python 3.11 or later.
- FFmpeg with `drawtext` and `libx264`, FFprobe, and a supported system TrueType font for rendering.
- A browser on the same machine.

The UI can open and save campaign plans without FFmpeg installed, but rendering will fail with an actionable error unless the renderer requirements are met.

## Start it

From the repository root:

    python tools/workbench_server.py

Open <http://127.0.0.1:8765/> on the same computer. Keep the terminal open. Press Ctrl+C to stop the server. Change the port with `--port`, for example `python tools/workbench_server.py --port 8766`.

## Typical workflow

1. Enter the actual offering, audience, objective, differentiators, and call to action. Track factual statements in the claims/evidence ledger using documented-source, direct-observation, inference, or unverified. Documented-source and direct-observation entries require a reference or observation note.
2. Edit the storyboard cards and duration. The current UI permits 1–8 cards and caps a storyboard at 90 seconds.
3. Save the project. The app writes a Markdown brief and a versioned JSON manifest; changes create a new version rather than replacing the old manifest.
4. Render a draft. The fixed `INTERNAL REVIEW DRAFT - NOT FOR PUBLICATION` watermark cannot be removed from this UI.
5. Play or download the MP4, and inspect/download the provenance manifest to confirm the renderer version, output checksum, media properties, and release blockers.
6. Review facts, source evidence, media rights, brand use, privacy, creative quality, and publication permission separately. Ledger references are user-entered and are not opened or independently verified by the app. A technically verified MP4 is not a release approval.

## Local data and security boundary

- The server binds only to `127.0.0.1`; it does not expose a remote-listening host option.
- Host validation and same-origin checks reject remote Host headers and cross-origin mutations. The UI uses a restrictive Content Security Policy and writes user text via safe text properties, not injected HTML.
- Project folders and versioned artifacts are saved under `.workbench/projects/`. `.workbench/` is ignored by Git and should not be committed. Store only material you are permitted to keep on this machine.
- There is no login, role system, remote access, database, queue, backup, or encrypted-at-rest store. Loopback-only is a useful boundary for a local pilot, not a substitute for a production threat model. Do not expose the server through a tunnel, reverse proxy, or LAN port.
- Rendering is a synchronous local request; a long render occupies the request until it completes. Stop the server only after the render request has returned.
- Saving a new version retains earlier versioned briefs, manifests, and completed renders. Delete the `.workbench/projects/<project-id>/` folder to remove a project and its local artifacts; back it up separately if retention is required.

## Known gaps before beta

This UI does not yet provide asset uploads, automatic claim discovery from storyboard copy, authenticated review and approval, team collaboration, durable job queues, cancellation/retry history, a database, deployment, retention automation, or a live ContribQuest product walkthrough. The ledger is manual and does not establish claim truth. It is not a campaign publishing tool.

The release gate remains a separate concept from technical render success. A watermark and a locally editable approval field would not prove the identity or authority of a reviewer, so this UI exposes neither unwatermarked output nor a pretend authenticated-approval control.
