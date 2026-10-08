param(
  [Parameter(Mandatory=$true)][string]$Path,
  [string]$Slug
)

if (-not (Test-Path $Path)) {
  Write-Error "File not found: $Path"
  exit 1
}

$html = Get-Content -Raw -Encoding UTF8 $Path

$required = @(
  '<html lang="fa" dir="rtl">',
  '<meta charset="utf-8">',
  '<meta name="viewport"',
  '<title>',
  '<meta name="description"',
  '<link rel="canonical"',
  '<meta property="og:type"',
  '<meta property="og:locale"',
  '<meta property="og:site_name"',
  '<meta property="og:title"',
  '<meta property="og:description"',
  '<meta property="og:url"',
  '<meta name="twitter:card"',
  '<script type="application/ld+json"',
  '<article',
  '</article>',
  '<h1',
  'مفید مقصودی',
  'data-consent="verified-anonymized"',
  'datePublished'
)

foreach ($r in $required) {
  if ($html -notlike "*$r*") {
    Write-Error "Missing required string: $r"
    exit 1
  }
}

foreach ($bad in @('TODO', 'FIXME', 'placeholder', '{{')) {
  if ($html -like "*$bad*") {
    Write-Error "Temporary marker found: $bad"
    exit 1
  }
}

$h1Matches = [regex]::Matches($html, '(?is)<h1[^>]*>')
if ($h1Matches.Count -ne 1) {
  Write-Error "Exactly one H1 required. Found: $($h1Matches.Count)"
  exit 1
}

$bodyMatch = [regex]::Match($html, '(?is)<body>(.*?)</body>')
if (-not $bodyMatch.Success) {
  Write-Error "No body element found"
  exit 1
}

$body = $bodyMatch.Groups[1].Value
$body = [regex]::Replace($body, '(?is)<script.*?</script>', ' ')
$body = [regex]::Replace($body, '(?is)<style.*?</style>', ' ')
$text = [regex]::Replace($body, '<[^>]+>', ' ')
$text = [System.Net.WebUtility]::HtmlDecode($text)
$text = $text -replace '\s+', ' '
$text = $text.Trim()

$len = $text.Length
if ($len -lt 1500) {
  Write-Error "Visible text too short: $len (minimum 1500)"
  exit 1
}

if ($Slug) {
  $expected = "https://geshpar.com/blog/$Slug/"
  $canonical = [regex]::Match($html, '(?is)<link rel="canonical" href="(.*?)">').Groups[1].Value

  if ($canonical -ne $expected) {
    Write-Error "Canonical mismatch: $canonical != $expected"
    exit 1
  }

  if (Test-Path 'sitemap.xml') {
    $sitemap = Get-Content -Raw -Encoding UTF8 'sitemap.xml'
    if ($sitemap -notlike "*$expected*") {
      Write-Error "URL missing from sitemap.xml: $expected"
      exit 1
    }
  }
}

$internalLinks = ([regex]::Matches($html, '(?is)<a\s+href="(/|https://geshpar\.com/)')).Count
if ($internalLinks -lt 3) {
  Write-Error "Need at least 3 internal links. Found: $internalLinks"
  exit 1
}

Write-Host "PASS: $len visible chars, internal links $internalLinks"
