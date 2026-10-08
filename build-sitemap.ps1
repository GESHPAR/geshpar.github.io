param(
    [string]$BaseUrl = "https://geshpar.github.io",
    [string]$SiteName = "«› Œ«—« ",
    [string]$SitemapPath = "sitemap.xml",
    [string]$IndexPath = "index.html"
)

$ErrorActionPreference = "Stop"

$root = Get-Location
$blogRoot = Join-Path $root "blog"

if (-not (Test-Path $blogRoot)) {
    throw "ÅÊ‘Â blog ÅÌœ« ‰‘œ. «Ì‰ «”ò—ÌÅ  —« «“ —Ì‘Â —ÌÅÊ «Ã—« ò‰."
}

$Base = $BaseUrl.TrimEnd("/")
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function ConvertTo-HtmlSafe {
    param([string]$Text)
    if ([string]::IsNullOrWhiteSpace($Text)) { return "" }
    $Text = $Text -replace '&', '&amp;'
    $Text = $Text -replace '<', '&lt;'
    $Text = $Text -replace '>', '&gt;'
    $Text = $Text -replace '"', '&quot;'
    return $Text
}

function ConvertTo-XmlSafe {
    param([string]$Text)
    if ([string]::IsNullOrWhiteSpace($Text)) { return "" }
    $Text = $Text -replace '&', '&amp;'
    $Text = $Text -replace '<', '&lt;'
    $Text = $Text -replace '>', '&gt;'
    $Text = $Text -replace '"', '&quot;'
    $Text = $Text -replace "'", '&apos;'
    return $Text
}

function Get-PageTitle {
    param([string]$Html)
    if ($Html -match '(?is)<title[^>]*>(.*?)</title>') {
        return $matches[1].Trim()
    }
    return ""
}

function Get-PageDescription {
    param([string]$Html)

    if ($Html -match '(?is)<meta[^>]+name=["'']description["''][^>]+content=["''](.*?)["'']') {
        return $matches[1].Trim()
    }

    if ($Html -match '(?is)<meta[^>]+content=["''](.*?)["''][^>]+name=["'']description["'']') {
        return $matches[1].Trim()
    }

    return ""
}

$posts = @()

Get-ChildItem -Path $blogRoot -Directory | ForEach-Object {
    $dir = $_
    $indexFile = Join-Path $dir.FullName "index.html"

    if (Test-Path $indexFile) {
        $html = Get-Content -Raw -Encoding UTF8 $indexFile

        $title = Get-PageTitle $html
        $description = Get-PageDescription $html

        if ([string]::IsNullOrWhiteSpace($title)) {
            $title = $dir.Name
        }

        if ([string]::IsNullOrWhiteSpace($description)) {
            $description = "„ﬁ«·Âù«Ì «“ »·«ê $SiteName"
        }

        $slug = $dir.Name
        $url = "$Base/blog/$slug/"
        $lastMod = (Get-Item $indexFile).LastWriteTime.ToUniversalTime().ToString("yyyy-MM-dd")

        $posts += [pscustomobject]@{
            Slug        = $slug
            Title       = $title
            Description = $description
            Url         = $url
            RelativeUrl = "/blog/$slug/"
            LastMod     = $lastMod
        }
    }
}

$posts = $posts | Sort-Object LastMod -Descending

if ($posts.Count -eq 0) {
    throw "ÂÌç „ﬁ«·Âù«Ì œ— blog/*/index.html ÅÌœ« ‰‘œ."
}

# -----------------------
# Build sitemap.xml
# -----------------------

$sb = New-Object System.Text.StringBuilder
[void]$sb.AppendLine('<?xml version="1.0" encoding="UTF-8"?>')
[void]$sb.AppendLine('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

$today = (Get-Date).ToUniversalTime().ToString("yyyy-MM-dd")

[void]$sb.AppendLine("  <url>")
[void]$sb.AppendLine("    <loc>$(ConvertTo-XmlSafe "$Base/")</loc>")
[void]$sb.AppendLine("    <lastmod>$today</lastmod>")
[void]$sb.AppendLine("    <changefreq>daily</changefreq>")
[void]$sb.AppendLine("    <priority>1.0</priority>")
[void]$sb.AppendLine("  </url>")

foreach ($post in $posts) {
    [void]$sb.AppendLine("  <url>")
    [void]$sb.AppendLine("    <loc>$(ConvertTo-XmlSafe $post.Url)</loc>")
    [void]$sb.AppendLine("    <lastmod>$($post.LastMod)</lastmod>")
    [void]$sb.AppendLine("    <changefreq>monthly</changefreq>")
    [void]$sb.AppendLine("    <priority>0.8</priority>")
    [void]$sb.AppendLine("  </url>")
}

[void]$sb.AppendLine('</urlset>')

$sitemapFullPath = Join-Path $root $SitemapPath
[System.IO.File]::WriteAllText($sitemapFullPath, $sb.ToString(), $utf8NoBom)

# -----------------------
# Build index.html
# -----------------------

$cards = foreach ($post in $posts) {
@"
        <article class="post-card">
          <h2><a href="$($post.RelativeUrl)">$(ConvertTo-HtmlSafe $post.Title)</a></h2>
          <p>$(ConvertTo-HtmlSafe $post.Description)</p>
          <div class="card-meta">
            <time datetime="$($post.LastMod)">$($post.LastMod)</time>
            <span>|</span>
            <a href="$($post.RelativeUrl)">„‘«ÂœÂ „ﬁ«·Â</a>
          </div>
        </article>
"@
}

$cardsHtml = $cards -join "`r`n"

$indexHtml = @"
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>$SiteName | »·«ê —Ê«‰ù‘‰«”Ì° —Ê«»ÿ Ê ”·«„  —Ê«‰</title>
    <meta name="description" content="„Ã„Ê⁄Â „ﬁ«·«   Õ·Ì·Ì —Ê«‰ù‘‰«”Ì° —Ê«»ÿ Œ«‰Ê«œêÌ° ”·«„  —Ê«‰° «“œÊ«Ã° ÿ·«ﬁ° «›”—œêÌ Ê ŒÊœ‘‰«”Ì.">
    <meta name="author" content="$SiteName">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="$Base/">
    <link rel="sitemap" type="application/xml" href="$Base/sitemap.xml">

    <meta property="og:type" content="website">
    <meta property="og:locale" content="fa_IR">
    <meta property="og:url" content="$Base/">
    <meta property="og:title" content="$SiteName | »·«ê —Ê«‰ù‘‰«”Ì° —Ê«»ÿ Ê ”·«„  —Ê«‰">
    <meta property="og:description" content="„Ã„Ê⁄Â „ﬁ«·«   Õ·Ì·Ì —Ê«‰ù‘‰«”Ì° —Ê«»ÿ Œ«‰Ê«œêÌ° ”·«„  —Ê«‰° «“œÊ«Ã° ÿ·«ﬁ° «›”—œêÌ Ê ŒÊœ‘‰«”Ì.">
    <meta property="og:site_name" content="$SiteName">

    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="$SiteName | »·«ê —Ê«‰ù‘‰«”Ì° —Ê«»ÿ Ê ”·«„  —Ê«‰">
    <meta name="twitter:description" content="„Ã„Ê⁄Â „ﬁ«·«   Õ·Ì·Ì —Ê«‰ù‘‰«”Ì° —Ê«»ÿ Œ«‰Ê«œêÌ° ”·«„  —Ê«‰° «“œÊ«Ã° ÿ·«ﬁ° «›”—œêÌ Ê ŒÊœ‘‰«”Ì.">

    <style>
        :root {
            --bg: #ffffff;
            --surface: #f8fafc;
            --text: #111827;
            --muted: #4b5563;
            --border: #e5e7eb;
            --primary: #0f766e;
            --primary-dark: #115e59;
            --danger: #b91c1c;
        }

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Vazirmatn, IRANSans, Tahoma, Arial, sans-serif;
            line-height: 1.9;
            color: var(--text);
            background: var(--bg);
        }

        a {
            color: var(--primary-dark);
            text-decoration: none;
        }

        a:hover,
        a:focus {
            text-decoration: underline;
        }

        .container {
            width: min(1080px, calc(100% - 32px));
            margin: 0 auto;
            padding: 32px 0 64px;
        }

        header.site-header {
            border-bottom: 1px solid var(--border);
            padding-bottom: 24px;
            margin-bottom: 32px;
        }

        h1 {
            margin: 0 0 12px;
            font-size: clamp(1.8rem, 4vw, 2.6rem);
            line-height: 1.35;
        }

        .lead {
            margin: 0;
            color: var(--muted);
            font-size: 1.05rem;
        }

        .toolbar {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-top: 18px;
            color: var(--muted);
            font-size: 0.95rem;
        }

        .posts {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 18px;
        }

        .post-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 20px;
            transition: transform 0.18s ease, box-shadow 0.18s ease;
        }

        .post-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
        }

        .post-card h2 {
            margin: 0 0 10px;
            font-size: 1.18rem;
            line-height: 1.6;
        }

        .post-card p {
            margin: 0 0 14px;
            color: var(--muted);
            font-size: 0.98rem;
        }

        .card-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            align-items: center;
            color: var(--muted);
            font-size: 0.9rem;
        }

        footer {
            margin-top: 48px;
            padding-top: 24px;
            border-top: 1px solid var(--border);
            color: var(--muted);
            font-size: 0.95rem;
        }

        .footer-links {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-top: 10px;
        }

        .notice {
            background: #ecfdf5;
            border: 1px solid #a7f3d0;
            border-right: 5px solid var(--primary);
            border-radius: 14px;
            padding: 16px 18px;
            margin: 24px 0 32px;
            color: #064e3b;
        }
    </style>
</head>
<body>
    <div class="container">
        <header class="site-header">
            <h1>$SiteName</h1>
            <p class="lead">
                »·«ê  Õ·Ì·Ì —Ê«‰ù‘‰«”Ì° —Ê«»ÿ° Œ«‰Ê«œÂ° ”·«„  —Ê«‰ Ê „”Ì—Â«Ì »«“ê‘  »Â “‰œêÌ „ ⁄«œ·ù —.
            </p>
            <div class="toolbar">
                <span> ⁄œ«œ „ﬁ«·« : $($posts.Count)</span>
                <span>|</span>
                <a href="$Base/sitemap.xml">‰ﬁ‘Â ”«Ì </a>
                <span>|</span>
                <a href="$Base/blog/">»«Ìê«‰Ì »·«ê</a>
            </div>
        </header>

        <div class="notice">
            <strong>Ì«œ¬Ê—Ì:</strong>
            «Ì‰ ”«Ì  Ã‰»Â ¬„Ê“‘Ì Ê ¬ê«ÂÌù»Œ‘Ì œ«—œ. œ— »Õ—«‰ùÂ«Ì ›Ê—Ì »« «Ê—é«‰” ???° «Ê—é«‰” «Ã „«⁄Ì ??? Ì« ’œ«Ì „‘«Ê—Â ????  „«” »êÌ—Ìœ.
        </div>

        <main>
            <section class="posts" aria-label="›Â—”  „ﬁ«·« ">
$cardsHtml
            </section>
        </main>

        <footer>
            <p>&copy; $(Get-Date -Format yyyy) $SiteName.  „«„Ì ÕﬁÊﬁ „Õ›ÊŸ «” .</p>
            <div class="footer-links">
                <a href="$Base/">Œ«‰Â</a>
                <a href="$Base/blog/">»·«ê</a>
                <a href="$Base/sitemap.xml">Sitemap</a>
                <a href="$Base/about/">œ—»«—Â „«</a>
                <a href="$Base/contact/"> „«” »« „«</a>
            </div>
        </footer>
    </div>
</body>
</html>
"@

$indexFullPath = Join-Path $root $IndexPath
[System.IO.File]::WriteAllText($indexFullPath, $indexHtml, $utf8NoBom)

Write-Host "Done." -ForegroundColor Green
Write-Host "Posts found: $($posts.Count)" -ForegroundColor Cyan
Write-Host "Sitemap: $sitemapFullPath" -ForegroundColor Cyan
Write-Host "Index: $indexFullPath" -ForegroundColor Cyan
