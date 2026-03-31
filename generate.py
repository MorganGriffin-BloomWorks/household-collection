import os
import requests
import markdown
import qrcode
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

AIRTABLE_TOKEN = os.environ.get("AIRTABLE_TOKEN")
BASE_ID = "appgOH3zKtzx3Q7gZ"
TABLE_ID = "tblb6dc8HS25MmYdU"
SITE_URL = "https://morgangriffin-bloomworks.github.io/household-collection"
OUTPUT_DIR = Path("docs")
QR_DIR = Path("qr-codes")


def fetch_items():
    headers = {"Authorization": f"Bearer {AIRTABLE_TOKEN}"}
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}"
    items = []
    params = {}
    while True:
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()
        items.extend(data["records"])
        if "offset" not in data:
            break
        params["offset"] = data["offset"]
    return items


def md_to_html(text):
    if not text:
        return ""
    return markdown.markdown(text)


def render_page(fields):
    title = fields.get("Title", "Untitled")
    category = fields.get("Category", "")
    description = md_to_html(fields.get("Description", ""))
    provenance = fields.get("Provenance", "")
    date_era = fields.get("Date / Era", "")
    notes = md_to_html(fields.get("Notes", ""))
    property_name = fields.get("Property", "")
    room = fields.get("Room / Spot", "")

    photos = fields.get("Photo", [])
    photo_html = ""
    if photos:
        photo_url = photos[0].get("url", "")
        if photo_url:
            photo_html = f'<img src="{photo_url}" alt="{title}">\n'

    meta_parts = [p for p in [category, date_era] if p]
    meta_html = f'<p class="meta">{" · ".join(meta_parts)}</p>\n' if meta_parts else ""

    location_parts = [p for p in [property_name, room] if p]
    location_html = f'<p class="location">{" · ".join(location_parts)}</p>\n' if location_parts else ""

    body_sections = ""
    if description:
        body_sections += f'<section class="description">{description}</section>\n'
    if provenance:
        body_sections += f'<section class="provenance"><h2>Provenance</h2><p>{provenance}</p></section>\n'
    if notes:
        body_sections += f'<section class="notes"><h2>Notes</h2>{notes}</section>\n'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow">
  <title>{title}</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: Georgia, 'Times New Roman', serif;
      background: #fafaf8;
      color: #1a1a1a;
      max-width: 660px;
      margin: 0 auto;
      padding: 2rem 1.25rem 5rem;
    }}
    img {{
      width: 100%;
      height: auto;
      display: block;
      border-radius: 3px;
      margin-bottom: 1.75rem;
    }}
    h1 {{
      font-size: 1.65rem;
      font-weight: normal;
      line-height: 1.25;
      margin-bottom: 0.4rem;
    }}
    h2 {{
      font-size: 0.72rem;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: #999;
      margin-bottom: 0.6rem;
      margin-top: 2.5rem;
    }}
    .meta, .location {{
      font-size: 0.85rem;
      color: #999;
      margin-bottom: 0.25rem;
    }}
    .meta {{ margin-bottom: 1.75rem; }}
    section {{ margin-top: 0.25rem; }}
    section p, section li {{
      font-size: 1rem;
      line-height: 1.75;
      color: #333;
    }}
    section p + p {{ margin-top: 0.75rem; }}
    .description p, .description li {{
      color: #1a1a1a;
      font-size: 1.05rem;
    }}
  </style>
</head>
<body>
{photo_html}<h1>{title}</h1>
{meta_html}{location_html}
{body_sections}
</body>
</html>"""


def generate_qr(item_id, url):
    QR_DIR.mkdir(exist_ok=True)
    img = qrcode.make(url)
    img.save(QR_DIR / f"{item_id}.png")


def main():
    if not AIRTABLE_TOKEN:
        raise SystemExit("Error: AIRTABLE_TOKEN not set. Add it to your .env file.")

    OUTPUT_DIR.mkdir(exist_ok=True)
    (OUTPUT_DIR / "robots.txt").write_text("User-agent: *\nDisallow: /\n")

    items = fetch_items()
    generated = []

    for record in items:
        fields = record.get("fields", {})
        item_id = fields.get("Item ID", "").strip()
        if not item_id:
            title = fields.get("Title", record["id"])
            print(f"  Skipping '{title}' — no Item ID set")
            continue

        html = render_page(fields)
        page_url = f"{SITE_URL}/{item_id}.html"
        (OUTPUT_DIR / f"{item_id}.html").write_text(html, encoding="utf-8")
        generate_qr(item_id, page_url)
        generated.append((fields.get("Title", item_id), page_url))
        print(f"  Generated: {fields.get('Title', item_id)}")

    print(f"\n{len(generated)} page(s) in docs/")
    print(f"{len(generated)} QR code(s) in qr-codes/\n")
    for title, url in generated:
        print(f"  {title}\n    {url}\n")


if __name__ == "__main__":
    main()
