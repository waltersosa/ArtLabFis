#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
correcciones5_cierre.py - Aplica las 5 correcciones finales de cierre.
"""

with open('template.tex', encoding='utf-8') as f:
    tex = f.read()
with open('template.tex.bak10', 'w', encoding='utf-8') as f:
    f.write(tex)
print("Backup guardado.")

orig = tex

# ══════════════════════════════════════════════════════════════
# C1: Añadir entradas bibliográficas bland1986 y giavarina2015
# La bibliografía es un thebibliography embebido.
# Insertar ANTES de \end{thebibliography}
# ══════════════════════════════════════════════════════════════
BIB_END = r'\end{thebibliography}'

BLAND_BIB = r"""
\bibitem{bland1986}
Bland, J.M.; Altman, D.G.
Statistical methods for assessing agreement between two methods of clinical measurement.
\textit{The Lancet} \textbf{1986}, \textit{327}(8476), 307--310.
\href{https://doi.org/10.1016/S0140-6736(86)90837-8}{doi:10.1016/S0140-6736(86)90837-8}

\bibitem{giavarina2015}
Giavarina, D.
Understanding Bland Altman analysis.
\textit{Biochemia Medica} \textbf{2015}, \textit{25}(2), 141--151.
\href{https://doi.org/10.11613/BM.2015.015}{doi:10.11613/BM.2015.015}

"""

# Verificar si ya existen las entradas
if r'\bibitem{bland1986}' in tex:
    print("INFO C1: bland1986 ya presente en biblio")
else:
    if BIB_END in tex:
        tex = tex.replace(BIB_END, BLAND_BIB + BIB_END)
        print("OK C1: entradas bland1986 y giavarina2015 añadidas")
    else:
        print("AVISO C1: no se encontró \\end{thebibliography}")

# ══════════════════════════════════════════════════════════════
# C2: Reconstruir párrafo fragmentado en Sección 4.2 (líneas 571-583)
# Reemplazar el bloque roto por el párrafo coherente
# ══════════════════════════════════════════════════════════════
# El bloque fragmentado empieza con "Es importante destacar..."
# y termina con "...ver Tabla~\ref{tab:resumen_global})."

OLD_FRAG_START = "Es importante destacar que los coeficientes de correlaci\\'on de Pearson obtenidos ($r = 0.61$--$0.62$) no"
OLD_FRAG_END = "sin introducir sesgo sistem\\'atico (ver Tabla~\\ref{tab:resumen_global})."

idx_start = tex.find(OLD_FRAG_START)
idx_end = tex.find(OLD_FRAG_END)
if idx_start >= 0 and idx_end >= 0:
    idx_end += len(OLD_FRAG_END)
    old_block = tex[idx_start:idx_end]
    NEW_PARA = ("Es importante destacar que los coeficientes de correlaci\\'on de Pearson obtenidos"
                " ($r = 0.61$--$0.62$) no deben interpretarse como una limitaci\\'on del sistema IoT."
                " Los valores de $r = 0.61$--$0.62$ son consistentes con lo esperado para series"
                " independientes no emparejadas que comparten la misma fuente de variabilidad f\\'isica:"
                " la naturaleza estoc\\'astica del lanzamiento manual del carrito introduce dispersi\\'on"
                " id\\'entica en ambas modalidades, lo que limita el coeficiente de correlaci\\'on sin"
                " afectar la equivalencia de las distribuciones~\\cite{giavarina2015}."
                " El an\\'alisis Bland--Altman (Tabla~\\ref{tab:bland_altman}) confirma que los l\\'imites"
                " de concordancia al 95\\% son inferiores a 0.08~s, lo que resulta t\\'ecnicamente aceptable"
                " para el prop\\'osito pedag\\'ogico del experimento.")
    tex = tex[:idx_start] + NEW_PARA + tex[idx_end:]
    print("OK C2: párrafo fragmentado reconstruido")
else:
    print("AVISO C2: no se encontró el bloque fragmentado (start=%d, end=%d)" % (idx_start, idx_end))

# ══════════════════════════════════════════════════════════════
# C3: Typos de doble terminación verbal configuró'o y registró'o
# ══════════════════════════════════════════════════════════════
typos = [
    ("configur\\'o\\'o",   "configur\\'o"),
    ("registr\\'o\\'o",    "registr\\'o"),
    # variantes unicode
    ("configur\u00f3\\'o", "configur\u00f3"),
    ("registr\u00f3\\'o",  "registr\u00f3"),
    ("configur\u00f3'o",   "configur\u00f3"),
    ("registr\u00f3'o",    "registr\u00f3"),
]
for bad, good in typos:
    count = tex.count(bad)
    if count:
        tex = tex.replace(bad, good)
        print("OK C3: '%s' corregido (%dx)" % (bad, count))

# ══════════════════════════════════════════════════════════════
# C4: "se realiz " sin acento → "se realizó "
# ══════════════════════════════════════════════════════════════
C4_OLD = "Finalmente, se realiz la validaci\\'on t\\'ecnica"
C4_NEW = "Finalmente, se realiz\\'o la validaci\\'on t\\'ecnica"
if C4_OLD in tex:
    tex = tex.replace(C4_OLD, C4_NEW)
    print("OK C4: 'se realiz' → 'se realizó' corregido")
else:
    # Buscar variante
    import re
    pat4 = re.compile(r'se realiz ([a-z])')
    m = pat4.search(tex)
    if m:
        print("AVISO C4: encontrado 'se realiz %s' — aplicar manualmente" % m.group(1))
    else:
        print("INFO C4: no se encontró 'se realiz' sin acento")

# ══════════════════════════════════════════════════════════════
# C5: "basada enretrofittinge IoT" → "basada en \textit{retrofitting} e IoT"
# ══════════════════════════════════════════════════════════════
C5_OLD = "basada enretrofittinge IoT"
C5_NEW = "basada en \\textit{retrofitting} e IoT"
count5 = tex.count(C5_OLD)
if count5:
    tex = tex.replace(C5_OLD, C5_NEW)
    print("OK C5: 'enretrofittinge' corregido (%dx)" % count5)
else:
    print("INFO C5: 'enretrofittinge' no encontrado")

# ══════════════════════════════════════════════════════════════
# GUARDAR
# ══════════════════════════════════════════════════════════════
with open('template.tex', 'w', encoding='utf-8') as f:
    f.write(tex)
print("\nDONE - template.tex guardado.")
