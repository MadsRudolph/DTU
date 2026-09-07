# HyperSketch Companion 1.1

An Obsidian desktop plugin that serves a local tablet drawing app. All rendering happens on the tablet. Finished drawings are saved as ordinary cropped SVGs plus editable `.hypersketch.json` files inside the current vault.

## On another PC after Git pull

1. Open this repository's **Obsidian** folder as your vault. Allow community plugins if Obsidian asks; trust settings are controlled by Obsidian.
2. Reload Obsidian if it was already open during the pull. **HyperSketch Companion** is included in the vault's enabled-plugin list.
3. Open **Settings → HyperSketch Companion**. Choose **Tailscale** or **Local Wi-Fi / LAN** and scan the QR with your tablet. The QR uses this PC's network addresses and a pairing key generated on this PC.
4. Open any Markdown note in editing mode. Draw on the tablet, check the displayed target note, and tap **Insert**. Repeat with other notes as needed. The server is built into Obsidian; do not run the standalone demo at the same time.

No npm install, build step, external relay, fixed worktree path, or background Node process is required. The plugin works in whichever vault contains it. Desktop Obsidian must remain open; allow its network access in the host firewall if the OS asks. Git remains your laptop↔home vault synchronization mechanism.

## Connections and PWA

- **Tailscale:** connect both devices to the same tailnet. Select Tailscale in plugin settings. Its detected 100.64.0.0/10 address works over HTTP for drawing.
- **Local Wi-Fi / LAN:** devices need a network permitting client-to-client connections. Choose the appropriate adapter if the PC has several. Guest-network/eduroam client isolation requires Tailscale or USB.
- **USB:** optional mode displays `adb reverse tcp:27123 tcp:27123` and a localhost QR.
- **Installable PWA:** HTTPS is required. Optionally run `tailscale serve --bg http://127.0.0.1:27123` on each host and paste the HTTPS URL it prints into that PC's plugin settings. Scan the refreshed QR, then use Chrome's Install / Add to home screen command. This is a per-host setup; the desktop's HTTPS hostname is not copied to a laptop.
- **Pairing:** the URL fragment contains a secret. The app remembers it on that origin for PWA launches. Reset pairing in settings if needed. `data.json` holds machine preferences, the key, and receipts and is intentionally Git-ignored.

An installed PWA can reopen its cached interface offline and retains completed strokes locally. Insertion requires a connection to the host running Obsidian. Switching HTTP/HTTPS or PCs changes browser origin and draft storage: insert or download a draft before switching.

## Engineering tools

- Freehand with immediate local feedback; optional pen-only input; stroke eraser.
- Solid, dashed, dotted strokes. Widths 2/3/5 and multiple colors.
- Line, arrow, rectangle and ellipse: choose a tool and drag.
- **Hold: ON:** draw a freehand line and pause the pen for about 550 ms before lifting; it straightens. Turn Hold off for handwritten derivations that contain pauses.
- Symbols: resistor, capacitor, ground, op-amp. Choose one, then tap to place. Each symbol remains one movable figure.
- Text labels: choose Text label and tap to enter a label.
- Select / move: tap near a stroke or symbol, then drag it. The selection outline is not exported. Use ✕ to delete it.
- **Rotate:** choose Select / move, tap a figure, then use ⟲ / ⟳ with 15°, 45°, or 90° steps. Components, shapes, strokes, and text rotate around their center. Rotation is saved, exported, and undoable.
- Undo / redo support drawing, erasing, moving, deleting and clearing.
- 💾 downloads an editable `.hypersketch` drawing. 📂 opens that format or the `.hypersketch.json` source saved in your vault. SVG previews remain usable without the plugin.
- Dots, square grid, or blank background. Grid is excluded from export. The paper fits below the controls and keeps its proportions.

This release is a usable engineering sketch toolkit, not a CAD/simulation system. Pen width is fixed rather than pressure-based. Selection moves whole figures; free-transform resizing, multi-select, image import, circuit netlists and handwriting recognition are not implemented. Whole-stroke erasing removes geometry and stays consistent with exported SVG.

## Delivery behavior

The tablet sends a validated drawing model with a stable submission ID. The plugin creates the SVG itself, saves the editable source and inserts the embed into the displayed target's open Markdown editor. Retries reuse the same ID, avoiding duplicate insertion. A closed or read-only target produces an error while the tablet retains its drawing. All assets are relative to the current vault. Attachment folder and embed width can be configured.

## Development

`main.js` is a committed self-contained build; only `main.js`, `manifest.json`, and `styles.css` are needed at runtime. Source modules and vendor QR code are kept here for maintenance. The build embeds geometry, PWA assets, and the QR generator so runtime module resolution cannot depend on a developer machine.

From the repository root:

    node tools/build-hypersketch.cjs
    node --test tools/test-engineering.cjs
    node tools/test-original-ink.cjs

The build pins esbuild 0.25.12. QR generator attribution is in vendor/LICENSE. Browser tests generate `/tmp/hypersketch-original-browser-test.html`; open it or run Chromium headless and inspect `#test-results`. Tests cover input/palm behavior, hold-to-straighten, shapes, move/delete/undo/redo, visible grid pixels, viewport fit, SVG/model validation, QR addressing and authenticated plugin insertion into multiple notes. Physical Tab S9 latency and installation UI still require device testing.
