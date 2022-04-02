
from typing import Tuple

import os
from azure.core.exceptions import ResourceNotFoundError
from azure.ai.formrecognizer import FormRecognizerClient, CustomFormModel, FormTrainingClient, RecognizedForm
from azure.core.credentials import AzureKeyCredential
import json
from NewDeclarationInQueue.formular_converter import FormularConverter

from NewDeclarationInQueue.preprocess.ocr_constants import OcrConstants
from NewDeclarationInQueue.processfiles.cmodelprocess.model_definition import ModelDefinition
from NewDeclarationInQueue.processfiles.process_messages import ProcessMessages
from NewDeclarationInQueue.processfiles.storage.storage_support import StorageSupport

class OcrCustomModelService:
    
    #form_training_client: FormTrainingClient = None
    #custom_model_info: CustomFormModel = None
    form_recognizer_model_client: FormRecognizerClient = None
    
    def create_form_recognizer_model_client(self, cnt: OcrConstants):
        #self.form_training_client = FormTrainingClient(endpoint=cnt.COMPUTER_VISION_FORM_ENDPOINT, 
        #                                          credential=AzureKeyCredential(cnt.COMPUTER_VISION_FORM_SUBSCRIPTION_KEY))
        #self.custom_model_info = self.form_training_client.get_custom_model(model_id=cnt.FORMULAR_COMPOSITE_MODEL_GUID)
        
        self.form_recognizer_model_client = FormRecognizerClient(endpoint=cnt.COMPUTER_VISION_FORM_ENDPOINT, 
                                                  credential=AzureKeyCredential(cnt.COMPUTER_VISION_FORM_SUBSCRIPTION_KEY))

        
        
    def get_custom_model(self, cnt: OcrConstants) -> FormRecognizerClient:
        if not self.form_recognizer_model_client:
            self.create_form_recognizer_model_client(cnt)
        
        return self.form_recognizer_model_client
        
        
    def get_service_result(self, storage: StorageSupport, output_path: str, initial_filename: str, 
                cnt: OcrConstants, message: ProcessMessages) -> Tuple[list, ProcessMessages]:
        
        custom_test_action_result = None
        # get the form recognizer model service and if it not exist, return error
        client = self.get_custom_model(cnt)
        if client is None:
           message.add_error('Form recognizer model creation', 'Form recognizer model service could not be created') 
           return message
        
        # call the service and wait for results
        input_file_url = storage.get_secure_file(output_path, initial_filename, cnt)
        
        #check file exists
        message, out_path = storage.check_file_exists(
            output_path + (initial_filename if output_path.endswith('/') else '/' + initial_filename) , cnt, message)
        if message.has_errors():
            return message
        
        try:
            custom_test_action = client.begin_recognize_custom_forms_from_url(
                                            model_id=cnt.FORMULAR_COMPOSITE_MODEL_GUID, 
                                            form_url=input_file_url)
            custom_test_action.result
            custom_test_action.status()

            custom_test_action_result = custom_test_action.result()
        except Exception as exex:
            message.add_exception('Custom Model OCR call failed: ' + input_file_url, exex)
            
        return custom_test_action_result, message
    
    def save_model_result(self, model_result: list, storage: StorageSupport, output_path: str, 
            ocr_json_table_filename: str, cnt: OcrConstants, message: ProcessMessages) -> Tuple[dict, ProcessMessages]:
        
        form_json = {}
        
        for model in model_result:
            node_json = model.to_dict()
            form_json[model.form_type] = node_json
            
        message.add_message('form recognizer service call', 'service called for the initial pdf file', '')
        message = storage.save_ocr_json(output_path, ocr_json_table_filename, form_json, cnt, message)
        
        return form_json, message
    
    def generate_and_save_custom_json(self, storage: StorageSupport, output_path: str, recognized_forms: list,
                                #config_tables: dict, 
                                ocr_json_custom_filename: str,
                                #declaration_type: int, formular_type: int, ocr_formular: dict, 
                                cnt: OcrConstants, doc_location: dict, message: ProcessMessages) -> ProcessMessages:
        
               
        # generate custom json
        extractor = ModelDefinition()
        form, document_type, model_name, message = extractor.get_formular_from_model(recognized_forms, message)
        if message.has_errors():
            return message
        
        message.set_model_name(model_name)
        message.set_declaration_type(document_type)
        
        formular_converter = FormularConverter()
        ocr_formular = formular_converter.get_formular_model_info(cnt, doc_location, document_type)
        
        json_dict, message = form.identify_all_data(ocr_formular, message)
        if message.has_errors():
            return message
        else:
            message.add_message('ocr worker process', 'Custon json generation -> '
                               + doc_location.ocr_table_json_filename, ' - ' + doc_location.ocr_table_json_filename)
        
        message = storage.save_ocr_json(output_path, ocr_json_custom_filename, json_dict, cnt, message)
            
        message.add_message('ocr worker process', 'custom json file saved -> '
                               + doc_location.ocr_table_json_filename, ' - ' + doc_location.ocr_custom_json_filename)
        
        return message
        
        
    def custom_model_service_call(self, storage: StorageSupport, output_path: str, initial_filename: str, 
                                      ocr_json_table_filename: str, 
                                      cnt: OcrConstants, message: ProcessMessages) -> Tuple[list, ProcessMessages]:
        
        
        custom_test_action_result, message = self.get_service_result(storage, output_path, initial_filename, cnt, message)
        if message.has_errors():
            return {}, message
        
        saved_json, message = self.save_model_result(custom_test_action_result, storage, output_path,
                        ocr_json_table_filename, cnt, message)
       
        
        
        #TODO: maybe get this out in another call
        #message = self.generate_and_save_custom_json(storage, output_path, dict_ocr, 
        #                                             ocr_formular, ocr_json_custom_filename,
        #                                             declaration_type, formular_type, ocr_formular, cnt, message)
        
        
        return saved_json, message
    