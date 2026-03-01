#!/usr/bin/env python3
# -*- coding: utf-8 -*-
with open('template.tex', encoding='utf-8') as f:
    tex = f.read()

# Fix 1: registró'o -> registró en linea de tasa 98.5%
old1 = "registr\\'o\\'o una tasa del 98.5"
new1 = "registr\\'o una tasa del 98.5"
n1 = tex.count(old1)
tex = tex.replace(old1, new1)
print("registro fix: %d ocurrencias" % n1)

# Fix 2: quitar italicas de Edge computing en todo el documento
old2a = '\\textit{Edge computing}'
new2a = 'Edge computing'
n2a = tex.count(old2a)
tex = tex.replace(old2a, new2a)
print("textit{Edge computing} fix: %d ocurrencias" % n2a)

old2b = '\\emph{Edge computing}'
new2b = 'Edge computing'
n2b = tex.count(old2b)
tex = tex.replace(old2b, new2b)
print("emph{Edge computing} fix: %d ocurrencias" % n2b)

with open('template.tex', 'w', encoding='utf-8') as f:
    f.write(tex)
print("DONE")
