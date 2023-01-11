
import json
from NewDeclarationInQueue.formular_converter import FormularConverter
from NewDeclarationInQueue.preprocess_one_step import PreprocessOneStep
from NewDeclarationInQueue.preprocess_two_steps import PreProcessTwoSteps
from NewDeclarationInQueue.processfiles.customprocess.search_text_line_parameter import SearchTextLineParameter
from NewDeclarationInQueue.processfiles.customprocess.table_config_detail import TableConfigDetail
from NewDeclarationInQueue.processfiles.customprocess.text_with_special_ch import TextWithSpecialCharacters
from NewDeclarationInQueue.processfiles.ocr_worker import OcrWorker
from NewDeclarationInQueue.processfiles.process_messages import ProcessMessages
from pdf_model.configs.configs import WealthDeclarationConfig
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
   
    
def test_pdf_model():
    WealthDeclarationParser(WealthDeclarationConfig).parse("pdf_model/ciuca_1_da.pdf")

    
test_pdf_model()
# 
# process_only_second_steps(r"test_url.json")
# process_two_steps(r"test_url.json")


