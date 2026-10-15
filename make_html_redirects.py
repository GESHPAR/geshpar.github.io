import pathlib

BLOG = pathlib.Path("blog")
SITE = "https://geshpar.com"
SLUGS = [
    "displaced-jealousy-family-conflict",
    "ethics-of-truth-telling",
    "attachment-trauma-abandonment-case",
    "diagnosing-pathological-lying",
    "husband-sulking",
    "right-choice",
    "self-sacrifice-trap",
]

for slug in SLUGS:
    folder_page = BLOG / slug / "index.html"
    html_page = BLOG / f"{slug}.html"

    if not folder_page.exists():
        print(f"SKIP    {slug}: folder version missing")
        continue
    if html_page.exists():
        print(f"SKIP    {slug}: .html already exists")
        continue

    url = f"{SITE}/blog/{slug}/"
    html = f"""<!DOCTYPE html>
<html lang="fa">
<head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="0; url={url}">
<link rel="canonical" href="{url}">
<title>Moved</title>
<script>location.replace("{url}");</script>
</head>
<body><a href="{url}">{url}</a></body>
</html>
"""
    html_page.write_text(html, encoding="utf-8")
    print(f"CREATED {html_page}")
