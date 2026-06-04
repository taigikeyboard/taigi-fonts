# TaigiKeyboard Fonts

This repository contains converted font assets for TaigiKeyboard.

## License Boundary

The repository root [LICENSE](LICENSE) is MIT, but it applies only to the repository metadata and documentation files in this repository.

The font files under [fonts/](fonts) are **not MIT licensed**. Each font directory includes its own `LICENSE.txt` and `SOURCE.txt`, and those upstream font licenses control use, redistribution, modification, and attribution requirements for the font files.

## Layout

Each font is stored in its own directory so the app can download, verify, cache, and delete fonts by `fontId`.

- `fonts/<font-id>/font.otf` or `font.ttf`
- `fonts/<font-id>/LICENSE.txt`
- `fonts/<font-id>/SOURCE.txt`

The machine-readable index is [manifest.json](manifest.json).
