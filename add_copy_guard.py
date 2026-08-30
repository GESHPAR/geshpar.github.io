import os

GUARD = '''
<script>
// Copy guard - geshpar.com
document.addEventListener('contextmenu', function(e){ e.preventDefault(); });
document.addEventListener('copy', function(e){ e.preventDefault(); });
document.addEventListener('cut', function(e){ e.preventDefault(); });
document.addEventListener('keydown', function(e){
  if ((e.ctrlKey || e.metaKey) && ['c','C','x','X','u','U','s','S'].includes(e.key)) { e.preventDefault(); }
});
</script>
'''

n = 0
for d in os.listdir('blog'):
    idx = os.path.join('blog', d, 'index.html')
    if not os.path.isfile(idx):
        continue
    with open(idx, 'r', encoding='utf-8') as f:
        html = f.read()
    if 'Copy guard' in html:
        continue
    html = html.replace('</body>', GUARD + '\n</body>')
    with open(idx, 'w', encoding='utf-8') as f:
        f.write(html)
    n += 1
    print('🔒', d)

print(f'✅ قفل روی {n} مقاله نصب شد')