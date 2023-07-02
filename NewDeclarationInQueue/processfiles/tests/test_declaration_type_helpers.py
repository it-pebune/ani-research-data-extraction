from NewDeclarationInQueue.processfiles.declaration_type_helpers import shouldUseOcr


def test_pdf_file_with_images():
    file_path = "tests/fixtures/pdf_models/ciuca_1_da.pdf"

    response = shouldUseOcr(file_path)
    assert response == False


def test_pdf_file_with_text():
    file_path = "tests/fixtures/pdf_models/ciolos_2020_da.pdf"

    response = shouldUseOcr(file_path)
    assert response == True
