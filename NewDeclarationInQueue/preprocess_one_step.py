import urllib.request, json

import json
from NewDeclarationInQueue.formular_converter import FormularConverter
from NewDeclarationInQueue.preprocess.api_constants import ApiConstants
from NewDeclarationInQueue.preprocess.document_location import DocumentLocation
from NewDeclarationInQueue.preprocess.models import DocumentType, InterestFormular, WelthFormular
from NewDeclarationInQueue.preprocess.ocr_constants import OcrConstants
from NewDeclarationInQueue.processfiles.ocr_worker import OcrWorker
from NewDeclarationInQueue.processfiles.process_messages import ProcessMessages


class PreprocessOneStep:
    def __init__(self):
        pass
    
    def get_env(self) -> OcrConstants:
        with open(r"local.settings.json") as json_data:
            d = json.load(json_data)
            json_data.close()
            node = d["Values"]
            
            ocr_constants = OcrConstants()
            ocr_constants.STORAGE_TYPE_AZURE = node["STORAGE_TYPE_AZURE"]
            ocr_constants.STORAGE_AZURE_BASE = node["STORAGE_AZURE_BASE"]
            ocr_constants.SAS_URL = node["SAS_URL"]
            ocr_constants.AZURE_CONNECTION_STRING = node["AZURE_CONNECTION_STRING"]
            ocr_constants.AZURE_SHARE_NAME = node["AZURE_SHARE_NAME"]
            ocr_constants.COMPUTER_VISION_SUBSCRIPTION_KEY = node["COMPUTER_VISION_SUBSCRIPTION_KEY"]
            ocr_constants.COMPUTER_VISION_ENDPOINT = node["COMPUTER_VISION_ENDPOINT"]
            ocr_constants.COMPUTER_VISION_FORM_SUBSCRIPTION_KEY = node["COMPUTER_VISION_FORM_SUBSCRIPTION_KEY"]
            ocr_constants.COMPUTER_VISION_FORM_ENDPOINT = node["COMPUTER_VISION_FORM_ENDPOINT"]
            ocr_constants.FORMULAR_CONFIG_AZURE_BASE = node["FORMULAR_CONFIG_AZURE_BASE"]
            ocr_constants.FORMULAR_CONFIG_PATH = node["FORMULAR_CONFIG_PATH"]
            
        return ocr_constants

    def get_input(self, s_input_file: str) -> DocumentLocation:
        node = []
        with open(s_input_file) as json_data:
            node = json.load(json_data)
            json_data.close()
            
        loc = (node[ApiConstants.PROCESS_REQUEST_NODE_FILE_DESCRIPTION] 
                if ApiConstants.PROCESS_REQUEST_NODE_FILE_DESCRIPTION in node.keys() else None)
        doc = DocumentLocation(loc[ApiConstants.PROCESS_REQUEST_NODE_ATTRIBUTE_TYPE], 
                                loc[ApiConstants.PROCESS_REQUEST_NODE_ATTRIBUTE_STORAGE], 
                                loc[ApiConstants.PROCESS_REQUEST_NODE_ATTRIBUTE_PATH], 
                                loc[ApiConstants.PROCESS_REQUEST_NODE_ATTRIBUTE_FILENAME],
                                loc[ApiConstants.PROCESS_REQUEST_NODE_ATTRIBUTE_OUTPATH],
                                loc[ApiConstants.PROCESS_REQUEST_NODE_ATTRIBUTE_PAGE_IMAGE_FILENAME],
                                loc[ApiConstants.PROCESS_REQUEST_NODE_ATTRIBUTE_OCR_JSON_FILENAME] 
                                    if ApiConstants.PROCESS_REQUEST_NODE_ATTRIBUTE_OCR_JSON_FILENAME in loc.keys() else None,
                                loc[ApiConstants.PROCESS_REQUEST_NODE_ATTRIBUTE_OCR_TABLE_JSON_FILENAME],
                                loc[ApiConstants.PROCESS_REQUEST_NODE_ATTRIBUTE_OCR_CUSTOM_JSON_FILENAME],
                                loc[ApiConstants.PROCESS_REQUEST_NODE_ATTRIBUTE_FORMULAR_TYPE])
        
        return doc
        
            
    def process_step_two(self, input_file_name: str):
        ocr_cnt = self.get_env()
        doc_loc = self.get_input(input_file_name)
        process_messages = ProcessMessages('OCR Process', 'dummy_id')

        #create the worker and send it the parameters for processing
        ocr = OcrWorker(doc_loc)
        url = ocr_cnt.STORAGE_AZURE_BASE + ('' if ocr_cnt.STORAGE_AZURE_BASE.endswith('/') else '/') + \
            doc_loc.out_path.replace(' ', '%20') + ('' if doc_loc.out_path.endswith('/') else '/') + doc_loc.ocr_table_json_filename + '.json' + \
            '?' + ocr_cnt.SAS_URL
            
        ocr_dict = []

        with urllib.request.urlopen(url) as url:
            ocr_dict = json.loads(url.read().decode())

        s_formular_config = ocr_cnt.FORMULAR_CONFIG_AZURE_BASE + ('' if ocr_cnt.FORMULAR_CONFIG_AZURE_BASE.endswith('/') else '/') + \
            ocr_cnt.FORMULAR_CONFIG_PATH + ('' if ocr_cnt.FORMULAR_CONFIG_PATH.endswith('/') else '/') 
            
        if doc_loc.type == DocumentType.DOC_WEALTH:
            if doc_loc.formular_type == WelthFormular.DOCUMENT01:
                s_formular_config += 'config_davere_01.json'
        else:
            if doc_loc.formular_type == DocumentType.DOC_INTERESTS:
                if doc_loc.formular_type == InterestFormular.DOCUMENT01:
                    s_formular_config += 'config_dinterese_01.json'

        s_formular_config += '?' + ocr_cnt.SAS_URL

        formular_converter = FormularConverter()
        config_tables = formular_converter.get_formular_info(ocr_cnt, doc_loc)

        process_messages = ocr.process_custom_file(ocr_cnt, config_tables, ocr_dict, process_messages)
        #process the document and obtain processing messages
        #messages_result = ocr.process(cnt, messages_result)

        #return the processing messages as JSON
        #return messages_result.get_json()


        s_message = process_messages.get_json()
        print(json.dumps(s_message))
        