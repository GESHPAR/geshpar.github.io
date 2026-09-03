git config user.email "np@geshpar.local"
git config user.name "GESHPAR"
git rebase --abort
git merge --abort
git add .
git commit -m "sync local work"
git fetch origin
git merge -X ours origin/main --no-edit
git push origin HEAD:main