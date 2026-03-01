"""
fix_tex2.py - Limpieza segura del template.tex post-inyeccion
"""
import re

tex = open('template.tex', encoding='utf-8').read()

# 1. Corregir el artefacto \\'\\1n -> \\'on dejado por el regex anterior 
tex = tex.replace("\\'\\1n", "\\'on")
tex = tex.replace("\\'\\1metro", "\\'ometro")
tex = tex.replace("\\'\\1", "\\'o")

# 2. Normalizar dobles/triples backslash en secuencias de acento
# Busca 2 o mas backslashes seguidos de comilla y vocal
# En el archivo real aparecen como \\\\' (que en texto es \\\')
for vowel in ['a', 'e', 'i', 'o', 'u', 'n', 'A', 'E', 'I', 'O', 'U', 'N']:
    # 4 backslashes + comilla + vocal -> 1 backslash + comilla + vocal  
    tex = tex.replace("\\\\\\\\'" + vowel, "\\'" + vowel)
    # 3 backslashes + comilla + vocal -> 1 backslash + comilla + vocal
    tex = tex.replace("\\\\\\'\\'" + vowel, "\\'" + vowel)
    tex = tex.replace("\\\\'" + vowel, "\\'" + vowel)

# 3. Eliminar numeros de referencia del PDF al final de parrafo
# Pattern: numero 3-4 digitos pegado al final antes de newline
tex = re.sub(r'\.\d{3,4}\r?\n', '.\n', tex)
tex = re.sub(r'\.\d{3,4}$', '.', tex, flags=re.MULTILINE)

# 4. Arreglar texto 'Table N.' y 'Figure N.' incrustado en parrafos 
# (son cabeceras del PDF que quedaron en medio del texto)
# Primero la del sensor S1 (linea 287)
tex = re.sub(r'Table \d+\.Resultados estad\\\'isticos para el Sensor S\d+\.\s*', '', tex)
tex = re.sub(r'Table \d+\.Resultados estad.{0,30}Sensor S\d+\.\s*', '', tex)
tex = re.sub(r'Figure \d+\.Gr\\\'afica de correlaci.*?Presencial\)\.\s*', '', tex)

# 5. Limpiar el barras extra en "Modalidad ¯x(s)..."
tex = re.sub(r'Modalidad\s+[¯\s\d\.\(\)]+(?=Presencial|Remota)', '', tex)
tex = re.sub(r'Presencial \d+\.\d+ \d+\.\d+ Remota \d+\.\d+ \d+\.\d+\s*', '', tex)

# 6. Arreglar palabras sin espacio del PDF
tex = tex.replace('deretrofittingIoT', 'de \\textit{retrofitting} IoT')
tex = tex.replace('deretrofittingcon', 'de \\textit{retrofitting} con')
tex = tex.replace('retrofittingIoT', '\\textit{retrofitting} IoT')

# 7. Reemplazar simbolos Unicode invalidos en LaTeX
tex = tex.replace('≈', r'\approx{}')

open('template.tex', 'w', encoding='utf-8') .write(tex)
print("Limpieza completada.")
