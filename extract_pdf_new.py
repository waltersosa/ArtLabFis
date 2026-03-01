import sys
import PyPDF2

def extract_text_from_pdf(pdf_path, txt_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for i, page in enumerate(reader.pages):
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
                print(f"Página {i+1} procesada.")
            
        with open(txt_path, 'w', encoding='utf-8') as out_file:
            out_file.write(text)
        print(f"Extracción completada. Guardado en {txt_path}")
    except Exception as e:
        print(f"Error al extraer texto: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python extract_pdf_new.py <ruta_del_pdf>")
    else:
        pdf_file = sys.argv[1]
        out_file = "temp_text_new_utf8.txt"
        extract_text_from_pdf(pdf_file, out_file)
