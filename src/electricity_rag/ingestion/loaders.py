import re
from collections import Counter
from dataclasses import dataclass

import pdfplumber


@dataclass
class LoadedDocument:
    title: str
    source: str
    text: str


def extract_pages_text(pdf) -> list[str]:
    """Extrae el texto de cada página de un PDF ya abierto con pdfplumber."""
    return [pagina.extract_text() for pagina in pdf.pages if pagina.extract_text()]


def normalize_for_comparison(line: str) -> str:
    """Sustituye cualquier secuencia de dígitos por '#', para poder detectar
    líneas de maquetación que se repiten en estructura aunque cambien en un
    número (números de página, fechas...)."""
    return re.sub(r"\d+", "#", line)


def _detect_repeated_line_count(pages_lines: list[list[str]], max_lines: int, threshold: float) -> int:
    """Función interna compartida: cuenta cuántas posiciones iniciales de
    `pages_lines` se repiten (tras normalizar) en al menos `threshold` de las
    páginas, deteniéndose en la primera posición que no cumpla el umbral.
    No sabe si trabaja con cabecera o pie — eso lo decide quien la llama,
    pasando las líneas en el orden que corresponda."""
    total_pages = len(pages_lines)
    repeated_count = 0

    for position in range(max_lines):
        lines_at_position = []
        for lineas in pages_lines:
            if position < len(lineas):
                lines_at_position.append(normalize_for_comparison(lineas[position]))

        if not lines_at_position:
            break

        _, count = Counter(lines_at_position).most_common(1)[0]
        if count / total_pages >= threshold:
            repeated_count += 1
        else:
            break

    return repeated_count


def detect_header_line_count(pages_text: list[str], max_header_lines: int = 3, threshold: float = 0.8) -> int:
    """Devuelve cuántas líneas iniciales son cabecera repetida (0 si no hay ninguna)."""
    pages_lines = [texto.split("\n") for texto in pages_text]
    return _detect_repeated_line_count(pages_lines, max_header_lines, threshold)


def detect_footer_line_count(pages_text: list[str], max_footer_lines: int = 3, threshold: float = 0.8) -> int:
    """Devuelve cuántas líneas finales son pie de página repetido (0 si no hay ninguna).
    Reutiliza la misma lógica que la cabecera, pasando las líneas de cada
    página invertidas (de abajo hacia arriba)."""
    pages_lines = [texto.split("\n")[::-1] for texto in pages_text]
    return _detect_repeated_line_count(pages_lines, max_footer_lines, threshold)


def remove_repeated_lines(pages_text: list[str], header_line_count: int, footer_line_count: int) -> list[str]:
    """Elimina las primeras `header_line_count` y últimas `footer_line_count`
    líneas de cada página."""
    cleaned_pages_text = []
    for texto in pages_text:
        lineas = texto.split("\n")
        end = len(lineas) - footer_line_count if footer_line_count else len(lineas)
        cleaned_lineas = lineas[header_line_count:end]
        cleaned_pages_text.append("\n".join(cleaned_lineas))
    return cleaned_pages_text


def load_pdf(
    path: str,
    title: str,
    max_header_lines: int = 3,
    max_footer_lines: int = 3,
    threshold: float = 0.8,
) -> LoadedDocument:
    """Carga un PDF, detecta y elimina cabeceras y pies de página de
    maquetación repetidos, y devuelve el texto completo limpio.

    Limitación conocida: `header_line_count`/`footer_line_count` se aplican
    uniformemente a todas las páginas, incluida la portada. Si la portada no
    comparte la cabecera/pie repetido del resto del documento (caso típico),
    sus primeras/últimas líneas reales pueden eliminarse igualmente si
    coinciden en posición. Aceptado conscientemente: el título real del
    documento se pasa por parámetro y no depende de este texto extraído.
    """
    with pdfplumber.open(path) as pdf:
        pages_text = extract_pages_text(pdf)
        header_line_count = detect_header_line_count(pages_text, max_header_lines, threshold)
        footer_line_count = detect_footer_line_count(pages_text, max_footer_lines, threshold)
        cleaned_pages_text = remove_repeated_lines(pages_text, header_line_count, footer_line_count)
        full_text = "\n\n".join(cleaned_pages_text)
    return LoadedDocument(title=title, source=path, text=full_text)