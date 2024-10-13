from enum import Enum


class ReportKeys(Enum):
    IMPACT = "Impact"
    DESCRIPTION = "Description"
    TARGET_ELEMENTS = "Target Elements"
    FAILURE_SUMMARY = "Failure Summary"
    HTML_SNIPPET = "HTML Snippet"
    HELP_URL = "Help URL"
    DEFAULT_IMPACT = "Impacto no especificado"
    DEFAULT_FAILURE_SUMMARY = "Resumen del fallo no proporcionado"
    DEFAULT_HTML_SNIPPET = "HTML snippet not available"
    DEFAULT_HELP_URL = "URL de ayuda no disponible"
