#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Corrige dise\\'n* -> dise\\~n* en todo el documento."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

SRC = 'template.tex'
with open(SRC, encoding='utf-8') as f:
    tex = f.read()

with open(SRC + '.bak8', 'w', encoding='utf-8') as f:
    f.write(tex)
print("Backup guardado.")

orig = tex

# La n con tilde en LaTeX es \~n, NO \'n
# Reemplazar todas las variantes mal escritas
pairs = [
    ("dise\\'nar",  "dise\\~nar"),
    ("dise\\'no",   "dise\\~no"),
    ("Dise\\'no",   "Dise\\~no"),
    ("Dise\\'nar",  "Dise\\~nar"),
    # Con llave: \'{n} no es correcto para n-tilde, pero por si acaso
    ("dise\\'{n}", "dise\\~{n}"),
    ("Dise\\'{n}", "Dise\\~{n}"),
]

for bad, good in pairs:
    count = tex.count(bad)
    if count:
        tex = tex.replace(bad, good)
        print("OK: %s => %s (%dx)" % (repr(bad), repr(good), count))

print("\n--- Verificacion final ---")
print("dise\\'no  restantes:", tex.count("dise\\'no"))
print("dise\\'nar restantes:", tex.count("dise\\'nar"))
print("dise\\~no  presentes:", tex.count("dise\\~no"))
print("dise\\~nar presentes:", tex.count("dise\\~nar"))

if tex != orig:
    with open(SRC, 'w', encoding='utf-8') as f:
        f.write(tex)
    print("\nDONE - archivo guardado.")
else:
    print("\nSIN CAMBIOS - no habia instancias incorrectas.")
