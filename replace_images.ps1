$htmlFiles = Get-ChildItem -Path "c:\suman pvt" -Filter "*.html"
$images = @(1..11 | ForEach-Object { "img/36046_page-{0:D4}.jpg" -f $_ })
$imgIdx = 0

foreach ($file in $htmlFiles) {
    $lines = Get-Content $file.FullName
    $newLines = @()
    foreach ($line in $lines) {
        if ($line -match "https://images.unsplash.com/") {
            if ($line -match 'class="hero-bg"' -or $line -match 'class="hero-image-bg"') {
                $newLines += $line
            } else {
                $img = $images[$imgIdx % $images.Length]
                $imgIdx++
                $newLine = $line -replace 'src="https://images\.unsplash\.com/[^"]+"', "src=`"$img`""
                $newLine = $newLine -replace '\s*style="filter:\s*hue-rotate[^"]+"', ""
                $newLines += $newLine
            }
        } else {
            $newLines += $line
        }
    }
    # Save the file with UTF-8 encoding
    $newLines | Set-Content $file.FullName -Encoding UTF8
}
Write-Host "Replacement done!"
