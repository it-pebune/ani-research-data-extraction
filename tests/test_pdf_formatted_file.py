from pdf_model.configs.configs import WealthDeclarationConfig
from pdf_model.wealth_declaration_parser import WealthDeclarationParser
from tests.fixtures.pdf_models_output.ciuca_1_da_output import CIUCA_DA_1_PDF_OUTPUT


def test_formatted_pdf_basic_case():
    file_path = "tests/fixtures/pdf_models/ciuca_1_da.pdf"

    response = WealthDeclarationParser(WealthDeclarationConfig).parse(file_path)
    assert response == CIUCA_DA_1_PDF_OUTPUT
