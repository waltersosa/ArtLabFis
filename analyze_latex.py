import re
from pathlib import Path
from collections import defaultdict

# Read the template file
template_path = r'c:\Articulo\template.tex'
with open(template_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("=" * 80)
print("ANÁLISIS COMPLETO DE TEMPLATE.TEX")
print("=" * 80)

# 1. Extract all citations
citations = re.findall(r'\\cite\{([^}]+)\}', content)
citation_set = set()
for cite in citations:
    # Handle multiple citations in one \cite{}
    for c in cite.split(','):
        citation_set.add(c.strip())

print(f"\n1. CITAS ENCONTRADAS ({len(citation_set)} únicas):")
for cite in sorted(citation_set):
    print(f"   - {cite}")

# 2. Extract all bibitem entries
bibitems = re.findall(r'\\bibitem\{([^}]+)\}', content)
bibitem_set = set(bibitems)

print(f"\n2. ENTRADAS DE BIBLIOGRAFÍA ({len(bibitem_set)}):")
for bib in sorted(bibitem_set):
    print(f"   - {bib}")

# 3. Compare citations vs bibitems
print(f"\n3. CITAS SIN ENTRADA BIBLIOGRÁFICA:")
missing_bibitems = citation_set - bibitem_set
if missing_bibitems:
    for missing in sorted(missing_bibitems):
        print(f"   ❌ {missing}")
else:
    print("   ✓ Todas las citas tienen entrada bibliográfica")

print(f"\n4. ENTRADAS BIBLIOGRÁFICAS NO CITADAS:")
unused_bibitems = bibitem_set - citation_set
if unused_bibitems:
    for unused in sorted(unused_bibitems):
        print(f"   ⚠ {unused}")
else:
    print("   ✓ Todas las entradas bibliográficas están citadas")

# 5. Extract all figures
figures = re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}', content)

print(f"\n5. FIGURAS REFERENCIADAS ({len(figures)}):")
figures_dir = Path(r'c:\Articulo\figures')
for fig in figures:
    fig_path = figures_dir / fig
    exists = fig_path.exists()
    status = "✓" if exists else "❌"
    print(f"   {status} {fig}")

# 6. Extract labels and refs
labels = re.findall(r'\\label\{([^}]+)\}', content)
label_set = set(labels)

refs = re.findall(r'\\ref\{([^}]+)\}', content)
ref_set = set(refs)

print(f"\n6. LABELS DEFINIDOS ({len(label_set)}):")
for label in sorted(label_set):
    print(f"   - {label}")

print(f"\n7. REFERENCIAS A LABELS ({len(ref_set)}):")
for ref in sorted(ref_set):
    print(f"   - {ref}")

print(f"\n8. REFERENCIAS SIN LABEL CORRESPONDIENTE:")
missing_labels = ref_set - label_set
if missing_labels:
    for missing in sorted(missing_labels):
        print(f"   ❌ {missing}")
else:
    print("   ✓ Todas las referencias tienen su label")

print(f"\n9. LABELS NO REFERENCIADOS:")
unused_labels = label_set - ref_set
if unused_labels:
    for unused in sorted(unused_labels):
        print(f"   ⚠ {unused}")
else:
    print("   ✓ Todos los labels están referenciados")

# 10. Check for common LaTeX errors
print(f"\n10. BÚSQUEDA DE ERRORES COMUNES:")

# Check for unmatched braces in a simple way
open_braces = content.count('{')
close_braces = content.count('}')
print(f"   - Llaves: {open_braces} abiertas, {close_braces} cerradas", end="")
if open_braces == close_braces:
    print(" ✓")
else:
    print(f" ❌ Diferencia: {abs(open_braces - close_braces)}")

# Check for special characters that might need escaping
problematic_chars = ['&', '%', '$', '#', '_']
lines = content.split('\n')
for i, line in enumerate(lines, 1):
    # Skip comments and command definitions
    if line.strip().startswith('%'):
        continue
    # Check for unescaped special characters outside math mode
    for char in ['&']:
        # This is a simple check; & is valid in tables
        pass

# 11. Check package usage
print(f"\n11. PAQUETES UTILIZADOS:")
packages = re.findall(r'\\usepackage(?:\[[^\]]*\])?\{([^}]+)\}', content)
for pkg in packages:
    print(f"   - {pkg}")

# 12. Summary
print(f"\n" + "=" * 80)
print("RESUMEN DE PROBLEMAS:")
print("=" * 80)

problems = []
if missing_bibitems:
    problems.append(f"❌ {len(missing_bibitems)} citas sin entrada bibliográfica")
if missing_labels:
    problems.append(f"❌ {len(missing_labels)} referencias sin label")

# Check figures
missing_figs = []
for fig in figures:
    fig_path = figures_dir / fig
    if not fig_path.exists():
        missing_figs.append(fig)

if missing_figs:
    problems.append(f"❌ {len(missing_figs)} archivos de figuras no encontrados")

if problems:
    for p in problems:
        print(p)
else:
    print("✓ No se encontraron problemas críticos")

if unused_bibitems:
    print(f"\n⚠ Advertencias: {len(unused_bibitems)} entradas bibliográficas no citadas")
if unused_labels:
    print(f"⚠ Advertencias: {len(unused_labels)} labels no referenciados")

print("\n" + "=" * 80)
