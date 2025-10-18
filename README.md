# Font Builder (TTF → WOFF2 + SEO-Optimized CSS)

This script scans all font family folders inside your "fonts" directory, converts every .ttf file to .woff2, and generates SEO-friendly and performance-optimized CSS files per family.

Each font family gets its own .css file (for example: barlow.css, barlow_condensed.css, funnel_display.css).
Existing CSS files are never overwritten.

## FEATURES

Automatic conversion from .ttf to .woff2 using Google’s WOFF2 compressor

SEO and performance optimized: uses font-display: swap and prioritizes WOFF2

Variable font support (font-weight: 100 900)

Recursive directory scanning through all subfolders

Idempotent: existing CSS files are skipped safely

## REQUIREMENTS

Python 3.7 or newer

The command-line tool woff2_compress (Google WOFF2 toolchain)

Check Python version:
`python3 --version`

If Python is installed, create a virtual environment (recommended):
```
python3 -m venv venv
source venv/bin/activate (on macOS/Linux)
venv\Scripts\activate (on Windows)
```

Then continue with the WOFF2 tool installation below.

## INSTALLING woff2_compress

macOS:
`brew install woff2`

Debian / Ubuntu:
`sudo apt-get install woff2`

If the package is not found, build it manually:
```
sudo apt-get install brotli
git clone https://github.com/google/woff2.git

cd woff2 && make
sudo cp woff2_compress /usr/local/bin
```

Check the installation:
`woff2_compress -h`

If this command shows help text instead of an error, it’s installed correctly.

## USAGE

Assume you have a folder structure like this:

```
/assets/fonts/
├── Barlow/
│ ├── Barlow-Regular.ttf
│ └── Barlow-Bold.ttf
├── Barlow_Condensed/
│ └── BarlowCondensed-Regular.ttf
└── Funnel_Display/
├── FunnelDisplay-VariableFont_wght.ttf
└── static/
└── FunnelDisplay-Bold.ttf
```

Place the fontbuilder.py script inside the "fonts" folder:
```
cd /assets/fonts
wget https://github.com/ugurakcil/fontbuilder/main/fontbuilder.py
```

Run the script inside that directory:
`python3 fontbuilder.py`

## WHAT IT DOES

Converts all .ttf files to .woff2 (if not already existing)

Creates one CSS file per font family

Adds font-display: swap for SEO and layout stability

Skips families that already have a CSS file

Uses relative URLs for portability

Console output example:
[ok] `barlow.css` → faces:18 woff2:18
[skip] CSS exists, leaving family untouched: `funnel_display.css`

## EXAMPLE OUTPUT CSS

```
@font-face {
font-family: 'Barlow';
src: url('./Barlow/Barlow-Regular.woff2') format('woff2'),
url('./Barlow/Barlow-Regular.ttf') format('truetype');
font-weight: 400;
font-style: normal;
font-display: swap;
}
```

## NOTES

The script is idempotent: existing CSS or WOFF2 files are never regenerated.

Font weights and italic styles are automatically detected from filenames.

Variable fonts are assigned a weight range of 100–900.

The script assumes that the CSS will be stored at the same directory level as the font folders.

## LICENSE

MIT License – free to use, modify, and distribute.
