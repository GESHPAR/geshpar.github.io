# sync.ps1
$env:GIT_EDITOR = "true"
$b = (git branch --show-current).Trim()
Write-Host "branch: $b"

git add .
git commit -m "sync all"

git fetch origin
git rebase "origin/$b"
if ($LASTEXITCODE -ne 0) { git add . ; git rebase --continue }

git push origin $b
Write-Host "done"
