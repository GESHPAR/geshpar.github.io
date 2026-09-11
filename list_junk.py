import pathlib

junk = []
for f in pathlib.Path(".").glob("**/*"):
    if f.is_dir() or ".git" in str(f):
        continue
    name = f.name
    if " " in name or name.startswith("e -ne") or name.startswith("t-Path"):
        junk.append(str(f))
    if name in ("itemap.xml inventory.json", "t-Path sitemap.xml"):
        junk.append(str(f))

print("Junk files found:")
for j in sorted(set(junk)):
    print(f"  {j}")
print(f"TOTAL: {len(set(junk))}")