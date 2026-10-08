param(
  [Parameter(Mandatory=$true)][string]$Slug
)

$url = "https://geshpar.com/blog/$Slug/"
$path = "sitemap.xml"

if (-not (Test-Path $path)) {
  Write-Error "sitemap.xml not found"
  exit 1
}

$xml = Get-Content -Raw -Encoding UTF8 $path

if ($xml -like "*$url*") {
  Write-Host "Already in sitemap: $url"
  exit 0
}

$date = Get-Date -Format yyyy-MM-dd
$entry = "  <url>`n    <loc>$url</loc>`n    <lastmod>$date</lastmod>`n  </url>`n"

$xml = $xml -replace '</urlset>', ($entry + '</urlset>')

Set-Content -Path $path -Value $xml -Encoding UTF8

Write-Host "Added: $url"
