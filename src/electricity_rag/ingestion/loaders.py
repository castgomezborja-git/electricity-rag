from dataclasses import dataclass

import pdfplumber
from collections import Counter


@dataclass
class LoadedDocument:
    title: str
    source: str
    text: str


def extract_pages_text(pdf) -> list[str]:
    """Extrae el texto de cada página de un PDF ya abierto con pdfplumber."""
    return [pagina.extract_text() for pagina in pdf.pages if pagina.extract_text()]

def detect_header_line_count(pages_text: list[str], max_header_lines: int = 3, threshold: float = 0.8) -> int:
    """Devuelve cuántas líneas iniciales son cabecera repetida (0 si no hay ninguna)."""
    total_pages = len(pages_text)
    header_line_count = 0

    for position in range(max_header_lines):
        lines_at_position = []
        for texto in pages_text:
            lineas = texto.split("\n")
            if position < len(lineas):
                lines_at_position.append(lineas[position])

        if not lines_at_position:
            break

        most_common_line, count = Counter(lines_at_position).most_common(1)[0]
        if count / total_pages >= threshold:
            header_line_count += 1
        else:
            break  # en cuanto una posición falla, dejamos de considerar cabecera

    return header_line_count

def remove_repeated_headers(pages_text: list[str], header_line_count: int) -> list[str]:
    """Elimina las primeras `header_line_count` líneas de cada página."""
    cleaned_pages_text = []
    for texto in pages_text:
            lineas = texto.split("\n")
            cleaned_lineas = lineas[header_line_count:]
            cleaned_pages_text.append("\n".join(cleaned_lineas))
    

    return cleaned_pages_text

def load_pdf(path: str, title: str, max_header_lines: int = 3, threshold: float = 0.8) -> LoadedDocument:
    """Carga un PDF, detecta y elimina cabeceras de maquetación repetidas, y devuelve el texto completo limpio.

    Limitación conocida: `header_line_count` se aplica uniformemente a todas
    las páginas, incluida la portada. Si la portada no comparte la cabecera
    repetida del resto del documento (caso típico), sus primeras líneas
    reales pueden eliminarse igualmente si coinciden en posición con las
    líneas de cabecera detectadas. Aceptado conscientemente: el título real
    del documento se pasa por parámetro y no depende de este texto extraído.
    """


    with pdfplumber.open(path) as pdf:
        pages_text = extract_pages_text(pdf)
        header_line_count = detect_header_line_count(pages_text, max_header_lines, threshold)
        cleaned_pages_text = remove_repeated_headers(pages_text, header_line_count)
        full_text = "\n\n".join(cleaned_pages_text)
    return LoadedDocument(title=title, source=path, text=full_text)