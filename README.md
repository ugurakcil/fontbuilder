# Font Builder (TTF → WOFF2 + SEO-Optimized CSS)

This tool scans all font family folders inside your `fonts` directory, converts every `.ttf` file to `.woff2`, and generates **SEO-friendly, performance-optimized** CSS files per family.

Each font family gets its own `.css` file (e.g., `barlow.css`, `barlow_condensed.css`, `funnel_display.css`).  
Existing CSS files are **never overwritten**.

---

## Features
- **Automatic conversion:** `.ttf → .woff2` using Google’s WOFF2 compressor  
- **SEO & performance optimized:** Uses `font-display: swap` and prioritizes WOFF2  
- **Variable font support:** Generates a single `@font-face` block with `font-weight: 100 900`  
- **Recursive scanning:** Works through all subfolders (`Barlow`, `Barlow_Condensed`, `Funnel_Display`, etc.)  
- **Idempotent behavior:** Existing CSS files are skipped (no accidental overwrites)

---

## ⚙️ Requirements
Python 3.7+  
`woff2_compress` command-line tool (Google WOFF2)

### macOS
```bash
brew install woff2
