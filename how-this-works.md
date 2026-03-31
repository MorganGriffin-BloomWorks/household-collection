# Household Collection — How This Works

This project creates a small website where each item in the house has its own page. A QR code sticker on the object links directly to that page. Anyone who scans it gets a description, photo, provenance, and any notes — no app required, just a phone camera.

---

## The pieces

| Piece | What it does |
|---|---|
| **Airtable** | Where you write and manage item descriptions |
| **generate.py** | Script that pulls from Airtable and builds the HTML pages and QR code images |
| **GitHub / GitHub Pages** | Hosts the pages at permanent URLs |
| **qr-codes/ folder** | PNG images of each item's QR code, ready to print |

---

## Adding or updating an item

1. Open the **Household collection** base in Airtable
2. Add a new record or edit an existing one
3. Make sure **Item ID** is filled in — this is the URL slug (e.g. `grandmas-rocking-chair`). Set it once and never change it, or the QR code sticker dies.
4. In Terminal, run:

```bash
cd "/Users/morgangriffin/Library/CloudStorage/GoogleDrive-morgan@bloomworks.digital/My Drive/Claude projects/Household QR codes"
source venv/bin/activate
python3 generate.py
git add docs/ qr-codes/
git commit -m "Update items"
git push
```

The page is live within a few seconds of the push.

---

## Airtable fields

| Field | Notes |
|---|---|
| **Title** | Name of the item |
| **Category** | Art, Furniture, Heirloom, Book, Decorative, Textile, Other |
| **Description** | Main story — supports basic markdown (bold, italics, paragraphs) |
| **Provenance** | Where it came from, who owned it before |
| **Date / Era** | Flexible text: "circa 1940s", "purchased 2003", etc. |
| **Notes** | Anything else — supports basic markdown |
| **Item ID** | URL slug. Set once, never change. |
| **Photo** | Attach images directly in Airtable. First image appears on the page. |
| **Property** | Which location: 64 Reservoir Drive, Writers' Mill, Anne's apartment, Other |
| **Room / Spot** | Where within that property |

---

## Printing QR codes

Each item gets a QR code PNG in the `qr-codes/` folder, named by Item ID (e.g. `bishop-brassrubbing.png`). Print these however works for the object:

- Label printer for small stickers
- Regular paper + clear packing tape for a quick and durable label
- Avoid pre-printed QR stickers from Amazon — those encode a fixed URL at the factory and break if you ever move the site

---

## The live site

Pages are at:
`https://morgangriffin-bloomworks.github.io/household-collection/[item-id].html`

The site has no index page and a `robots.txt` that blocks search engines. Pages are technically public but not findable unless someone has the exact URL.

---

## If you want more privacy later

Switch to Netlify (free tier):

1. Create a Netlify account, connect it to the same GitHub repo
2. Set publish directory to `docs`
3. Enable password protection under Site settings → Access control
4. Update `SITE_URL` in `generate.py` to the new Netlify URL
5. Run `generate.py` again to rebuild QR codes with new URLs
6. Reprint and replace QR code stickers (one-time cost)

---

## Migrating away from work accounts

Do this before printing and placing QR stickers, so you only print once.

**GitHub:**
1. Create a personal GitHub account
2. Create a new repo called `household-collection`
3. Update `SITE_URL` in `generate.py` to `https://[your-personal-username].github.io/household-collection`
4. Run `python3 generate.py` to rebuild everything with new URLs
5. Push to the new repo and enable GitHub Pages (Settings → Pages → Branch: main, Folder: /docs)

**Airtable:**
1. In the Household collection base: Grid view → Download CSV
2. Log into your personal Airtable account, create a new base, import the CSV
3. Update `BASE_ID` and `TABLE_ID` in `generate.py` with the new base's IDs
4. Create a new personal access token scoped to the new base, update `.env`

---

## Files in this folder

```
generate.py          — the script that builds everything
requirements.txt     — Python dependencies
.gitignore           — keeps .env and venv out of GitHub
.env                 — your Airtable token (never commit this)
docs/                — generated HTML pages (committed to GitHub)
qr-codes/            — generated QR code PNGs (committed to GitHub)
venv/                — Python virtual environment (local only)
```

---

## If something breaks

**403 error from Airtable:** Token permissions changed. Go to Airtable → Developer hub → your token, confirm it has `data.records:read` scope and access to the Household collection base.

**Page not found after pushing:** GitHub Pages can take a minute or two. Also confirm Settings → Pages is set to Branch: main, Folder: /docs.

**QR code scans but page is blank or wrong:** Check that the Item ID in Airtable matches the filename in `docs/`. They're the same thing.

**`python3: command not found`:** You're in a new Terminal window. Run `source venv/bin/activate` first.
