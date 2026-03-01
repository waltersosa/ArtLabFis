#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Corrige el párrafo Bland-Altman con dobles backslashes."""

with open('template.tex', encoding='utf-8') as f:
    tex = f.read()

# Encontrar y mostrar el párrafo problemático
idx = tex.find('Es importante se')
if idx < 0:
    print("No encontrado")
    exit()

chunk = tex[idx:idx+500]
print("ANTES:", repr(chunk[:200]))

# El problema: \\'isicos debería ser \'isicos en el .tex
# En el archivo real, lo que hay es \\' (dos chars: backslash backslash quote)
# lo que queremos es \' (un backslash + quote)
end_idx = tex.find('\\cite{giavarina2015}.', idx)
if end_idx < 0:
    print("No se encontró el fin del párrafo")
    exit()
end_idx += len('\\cite{giavarina2015}.')

old_para = tex[idx:end_idx]
print("VIEJO:", repr(old_para))

# Reemplazar \\\' (4 chars en el string Python: \\\\\\') por \' (2 chars: \\')
new_para = old_para.replace("\\\\'", "\\'")
print("NUEVO:", repr(new_para))

tex = tex[:idx] + new_para + tex[end_idx:]

with open('template.tex', 'w', encoding='utf-8') as f:
    f.write(tex)
print("OK - guardado")
