"""
fix_tex.py
Limpia el template.tex de:
1. Backslashes dobles/triples en secuencias de acento (e.g. correlaci\\\\'on -> correlaci\'on)
2. Numeros de referencia del PDF pegados al final de parrafos (e.g. .358)
3. Texto de tabla/figura del PDF incrustado en parrafos (e.g. "Table 4.Resultados...")
4. Palabras sin espacio como "deretrofittingIoT" -> "de \textit{retrofitting} IoT"
"""
import re

def fix_accents(text):
    """Normaliza las secuencias de acento con backslashes extra."""
    # \\\\'on -> \'on  (cuatro backslashes + comilla + on)
    text = re.sub(r"\\{3,}'([aeiouAEIOUn])", r"\\'\\1", text)
    # \\\\'on -> \'on  (tres backslashes + comilla)
    text = re.sub(r"\\{2}'([aeiouAEIOUn])", r"\\'\\1", text)
    return text

def fix_paragraph_numbers(text):
    """Elimina numeros de referencia del PDF al final de parrafos."""
    # Patron: numero de 3 digitos al final de un parrafo
    text = re.sub(r'\.(\d{3,4})\s*$', '.', text, flags=re.MULTILINE)
    text = re.sub(r'\.(\d{3,4})\s*\n', '.\n', text)
    return text

def fix_embedded_table_text(text):
    """Elimina texto de tabla/figura del PDF incrustado en parrafos."""
    # "Table N.Texto..." al inicio de oracion en medio de parrafo
    text = re.sub(r'\s*Table \d+\.[\w\s\'\.\,\(\)\\\{\}]+?(?=El |Los |La |Un |En |Para |Como |Este |A |Se )', ' ', text)
    text = re.sub(r'\s*Figure \d+\.[\w\s\'\.\,\(\)\\\{\}]+?(?=El |Los |La |Un |En |Para |Como |Este |A |Se )', ' ', text)
    # "Modalidad ¯x(s)s(s)n Presencial ... Figure" - texto de tabla crudo
    text = re.sub(r'Modalidad\s+[¯¯\s\w\.\(\)]+(?=Figure|El |Los |La |Como )', '', text)
    return text

def fix_missing_spaces(text):
    """Arregla palabras pegadas sin espacio como 'deretrofittingIoT'."""
    text = text.replace('deretrofittingIoT', 'de \\textit{retrofitting} IoT')
    text = text.replace('deretrofittingcon', 'de \\textit{retrofitting} con')
    text = text.replace('retrofittingIoT', '\\textit{retrofitting} IoT')
    return text

def fix_approx(text):
    """Reemplaza simbolo Unicode ≈ por comando LaTeX."""
    text = text.replace('≈', r'\approx{}')
    return text

def main():
    with open('template.tex', 'r', encoding='utf-8') as f:
        tex = f.read()
    
    # Separar preambulo del cuerpo del documento para no tocar comandos LaTeX
    # Procesamos todo el texto de forma segura
    tex = fix_accents(tex)
    tex = fix_paragraph_numbers(tex)
    tex = fix_embedded_table_text(tex)
    tex = fix_missing_spaces(tex)
    tex = fix_approx(tex)
    
    with open('template.tex', 'w', encoding='utf-8') as f:
        f.write(tex)
    
    print("Limpieza completada exitosamente.")

if __name__ == '__main__':
    main()
