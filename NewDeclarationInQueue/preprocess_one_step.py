from email import message
import urllib.request, json

import json
from NewDeclarationInQueue.formular_converter import FormularConverter
from NewDeclarationInQueue.preprocess.api_constants import ApiConstants
from NewDeclarationInQueue.preprocess.document_location import DocumentLocation
from NewDeclarationInQueue.preprocess.models import DocumentType, InterestFormular, WelthFormular
from NewDeclarationInQueue.preprocess.ocr_constants import EnvConstants, OcrConstants
from NewDeclarationInQueue.processfiles.cmodelprocess.formulars.raw_table import RawTable
from NewDeclarationInQueue.processfiles.cmodelprocess.model_definition import ModelDefinition
from NewDeclarationInQueue.processfiles.customprocess.table_extractor import TableExtractor
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
            ocr_constants.STORAGE_TYPE_AZURE = node[EnvConstants.ENV_STORAGE_AZURE]
            ocr_constants.STORAGE_AZURE_BASE = node[EnvConstants.ENV_STORAGE_BASE]
            ocr_constants.SAS_URL = node[EnvConstants.ENV_SASURL]
            ocr_constants.AZURE_CONNECTION_STRING = node[EnvConstants.ENV_CONNECTION_STRING]
            ocr_constants.AZURE_SHARE_NAME = node[EnvConstants.ENV_SHARE_NAME]
            ocr_constants.COMPUTER_VISION_SUBSCRIPTION_KEY = node[EnvConstants.ENV_CV_SUBSCRIPTION_KEY]
            ocr_constants.COMPUTER_VISION_ENDPOINT = node[EnvConstants.ENV_CV_ENDPOINT]
            ocr_constants.COMPUTER_VISION_FORM_SUBSCRIPTION_KEY = node[EnvConstants.ENV_CV_FORM_SUBSCRIPTION_KEY]
            ocr_constants.COMPUTER_VISION_FORM_ENDPOINT = node[EnvConstants.ENV_CV_FORM_ENDPOINT]
            ocr_constants.FORMULAR_CONFIG_AZURE_BASE = node[EnvConstants.ENV_FRM_CONFIG_AZURE_BASE]
            ocr_constants.FORMULAR_CONFIG_PATH = node[EnvConstants.ENV_FRM_CONFIG_PATH]
            ocr_constants.FORMULAR_MODEL_CONFIG_PATH = node[EnvConstants.ENV_FRM_MODEL_CONFIG_PATH]
            ocr_constants.FORMULAR_COMPOSITE_MODEL_GUID = node[EnvConstants.FORMULAR_COMPOSITE_MODEL_GUID]
            
        return ocr_constants

    def get_input(self, s_input_file: str) -> DocumentLocation:
        loc = []
        with open(s_input_file) as json_data:
            loc = json.load(json_data)
            json_data.close()
            
        
        doc = DocumentLocation(loc[ApiConstants.PROCESS_REQUEST_NODE_ATTRIBUTE_TYPE], 
                                loc[ApiConstants.PROCESS_REQUEST_NODE_ATTRIBUTE_STORAGE], 
                                loc[ApiConstants.PROCESS_REQUEST_NODE_ATTRIBUTE_PATH], 
                                loc[ApiConstants.PROCESS_REQUEST_NODE_ATTRIBUTE_FILENAME],
                                loc[ApiConstants.PROCESS_REQUEST_NODE_ATTRIBUTE_OUTPATH],
                                loc[ApiConstants.PROCESS_REQUEST_NODE_ATTRIBUTE_PAGE_IMAGE_FILENAME]
                                    if ApiConstants.PROCESS_REQUEST_NODE_ATTRIBUTE_PAGE_IMAGE_FILENAME in loc.keys() else None,
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
            doc_loc.out_path.replace(' ', '%20') + ('' if doc_loc.out_path.endswith('/') else '/') + doc_loc.ocr_table_json_filename + \
            '?' + ocr_cnt.SAS_URL
            
        ocr_dict = []

        with urllib.request.urlopen(url) as url:
            ocr_dict = json.loads(url.read().decode())

        #s_formular_config = ocr_cnt.FORMULAR_CONFIG_AZURE_BASE + ('' if ocr_cnt.FORMULAR_CONFIG_AZURE_BASE.endswith('/') else '/') + \
        #    ocr_cnt.FORMULAR_CONFIG_PATH + ('' if ocr_cnt.FORMULAR_CONFIG_PATH.endswith('/') else '/') 
            
        #if doc_loc.type == DocumentType.DOC_WEALTH:
        #    if doc_loc.formular_type == WelthFormular.DOCUMENT01:
        #        s_formular_config += 'config_davere_01.json'
        #else:
        #    if doc_loc.formular_type == DocumentType.DOC_INTERESTS:
        #        if doc_loc.formular_type == InterestFormular.DOCUMENT01:
        #            s_formular_config += 'config_dinterese_01.json'

        #s_formular_config += '?' + ocr_cnt.SAS_URL

        formular_converter = FormularConverter()
        config_tables = formular_converter.get_formular_info(ocr_cnt, doc_loc)

        process_messages = ocr.process_custom_file(ocr_cnt, config_tables, ocr_dict, process_messages)
        #process the document and obtain processing messages
        #messages_result = ocr.process(cnt, messages_result)

        #return the processing messages as JSON
        #return messages_result.get_json()


        s_message = process_messages.get_json()
        print(json.dumps(s_message))
        
        
    def process_custom_model_step_two(self, input_file_name: str) -> ProcessMessages:
        ocr_cnt = self.get_env()
        doc_loc = self.get_input(input_file_name)
        process_messages = ProcessMessages('OCR Process', 'dummy_id')

        #create the worker and send it the parameters for processing
        ocr = OcrWorker(doc_loc)
        url = ocr_cnt.STORAGE_AZURE_BASE + ('' if ocr_cnt.STORAGE_AZURE_BASE.endswith('/') else '/') + \
            doc_loc.out_path.replace(' ', '%20') + ('' if doc_loc.out_path.endswith('/') else '/') + doc_loc.ocr_table_json_filename + \
            '?' + ocr_cnt.SAS_URL
            
        raw_ocr_dict = []
        with urllib.request.urlopen(url) as url:
            raw_ocr_dict = json.loads(url.read().decode())
            
        extractor = ModelDefinition()
        form, document_type, main_key, process_messages = extractor.get_formular_from_model(raw_ocr_dict, process_messages)
        # print("lalal", process_messages)
        if process_messages.has_errors():
            return process_messages
        
        raw_pages = form.cmformular['pages']
        raw_tables = []
        for raw_page in raw_pages:
            for raw_tab in raw_page['tables']:
                raw_tables.append(RawTable(raw_tab))
        
        formular_converter = FormularConverter()
        ocr_formular = formular_converter.get_formular_model_info(ocr_cnt, doc_loc, document_type)
        # print(ocr_formular)
        
        root_json, raw_json, process_messages = form.identify_all_data(ocr_formular, raw_tables, process_messages)
        #get raw table info as main info, and add model table as extra info
        raw_json['model_info'] = root_json
        
        # print (raw_json)
        print("first", json.dumps(root_json))

        return process_messages

        #s_formular_config = ocr_cnt.FORMULAR_CONFIG_AZURE_BASE + ('' if ocr_cnt.FORMULAR_CONFIG_AZURE_BASE.endswith('/') else '/') + \
        #    ocr_cnt.FORMULAR_CONFIG_PATH + ('' if ocr_cnt.FORMULAR_CONFIG_PATH.endswith('/') else '/') 
            
        #if doc_loc.type == DocumentType.DOC_WEALTH:
        #    if doc_loc.formular_type == WelthFormular.DOCUMENT01:
        #        s_formular_config += 'config_davere_01.json'
        #else:
        #    if doc_loc.formular_type == DocumentType.DOC_INTERESTS:
        #        if doc_loc.formular_type == InterestFormular.DOCUMENT01:
        #            s_formular_config += 'config_dinterese_01.json'

        #s_formular_config += '?' + ocr_cnt.SAS_URL

        #formular_converter = FormularConverter()
        #config_tables = formular_converter.get_formular_info(ocr_cnt, doc_loc)

        #process_messages = ocr.process_custom_file(ocr_cnt, config_tables, ocr_dict, process_messages)
        ##process the document and obtain processing messages
        ##messages_result = ocr.process(cnt, messages_result)

        ##return the processing messages as JSON
        ##return messages_result.get_json()


        #s_message = process_messages.get_json()
        #print(json.dumps(s_message))
        