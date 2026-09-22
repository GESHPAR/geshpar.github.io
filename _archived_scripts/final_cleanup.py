import os, shutil

def size(p):
    ip = os.path.join(p, 'index.html')
    return os.path.getsize(ip) if os.path.exists(ip) else 0

for name in os.listdir('blog'):
    path = os.path.join('blog', name)
    if os.path.isdir(path) and name.endswith('.html'):
        proper = os.path.join('blog', name[:-5])
        if os.path.exists(proper):
            # اگه نسخه آشغال محتوای غنی‌تری داره، اول منتقلش کن
            if size(path) > size(proper):
                shutil.copy2(os.path.join(path, 'index.html'),
                             os.path.join(proper, 'index.html'))
                print(f'📦 محتوای غنی‌تر منتقل شد: {name}')
            shutil.rmtree(path)
            print(f'🗑️ حذف تکراری: {name}')
        else:
            os.rename(path, proper)
            print(f'✏️ تغییر نام: {name} ➜ {name[:-5]}')

print('✅ تمیزکاری نهایی تمام شد')