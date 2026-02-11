# Compilar `template.tex` a PDF

Este repositorio incluye un script reproducible para generar el PDF del artículo.

## Opción recomendada

```bash
./compile_pdf.sh
```

El script intenta, en este orden:

1. `pdflatex` local
2. `xelatex` local
3. `lualatex` local
4. Docker (`blang/latex:ctanfull`) si no hay compilador local

También puedes pasar otro archivo `.tex`:

```bash
./compile_pdf.sh template.tex
```

## Salida esperada

Si compila correctamente, se genera:

- `template.pdf`

## Errores comunes

- **"no hay compilador LaTeX local ni Docker disponible"**:
  instala TeX Live/MiKTeX localmente o Docker.
- **Errores de LaTeX por figuras/rutas**:
  verifica que los archivos de `figures/` existan y que los nombres coincidan exactamente.
