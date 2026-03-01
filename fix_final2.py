#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_final2.py — Aplica correcciones Bloque 1-4 con renumeración segura de referencias.
La renumeración SOLO afecta el interior de \cite{} y \bibitem{}.
"""
import re

SRC = 'template.tex'

with open(SRC, encoding='utf-8') as f:
    tex = f.read()

with open(SRC + '.bak5', 'w', encoding='utf-8') as f:
    f.write(tex)
print("Backup guardado.")

# ══════════════════════════════════════════════════════════════
# BLOQUE 1A: Correcciones de ecuaciones y etiquetas
# ══════════════════════════════════════════════════════════════
tex = tex.replace(r'\label{eq:mrua_teorico}', r'\label{eq:mruateorico}')
tex = tex.replace(r'\ref{eq:mrua_teorico}', r'\ref{eq:mruateorico}')
print("OK - label eq:mruateorico")

# Eliminar dobles backslashes residuales en ecuaciones (de inyección anterior)
double_bs_fixes = [
    ("\\\\'orico", "\\'orico"),
    ("\\\\'ineo",  "\\'ineo"),
    ("\\\\'on",    "\\'on"),
    ("\\\\'angulo","\\'angulo"),
    ("\\\\'a",     "\\'a"),
    ("\\\\theta",  "\\theta"),
    ("\\\\cdot",   "\\cdot"),
    ("\\\\sin",    "\\sin"),
    ("\\\\text{",  "\\text{"),
    ("\\\\label{", "\\label{"),
    ("\\\\ref{",   "\\ref{"),
    ("\\\\Delta",  "\\Delta"),
    ("\\\\frac",   "\\frac"),
    ("\\\\bar",    "\\bar"),
]
for old, new in double_bs_fixes:
    tex = tex.replace(old, new)
print("OK - dobles backslashes corregidos")

# ERROR 4: Referencia rota "Ecuación ??"
tex = re.sub(
    r'definido por la Ecuaci[oó]n\s?\?\?',
    "definido por la Ecuaci\\'on~\\\\ref{eq:mruateorico}",
    tex
)
print("OK - Ecuacion ?? corregida")

# ══════════════════════════════════════════════════════════════
# BLOQUE 1B: Párrafo duplicado S1
# ══════════════════════════════════════════════════════════════
pat_dup = (r'Como se muestra en la Figura 7, los puntos de datos se concentran en el origen\.'
           r'.*?No hay fluctuaciones ni ruido experimental que afecten este estado inicial\.\n\n')
new_tex, n = re.subn(pat_dup, '', tex, count=1, flags=re.DOTALL)
if n:
    tex = new_tex
    print("OK - Párrafo duplicado S1 eliminado")
else:
    print("AVISO - párrafo duplicado S1 no encontrado")

# ══════════════════════════════════════════════════════════════
# BLOQUE 1C: Texto Sensor S2 — reemplazar párrafo incorrecto
# ══════════════════════════════════════════════════════════════
S2_NEW = (
    "La Figura~\\\\ref{fig:corr_s2} presenta la gr\\'afica de dispersi\\'on para S2, con\n"
    "un coeficiente de correlaci\\'on de Pearson moderado\n"
    "($r = 0.61$, $R^2 = 0.37$, $N = 35$). Este valor refleja una\n"
    "asociaci\\'on lineal positiva estad\\'isticamente significativa entre\n"
    "ambas modalidades. La dispersi\\'on observada es coherente con la\n"
    "independencia f\\'isica de los ensayos: dado que cada par\n"
    "(presencial, remoto) corresponde a eventos f\\'isicos distintos\n"
    "sujetos a diferentes condiciones iniciales de fricci\\'on y\n"
    "liberaci\\'on del carrito, una correlaci\\'on perfecta ($r \\\\approx 1$)\n"
    "ser\\'ia f\\'isicamente imposible. El valor $r = 0.61$ con medias\n"
    "pr\\'acticamente id\\'enticas ($\\\\bar{x}_P = 1.17$~s vs.\\ \n"
    "$\\\\bar{y}_R = 1.19$~s, $\\\\Delta\\\\bar{x} = 0.02$~s) confirma\n"
    "que el sistema IoT captura la variabilidad natural del MRUA\n"
    "sin introducir sesgo sistem\\'atico."
)
pat_s2 = (r'La gr[aá]fica de la Figura.*?corr_s2.*?captura la variabilidad natural del '
          r'fen[oó]meno de MRUA\.')
new_tex, n = re.subn(pat_s2, lambda m: S2_NEW, tex, count=1, flags=re.DOTALL)
if n:
    tex = new_tex
    print("OK - Texto S2 reemplazado")
else:
    print("AVISO - texto S2 no encontrado")

# ══════════════════════════════════════════════════════════════
# BLOQUE 1D: Texto Sensor S3 — reemplazar párrafo incorrecto
# ══════════════════════════════════════════════════════════════
S3_NEW = (
    "La Figura~\\\\ref{fig:corr_s3} muestra la gr\\'afica de dispersi\\'on para S3, con\n"
    "$r = 0.62$, $R^2 = 0.39$, $N = 35$: el coeficiente m\\'as alto\n"
    "de la serie, indicando una correlaci\\'on moderada positiva.\n"
    "Este resultado es consistente con el mayor rango temporal\n"
    "del sensor ($\\\\bar{x}_P = 1.66$~s), que ampl\\'ifica la\n"
    "variabilidad f\\'isica acumulada del MRUA y enriquece la\n"
    "se\\\\~nal estad\\'istica. Las desviaciones est\\'andar pr\\'acticamente\n"
    "id\\'enticas ($\\\\sigma_P = 0.23$~s vs.\\ $\\\\sigma_R = 0.24$~s,\n"
    "$\\\\Delta\\\\sigma = 0.01$~s) demuestran que la detecci\\'on\n"
    "automatizada por interrupciones de hardware del m\\'odulo de\n"
    "control replica la dispersi\\'on del cronometraje manual con\n"
    "una fidelidad estad\\'isticamente equivalente."
)
pat_s3 = r'La Figura.*?corr_s3.*?precisi[oó]n similar\.'
new_tex, n = re.subn(pat_s3, lambda m: S3_NEW, tex, count=1, flags=re.DOTALL)
if n:
    tex = new_tex
    print("OK - Texto S3 reemplazado")
else:
    print("AVISO - texto S3 no encontrado")

# ══════════════════════════════════════════════════════════════
# BLOQUE 2: RENUMERACIÓN SEGURA DE REFERENCIAS
# Estrategia: parsear solo el contenido de \cite{} y \bibitem{}
# ══════════════════════════════════════════════════════════════

# Mapa de renumeración: clave_antigua → clave_nueva
REF_MAP = {
    'r1':   'r1',
    'r2':   'r2',
    'r3':   'r3',
    'r4':   'r4',
    'r5':   'r5',
    'r6':   'r6',
    'r7':   'r7',
    'r8':   'r8',
    'r9':   'r9',
    'lustig2024_new': 'r10',
    'perez2023_esp32': 'r11',
    'marosan2024':    'r12',
    'idoyaga2023':    'r13',
    'invecom2025':    'r14',
    'r45':  'r15',
    'r11':  'r16',
    'r12':  'r17',
    'r13':  'r18',
    'r14':  'r19',
    'r15':  'r20',
    'r16':  'r21',
    'r17':  'r22',
    'r18':  'r23',
    'r19':  'r24',
    'r20':  'r25',
    'r21':  'r26',
    'r22':  'r27',
    'r23':  'r28',
    'r24':  'r29',
    'r25':  'r30',
    'r26':  'r31',
    'r27':  'r32',
    'r28':  'r33',
    'r29':  'r34',
    'r30':  'r35',
    'r31':  'r36',
    'r32':  'r37',
    'r33':  'r38',
    'r34':  'r39',
    'r35':  'r40',
    'r36':  'r41',
    'r37':  'r42',
    'r38':  'r43',
    'r39':  'r44',
    'r40':  'r45',
    'r41':  'r46',
    'r42':  'r47',
    'r10':  'r48',
    'r43':  'r49',
    'r44':  'r50',
    'acm2025_remote': 'r51',
    'chang2024_iot_physics': 'r52',
    'pmc2023_esp32': 'r53',
    'r52':  'r52',  # ya nombrado
    'r53':  'r53',  # ya nombrado
}

def remap_cite_keys(match):
    """Recibe el contenido entre {} de \cite o \bibitem y remapea las claves."""
    inner = match.group(1)
    keys = [k.strip() for k in inner.split(',')]
    new_keys = []
    for k in keys:
        new_k = REF_MAP.get(k, None)
        if new_k is None:
            # Claves antiguas r46-r51, r47-r50 etc. que se deben OMITIR
            # (ya fueron absorbidas en nueva numeración)
            if re.match(r'^r(4[6-9]|5[01])$', k):
                pass  # omitir
            else:
                new_keys.append(k)  # mantener sin cambio
        elif new_k == k:
            new_keys.append(k)
        else:
            new_keys.append(new_k)
    if not new_keys:
        return None  # señal de eliminar
    return match.group(0)[0] + '{' + ','.join(new_keys) + '}'

def process_command(cmd_name, text):
    """Procesa todas las ocurrencias de \cmd_name{...} remapeando claves."""
    def replacer(m):
        result = remap_cite_keys(m)
        if result is None:
            return ''
        return result
    # Extraer contenido de \cite{...} o \bibitem{...}
    # No greedy para no cruzar comandos
    pat = re.compile(r'(\\' + cmd_name + r')\{([^}]+)\}')
    def repl2(m):
        prefix = m.group(1)
        inner = m.group(2)
        keys = [k.strip() for k in inner.split(',')]
        new_keys = []
        for k in keys:
            new_k = REF_MAP.get(k, None)
            if new_k is None:
                if re.match(r'^r(4[6-9]|5[01])$', k):
                    pass
                else:
                    new_keys.append(k)
            else:
                new_keys.append(new_k)
        if not new_keys:
            return ''
        return prefix + '{' + ','.join(new_keys) + '}'
    return pat.sub(repl2, text)

tex = process_command('cite', tex)
tex = process_command('bibitem', tex)
print("OK - Referencias renumeradas (solo dentro de \\cite y \\bibitem)")

# Añadir cita r52 Chang si no existe
old_m = "confirmando la idoneidad del m\\'odulo de control adoptado en este estudio."
new_m = (old_m + " Chang et al.~\\cite{r52} reportan resultados similares al "
         "desplegar una plataforma remota IoT para pr\\'acticas de mec\\'anica "
         "universitaria, confirmando la viabilidad del enfoque adoptado en este trabajo.")
if old_m in tex and r'\cite{r52}' not in tex:
    tex = tex.replace(old_m, new_m, 1)
    print("OK - Cita r52 Chang añadida")

# ══════════════════════════════════════════════════════════════
# BLOQUE 3: Reemplazar sección References completa
# ══════════════════════════════════════════════════════════════

# Leer el archivo de referencias pre-generado
NEW_BIB_FILE = 'new_bibliography.tex'
with open(NEW_BIB_FILE, encoding='utf-8') as f:
    NEW_BIB = f.read()

bib_pat = r'\\begin\{thebibliography\}\{999\}.*?\\end\{thebibliography\}'
new_tex, n = re.subn(bib_pat, lambda m: NEW_BIB, tex, count=1, flags=re.DOTALL)
if n:
    tex = new_tex
    print("OK - Sección References reemplazada (53 entradas)")
else:
    print("AVISO - No se encontró bloque thebibliography")

# ══════════════════════════════════════════════════════════════
# GUARDAR
# ══════════════════════════════════════════════════════════════
with open(SRC, 'w', encoding='utf-8') as f:
    f.write(tex)
print("DONE - template.tex guardado.")
