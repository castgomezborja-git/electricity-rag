from electricity_rag.ingestion.loaders import detect_header_line_count


def test_detect_header_line_count_detects_repeated_lines():
    # Arrange
    pages_text = [
        "CABECERA\nSUBTÍTULO\nContenido único de la página 1",
        "CABECERA\nSUBTÍTULO\nContenido único de la página 2",
        "CABECERA\nSUBTÍTULO\nContenido único de la página 3",
        "CABECERA\nSUBTÍTULO\nContenido único de la página 4",
        "CABECERA\nSUBTÍTULO\nContenido único de la página 5",
    ]

    # Act
    resultado = detect_header_line_count(pages_text)

    # Assert
    assert resultado == 2


def test_detect_short_pages():
    # Arrange
    pages_text = [
        "CABECERA\nSUBTÍTULO\nContenido único de la página 1",
        " ",
        "CABECERA\nSUBTÍTULO\nContenido único de la página 3",
        "CABECERA\nSUBTÍTULO\nContenido único de la página 4",
        "CABECERA\nSUBTÍTULO\nContenido único de la página 5",
    ]

    # Act
    resultado = detect_header_line_count(pages_text)

    # Assert
    assert resultado == 2


def test_detect_header_line_count_no_repeated_lines():
    # Arrange
    pages_text = [
        "CABECERA\nSUBTÍTULO\nContenido único de la página 1",
        "CABECERA DIFERENTE\nSUBTÍTULO DIFERENTE\nContenido único de la página 2",
        "CABECERA 3\nSUBTÍTULO 3\nContenido único de la página 3",
        "CABECERA DIFERENTE 4\nSUBTÍTULO DIFERENTE 4\nContenido único de la página 4",
        "CABECERA 5\nSUBTÍTULO 5\nContenido único de la página 5",
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
        "CABECERA\nSUBTÍTULO\nContenido único de la página 3",
        "CABECERA\nSUBTÍTULO\nContenido único de la página 4",
        "CABECERA\nSUBTÍTULO\nContenido único de la página 5",
    ]

    # Act
    resultado = detect_header_line_count(pages_text)

    # Assert
    assert resultado == 2