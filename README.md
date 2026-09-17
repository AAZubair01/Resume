# Abdulrazaq A. Zubair — Resume / Academic Homepage

Source of the personal resume site published with GitHub Pages at
**https://aazubair01.github.io/Resume/**.

The site is plain HTML/CSS/JS — no build step, no frameworks. All dynamic
content (publications, awards & activities) lives in two data files, so
updating the site never requires touching HTML.

```
├── index.html                  # the single page
├── css/style.css               # all styling
├── js/main.js                  # renders data files + scroll behavior
├── data/
│   ├── publications.js         # ← EDIT THIS to add a publication
│   └── activities.js           # ← EDIT THIS to add an award/activity
├── assets/
│   ├── headshot.png            # profile photo
│   └── Abdulrazaq-Zubair-CV.docx
├── scripts/fetch_scholar.py    # Google Scholar sync
└── .github/workflows/update-publications.yml
```

## 1. Deploy / redeploy to GitHub Pages

1. Push (or drag-and-drop upload) all files to the `main` branch of
   `AAZubair01/Resume`.
2. In the repo: **Settings → Pages → Source: "Deploy from a branch" →
   Branch: `main`, folder: `/ (root)` → Save**.
3. The site goes live at `https://aazubair01.github.io/Resume/` within a
   minute or two. Every later push updates it automatically.

## 2. Add a new publication (manual — 30 seconds)

Open `data/publications.js` and add one entry anywhere in the array
(the page sorts by year automatically):

```js
{
  "title": "Full title of the paper",
  "year": 2026,                       // or null if not yet assigned
  "venue": "Journal or conference",   // or "" if unknown
  "url": "https://doi.org/10.xxxx/...",
  "source": "manual"
}
```

Commit and push — the site updates itself. The same pattern applies to
`data/activities.js` for awards and activities.

## 3. Automated Google Scholar sync (optional)

A GitHub Action (`.github/workflows/update-publications.yml`) runs **every
Monday** and can also be triggered manually from the repo's **Actions** tab.
It fetches your Scholar profile (author ID `JNqveLcAAAAJ`) and merges new
papers into `data/publications.js`:

- Entries you added by hand (`"source": "manual"`) are never modified.
- Scholar papers are deduplicated by title; new ones are appended with
  `"source": "scholar"`.

> **Honest caveat:** Google Scholar has no official API and frequently
> captchas automated requests from cloud servers. If a run is blocked, the
> workflow simply makes no changes — the site keeps working with the current
> data. Manual editing (section 2) always works. You can also run the sync
> from your own computer, where Scholar is far less likely to block you:
>
> ```bash
> pip install scholarly
> python3 scripts/fetch_scholar.py
> git add data/publications.js && git commit -m "sync publications" && git push
> ```

To use a different Scholar profile, change `SCHOLAR_AUTHOR_ID` at the top of
`scripts/fetch_scholar.py`.

## 4. Update the CV download or photo

Replace `assets/Abdulrazaq-Zubair-CV.docx` or `assets/headshot.png` with a
new file of the **same name**, commit, and push.
