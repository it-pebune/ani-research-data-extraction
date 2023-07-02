import json

import azure.functions as func

from NewDeclarationInQueue.formular_converter import FormularConverter
from NewDeclarationInQueue.preprocess.document_location import DocumentLocation
from NewDeclarationInQueue.preprocess.ocr_constants import OcrConstants
from NewDeclarationInQueue.preprocess_two_steps import PreProcessTwoSteps
from NewDeclarationInQueue.processfiles.ocr_worker import OcrWorker
from NewDeclarationInQueue.processfiles.process_messages import ProcessMessages


def main(msg: func.QueueMessage) -> None:
    message_str = msg.get_body().decode('utf-8')
    data = json.loads(message_str)
        
    two_steps = PreProcessTwoSteps()
    process_messages = ProcessMessages('OCR Process', msg.id)
    
    ocr_constants = two_steps.get_constats()
    ocr_file, process_messages = two_steps.get_file_info(data, process_messages)
    
    # TODO: this has to be done later, based on what the composite model returns
    # TODO: including when it returns a document it does not recognize
    #formular_converter = FormularConverter()
    #ocr_formular = formular_converter.get_formular_info(ocr_constants, ocr_file)
    
    #TODO: point of divergence, here call a method that uses the composite model
    #process_messages = two_steps.process_document(ocr_file, ocr_constants, ocr_formular, process_messages)
    process_messages = two_steps.process_document_with_custom_model(ocr_file, ocr_constants, process_messages)
    
    two_steps.save_in_output_queue(data, process_messages)
  
    

