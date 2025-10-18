#!/usr/bin/env python3
# compact font pipeline: scan subfolders, make .woff2, emit per-family CSS (skip if CSS already exists)

import os, re, subprocess, sys
ROOT = os.getcwd()

# --- tiny helpers ---
def css_name(folder):  # keep underscores, lowercase
    return f"{folder.lower()}.css"

def family_name(folder):  # underscores -> spaces
    return folder.replace("_"," ")

def rel(p):  # path relative to fonts root for CSS urls
    return "./" + os.path.relpath(p, ROOT).replace("\\","/")

def has_tool(cmd="woff2_compress"):
    try: subprocess.run([cmd,"-h"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError: return False
    return True

# map filename tokens to weights
WMAP = [("Thin",100),("ExtraLight",200),("UltraLight",200),("Light",300),
        ("Regular",400),("Book",400),("Roman",400),("Medium",500),
        ("SemiBold",600),("DemiBold",600),("Bold",700),
        ("ExtraBold",800),("UltraBold",800),("Black",900),("Heavy",900)]

def parse_weight_style(fn):
    n = os.path.basename(fn)
    style = "italic" if re.search(r"italic", n, re.I) else "normal"
    for k,w in WMAP:
        if re.search(k, n, re.I): return w, style
    return 400, style

def is_variable(fn): return bool(re.search(r"variable", os.path.basename(fn), re.I))

def ensure_woff2(ttf):
    w2 = os.path.splitext(ttf)[0] + ".woff2"
    if os.path.exists(w2): return w2
    # run external tool
    r = subprocess.run(["woff2_compress", ttf], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if r.returncode != 0: print(f"[warn] woff2_compress failed: {ttf}\n{r.stderr.decode('utf-8')}", file=sys.stderr)
    return w2 if os.path.exists(w2) else None

# --- sanity check ---
if not has_tool(): 
    sys.exit("woff2_compress not found. Install it and rerun.")

families = [d for d in sorted(os.listdir(ROOT)) if os.path.isdir(d) and not d.startswith(".")]
if not families: sys.exit("No subfolders found. Run this in your fonts directory.")

for folder in families:
    fam = family_name(folder)
    out_css = os.path.join(ROOT, css_name(folder))
    if os.path.exists(out_css):  # per user: do nothing if css exists
        print(f"[skip] CSS exists, leaving family untouched: {os.path.basename(out_css)}")
        continue

    # collect all .ttf in folder (including static/)
    ttfs = []
    for base,_,files in os.walk(os.path.join(ROOT, folder)):
        for f in files:
            if f.lower().endswith(".ttf"): ttfs.append(os.path.join(base,f))
    if not ttfs:
        print(f"[info] No TTF in {folder}, skipping."); continue

    # convert to woff2 (only for this family we're emitting)
    converted = 0
    records_var, records_static = [], []
    for ttf in sorted(ttfs):
        w2 = ensure_woff2(ttf)
        if w2: converted += 1 if os.path.getmtime(w2) >= os.path.getmtime(ttf) else 0
        italic = "italic" if re.search(r"italic", os.path.basename(ttf), re.I) else "normal"
        if is_variable(ttf):
            records_var.append({"w2": w2, "ttf": ttf, "style": italic})
        else:
            w, st = parse_weight_style(ttf)
            records_static.append({"w": w, "style": st, "w2": w2, "ttf": ttf})

    # build CSS text
    lines = []
    # variable faces first (normal & italic separate if present)
    for st in ("normal","italic"):
        for r in [x for x in records_var if x["style"]==st]:
            if not r["w2"]: continue
            lines += [
                "@font-face{",
                f"font-family:'{fam}';",
                f"src:url('{rel(r['w2'])}') format('woff2'),url('{rel(r['ttf'])}') format('truetype');",
                "font-weight:100 900;",
                f"font-style:{st};",
                "font-display:swap;",
                "}"
            ]
    # static faces (per file)
    # sort for deterministic output
    for r in sorted(records_static, key=lambda x:(x["w"], x["style"])):
        if not r["w2"]: continue
        lines += [
            "@font-face{",
            f"font-family:'{fam}';",
            f"src:url('{rel(r['w2'])}') format('woff2'),url('{rel(r['ttf'])}') format('truetype');",
            f"font-weight:{r['w']};",
            f"font-style:{r['style']};",
            "font-display:swap;",
            "}"
        ]

    if not lines: 
        print(f"[warn] No CSS entries for {folder} (missing woff2?). Skipping.")
        continue

    with open(out_css, "w", encoding="utf-8") as f: f.write("\n".join(lines)+"\n")
    print(f"[ok] {os.path.basename(out_css)} → faces:{(len(records_var)>0)+(len(records_static))} woff2:{converted}")
