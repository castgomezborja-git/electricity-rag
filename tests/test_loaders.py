from electricity_rag.ingestion.loaders import (
    detect_header_line_count,
    detect_footer_line_count,
    normalize_for_comparison,
)


def test_detect_header_line_count_detects_repeated_lines():
    # Arrange
    pages_text = [
        "CABECERA\nSUBTÍTULO\nContenido específico A",
        "CABECERA\nSUBTÍTULO\nContenido específico B",
        "CABECERA\nSUBTÍTULO\nContenido específico C",
        "CABECERA\nSUBTÍTULO\nContenido específico D",
        "CABECERA\nSUBTÍTULO\nContenido específico E",
    ]

    # Act
    resultado = detect_header_line_count(pages_text)

    # Assert
    assert resultado == 2


def test_detect_short_pages():
    # Arrange
    pages_text = [
        "CABECERA\nSUBTÍTULO\nContenido específico A",
        " ",
        "CABECERA\nSUBTÍTULO\nContenido específico C",
        "CABECERA\nSUBTÍTULO\nContenido específico D",
        "CABECERA\nSUBTÍTULO\nContenido específico E",
    ]

    # Act
    resultado = detect_header_line_count(pages_text)

    # Assert
    assert resultado == 2


def test_detect_header_line_count_no_repeated_lines():
    # Arrange
    pages_text = [
        "CABECERA\nSUBTÍTULO\nContenido específico A",
        "CABECERA DIFERENTE\nSUBTÍTULO DIFERENTE\nContenido específico B",
        "CABECERA X\nSUBTÍTULO X\nContenido específico C",
        "CABECERA DIFERENTE X\nSUBTÍTULO DIFERENTE X\nContenido específico D",
        "CABECERA Y\nSUBTÍTULO Y\nContenido específico E",
    ]

    # Act
    resultado = detect_header_line_count(pages_text)

    # Assert
    assert resultado == 0


def test_detect_header_line_count_partial_repetition():
    # Arrange
    pages_text = [
        "CABECERA\nSUBTÍTULO\nEsta línea se repite por casualidad",
        "CABECERA\nSUBTÍTULO\nEsta línea se repite por casualidad",
        "CABECERA\nSUBTÍTULO\nContenido específico C",
        "CABECERA\nSUBTÍTULO\nContenido específico D",
        "CABECERA\nSUBTÍTULO\nContenido específico E",
    ]

    # Act
    resultado = detect_header_line_count(pages_text)

    # Assert
    assert resultado == 2


def test_normalize_for_comparison_replaces_digits():
    # Arrange / Act / Assert
    assert normalize_for_comparison("Página 3 de 28") == "Página # de #"


def test_detect_footer_line_count_handles_varying_page_numbers():
    # Arrange: pie de página con número de página distinto en cada una,
    # el caso real que motivó la normalización con regex
    pages_text = [
        "Contenido específico A\nComisión Nacional 1 de 5",
        "Contenido específico B\nComisión Nacional 2 de 5",
        "Contenido específico C\nComisión Nacional 3 de 5",
        "Contenido específico D\nComisión Nacional 4 de 5",
        "Contenido específico E\nComisión Nacional 5 de 5",
    ]

    # Act
    resultado = detect_footer_line_count(pages_text)

    # Assert
    assert resultado == 1