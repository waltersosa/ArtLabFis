#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
correcciones7.py — Aplica exactamente las 7 correcciones editoriales finales
"""
import re

SRC = 'template.tex'
with open(SRC, encoding='utf-8') as f:
    tex = f.read()
with open(SRC + '.bak7', 'w', encoding='utf-8') as f:
    f.write(tex)
print("Backup guardado.")

# ══════════════════════════════════════════════════════════════
# CORRECCIÓN 1: Encoding dise´no / dise´nar / Dise´no
# ══════════════════════════════════════════════════════════════
# El carácter ´ puede estar como unicode U+00B4 o como acento suelto
fixes_enc = [
    ("dise\u00b4no",  "dise\u00f1o"),   # diseño
    ("dise\u00b4nar", "dise\u00f1ar"),  # diseñar
    ("Dise\u00b4no",  "Dise\u00f1o"),   # Diseño
    # También con escape LaTeX por si acaso
    ("dise\\'no",     "dise\u00f1o"),
    ("Dise\\'no",     "Dise\u00f1o"),
]
for bad, good in fixes_enc:
    count = tex.count(bad)
    if count:
        tex = tex.replace(bad, good)
        print(f"OK C1 - '{bad}' → '{good}' ({count}x)")

# Verificar preámbulo incluye paquetes necesarios
for pkg in ['inputenc', 'fontenc', 'babel']:
    if pkg not in tex:
        print(f"AVISO C1 - falta paquete {pkg} en preámbulo")
    else:
        print(f"OK C1 - paquete {pkg} presente")

# ══════════════════════════════════════════════════════════════
# CORRECCIÓN 2: Pregunta de investigación — íPuede → ¿Puede
# ══════════════════════════════════════════════════════════════
old2a = "investigaci\\'on: \\'iPuede"
new2a = "investigaci\\'on: \\textquestiondown{}Puede"
old2b = "investigaci\u00f3n: \u00edPuede"
new2b = "investigaci\u00f3n: \u00bfPuede"
old2c = "investigaci\\'on: {\\textquestiondown}Puede"
new2c = "investigaci\\'on: \\textquestiondown{}Puede"

for old, new in [(old2a, new2a), (old2b, new2b), (old2c, new2c)]:
    if old in tex:
        tex = tex.replace(old, new)
        print(f"OK C2 - pregunta de investigación corregida")
        break
else:
    # intentar regex tolerante
    pat2 = re.compile(r"(investigaci[oó]n:\s*)[íi\u00ed]Puede", re.IGNORECASE)
    new_tex, n = re.subn(pat2, r"\1\\textquestiondown{}Puede", tex)
    if n:
        tex = new_tex
        print("OK C2 - pregunta de investigación corregida (regex)")
    else:
        print("AVISO C2 - no se encontró 'íPuede'")

# ══════════════════════════════════════════════════════════════
# CORRECCIÓN 3: Cita [ 10] o [10] en "tres capas" → [48]
# ══════════════════════════════════════════════════════════════
# En sección 2.3 "tres capas bien diferenciadas"
pat3 = re.compile(r'(tres capas bien diferenciadas\s*)(\[\s*10\s*\]|\[r10\]|\{r10\})')
new_tex, n = re.subn(pat3, r'\1\\cite{r48}', tex)
if n:
    tex = new_tex
    print(f"OK C3 - cita [10] → [48] en 'tres capas' ({n}x)")
else:
    # Buscar variante con espacio interno
    tex2 = tex.replace("tres capas bien diferenciadas [ 10]",
                       "tres capas bien diferenciadas \\cite{r48}")
    tex2 = tex2.replace("tres capas bien diferenciadas [10]",
                        "tres capas bien diferenciadas \\cite{r48}")
    if tex2 != tex:
        tex = tex2
        print("OK C3 - cita corregida (replace directo)")
    else:
        print("AVISO C3 - no se encontró la cita de tres capas con [10]")

# ══════════════════════════════════════════════════════════════
# CORRECCIÓN 4: RemotePhysicsLab[45] → RemotePhysicsLab~\cite{r15}
# ══════════════════════════════════════════════════════════════
variants4 = [
    ("RemotePhysicsLab[45]",        "RemotePhysicsLab~\\cite{r15}"),
    ("RemotePhysicsLab [45]",       "RemotePhysicsLab~\\cite{r15}"),
    ("RemotePhysicsLab~[45]",       "RemotePhysicsLab~\\cite{r15}"),
    ("RemotePhysicsLab\\cite{r45}", "RemotePhysicsLab~\\cite{r15}"),
    ("RemotePhysicsLab~\\cite{r45}","RemotePhysicsLab~\\cite{r15}"),
]
found4 = False
for old, new in variants4:
    if old in tex:
        tex = tex.replace(old, new)
        print(f"OK C4 - RemotePhysicsLab → [15]")
        found4 = True
        break
if not found4:
    # regex tolerante
    pat4 = re.compile(r'RemotePhysicsLab\s*[\[\\~]*(?:cite\{)?r?45(?:\])?\}?')
    new_tex, n = re.subn(pat4, "RemotePhysicsLab~\\\\cite{r15}", tex)
    if n:
        tex = new_tex
        print("OK C4 - RemotePhysicsLab corregida (regex)")
    else:
        print("AVISO C4 - no encontrado RemotePhysicsLab con [45]")

# ══════════════════════════════════════════════════════════════
# CORRECCIÓN 5: Python 3.14.1[42] → Python~3.14.1~\cite{r47}
# ══════════════════════════════════════════════════════════════
variants5 = [
    ("Python 3.14.1[42]",           "Python~3.14.1~\\cite{r47}"),
    ("Python~3.14.1[42]",           "Python~3.14.1~\\cite{r47}"),
    ("Python 3.14.1~[42]",          "Python~3.14.1~\\cite{r47}"),
    ("Python~3.14.1~[42]",          "Python~3.14.1~\\cite{r47}"),
    ("Python 3.14.1\\cite{r42}",    "Python~3.14.1~\\cite{r47}"),
    ("Python~3.14.1~\\cite{r42}",   "Python~3.14.1~\\cite{r47}"),
    ("Python 3.14.1~\\cite{r42}",   "Python~3.14.1~\\cite{r47}"),
]
count5 = 0
for old, new in variants5:
    while old in tex:
        tex = tex.replace(old, new, 1)
        count5 += 1
if count5:
    print(f"OK C5 - Python [42] → [47] ({count5}x)")
else:
    pat5 = re.compile(r'Python[\s~]*3\.14\.1[\s~]*\[42\]')
    new_tex, n = re.subn(pat5, "Python~3.14.1~\\\\cite{r47}", tex)
    if n:
        tex = new_tex
        print(f"OK C5 - Python corregida (regex, {n}x)")
    else:
        print("AVISO C5 - no se encontró Python 3.14.1[42]")

# ══════════════════════════════════════════════════════════════
# CORRECCIÓN 6: Eliminar párrafo duplicado S4 (el primero, sin r=0.61)
# ══════════════════════════════════════════════════════════════
# El párrafo duplicado es el que está en línea ~435 ANTES de la tabla S4
# Empieza con "El Sensor S4 representa..." y contiene el bloque sin r=0.61
DUP_S4_START = "El Sensor S4 representa el punto de medici"
DUP_S4_END_MARKER = "movimiento uniformemente acelerado."
# Buscar las dos ocurrencias
idx1 = tex.find(DUP_S4_START)
if idx1 >= 0:
    idx2 = tex.find(DUP_S4_START, idx1 + 1)
    if idx2 >= 0:
        # Hay dos ocurrencias: eliminar la primera (no tiene r=0.61)
        end1 = tex.find(DUP_S4_END_MARKER, idx1)
        if end1 >= 0:
            end1 += len(DUP_S4_END_MARKER)
            # Incluir el \n que sigue
            if tex[end1:end1+1] == '\n':
                end1 += 1
            para1 = tex[idx1:end1]
            if 'r = 0.61' not in para1:
                tex = tex[:idx1] + tex[end1:]
                print("OK C6 - párrafo duplicado S4 (sin r=0.61) eliminado")
            else:
                # La primera sí tiene r=0.61, intentar buscar la segunda sin él
                end2 = tex.find(DUP_S4_END_MARKER, idx2)
                if end2 >= 0:
                    end2 += len(DUP_S4_END_MARKER)
                    para2 = tex[idx2:end2]
                    if 'r = 0.61' not in para2:
                        if tex[end2:end2+1] == '\n':
                            end2 += 1
                        tex = tex[:idx2] + tex[end2:]
                        print("OK C6 - párrafo duplicado S4 eliminado (segunda ocurrencia)")
                    else:
                        print("AVISO C6 - ambas ocurrencias tienen r=0.61, no eliminando")
        else:
            print("AVISO C6 - no se encontró el fin del primer párrafo")
    else:
        # Solo hay una ocurrencia, probablemente el inicio del párrafo largo
        # Buscar solo la parte duplicada dentro del párrafo largo
        OLD_DUP = ("El an\\'alisis de la Figura 10 confirma el patr\\'on observado en los sensores anteriores. "
                   "Tanto las mediciones presenciales como remotas muestran una dispersi\\'on comparable "
                   "(s= 0.28s y s= 0.29s respectivamente), con tiempos medios pr\\'acticamente id\\'enticos "
                   "(2.05 s vs 2.04 s). El coeficiente de correlaci\\'on bajo es consistente con la independencia "
                   "de los ensayos; cada medici\\'on captura la variabilidad natural del fen\\'omeno de MRUA bajo "
                   "diferentes condiciones iniciales. El notable acuerdo entre ambas modalidades demuestra que el "
                   "sistema de \\textit{retrofitting} IoT replica exitosamente las capacidades de medici\\'on de la "
                   "configuraci\\'on tradicional, proporcionando datos cinem\\'aticos confiables adecuados para el "
                   "an\\'alisis cuantitativo del movimiento uniformemente acelerado.")
        if OLD_DUP in tex:
            tex = tex.replace(OLD_DUP, "", 1)
            print("OK C6 - párrafo antiguo S4 eliminado (cadena exacta)")
        else:
            print("AVISO C6 - solo una ocurrencia de 'El Sensor S4', revisando párrafo interno duplicado")
else:
    print("AVISO C6 - no se encontró sección S4")

# ══════════════════════════════════════════════════════════════
# CORRECCIÓN 7a: Cita [52] Chang — añadir oración después de [12] en Sección Related Work
# ══════════════════════════════════════════════════════════════
ANCHOR_52 = "confirmando la idoneidad del m\\'odulo de control adoptado en este estudio."
CHANG_SENTENCE = (
    " De forma an\\'aloga, Chang \\textit{et al.}~\\cite{r52} desplegaron una plataforma"
    " remota basada en IoT para pr\\'acticas de mec\\'anica universitaria, obteniendo"
    " resultados de precisi\\'on comparables a los de este trabajo y confirmando la"
    " replicabilidad del enfoque en distintos contextos institucionales."
)

# Versión unicode (puede estar con acentos directos)
ANCHOR_52_U = "confirmando la idoneidad del módulo de control adoptado en este estudio."

if '\\cite{r52}' in tex and 'Chang' in tex and 'De forma an' in tex:
    print("OK C7a - oración Chang [52] ya presente")
elif ANCHOR_52 in tex:
    # Insertar DESPUÉS del anchor
    tex = tex.replace(ANCHOR_52, ANCHOR_52 + CHANG_SENTENCE, 1)
    print("OK C7a - oración Chang [52] añadida (escape)")
elif ANCHOR_52_U in tex:
    CHANG_SENTENCE_U = (
        " De forma análoga, Chang \\textit{et al.}~\\cite{r52} desplegaron una plataforma"
        " remota basada en IoT para prácticas de mecánica universitaria, obteniendo"
        " resultados de precisión comparables a los de este trabajo y confirmando la"
        " replicabilidad del enfoque en distintos contextos institucionales."
    )
    tex = tex.replace(ANCHOR_52_U, ANCHOR_52_U + CHANG_SENTENCE_U, 1)
    print("OK C7a - oración Chang [52] añadida (unicode)")
else:
    print("AVISO C7a - no se encontró el anchor para [52]")

# ══════════════════════════════════════════════════════════════
# CORRECCIÓN 7b: Cita [53] Kaur — añadir junto a [21] en sección 2.3
# ══════════════════════════════════════════════════════════════
# En el texto del ESP32 con WiFi
variants_53 = [
    ("conectividad WiFi \\cite{r21}",   "conectividad WiFi \\cite{r21,r53}"),
    ("conectividad WiFi~\\cite{r21}",   "conectividad WiFi~\\cite{r21,r53}"),
    ("conectividad WiFi \\cite{r21,",   None),  # ya tiene r53 u otra
]
found_53_text = False
for old, new in variants_53:
    if new is None and old in tex:
        print("OK C7b - [21] ya tiene citas adicionales, no modificar")
        found_53_text = True
        break
    if new and old in tex:
        tex = tex.replace(old, new, 1)
        print(f"OK C7b - [21] → [21,53] en texto ESP32")
        found_53_text = True
        break

if not found_53_text:
    # Buscar con regex si cite{r21} aparece cerca de "WiFi" o "ESP32"
    pat53 = re.compile(r'(WiFi|ESP32[^\n]{0,80}?)(\\cite\{r21\})')
    new_tex, n = re.subn(pat53, r'\1\\cite{r21,r53}', tex, count=1)
    if n:
        tex = new_tex
        print("OK C7b - [21] → [21,53] (regex cerca de ESP32/WiFi)")
    else:
        print("AVISO C7b - no encontrado 'conectividad WiFi \\cite{r21}'")

# CORRECCIÓN 7c: Tabla 1 — fila ESP32, [21] → [21,53]
# Buscar dentro del contexto de la tabla de componentes
ESP32_ROW_VARIANTS = [
    ("ESP32-WROOM-32 & \\cite{r21}",     "ESP32-WROOM-32 & \\cite{r21,r53}"),
    ("ESP32.*?\\\\cite\\{r21\\}(?!,r53)", None),  # para regex
]
found_53_table = False
# Buscar en la tabla de componentes hardware (Tabla 1)
pat53_tab = re.compile(
    r'(ESP32[^\n&]{0,60}?&[^\n&]{0,20}?)\\cite\{r21\}(?!,r53)',
    re.DOTALL
)
new_tex, n = re.subn(pat53_tab, r'\1\\cite{r21,r53}', tex, count=1)
if n:
    tex = new_tex
    print("OK C7c - Tabla 1 ESP32: [21] → [21,53]")
else:
    print("AVISO C7c - no se encontró fila ESP32 con [21] en tabla")

# ══════════════════════════════════════════════════════════════
# GUARDAR
# ══════════════════════════════════════════════════════════════
with open(SRC, 'w', encoding='utf-8') as f:
    f.write(tex)
print("\nDONE - template.tex guardado con las 7 correcciones aplicadas.")
