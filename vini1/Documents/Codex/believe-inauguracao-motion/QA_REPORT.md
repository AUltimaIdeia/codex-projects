# QA Report

## Scope
- Master vertical video for B. Living inauguration.
- 136 SRT-derived text screens.
- Duration: 276.000s.

## Generated Assets
- data/captions.json
- data/captions.ass
- index.html
- tools/render-video.mjs

## Verification Status
- Project generation: passed.
- Caption count: passed (136 screens).
- MP4 render: pending.
- Visual/audio inspection: pending after render.

## Known Environment Notes
- Local workspace path C:\Users\MEU CODEX\PROJECTS\B. LIVING is read-only for this user; production files were created in C:\Users\vini1\Documents\Codex\believe-inauguracao-motion.
- HyperFrames CLI was not available through npm/npx in PATH. The source follows the HyperFrames HTML contract, and final MP4 rendering uses local FFmpeg.
