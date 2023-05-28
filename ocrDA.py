from enum import Enum
import json

from NewDeclarationInQueue.formular_converter import FormularConverter
from NewDeclarationInQueue.preprocess_one_step import PreprocessOneStep
from NewDeclarationInQueue.preprocess_two_steps import PreProcessTwoSteps
from NewDeclarationInQueue.processfiles.declaration_type_helpers import shouldUseOcr
from NewDeclarationInQueue.processfiles.process_messages import ProcessMessages
from pdf_model.InterestDeclaration import InterestDeclarationParser
from pdf_model.configs.configs import InterestDeclarationConfig, WealthDeclarationConfig
from pdf_model.wealth_declaration_parser import WealthDeclarationParser


def process_only_second_steps(input_file_path: str):
    second_step = PreprocessOneStep()
    #second_step.process_step_two(input_file_path)
    second_step.process_custom_model_step_two(input_file_path)


def get_input(input_file: str):
    node = []
    with open(input_file) as json_data:
        node = json.load(json_data)
        json_data.close()
    return node


def process_two_steps(sfile: str):
    str_msg_id = 'abc'
    dict_input = get_input(sfile)

    two_steps = PreProcessTwoSteps()
    process_messages = ProcessMessages('OCR Process', str_msg_id)

    one_step = PreprocessOneStep()
    ocr_constants = one_step.get_env()
    ocr_file, process_messages = two_steps.get_file_info(dict_input, process_messages)

    formular_converter = FormularConverter()
    ocr_formular = formular_converter.get_formular_info(ocr_constants, ocr_file)

    #process_messages_json = two_steps.process_document(ocr_file, ocr_constants, ocr_formular, process_messages)
    process_messages = two_steps.process_document_with_custom_model(ocr_file, ocr_constants, process_messages)

    #two_steps.save_in_output_queue(process_messages_json)


class FormularType(Enum):
    WEALTH_DECLARATION = 1
    INTEREST_DECLARATION = 2


if __name__ == '__main__':

    formularType, pdf_file_path = FormularType.WEALTH_DECLARATION, 'pdf_model/ciuca_1_da.pdf'
    # formularType, pdf_file_path = FormularType.INTEREST_DECLARATION, 'pdf_model/ciolos_di.pdf'
    formularType, pdf_file_path = FormularType.INTEREST_DECLARATION, 'pdf_model/ciolacu_di_2022.pdf'

    if shouldUseOcr(pdf_file_path):
        pass
    else:
        if formularType is FormularType.WEALTH_DECLARATION:
            print("Processing wealth declaration")
            WealthDeclarationParser(WealthDeclarationConfig).parse(pdf_file_path)
        elif formularType is FormularType.INTEREST_DECLARATION:
            print("Processing interest declaration")
            InterestDeclarationParser(InterestDeclarationConfig).parse(pdf_file_path)

# def test_pdf_model():

# test_pdf_model()
#
#process_only_second_steps(r"test_url_di.json")
# process_two_steps(r"test_url.json")
