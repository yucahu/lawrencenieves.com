# lawrencenieves.com

Plain HTML and CSS. Nothing to install and no framework.

## What's here

| File | What it is |
|---|---|
| `index.html` | Home page: the intro, résumé and portfolio links, and contact links. Edit by hand. |
| `hobbies.html` | Hobbies page: one `<section class="hobby">` per hobby, images in `images/personal/`. Edit by hand. |
| `404.html` | Page shown for a broken address. Edit by hand. |
| `projects.json` | Every project: title, year, client, role, description, links, images and tags. |
| `build.py` | Turns `projects.json` into the project pages. |
| `projects.html`, `projects/`, `tags/` | Pages made by `build.py`. Don't edit these by hand, because the next build replaces them. |
| `style.css` | All styles, using the Kudzu colours and type. |
| `site.js` | Optional extras: the hover preview, ← → keys between projects, and keeping the current project in view in the list. |
| `images/` | Project images. `-01` is each project's cover. |
| `images/portrait.svg` | The line drawing on the home page. To change its colour, edit `fill="#e0b652"` near the start of the file. |
| `og-image.png` | The card shown when someone shares a link to the site on LinkedIn, Slack or in a text. Project pages use their cover image instead. |
| `lawrence-nieves-resume.pdf`, `lawrence-nieves-portfolio.pdf` | The PDFs linked from the home page and the top of every page. To update one, replace the file and keep the name. |

## Changing projects

1. Edit `projects.json`. Projects appear in the order they're listed, newest first.
2. Run `python build.py` in this folder.
3. Open `index.html` in a browser to check.

To add a tag, type it in a project's `tags` list. A new tag gets its own page automatically. `tag_order` at the top of the file sets the order tags are listed in.

To show a YouTube video in place of an image, use an entry like `{"youtube": "VIDEO_ID", "caption": "Project video", "aspect": "16/9"}` (`"9/16"` for Shorts). If a project's first item is a video, set `thumb` to an image for the hover preview. To put a video directly under a project's description instead, add the same kind of entry as that project's `video` field.

To add images to a project, put the file in `images/` and add an entry to that project's `images` list with its `file`, `caption`, `width` and `height`.

## Publishing

Upload the whole folder to any static host, such as GitHub Pages, Netlify, Cloudflare Pages or Neocities. Every link is relative, so the site also works when you open the files straight from your computer.
