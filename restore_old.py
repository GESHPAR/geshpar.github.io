import subprocess, os

def runb(*cmd):
    return subprocess.run(cmd, capture_output=True).stdout

log = runb('git', 'log', '--format=%H %s').decode('utf-8', errors='replace')
target = None
for line in log.splitlines():
    if 'حذف پوسته' in line:
        target = line.split()[0]
        break

if not target:
    print('❌ کامیت پاک‌سازی پیدا نشد')
    raise SystemExit

parent = target + '~1'
names = runb('git', 'diff', '--name-only', '--diff-filter=D', parent, target).decode('utf-8')

n = 0
for rel in names.splitlines():
    rel = rel.strip()
    if not rel.startswith('blog/') or not rel.endswith('.html'):
        continue
    slug = rel[len('blog/'):-len('.html')]
    if slug in ('index', 'template'):
        continue

    old = runb('git', 'show', parent + ':' + rel).decode('utf-8', errors='replace')
    if len(old.strip()) < 200:
        print('⚠️ محتوای کافی نیست:', slug)
        continue

    d = os.path.join('blog', slug)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(old)

    redir = ('<!DOCTYPE html>\n<html lang="fa"><head><meta charset="UTF-8">\n'
             '<meta http-equiv="refresh" content="0; url=/blog/' + slug + '/">\n'
             '<link rel="canonical" href="https://geshpar.com/blog/' + slug + '/">\n'
             '<title>در حال انتقال…</title></head>\n<body><p>این مقاله منتقل شده است. '
             '<a href="/blog/' + slug + '/">مشاهده مقاله</a></p></body></html>')
    with open(os.path.join('blog', slug + '.html'), 'w', encoding='utf-8') as f:
        f.write(redir)

    n += 1
    print('♻️', slug)

print(f'✅ {n} مقاله با آدرس تمیز بازگشت + تغییرمسیر ساخته شد')