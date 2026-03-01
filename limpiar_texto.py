import re
import sys

def clean_pdf_text(raw_text):
    """
    Limpia el texto extraído del PDF eliminando los números de línea al final
    y los encabezados/pies de página como:
    'Version February 11, 2026 submitted toJournal Not Specified'
    """
    # Eliminar encabezados/pies de página
    text = re.sub(r'Version February 11, 2026 submitted toJournal Not Specified.*?of 18\n', '', raw_text)
    text = re.sub(r'Version February 11, 2026 submitted toJournal Not Specifiedhttps://doi\.org/10\.3390/1010000\n', '', text)
    
    # Eliminar números aislados al final de las líneas (ejemplo: "palabra 18\n" -> "palabra\n")
    # Maneja casos donde hay un espacio y luego de 1 a 3 digitos al final.
    text = re.sub(r' \d{1,3}\n', '\n', text)
    
    # Unir líneas que quedaron cortadas (párrafos)
    # Si una línea termina sin punto, y la siguiente empieza con minúscula o es continuación
    # lo manejaremos reemplazando un salto de linea simple por espacio,
    # y doble salto de línea se mantiene como nuevo párrafo.
    
    # Primero forzar doble salto de linea antes de las viñetas o numeraciones principales
    text = re.sub(r'\n(\d+\.\d*\s+[A-Z])', r'\n\n\1', text)
    
    # Reemplazar doble salto temporalmente
    text = text.replace('\n\n', '<PARAGRAPH>')
    
    # Eliminar saltos simples
    text = text.replace('\n', ' ')
    
    # Restaurar párrafos
    text = text.replace('<PARAGRAPH>', '\n\n')
    
    # Arreglar espacios dobles que se formaron
    text = re.sub(r' +', ' ', text)
    
    return text

def escape_latex(text):
    """
    Escapa los caracteres especiales de español para que LaTeX los procese bien.
    e.g. á -> \'a
    """
    replacements = {
        'á': r"\'a", 'é': r"\'e", 'í': r"\'i", 'ó': r"\'o", 'ú': r"\'u",
        'Á': r"\'A", 'É': r"\'E", 'Í': r"\'I", 'Ó': r"\'O", 'Ú': r"\'U",
        'ñ': r"\~n", 'Ñ': r"\~N",
        # Simbolos raros que aparecieron en el text extraido del PDF (fallos de encoding de la fuente)
        'ǭ': r"\'a", 'Ǹ': r"\'e", '': r"\'i", '': r"\'o", 'ǧ': r"\'u",
        '': r"\~n"
    }
    for search, replace in replacements.items():
        text = text.replace(search, replace)
    
    return text

def extract_sections(cleaned_text):
    sections = {}
    
    # Abstract
    match = re.search(r'Abstract:(.*?)(?=Keywords:)', cleaned_text, re.DOTALL)
    if match:
        sections['abstract'] = escape_latex(match.group(1).strip())
        
    # Introduction
    match = re.search(r'1\. Introduction(.*?)1\.1\. Related Work and Research Gap', cleaned_text, re.DOTALL)
    if match:
        sections['intro'] = escape_latex(match.group(1).strip())
        
    # Related Work
    match = re.search(r'1\.1\. Related Work and Research Gap(.*?)2\. Materials and Methods', cleaned_text, re.DOTALL)
    if match:
        sections['related_work'] = escape_latex(match.group(1).strip())

    # Dise~no de la investigacion
    match = re.search(r'2\.1\. Dise\~no de la investigaci\'on(.*?)2\.2\. Hardware y software', escape_latex(cleaned_text), re.DOTALL)
    if match:
        sections['research_design'] = match.group(1).strip()
        
    # El resto se puede seguir extrayendo...
    
    return sections

if __name__ == "__main__":
    with open('temp_text_new_utf8.txt', 'r', encoding='utf-8') as f:
        raw_content = f.read()
        
    cleaned = clean_pdf_text(raw_content)
    # Debug impreso para ver cómo queda
    print(cleaned[:1000])
    
    sections = extract_sections(cleaned)
    print("Secciones extraídas:", list(sections.keys()))
