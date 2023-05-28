from pdf_model.InterestDeclaration import InterestDeclarationParser
from pdf_model.configs.configs import InterestDeclarationConfig, WealthDeclarationConfig
from pdf_model.wealth_declaration_parser import WealthDeclarationParser
from tests.fixtures.pdf_models_output.ciuca_1_da_output import CIUCA_DA_1_PDF_OUTPUT
from tests.fixtures.pdf_models_output.ciuca_1_di_output import CIUCA_DI_1_PDF_OUTPUT


def test_formatted_pdf_basic_case():
    file_path = "tests/fixtures/pdf_models/ciuca_1_da.pdf"

    response = WealthDeclarationParser(WealthDeclarationConfig).parse(file_path)
    assert response == CIUCA_DA_1_PDF_OUTPUT


def test_formatted_pdf_interest_declaration_basic_case():
    file_path = "tests/fixtures/pdf_models/ciolacu_di_2022.pdf"

    response = InterestDeclarationParser(InterestDeclarationConfig).parse(file_path)
    assert response == CIUCA_DI_1_PDF_OUTPUT
