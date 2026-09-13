import os

pairs = {
    "blog/you-are-not-the-main-actor/addictive-mother-controlling-son.html": "/blog/addictive-mother-controlling-son/",
    "blog/you-are-not-the-main-actor/let-your-child-fail.html": "/blog/let-your-child-fail/",
}

tpl = '''<!DOCTYPE html>
<html lang="fa">
<head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="0; url={url}">
<link rel="canonical" href="https://geshpar.com{url}">
<title>در حال انتقال…</title>
</head>
<body>
<p>این صفحه منتقل شده است: <a href="{url}">مشاهده مقاله</a></p>
</body>
</html>'''

for path, url in pairs.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(tpl.format(url=url))
    print("ساخته شد:", path)