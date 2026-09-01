# -*- coding: utf-8 -*-
# transcribe_case.py
# فایل صوتی کیس رو می‌ذاریم توی پوشه cases و این اسکریپت متنش رو می‌سازه
import sys
from pathlib import Path

try:
    import static_ffmpeg
    static_ffmpeg.add_paths()
except Exception:
    pass

import whisper

ROOT = Path(__file__).parent
CASES = ROOT / "cases"
CASES.mkdir(exist_ok=True)

files = sorted(
    list(CASES.glob("*.m4a")) + list(CASES.glob("*.M4A")) +
    list(CASES.glob("*.mp3")) + list(CASES.glob("*.wav"))
)

if not files:
    print("پوشه cases ساخته شد ولی خالیه:")
    print(CASES)
    print("فایل صوتی کیس رو کپی کن توی این پوشه، بعد دوباره اسکریپت رو اجرا کن.")
    input("برای خروج Enter بزن...")
    sys.exit()

print("داره مدل دانلود/بارگذاری می‌شه (فقط بار اول چند دقیقه)...")
model = whisper.load_model("base")

for f in files:
    out = f.with_suffix(".txt")
    if out.exists():
        print("این قبلاً تبدیل شده:", f.name)
        continue
    print("در حال تبدیل:", f.name, "- صبر کن، چند دقیقه...")
    r = model.transcribe(str(f), language="fa")
    out.write_text(r["text"], encoding="utf-8")
    print("متن آماده شد:", out.name)

input("برای خروج Enter بزن...")
