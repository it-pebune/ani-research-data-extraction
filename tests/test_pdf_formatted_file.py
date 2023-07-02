from pdf_model.InterestDeclaration import InterestDeclarationParser
from pdf_model.configs.configs import InterestDeclarationConfig, WealthDeclarationConfig
from pdf_model.wealth_declaration_parser import WealthDeclarationParser
from tests.fixtures.pdf_models_output.barna_bogdan_da_19_05_2023 import BARNA_BOGDAN_DA_19_05_2023
from tests.fixtures.pdf_models_output.barna_bogdan_di_19_05_2023 import BARNA_BOGDAN_DI_19_05_2023
from tests.fixtures.pdf_models_output.ciuca_1_da_09_06_2022 import CIUCA_DA_1_PDF_OUTPUT
from tests.fixtures.pdf_models_output.ciolacu_1_di_26_05_2022 import CIOLACU_DI_1_PDF_OUTPUT
from tests.fixtures.pdf_models_output.joitoiu_da_09_06_2022 import JOITOIU_DA_09_06_22
from tests.fixtures.pdf_models_output.licsandru_nicusor_daniel_da_30_06_2022 import LICSANDRU_NICUSOR_30_06_22
from tests.fixtures.pdf_models_output.sarconeli_da_02_06_2022 import SARCONELI_DA_2_06_22


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
            "expected_output": BARNA_BOGDAN_DA_19_05_2023,
            "description": "TODO"
        },
        {
            "input_path": "tests/fixtures/pdf_models/joitoiu_da_09_06_2022.pdf",
            "expected_output": JOITOIU_DA_09_06_22,
            "description": "TODO"
        },
        {
            "input_path": "tests/fixtures/pdf_models/licsandru_nicusor_daniel_da_30_06_2022.pdf",
            "expected_output": LICSANDRU_NICUSOR_30_06_22,
            "description": "MERGE LAST TABLE WITH LAST LINE ON PAGE A SUBTABLE"
        },
        {
            "input_path": "tests/fixtures/pdf_models/sarconeli_da_02_06_2022.pdf",
            "expected_output": SARCONELI_DA_2_06_22,
            "description": "MERGE LAST TABLE WITH LAST LINE A SUBCATEGORY"
        },
    ]
    print('\n')
    for testCase in tests:
        print("Testing ---- ", testCase["description"], "----- input:", testCase["input_path"])
        response = WealthDeclarationParser(WealthDeclarationConfig).parse(testCase["input_path"])
        assert response == testCase["expected_output"]


def test_interest_declaration_multiple_examples():
    tests = [
        {
            "input_path": "tests/fixtures/pdf_models/barna_bogdan_di_19_05_2023.pdf",
            "expected_output": BARNA_BOGDAN_DI_19_05_2023,
            "description": "EMPTY INTEREST DECLARATION"
        },
    ]
    print('\n')
    for testCase in tests:
        print("Testing ---- ", testCase["description"], "----- input:", testCase["input_path"])
        response = InterestDeclarationParser(InterestDeclarationConfig).parse(testCase["input_path"])
        assert response == testCase["expected_output"]
