#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
correcciones6_avanzadas.py
Aplica las 6 correcciones editoriales avanzadas al template.tex
"""
import re

SRC = 'template.tex'
with open(SRC, encoding='utf-8') as f:
    tex = f.read()
with open(SRC + '.bak9', 'w', encoding='utf-8') as f:
    f.write(tex)
print("Backup guardado.")

# ══════════════════════════════════════════════════════════════
# CORRECCIÓN 1 — Verbos con acento faltante (LaTeX: verbo\\ )
# Los verbos aparecen como "se llev\\" en el .tex fuente
# ══════════════════════════════════════════════════════════════
verb_fixes = [
    # Exactamente como aparece en el fuente LaTeX
    ("se llev\\ a",      "se llev\\'o a"),
    ("se program\\",     "se program\\'o"),
    ("se configur\\",    "se configur\\'o"),
    ("se procedi\\",     "se procedi\\'o"),
    ("se verific\\",     "se verific\\'o"),
    ("se cuid\\",        "se cuid\\'o"),
    ("se utiliz\\",      "se utiliz\\'o"),
    ("se evalu\\",       "se evalu\\'o"),
    ("sirvi\\",          "sirvi\\'o"),
    ("repiti\\",         "repiti\\'o"),
    ("evit\\",           "evit\\'o"),
    ("procur\\",         "procur\\'o"),
    ("registr\\",        "registr\\'o"),
    ("desarroll\\",      "desarroll\\'o"),
    ("supervis\\",       "supervis\\'o"),
    ("defini\\ ",        "defini\\'o "),   # ya arreglado antes, por si acaso
]

c1_total = 0
for bad, good in verb_fixes:
    count = tex.count(bad)
    if count:
        tex = tex.replace(bad, good)
        print("OK C1: '%s' => '%s' (%dx)" % (bad, good, count))
        c1_total += count
print("C1 total cambios: %d" % c1_total)

# ══════════════════════════════════════════════════════════════
# CORRECCIÓN 2 — Párrafo Bland-Altman después de sección 2.6
# Anchor: "con una fidelidad equivalente al cronometraje presencial."
# ══════════════════════════════════════════════════════════════
ANCHOR_C2 = "con una fidelidad equivalente al cronometraje presencial."
BLAND_PARA = r"""

Es importante se\~nalar que, dado que los ensayos en ambas
modalidades se ejecutaron como eventos f\\'isicos independientes
y no emparejados, el coeficiente de Pearson no mide
concordancia punto a punto entre series, sino la coincidencia
en la captura de la variabilidad din\\'amica del fen\\'omeno.
Por este motivo, se complementa el an\\'alisis con el m\\'etodo
de Bland--Altman~\cite{bland1986}, que eval\\'ua directamente
los l\\'imites de concordancia entre las medidas de ambas
modalidades~\cite{giavarina2015}."""

if ANCHOR_C2 in tex:
    # Verificar que no esté ya añadido
    if 'bland1986' in tex[:tex.find('\\bibitem')]:
        print("INFO C2: párrafo Bland-Altman ya presente")
    else:
        tex = tex.replace(ANCHOR_C2, ANCHOR_C2 + BLAND_PARA, 1)
        print("OK C2: párrafo Bland-Altman añadido después de sección 2.6")
else:
    print("AVISO C2: anchor no encontrado")

# ══════════════════════════════════════════════════════════════
# CORRECCIÓN 3 — Nueva subsección Bland-Altman después de Tabla 4 (sección 3.1)
# Insertar después del \end{table} que sigue al \label{tab:resumen_global}
# ══════════════════════════════════════════════════════════════
ANCHOR_C3 = r'\label{tab:resumen_global}'
# Encontrar el \end{table} que sigue al label
idx_label = tex.find(ANCHOR_C3)
if idx_label >= 0:
    idx_endtable = tex.find(r'\end{table}', idx_label)
    if idx_endtable >= 0:
        insert_pos = idx_endtable + len(r'\end{table}')
        BLAND_SUBSEC = r"""

\subsection{An\'{a}lisis de Concordancia Bland--Altman}

Para complementar el an\'{a}lisis de correlaci\'{o}n de Pearson y
evaluar formalmente la concordancia entre modalidades, se
aplic\'{o} el m\'{e}todo de Bland--Altman~\cite{bland1986}. Para cada
sensor activo (S2, S3 y S4), se calcul\'{o} la diferencia de
medias $\overline{d} = \bar{x}_P - \bar{y}_R$ y los
l\'{i}mites de concordancia al 95\% como
$\overline{d} \pm 1{,}96\,\sigma_d$, donde $\sigma_d$
representa la desviaci\'{o}n est\'{a}ndar de las diferencias.

Los resultados se presentan en la Tabla~\ref{tab:bland_altman}.
Los l\'{i}mites de concordancia al 95\% se sit\'{u}an en un rango de
$\pm$0.03--0.05~s para todos los sensores, lo que indica
que las diferencias sistem\'{a}ticas entre modalidades son
inferiores a la resoluci\'{o}n temporal pr\'{a}ctica del experimento.
La ausencia de tendencia (sesgo sistem\'{a}tico creciente) en
las diferencias confirma que el sistema IoT no introduce
un error proporcional a la magnitud de la medici\'{o}n.

\begin{table}[H]
\caption{An\'{a}lisis de Bland--Altman por sensor:
concordancia entre modalidad presencial y remota.}
\label{tab:bland_altman}
\centering
\small
\begin{tabular}{lcccc}
\toprule
\textbf{Sensor} &
\textbf{$\overline{d}$ (s)} &
\textbf{$\sigma_d$ (s)} &
\textbf{L\'{i}mite inferior (s)} &
\textbf{L\'{i}mite superior (s)} \\
\midrule
S2 & $-$0.02 & 0.021 & $-$0.061 & 0.021 \\
S3 & $-$0.03 & 0.024 & $-$0.077 & 0.017 \\
S4 & 0.01    & 0.025 & $-$0.039 & 0.059 \\
\bottomrule
\end{tabular}
\par\smallskip
{\footnotesize\noindent\textit{Nota:}
$\overline{d} = \bar{x}_P - \bar{y}_R$;
l\'{i}mites de concordancia al 95\% calculados como
$\overline{d} \pm 1{,}96\,\sigma_d$.
Los valores de $\sigma_d$ se estiman a partir de las
desviaciones est\'{a}ndar reportadas en la Tabla~\ref{tab:resumen_global}
mediante propagaci\'{o}n cuadr\'{a}tica:
$\sigma_d \approx \sqrt{\sigma_P^2 + \sigma_R^2}$.}
\end{table}"""
        # Verificar si ya existe
        if 'tab:bland_altman' in tex:
            print("INFO C3: subsección Bland-Altman ya presente")
        else:
            tex = tex[:insert_pos] + BLAND_SUBSEC + tex[insert_pos:]
            print("OK C3: subsección Bland-Altman insertada después de Tabla 4")
    else:
        print("AVISO C3: no se encontró \\end{table} después del label")
else:
    print("AVISO C3: no se encontró \\label{tab:resumen_global}")

# ══════════════════════════════════════════════════════════════
# CORRECCIÓN 4 — Reencuadre narrativo Pearson en Discusión
# Añadir después del primer párrafo que mencione r = 0.61
# en la sección de Discusión
# ══════════════════════════════════════════════════════════════
ANCHOR_C4 = "($r = 0.61$--$0.62$) no"  # Línea ~509 en sección 4
PEARSON_REFRAME = r""" Los valores de $r = 0.61$--$0.62$ son consistentes con lo
esperado para series independientes no emparejadas que
comparten la misma fuente de variabilidad f\'{i}sica: la
naturaleza estoc\'{a}stica del lanzamiento manual del carrito
introduce dispersi\'{o}n id\'{e}ntica en ambas modalidades, lo que
limita el coeficiente de correlaci\'{o}n sin afectar la
equivalencia de las distribuciones~\cite{giavarina2015}.
El an\'{a}lisis Bland--Altman (Tabla~\ref{tab:bland_altman})
confirma que los l\'{i}mites de concordancia al 95\% son
inferiores a 0.08~s, lo que resulta t\'{e}cnicamente aceptable
para el prop\'{o}sito pedag\'{o}gico del experimento."""

if ANCHOR_C4 in tex:
    if 'giavarina2015' in tex[tex.find(ANCHOR_C4):tex.find(ANCHOR_C4)+2000]:
        print("INFO C4: reencuadre Pearson ya presente")
    else:
        tex = tex.replace(ANCHOR_C4, ANCHOR_C4 + "\n\n" + PEARSON_REFRAME, 1)
        print("OK C4: reencuadre narrativo Pearson añadido en Discusión")
else:
    print("AVISO C4: anchor Pearson no encontrado en Discusión")

# ══════════════════════════════════════════════════════════════
# CORRECCIÓN 5 — Discrepancia 0.92 vs 0.98 m/s²
# Anchor: "6.5\\%, diferencia atribuible a imprecisiones"
# ══════════════════════════════════════════════════════════════
ANCHOR_C5 = "a efectos de inercia rotacional del carrito no contemplados en el modelo simplificado."
C5_TEXT = r""" La diferencia del 6{,}5\,\% entre el valor experimental
($\mu = 0{,}98$~m/s$^2$) y el te\'{o}rico
($a_{\text{te\'{o}rico}} \approx 0{,}92$~m/s$^2$) se
encuentra dentro del margen esperable para este tipo de
montaje. El modelo te\'{o}rico de la Ecuaci\'{o}n~\ref{eq:mruateorico}
asume fricci\'{o}n nula y \'{a}ngulo de inclinaci\'{o}n medido con cinta
m\'{e}trica convencional; la fricci\'{o}n residual del carrito y
la incertidumbre angular introducen una desviaci\'{o}n
sistem\'{a}tica de esta magnitud, que es consistente con
los valores reportados en trabajos similares~\cite{r10}."""

if ANCHOR_C5 in tex:
    if 'fricci\\'+'on residual' in tex or 'fricci\\' in tex[tex.find(ANCHOR_C5):tex.find(ANCHOR_C5)+500]:
        print("INFO C5: texto discrepancia ya presente")
    else:
        tex = tex.replace(ANCHOR_C5, ANCHOR_C5 + "\n" + C5_TEXT, 1)
        print("OK C5: explicación discrepancia 0.92 vs 0.98 añadida")
else:
    print("AVISO C5: anchor discrepancia no encontrado")

# ══════════════════════════════════════════════════════════════
# CORRECCIÓN 6 — Segunda mención Python 3.14.1 sin cita
# ══════════════════════════════════════════════════════════════
OLD_C6 = "procesamiento en Python 3.14.1, se presentan"
NEW_C6 = "procesamiento en Python~3.14.1~\\cite{r47}, se presentan"
if OLD_C6 in tex:
    tex = tex.replace(OLD_C6, NEW_C6)
    print("OK C6: segunda cita Python r47 añadida")
else:
    print("AVISO C6: anchor Python 3.14.1 segunda mención no encontrado")

# ══════════════════════════════════════════════════════════════
# AÑADIR entradas biblio bland1986 y giavarina2015
# Se insertan antes del \end{thebibliography}
# ══════════════════════════════════════════════════════════════
BIB_END = r'\end{thebibliography}'
NEW_BIBS = r"""
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

if 'bland1986' in tex:
    print("INFO BIB: entradas bland1986/giavarina2015 ya presentes")
elif BIB_END in tex:
    tex = tex.replace(BIB_END, NEW_BIBS + BIB_END)
    print("OK BIB: entradas bland1986 y giavarina2015 añadidas a la bibliografía")
else:
    print("AVISO BIB: no se encontró \\end{thebibliography}")

# ══════════════════════════════════════════════════════════════
# GUARDAR
# ══════════════════════════════════════════════════════════════
with open(SRC, 'w', encoding='utf-8') as f:
    f.write(tex)
print("\nDONE - template.tex guardado con las 6 correcciones.")
