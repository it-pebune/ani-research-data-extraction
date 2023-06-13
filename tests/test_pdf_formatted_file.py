from pdf_model.InterestDeclaration import InterestDeclarationParser
from pdf_model.configs.configs import InterestDeclarationConfig, WealthDeclarationConfig
from pdf_model.wealth_declaration_parser import WealthDeclarationParser
from tests.fixtures.pdf_models_output.ciuca_1_da_09_06_2022 import CIUCA_DA_1_PDF_OUTPUT
from tests.fixtures.pdf_models_output.ciolacu_1_di_26_05_2022 import CIOLACU_DI_1_PDF_OUTPUT


def test_formatted_pdf_basic_case():
    file_path = "tests/fixtures/pdf_models/ciuca_da_09_06_2022.pdf"

    response = WealthDeclarationParser(WealthDeclarationConfig).parse(file_path)
    assert response == CIUCA_DA_1_PDF_OUTPUT


def test_formatted_pdf_interest_declaration_basic_case():
    file_path = "tests/fixtures/pdf_models/ciolacu_di_26_05_2022.pdf"

    response = InterestDeclarationParser(InterestDeclarationConfig).parse(file_path)
    assert response == CIOLACU_DI_1_PDF_OUTPUT


def test_wealth_declaration_multiple_examples():
    tests = [
        {
            "input_path": "tests/fixtures/pdf_models/barna_bogdan_da_19_05_2023.pdf",
            "expected_output": {},
            "description": "TODO"
        },
        # "tests/fixtures/pdf_models/barna_bogdan_da_19_05_2022.pdf",
        # [],
        # [],
        # [],
    ]

    for testCase in tests:
        print(testCase)
        result = WealthDeclarationParser(WealthDeclarationConfig).parse(testCase["input_path"])
        # import ipdb
        # ipdb.set_trace()
