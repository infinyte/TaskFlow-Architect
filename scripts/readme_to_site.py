#!/usr/bin/env python3
"""
readme_to_site.py
Generate a static site from README.md, create assets and a GitHub Actions workflow,
and package site/ + workflow into taskflow_site_package.zip.
"""
import sys, os, io, zipfile, shutil, textwrap
from pathlib import Path

ROOT = Path.cwd()
README = ROOT / "README.md"
OUT_DIR = ROOT / "site"
IMG_DIR = OUT_DIR / "images"
CSS_DIR = OUT_DIR / "css"
WORKFLOW_DIR = ROOT / ".github" / "workflows"
ZIP_PATH = ROOT / "taskflow_site_package.zip"

def e(msg): print(msg, file=sys.stderr)

def read_readme():
    if not README.exists():
        e("ERROR: README.md not found in repository root.")
        sys.exit(2)
    return README.read_text(encoding="utf-8")

def extract_header_and_intro(md):
    lines = md.splitlines()
    title = None
    intro = None
    i = 0
    while i < len(lines):
        l = lines[i].strip()
        if l.startswith("# "):
            title = l[2:].strip()
            # find next non-empty paragraph
            j = i+1
            while j < len(lines) and lines[j].strip()=="":
                j += 1
            if j < len(lines):
                # collect paragraph lines
                para = []
                while j < len(lines) and lines[j].strip() != "":
                    para.append(lines[j].strip())
                    j += 1
                intro = " ".join(para)
            break
        i += 1
    if not title:
        title = ROOT.name
    if not intro:
        intro = ""
    return title, intro

def md_to_html(md):
    try:
        import markdown
        return markdown.markdown(md, extensions=["fenced_code","tables","codehilite"])
    except Exception:
        # Minimal converter: headings, fenced code, inline code, lists, paragraphs, tables
        out = []
        lines = md.splitlines()
        in_code = False
        code_buf = []
        for ln in lines:
            if ln.strip().startswith("```"):
                if not in_code:
                    in_code = True
                    code_buf = []
                else:
                    in_code = False
                    out.append("<pre><code>{}</code></pre>".format(
                        html_escape("\n".join(code_buf))))
                continue
            if in_code:
                code_buf.append(ln)
                continue
            if ln.startswith("#"):
                level = len(ln) - len(ln.lstrip("#"))
                out.append(f"<h{level}>{html_escape(ln.lstrip('#').strip())}</h{level}>")
            elif ln.strip().startswith("- ") or ln.strip().startswith("* "):
                # simple list handling
                if not out or not out[-1].startswith("<ul>"):
                    out.append("<ul>")
                out.append(f"<li>{html_escape(ln.strip()[2:])}</li>")
                # close lists later (simple)
            elif "|" in ln and ln.strip().startswith("|"):
                out.append(html_escape(ln))
            elif ln.strip()=="":
                out.append("<p></p>")
            else:
                out.append(f"<p>{html_escape(ln)}</p>")
        # close any open ul
        html = "\n".join(out).replace("<ul>\n<li>", "<ul>\n<li>").replace("</li>\n</ul>", "</li>\n</ul>")
        return html

def html_escape(s):
    return (s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
            .replace('"',"&quot;"))

def ensure_dirs():
    for d in (OUT_DIR, IMG_DIR, CSS_DIR, WORKFLOW_DIR):
        d.mkdir(parents=True, exist_ok=True)

def write_css():
    css = """/* styles.css - clean responsive layout */
:root{--accent:#2b7cff;--bg:#f7f9fc;--card:#ffffff;--text:#0f1724}
*{box-sizing:border-box}body{font-family:Inter,system-ui,Arial,sans-serif;margin:0;background:var(--bg);color:var(--text)}
.container{max-width:980px;margin:0 auto;padding:20px}
.header{background:var(--card);padding:28px;border-bottom:1px solid #e6eef8;display:flex;align-items:center;gap:16px}
.logo{height:56px;width:auto}
h1{margin:0;font-size:1.6rem}
.tag{color:#475569}
nav{margin-left:auto}
nav a{margin-left:12px;color:var(--accent);text-decoration:none}
main{padding:20px}
section{background:var(--card);padding:18px;margin:18px 0;border-radius:8px;box-shadow:0 1px 2px rgba(15,23,36,0.04)}
pre{background:#0b1220;color:#dbeafe;padding:12px;border-radius:6px;overflow:auto}
table{width:100%;border-collapse:collapse}
table th,table td{padding:8px;border-bottom:1px solid #eef2f7;text-align:left}
footer{color:#64748b;text-align:center;padding:12px 0;font-size:0.9rem}
@media(max-width:640px){.header{flex-direction:column;align-items:flex-start}nav{margin-left:0}}
"""
    (CSS_DIR / "styles.css").write_text(css, encoding="utf-8")

def write_workflow():
    wf = textwrap.dedent("""\
    name: Deploy GitHub Pages

    on:
      push:
        branches:
          - main

    jobs:
      build-and-deploy:
        runs-on: ubuntu-latest
        steps:
          - name: Checkout
            uses: actions/checkout@v4
            with:
              persist-credentials: false

          - name: Setup Node
            uses: actions/setup-node@v4
            with:
              node-version: '18'

          - name: Deploy to GitHub Pages
            uses: peaceiris/actions-gh-pages@v3
            with:
              github_token: ${{ secrets.GITHUB_TOKEN }}
              publish_dir: ./site
              publish_branch: gh-pages
    """)
    (WORKFLOW_DIR / "deploy-pages.yml").write_text(wf, encoding="utf-8")

def make_logo():
    try:
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new("RGBA",(512,128),(255,255,255,0))
        draw = ImageDraw.Draw(img)
        # simple rectangle and text
        draw.rectangle([0,0,512,128], fill=(43,124,255))
        try:
            f = ImageFont.truetype("DejaVuSans-Bold.ttf", 48)
        except Exception:
            f = None
        text = "TaskFlow"
        w,h = draw.textsize(text, font=f)
        draw.text(((512-w)/2,(128-h)/2), text, fill="white", font=f)
        outp = IMG_DIR / "logo.png"
        img.save(outp)
        return "images/logo.png"
    except Exception:
        # fallback to SVG
        svg = '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="128"><rect width="100%" height="100%" fill="#2b7cff"/><text x="50%" y="55%" font-family="Arial,Helvetica,sans-serif" font-size="48" fill="#fff" text-anchor="middle">TaskFlow</text></svg>'
        (IMG_DIR / "logo.svg").write_text(svg, encoding="utf-8")
        return "images/logo.svg"

def write_index(title, intro, body_html, logo_path, license_text):
    nav = '<nav><a href="#overview">Overview</a><a href="#features">Features</a><a href="#architecture">Architecture</a><a href="#usage">Usage</a><a href="#api">API</a><a href="#roadmap">Roadmap</a><a href="#contributing">Contributing</a><a href="#license">License</a></nav>'
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><title>{html_escape(title)}</title><link rel="stylesheet" href="css/styles.css"/></head>
<body>
<header class="header container"><img src="{logo_path}" alt="logo" class="logo"/><div><h1>{html_escape(title)}</h1><div class="tag">{html_escape(intro)}</div></div>{nav}</header>
<main class="container">{body_html}
<section id="license"><h2>License</h2><p>{html_escape(license_text)}</p></section>
<footer class="container"><p>Generated site for {html_escape(title)}</p></footer>
</main></body></html>"""
    (OUT_DIR / "index.html").write_text(html, encoding="utf-8")

def find_license(md):
    if "\n## License" in md or "\n# License" in md:
        # simple extract
        parts = md.splitlines()
        try:
            idx = next(i for i,l in enumerate(parts) if l.strip().lower().startswith("## license") or l.strip().lower().startswith("# license"))
            # collect next paragraph
            j = idx+1
            para=[]
            while j < len(parts) and parts[j].strip()=="":
                j+=1
            while j < len(parts) and parts[j].strip()!="":
                para.append(parts[j].strip()); j+=1
            return " ".join(para) if para else "MIT License"
        except StopIteration:
            return "MIT License"
    return "MIT License"

def make_zip():
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as z:
        # add site/
        for p in OUT_DIR.rglob("*"):
            z.write(p, p.relative_to(ROOT))
        # add workflow
        wf = WORKFLOW_DIR / "deploy-pages.yml"
        if wf.exists():
            z.write(wf, wf.relative_to(ROOT))
    print(f"Created zip: {ZIP_PATH}")

def main():
    print("Starting README -> site generation...")
    md = read_readme()
    title,intro = extract_header_and_intro(md)
    print(f"Project title: {title}")
    ensure_dirs()
    print("Converting markdown to HTML...")
    body_html = md_to_html(md)
    print("Writing CSS...")
    write_css()
    print("Creating logo...")
    logo_rel = make_logo()
    print("Writing workflow...")
    write_workflow()
    license_text = find_license(md)
    print("Writing index.html...")
    write_index(title,intro,body_html,logo_rel,license_text)
    print("Packaging into zip...")
    make_zip()
    print("Done. Zip file created at:", ZIP_PATH)
    sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        e(f"ERROR: {exc}")
        sys.exit(3)