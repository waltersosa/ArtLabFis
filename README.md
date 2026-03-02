# ArtLabFis — Artículo: Retrofitting IoT para Laboratorio Remoto de Cinemática

Repositorio con el código fuente LaTeX del artículo científico en **dos idiomas**:

| Archivo | Idioma | Uso |
|---------|--------|-----|
| `template_ES.tex` | Español 🇪🇸 | Versión para revisión de profesores |
| `template_EN.tex` | Inglés 🇬🇧 | Versión para envío a la revista |

Ambas versiones comparten la misma carpeta `figures/` y bibliografía embebida (sin duplicación).

---

## Requisitos previos

### Distribución LaTeX
Instalar **una** de las siguientes distribuciones:

- **Windows**: [MiKTeX](https://miktex.org/download) o [TeX Live](https://www.tug.org/texlive/)
- **macOS**: [MacTeX](https://www.tug.org/mactex/)
- **Linux**: `sudo apt install texlive-full` (Debian/Ubuntu)

> **Nota:** Se requiere `pdflatex` y los paquetes del template MDPI (incluidos en la carpeta `Definitions/`).

---

## Compilación

### Opción 1: Línea de comandos

```bash
# Compilar versión en español
pdflatex -interaction=nonstopmode template_ES.tex

# Compilar versión en inglés
pdflatex -interaction=nonstopmode template_EN.tex
```

> Ejecutar **dos veces** para resolver referencias cruzadas (`\ref`, `\cite`):
> ```bash
> pdflatex -interaction=nonstopmode template_ES.tex
> pdflatex -interaction=nonstopmode template_ES.tex
> ```

Los PDFs generados serán `template_ES.pdf` y `template_EN.pdf`.

### Opción 2: Editor LaTeX (recomendado)

1. Abrir `template_ES.tex` o `template_EN.tex` en tu editor preferido:
   - [TeXstudio](https://www.texstudio.org/) (recomendado)
   - [Overleaf](https://www.overleaf.com/) (online, subir todo el proyecto como ZIP)
   - VS Code + extensión [LaTeX Workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop)
2. Compilar con **pdfLaTeX** (no XeLaTeX ni LuaLaTeX)
3. El PDF se genera automáticamente

### Opción 3: Compilar ambos PDFs de una vez (Windows PowerShell)

```powershell
pdflatex -interaction=nonstopmode template_ES.tex; pdflatex -interaction=nonstopmode template_ES.tex; pdflatex -interaction=nonstopmode template_EN.tex; pdflatex -interaction=nonstopmode template_EN.tex
```

---

## Estructura del proyecto

```
ArtLabFis/
├── template_ES.tex          # Artículo en español
├── template_EN.tex          # Artículo en inglés
├── template.tex             # Archivo fuente original
├── figures/                 # Figuras compartidas por ambas versiones
│   ├── fig1_arquitectura_labfisica.png
│   ├── bland_altman_english_white.png
│   ├── correlation_sensor_S1.png
│   ├── ...
├── Definitions/             # Clase y estilos MDPI (no modificar)
│   ├── mdpi.cls
│   ├── mdpi.bst
│   └── ...
├── gen_bland_altman.py      # Script Python para generar figura Bland-Altman
└── README.md                # Este archivo
```

---

## Notas importantes

- **Motor de compilación**: Usar `pdflatex`. No usar `xelatex` ni `lualatex`.
- **Bibliografía**: Está embebida en el `.tex` (`thebibliography`), no requiere BibTeX externo.
- **Figuras**: Ambas versiones usan las mismas imágenes de `figures/`. Las figuras están en inglés para evitar duplicación.
- **Clase MDPI**: Los archivos en `Definitions/` son la plantilla oficial de la revista MDPI IoT. No modificarlos.

---

## Autor

**Walter Santiago Sosa Mejía**  
Pontificia Universidad Católica del Ecuador, Sede Esmeraldas  
wssosa@pucese.edu.ec
