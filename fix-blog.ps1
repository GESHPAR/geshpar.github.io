$basePath = "c:\Users\NP\Documents\GitHub\geshpar.github.io\Blog"

Write-Host "=== شروع تعمیرات ===" -ForegroundColor Green

Remove-Item -Path "$basePath\son-military-evasion-responsibility" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "$basePath\daughter-hostility-parental-guilt" -Force -ErrorAction SilentlyContinue

New-Item -ItemType Directory -Path "$basePath\son-military-evasion-responsibility" -Force | Out-Null
New-Item -ItemType Directory -Path "$basePath\daughter-hostility-parental-guilt" -Force | Out-Null

Write-Host "=== کارها انجام شد! ===" -ForegroundColor Green