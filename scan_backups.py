import os

missing = [l.strip() for l in open('missing_list.txt', encoding='utf-8') if l.strip()]
print('--- ۶ گمشده ---')
for s in missing: print('❌', s)

print('\n--- جستجو در همه بکاپ‌ها ---')
found_any = False
for bk in sorted(os.listdir('backup_cleanup')):
    blogdir = os.path.join('backup_cleanup', bk, 'blog')
    if not os.path.isdir(blogdir): continue
    names = set(os.listdir(blogdir))
    hits = [s for s in missing if s in names or s + '.html' in names]
    if hits:
        found_any = True
        print(f'📦 {bk}:')
        for h in hits: print('   ✅', h)

if not found_any:
    print('(در هیچ بکاپی پیدا نشد — می‌ریم سراغ git history)')