import re

def check_citations(tex_file):
    with open(tex_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all citations
    # \cite{key1,key2} or \cite{key}
    # We need to handle multiple keys separated by commas
    cite_pattern = re.compile(r'\\cite\{([^}]+)\}')
    cites = cite_pattern.findall(content)
    
    cited_keys = set()
    for citation in cites:
        # Split by comma and strip whitespace
        keys = [k.strip() for k in citation.split(',')]
        for k in keys:
            cited_keys.add(k)

    # Find all bibitems
    # \bibitem{key}
    bibitem_pattern = re.compile(r'\\bibitem\{([^}]+)\}')
    bibitems = bibitem_pattern.findall(content)
    defined_keys = set(bibitems)

    missing = cited_keys - defined_keys
    unused = defined_keys - cited_keys

    print(f"Total cited keys: {len(cited_keys)}")
    print(f"Total defined keys: {len(defined_keys)}")
    
    if missing:
        print("MISSING KEYS (Undefined citations):")
        for k in sorted(missing):
            print(f" - {k}")
    else:
        print("No missing keys found.")

    if unused:
        print("UNUSED KEYS (Defined but not cited):")
        for k in sorted(unused):
            print(f" - {k}")

if __name__ == "__main__":
    check_citations('c:/Articulo/template.tex')
