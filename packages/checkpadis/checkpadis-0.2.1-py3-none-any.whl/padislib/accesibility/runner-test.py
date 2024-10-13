from padislib.accessibility.runner import AccessibilityRunner

html_path = "archivo.html"
test_runner = AccessibilityRunner()

try:
    test_runner.verify_form_labels_check()
    test_runner.verify_color_contrast_check("AAA")
    test_runner.verify_image_alt_check(True)

    result_boolean = test_runner.run_checks(html_path, True)
    print("Resultado Booleano:", result_boolean)


except Exception as e:
    print(f"Ocurrió un error durante la ejecución de las pruebas: {e}")
