#!/usr/bin/env python3
"""Builds the project pages from projects.json.

    python build.py

Writes projects.html, projects/<slug>.html and tags/<tag>.html.
index.html (home), hobbies.html and 404.html are written by hand and are not touched.
Needs nothing but Python 3.
"""
import json
import re
import shutil
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EMAIL = "lawrenceenieves@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/lawrencenieves/"
NAME = "Lawrence Nieves"
SITE = "https://lawrencenieves.com/"  # used for link previews on LinkedIn, Slack, etc.

data = json.loads((ROOT / "projects.json").read_text(encoding="utf-8"))
projects = data["projects"]
tag_order = data.get("tag_order", [])


def e(s):
    return escape(str(s), quote=True)


def tag_slug(tag):
    s = tag.lower().replace("°", "")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


# Every tag in use, in the preferred order, then any new ones alphabetically.
used = []
for p in projects:
    for t in p["tags"]:
        if t not in used:
            used.append(t)
tags = [t for t in tag_order if t in used] + sorted(t for t in used if t not in tag_order)
tag_counts = {t: sum(t in p["tags"] for p in projects) for t in tags}


def head(prefix, title, description, body_class="", share_image="og-image.png"):
    return f"""<!doctype html>
<html lang="en" class="work">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<meta name="theme-color" content="#ffffff">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:image" content="{SITE}{e(share_image)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{prefix}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&amp;family=Schibsted+Grotesk:wght@400;500;700;800&amp;display=swap">
<link rel="stylesheet" href="{prefix}style.css">
<script src="{prefix}site.js" defer></script>
</head>
<body{f' class="{body_class}"' if body_class else ''}>
<a class="skip" href="#main">Skip to content</a>
<header class="bar"><a class="home-link" href="{prefix}index.html">&larr; Home</a></header>
<nav class="top" aria-label="More">
  <a href="{prefix}hobbies.html">Hobbies</a>
  <a href="{prefix}lawrence-nieves-resume.pdf">R&eacute;sum&eacute;</a>
  <a href="{prefix}lawrence-nieves-portfolio.pdf">Portfolio</a>
  <a href="mailto:{EMAIL}">Email</a>
  <a href="{LINKEDIN}">LinkedIn</a>
</nav>
"""


FOOT = "</body>\n</html>\n"


def meta_line(p):
    return f"{p['year']} · {p['client']} · {p['type']}"


def index_nav(prefix, current_slug=None, current_tag=None, preview=False):
    items = []
    for p in projects:
        attrs = ""
        if current_slug == p["slug"]:
            attrs += ' aria-current="page"'
        if preview:
            attrs += f' data-meta="{e(meta_line(p))}" data-role="{e(p["role"])}"'
            c = cover_image(p)
            if c:
                attrs += (f' data-img="{e(prefix + c["file"])}" data-w="{c["width"]}"'
                          f' data-h="{c["height"]}" data-cap="{e(c["caption"])}"')
        items.append(
            f'    <li><a href="{prefix}projects/{p["slug"]}.html"{attrs}>'
            f'<span class="t">{e(p["title"])}</span><span class="y">{e(p["year"])}</span></a></li>'
        )
    tag_items = []
    for t in tags:
        cur = ' aria-current="page"' if t == current_tag else ""
        tag_items.append(
            f'      <li><a href="{prefix}tags/{tag_slug(t)}.html"{cur}>{e(t)}</a><sup>{tag_counts[t]}</sup></li>'
        )
    return f"""<nav class="index" aria-label="Projects">
  <h2 class="label mobile-only" style="margin:0">All projects</h2>
  <ol class="index-list">
{chr(10).join(items)}
  </ol>
  <div class="tag-cloud">
    <h2 class="label" id="tags-label" style="margin:0">Tags</h2>
    <ul aria-labelledby="tags-label">
{chr(10).join(tag_items)}
    </ul>
  </div>
</nav>
"""


def cover_image(p):
    """The still used for the hover preview: 'thumb' if set, else the first image file."""
    if p.get("thumb"):
        return p["thumb"]
    return next((im for im in p["images"] if "file" in im), None)


def figure(prefix, img, eager=False):
    if "youtube" in img:
        vid = e(img["youtube"])
        tall = " tall" if img.get("aspect") == "9/16" else ""
        return (f'<figure class="video{tall}"><div class="embed" style="aspect-ratio: {e(img.get("aspect", "16/9"))}">'
                f'<iframe src="https://www.youtube-nocookie.com/embed/{vid}" title="{e(img["caption"])}" loading="lazy"'
                f' allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"'
                f' referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div>'
                f'<figcaption>{e(img["caption"])}</figcaption></figure>')
    loading = "" if eager else ' loading="lazy"'
    return (f'<figure><a href="{prefix}{e(img["file"])}">'
            f'<img src="{prefix}{e(img["file"])}" width="{img["width"]}" height="{img["height"]}"'
            f' alt="{e(img["caption"])}"{loading} decoding="async"></a>'
            f'<figcaption>{e(img["caption"])}</figcaption></figure>')


def project_page(i, p):
    pre = "../"
    n = len(projects)
    prev_p = projects[(i - 1) % n]
    next_p = projects[(i + 1) % n]
    imgs = p["images"]
    cover = figure(pre, imgs[0], eager=True) if imgs else ""
    gallery = ""
    if len(imgs) > 1:
        gallery = '<div class="gallery">' + "".join(figure(pre, im) for im in imgs[1:]) + "</div>"
    links = ""
    if p["links"]:
        links = '<ul class="links">' + "".join(
            f'<li><a href="{e(l["url"])}">{e(l["label"])} &#8599;</a></li>' for l in p["links"]) + "</ul>"
    facts = [("Client", p["client"]), ("With", p["with"]), ("Type", p["type"]), ("Notes", p["context"])]
    facts_html = "".join(f"<div><dt>{k}</dt><dd>{e(v)}</dd></div>" for k, v in facts if v)
    tag_links = "".join(f'<li><a href="{pre}tags/{tag_slug(t)}.html">{e(t)}</a></li>' for t in p["tags"])
    desc = p["description"].split(". ")[0].rstrip(".") + "."
    still = cover_image(p)
    share = still["file"] if still else "og-image.png"
    return (head(pre, f"{p['title']} · {NAME}", desc, share_image=share)
            + index_nav(pre, current_slug=p["slug"])
            + f"""<main id="main">
<article class="col">
  <header class="head">
    <p class="eyebrow">{e(p['year'])} · {e(p['client'])}</p>
    <h1 class="page-title">{e(p['title'])}</h1>
    <p class="role">{e(p['role'])}</p>
  </header>
  {cover}
  <p class="lead">{e(p['description'])}</p>
  {figure(pre, p["video"]) if p.get("video") else ""}
  {links}
  <dl class="facts">{facts_html}</dl>
  <div class="tags"><span class="label">Tags</span><ul>{tag_links}</ul></div>
  {gallery}
  <nav class="pager" aria-label="More projects">
    <a href="{prev_p['slug']}.html" rel="prev"><span class="meta">&larr; Previous</span><span class="t">{e(prev_p['title'])}</span></a>
    <a class="next" href="{next_p['slug']}.html" rel="next"><span class="meta">Next &rarr;</span><span class="t">{e(next_p['title'])}</span></a>
  </nav>
</article>
</main>
""" + FOOT)


def tag_page(t):
    pre = "../"
    matching = [p for p in projects if t in p["tags"]]
    count = len(matching)
    rows = "".join(
        f'<li><a href="{pre}projects/{p["slug"]}.html"><span class="t">{e(p["title"])}</span>'
        f'<span class="y">{e(p["year"])}</span><span class="meta">{e(p["client"])} · {e(p["type"])}</span></a></li>'
        for p in matching)
    return (head(pre, f"{t} · {NAME}", f"{count} projects tagged {t}.")
            + index_nav(pre, current_tag=t)
            + f"""<main id="main">
<div class="col">
  <header class="head">
    <p class="eyebrow">Tag</p>
    <h1 class="page-title">{e(t)}</h1>
    <p class="meta">{count} project{'s' if count != 1 else ''}</p>
  </header>
  <ol class="rows">{rows}</ol>
</div>
</main>
""" + FOOT)


def projects_page():
    years = [int(y) for p in projects for y in re.findall(r"\d{4}", p["year"])]
    span = f"{min(years)}–{max(years)}" if years else ""
    return (head("", f"Projects · {NAME}", f"{len(projects)} projects by {NAME}, {span}.", "listing")
            + index_nav("", preview=True)
            + f"""<main id="main">
<div class="col">
  <header class="head">
    <h1 class="page-title">Projects</h1>
    <p class="hint">{len(projects)} projects, {span}. Point at a title to preview it; click to open it.</p>
  </header>
  <div class="preview" aria-hidden="true">
    <figure hidden><a href="#" tabindex="-1"><img src="data:," alt=""></a><figcaption></figcaption></figure>
    <div class="preview-text" hidden>
      <p class="name"></p>
      <p class="meta"></p>
      <p class="role"></p>
    </div>
  </div>
</div>
</main>
""" + FOOT)


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


# Clear old generated pages so renamed projects or tags don't linger.
for folder in ("projects", "tags"):
    shutil.rmtree(ROOT / folder, ignore_errors=True)

write(ROOT / "projects.html", projects_page())
for i, p in enumerate(projects):
    write(ROOT / "projects" / f"{p['slug']}.html", project_page(i, p))
for t in tags:
    write(ROOT / "tags" / f"{tag_slug(t)}.html", tag_page(t))

print(f"Built projects.html, {len(projects)} project pages and {len(tags)} tag pages.")
