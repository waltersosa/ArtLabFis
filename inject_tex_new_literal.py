import re

def clean_pdf_text(raw_text):
    text = re.sub(r'Version February 11, 2026 submitted toJournal Not Specified.*?of 18\n', '', raw_text)
    text = re.sub(r'Version February 11, 2026 submitted toJournal Not Specifiedhttps://doi\.org/10\.3390/1010000\n', '', text)
    text = re.sub(r' \d{1,3}\n', '\n', text)
    text = re.sub(r'\n(\d+\.\d*\s+[A-Z])', r'\n\n\1', text)
    text = text.replace('\n\n', '<PARAGRAPH>')
    text = text.replace('\n', ' ')
    text = text.replace('<PARAGRAPH>', '\n\n')
    text = re.sub(r' +', ' ', text)
    return text

def escape_latex(text):
    text = text.replace('ǭ', 'a').replace('Ǹ', 'e').replace('ǧ', 'u')
    # Letras con tilde ocultas y problemas fonéticos captados del PDF
    text = text.replace('anlisis', 'an\'alisis').replace('a\'nlisis', 'an\'alisis').replace('a\~nlisis', 'an\'alisis')
    text = text.replace('tcnica', 't\'ecnica').replace('t\'cnica', 't\'ecnica')
    
    replacements = {
        'á': r"\'a", 'é': r"\'e", 'í': r"\'i", 'ó': r"\'o", 'ú': r"\'u",
        'Á': r"\'A", 'É': r"\'E", 'Í': r"\'I", 'Ó': r"\'O", 'Ú': r"\'U",
        'ñ': r"\~n", 'Ñ': r"\~N",
    }
    for search, replace in replacements.items():
        text = text.replace(search, replace)
    
    # Limpieza heurística de glifos residuales rotos generados post-sustitución "literal"
    text = re.sub(r'\'o\'([a-zA-Z])', r'\'\1', text) 
    text = re.sub(r'\\\'([a-zA-Z])\'o', r'\\\'\1', text)
    text = re.sub(r'\'o([^\']*?)\'o', r'\1', text) 
    
    return text

def extract_sections(cleaned_text):
    sections = {}
    
    # Abstract
    match = re.search(r'Abstract(.*?)Keywords:', cleaned_text, re.DOTALL | re.IGNORECASE)
    if match:
        sections['abstract'] = escape_latex(match.group(1).strip())
        
    # Introduction
    match = re.search(r'1\. Introduction(.*?)1\.1\. Related Work', cleaned_text, re.DOTALL)
    if match:
        sections['intro'] = escape_latex(match.group(1).strip())
        
    # Related Work
    match = re.search(r'1\.1\. Related Work and Research Gap(.*?)2\. Materials and Methods', cleaned_text, re.DOTALL)
    if match:
        sections['related_work'] = escape_latex(match.group(1).strip())

    # Dise~no de la investigacion
    match = re.search(r'2\.1\. Dise...o de la investigaci.n(.*?)2\.2\. Hardware y software', cleaned_text, re.DOTALL)
    if match:
        sections['research_design'] = escape_latex(match.group(1).strip())

    # Hardware y software
    match = re.search(r'2\.2\. Hardware y software utilizados(.*?)Table 1', cleaned_text, re.DOTALL)
    if match:
        sections['hardware_software'] = escape_latex(match.group(1).strip())

    # Arquitectura general
    match = re.search(r'2\.3\. Arquitectura general del sistema(.*?)Figure 1', cleaned_text, re.DOTALL)
    if match:
        sections['arquitectura'] = escape_latex(match.group(1).strip())

    # Poblacion y muestra
    match = re.search(r'2\.4\. Poblaci.n, muestra y entorno experimental(.*?)2\.5\. Procedimiento de implementaci.n', cleaned_text, re.DOTALL)
    if match:
        sections['poblacion'] = escape_latex(match.group(1).strip())

    # Procedimiento
    match = re.search(r'2\.5\. Procedimiento de implementaci.n(.*?)Figure 3', cleaned_text, re.DOTALL)
    if match:
        sections['procedimiento'] = escape_latex(match.group(1).strip())

    # Metricas
    match = re.search(r'2\.6\. M.tricas de an.lisis y comparaci.n(.*?)Los indicadores se definen mediante las siguientes ecuaciones:', cleaned_text, re.DOTALL)
    if match:
        sections['metricas'] = escape_latex(match.group(1).strip())
    
    # Metodos analisis
    match = re.search(r'2\.7\. M.todos de an.lisis de datos(.*?)2\.8\. Control de validez', cleaned_text, re.DOTALL)
    if match:
        sections['analisis_datos'] = escape_latex(match.group(1).strip())

    # Control de validez
    match = re.search(r'2\.8\. Control de validez y confiabilidad(.*?)2\.9\. Reproducibilidad', cleaned_text, re.DOTALL)
    if match:
        sections['validez'] = escape_latex(match.group(1).strip())

    # Reproducibilidad
    match = re.search(r'2\.9\. Reproducibilidad y .tica(.*?)3\. Results', cleaned_text, re.DOTALL)
    if match:
        sections['reproducibilidad'] = escape_latex(match.group(1).strip())

    # Resultados (3, 3.1..3.5)
    match = re.search(r'3\. Results(.*?)3\.1\. Experimental Configuration', cleaned_text, re.DOTALL)
    if match: sections['results_intro'] = escape_latex(match.group(1).strip())
    match = re.search(r'3\.1\. Experimental Configuration and Prototype Implementation(.*?)3\.2\. Sensor S1', cleaned_text, re.DOTALL)
    if match: sections['results_31'] = escape_latex(match.group(1).strip())
    match = re.search(r'3\.2\. Sensor S1: Inicio del movimiento(.*?)3\.3\. Sensor S2', cleaned_text, re.DOTALL)
    if match: sections['results_32'] = escape_latex(match.group(1).strip())
    match = re.search(r'3\.3\. Sensor S2: Primera secci.n intermedia(.*?)3\.4\. Sensor S3', cleaned_text, re.DOTALL)
    if match: sections['results_33'] = escape_latex(match.group(1).strip())
    match = re.search(r'3\.4\. Sensor S3: Segunda secci.n intermedia(.*?)3\.5\. Sensor S4', cleaned_text, re.DOTALL)
    if match: sections['results_34'] = escape_latex(match.group(1).strip())
    match = re.search(r'3\.5\. Sensor S4: Final de la pista(.*?)4\. Discussion', cleaned_text, re.DOTALL)
    if match: sections['results_35'] = escape_latex(match.group(1).strip())

    # Discussion (4, 4.1..4.4)
    match = re.search(r'4\.1\. Interpretaci.n de resultados temporales(.*?)4\.2\. Implications of IoT', cleaned_text, re.DOTALL)
    if match: sections['discussion_41'] = escape_latex(match.group(1).strip())
    match = re.search(r'4\.2\. Implications of IoT .*? in Physics Laboratories(.*?)4\.3\. Comparaci.n con trabajos relacionados', cleaned_text, re.DOTALL)
    if match: sections['discussion_42'] = escape_latex(match.group(1).strip())
    match = re.search(r'4\.3\. Comparaci.n con trabajos relacionados(.*?)4\.4\. Limitaciones del estudio', cleaned_text, re.DOTALL)
    if match: sections['discussion_43'] = escape_latex(match.group(1).strip())
    match = re.search(r'4\.4\. Limitaciones del estudio(.*?)4\.5\. Trabajo futuro', cleaned_text, re.DOTALL)
    if match: sections['discussion_44'] = escape_latex(match.group(1).strip())
    match = re.search(r'4\.5\. Trabajo futuro(.*?)5\. Conclusions', cleaned_text, re.DOTALL)
    if match: sections['discussion_45'] = escape_latex(match.group(1).strip())

    # Conclusions
    match = re.search(r'5\. Conclusions(.*?)References', cleaned_text, re.DOTALL)
    if match: sections['conclusions'] = escape_latex(match.group(1).strip())

    return sections

def process_tex():
    with open('temp_text_new_utf8.txt', 'r', encoding='utf-8') as f:
        raw_content = f.read()
        
    cleaned = clean_pdf_text(raw_content)
    sections = extract_sections(cleaned)

    tex_file = 'template.tex'
    with open(tex_file, 'r', encoding='utf-8') as f:
        tex_content = f.read()

    # Reemplazo principal de Intro, Method
    if 'abstract' in sections: tex_content = re.sub(r'\\abstract\{.*?\}', lambda m: r'\abstract{' + sections['abstract'] + '}', tex_content, flags=re.DOTALL)
    if 'intro' in sections: tex_content = re.sub(r'\\section\{Introducci\\\'on\}\n\n(.*?)\n\n\\subsection\{Trabajo', lambda m: r'\section{Introducci\'on}' + '\n\n' + sections['intro'] + '\n\n\\subsection{Trabajo', tex_content, flags=re.DOTALL)
    if 'related_work' in sections: tex_content = re.sub(r'\\subsection\{Trabajo relacionado y brecha de investigaci\\\'on\}\n\n(.*?)\n\n%-------------------------------------------------\n% MATERIALS', lambda m: r'\subsection{Trabajo relacionado y brecha de investigaci\'on}' + '\n\n' + sections['related_work'] + '\n\n%-------------------------------------------------\n% MATERIALS', tex_content, flags=re.DOTALL)
    
    # Method
    if 'research_design' in sections: tex_content = re.sub(r'\\subsection\{Dise\\~no de la investigaci\\\'on\}\n\n(.*?)\n\n%-------------------------------------------------\n\\subsection\{Hardware', lambda m: r'\subsection{Dise\~no de la investigaci\'on}' + '\n\n' + sections['research_design'] + '\n\n%-------------------------------------------------\n\\subsection{Hardware', tex_content, flags=re.DOTALL)
    if 'hardware_software' in sections: tex_content = re.sub(r'\\subsection\{Hardware y software utilizados\}\n\n(.*?)\n\n\\begin\{table\}', lambda m: r'\subsection{Hardware y software utilizados}' + '\n\n' + sections['hardware_software'] + '\n\n\\begin{table}', tex_content, flags=re.DOTALL)
    if 'arquitectura' in sections: tex_content = re.sub(r'\\subsection\{Arquitectura general del sistema\}\n\n(.*?)\n\n\\begin\{figure\}', lambda m: r'\subsection{Arquitectura general del sistema}' + '\n\n' + sections['arquitectura'] + '\n\n\\begin{figure}', tex_content, flags=re.DOTALL)
    if 'poblacion' in sections: tex_content = re.sub(r'Experimental Context and Trial Plan.*?\n\n(.*?)\n\n%-------------------------------------------------\n\\subsection\{Procedimiento', lambda m: r'Poblaci\'on, muestra y entorno experimental}\n\n' + sections['poblacion'] + '\n\n%-------------------------------------------------\n\\subsection{Procedimiento', tex_content, flags=re.DOTALL)
    if 'procedimiento' in sections: tex_content = re.sub(r'\\subsection\{Procedimiento de implementaci\\\'on\}\n\n(.*?)\n\n\\begin\{figure\}', lambda m: r'\subsection{Procedimiento de implementaci\'on}' + '\n\n' + sections['procedimiento'] + '\n\n\\begin{figure}', tex_content, flags=re.DOTALL)
    if 'analisis_datos' in sections: tex_content = re.sub(r'\\subsection\{M\\\'etodos de an\\\'alisis de datos\}\n\n(.*?)\n\n\n%-------------------------------------------------\n\\subsection\{Control', lambda m: r'\subsection{M\'etodos de an\'alisis de datos}' + '\n\n' + sections['analisis_datos'] + '\n\n\n%-------------------------------------------------\n\\subsection{Control', tex_content, flags=re.DOTALL)
    if 'validez' in sections: tex_content = re.sub(r'\\subsection\{Control de validez y confiabilidad\}\n\n(.*?)\n\n\\subsection\{Reproducibilidad', lambda m: r'\subsection{Control de validez y confiabilidad}' + '\n\n' + sections['validez'] + '\n\n\\subsection{Reproducibilidad', tex_content, flags=re.DOTALL)
    
    # Results
    if 'results_intro' in sections: tex_content = re.sub(r'\\section\{Resultados\}\n\n(.*?)\n\n\\subsection\{Configuraci\\\'on', lambda m: r'\section{Resultados}' + '\n\n' + sections['results_intro'] + '\n\n\\subsection{Configuraci\'on', tex_content, flags=re.DOTALL)
    if 'results_31' in sections: tex_content = re.sub(r'\\subsection\{Configuraci\\\'on experimental e implementaci\\\'on del prototipo\}\n\n(.*?)\n\n\\begin\{figure\}', lambda m: r'\subsection{Configuraci\'on experimental e implementaci\'on del prototipo}' + '\n\n' + sections['results_31'] + '\n\n\\begin{figure}', tex_content, flags=re.DOTALL)
    if 'results_32' in sections: tex_content = re.sub(r'\\subsection\{Sensor S1: Inicio del movimiento\}\n\n(.*?)\n\n\\begin\{table\}', lambda m: r'\subsection{Sensor S1: Inicio del movimiento}' + '\n\n' + sections['results_32'] + '\n\n\\begin{table}', tex_content, flags=re.DOTALL)
    if 'results_33' in sections: tex_content = re.sub(r'\\subsection\{Sensor S2: Primera secci\\\'on intermedia\}\n\n(.*?)\n\n\\begin\{table\}', lambda m: r'\subsection{Sensor S2: Primera secci\'on intermedia}' + '\n\n' + sections['results_33'] + '\n\n\\begin{table}', tex_content, flags=re.DOTALL)
    if 'results_34' in sections: tex_content = re.sub(r'\\subsection\{Sensor S3: Segunda secci\\\'on intermedia\}\n\n(.*?)\n\n\\begin\{table\}', lambda m: r'\subsection{Sensor S3: Segunda secci\'on intermedia}' + '\n\n' + sections['results_34'] + '\n\n\\begin{table}', tex_content, flags=re.DOTALL)
    if 'results_35' in sections: tex_content = re.sub(r'\\subsection\{Sensor S4: Final de la pista\}\n\n(.*?)\n\n\\begin\{table\}', lambda m: r'\subsection{Sensor S4: Final de la pista}' + '\n\n' + sections['results_35'] + '\n\n\\begin{table}', tex_content, flags=re.DOTALL)

    # Discussions & conclusions
    if 'discussion_41' in sections: tex_content = re.sub(r'\\subsection\{Interpretaci\\\'on de resultados temporales y cinem\\\'aticos\}\n\n(.*?)\n\n\\subsection\{Implicaciones', lambda m: r'\subsection{Interpretaci\'on de resultados temporales y cinem\'aticos}' + '\n\n' + sections['discussion_41'] + '\n\n\\subsection{Implicaciones', tex_content, flags=re.DOTALL)
    if 'discussion_43' in sections: tex_content = re.sub(r'\\subsection\{Comparaci\\\'on con trabajos relacionados\}\n\n(.*?)\n\n\\subsection\{Limitaciones', lambda m: r'\subsection{Comparaci\'on con trabajos relacionados}' + '\n\n' + sections['discussion_43'] + '\n\n\\subsection{Limitaciones', tex_content, flags=re.DOTALL)
    if 'discussion_44' in sections: tex_content = re.sub(r'\\subsection\{Limitaciones del estudio\}\n\n(.*?)\n\n\\subsection\{Trabajo futuro\}', lambda m: r'\subsection{Limitaciones del estudio}' + '\n\n' + sections['discussion_44'] + '\n\n\\subsection{Trabajo futuro}', tex_content, flags=re.DOTALL)
    if 'discussion_45' in sections: tex_content = re.sub(r'\\subsection\{Trabajo futuro\}\n\n(.*?)\n\n\\section\{Conclusiones\}', lambda m: r'\subsection{Trabajo futuro}' + '\n\n' + sections['discussion_45'] + '\n\n\\section{Conclusiones}', tex_content, flags=re.DOTALL)
    if 'conclusions' in sections: tex_content = re.sub(r'\\section\{Conclusiones\}\n\n(.*?)\n\n%-------------------------------------------------\n% REFERENCES', lambda m: r'\section{Conclusiones}' + '\n\n' + sections['conclusions'] + '\n\n%-------------------------------------------------\n% REFERENCES', tex_content, flags=re.DOTALL)

    with open(tex_file, 'w', encoding='utf-8') as f:
        f.write(tex_content)
    
    print(f"Reemplazadas {len(sections.keys())} secciones: {list(sections.keys())}")

if __name__ == '__main__':
    process_tex()
