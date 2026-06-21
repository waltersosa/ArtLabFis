$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
    xelatex -interaction=nonstopmode -halt-on-error articulo_espol.tex
    if ($LASTEXITCODE -ne 0) { throw 'Fallo la primera pasada de XeLaTeX.' }
    biber articulo_espol
    if ($LASTEXITCODE -ne 0) { throw 'Fallo Biber.' }
    xelatex -interaction=nonstopmode -halt-on-error articulo_espol.tex
    if ($LASTEXITCODE -ne 0) { throw 'Fallo la segunda pasada de XeLaTeX.' }
    xelatex -interaction=nonstopmode -halt-on-error articulo_espol.tex
    if ($LASTEXITCODE -ne 0) { throw 'Fallo la pasada final de XeLaTeX.' }
}
finally {
    Pop-Location
}
