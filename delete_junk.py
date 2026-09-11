import pathlib, shutil, re

removed, skipped = 0, []
junk = []
for f in sorted(pathlib.Path(".").glob("**/*")):
    if ".git" in f.parts:
        continue
    n = f.name
    if (" - Copy" in n) or n.startswith("e -ne") or n.startswith("t-Path") \
       or n == "itemap.xml inventory.json":
        junk.append(f)

for f in junk:
    if " - Copy" in f.name:
        orig = f.parent / re.sub(r" - Copy( \(\d+\))?$", "", f.name)
        if not orig.exists():
            skipped.append(str(f)); continue
    if f.is_dir():
        shutil.rmtree(f, ignore_errors=True)
    else:
        f.unlink(missing_ok=True)
    print("removed:", f); removed += 1

print("TOTAL removed:", removed)
print("SKIPPED (no original):", skipped)