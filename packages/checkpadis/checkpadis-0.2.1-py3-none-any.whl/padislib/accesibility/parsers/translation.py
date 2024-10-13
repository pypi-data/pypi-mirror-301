from enum import Enum


class Translation(Enum):
    LABEL_ELEMENT = "Ensures every form element has a label"
    FIX_ANY = "Fix any of the following:"
    CONTRAST_THRESHOLD = (
        "Ensures the contrast between foreground and background colors meets "
        "WCAG 2 AA contrast ratio thresholds"
    )
    INSUFFICIENT_CONTRAST = "Element has insufficient color contrast of"
    ARIA_LABEL_MISSING = "aria-label attribute does not exist or is empty"
    ARIA_LABELLEDBY_MISSING = (
        "aria-labelledby attribute does not exist, references elements that "
        "do not exist or references elements that are empty"
    )
    NO_IMPLICIT_LABEL = (
        "Form element does not have an implicit (wrapped) <label>"
    )
    NO_EXPLICIT_LABEL = "Form element does not have an explicit <label>"
    NO_TITLE_ATTRIBUTE = (
        "Element has no title attribute or the title attribute is empty"
    )
    EXPECTED_CONTRAST_RATIO = "Expected contrast ratio of"

    @classmethod
    def get_translation(cls, text):
        translations = {
            cls.LABEL_ELEMENT.value: (
                "Asegúrese de que cada elemento de formulario tenga una "
                "etiqueta"
            ),
            cls.FIX_ANY.value: "Corrija cualquiera de los siguientes:",
            cls.CONTRAST_THRESHOLD.value: (
                "Asegura que el contraste entre los colores de primer plano y "
                "fondo cumple con los umbrales de la relación de contraste "
                "WCAG 2 AA"
            ),
            cls.INSUFFICIENT_CONTRAST.value: (
                "El elemento tiene un contraste de color insuficiente de"
            ),
            cls.ARIA_LABEL_MISSING.value: (
                "El atributo aria-label no existe o está vacío"
            ),
            cls.ARIA_LABELLEDBY_MISSING.value: (
                "El atributo aria-labelledby no existe, hace referencia a "
                "elementos que no existen o vacíos"
            ),
            cls.NO_IMPLICIT_LABEL.value: (
                "El elemento de formulario no tiene una etiqueta <label> "
                "implícita (envolvente)"
            ),
            cls.NO_EXPLICIT_LABEL.value: (
                "El elemento de formulario no tiene una etiqueta <label> "
                "explícita"
            ),
            cls.NO_TITLE_ATTRIBUTE.value: (
                "El elemento no tiene un atributo title o el atributo title "
                "está vacío"
            ),
            cls.EXPECTED_CONTRAST_RATIO.value: (
                "Relación de contraste esperada"
            ),
        }
        return translations.get(text, text)
