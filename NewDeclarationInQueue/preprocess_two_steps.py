from ast import Tuple
import json
import os

from azure.storage.queue import (
        QueueService,
        QueueMessageFormat
)

import azure.functions as func
from NewDeclarationInQueue.preprocess.api_constants import ApiConstants
from NewDeclarationInQueue.preprocess.document_location import DocumentLocation
from NewDeclarationInQueue.preprocess.ocr_constants import EnvConstants, OcrConstants
from NewDeclarationInQueue.processfiles.ocr_worker import OcrWorker

from NewDeclarationInQueue.processfiles.process_messages import ProcessMessages

class PreProcessTwoSteps:
    
    def __init__(self):
        pass
    
      
    
    def save_in_output_queue(self, input_msg: dict, msg: dict):
        input_msg[ApiConstants.PROCESS_REQUEST_NODE_OUTPUT] = msg
        
        connect_str = os.getenv(EnvConstants.ENV_CONNECTION_STRING)
        queue_service = QueueService(connection_string=connect_str)
        output_queue = 'outputqueueprocess'
        queue_service.put_message(output_queue, json.dumps(input_msg))


    def process_document(self, doc: DocumentLocation, cnt: OcrConstants, ocr_formular: dict, messages_result: ProcessMessages) -> dict:
        #create the worker and send it the parameters for processing
        ocr = OcrWorker(doc)
        #process the document and obtain processing messages
        messages_result = ocr.process(cnt, ocr_formular, messages_result)
        
        #return the processing messages as JSON
        return messages_result.get_json()
    
    def get_constats(self) -> OcrConstants:
        cnt = OcrConstants()
        cnt.STORAGE_TYPE_AZURE = os.getenv(EnvConstants.ENV_STORAGE_AZURE)
        cnt.STORAGE_AZURE_BASE = os.getenv(EnvConstants.ENV_STORAGE_BASE)
        cnt.SAS_URL = os.getenv(EnvConstants.ENV_SASURL)
        cnt.AZURE_CONNECTION_STRING = os.getenv(EnvConstants.ENV_CONNECTION_STRING)
        cnt.AZURE_SHARE_NAME = os.getenv(EnvConstants.ENV_SHARE_NAME)
        cnt.COMPUTER_VISION_SUBSCRIPTION_KEY = os.getenv(EnvConstants.ENV_CV_SUBSCRIPTION_KEY)
        cnt.COMPUTER_VISION_ENDPOINT = os.getenv(EnvConstants.ENV_CV_ENDPOINT)
        cnt.COMPUTER_VISION_FORM_SUBSCRIPTION_KEY = os.getenv(EnvConstants.ENV_CV_FORM_SUBSCRIPTION_KEY)
        cnt.COMPUTER_VISION_FORM_ENDPOINT = os.getenv(EnvConstants.ENV_CV_FORM_ENDPOINT)
        cnt.FORMULAR_CONFIG_AZURE_BASE = os.getenv(EnvConstants.ENV_FRM_CONFIG_AZURE_BASE)
        cnt.FORMULAR_CONFIG_PATH = os.getenv(EnvConstants.ENV_FRM_CONFIG_PATH)
        cnt.FORMULAR_CONFIG_AZURE_BASE = os.getenv(EnvConstants.ENV_FRM_CONFIG_AZURE_BASE)
        cnt.FORMULAR_CONFIG_PATH = os.getenv(EnvConstants.ENV_FRM_CONFIG_PATH)
        return cnt
    
        
    def get_file_info(self, data: dict, messages_result: ProcessMessages) -> Tuple(DocumentLocation, ProcessMessages):   
        
        
        #check if parameters for processing info exists in request
        loc = (data[ApiConstants.PROCESS_REQUEST_NODE_FILE_DESCRIPTION] 
                if ApiConstants.PROCESS_REQUEST_NODE_FILE_DESCRIPTION in data.keys() else None)

        #if it does not exist, return 404 error
        if None == loc:
            messages_result.add_error('process document parameter validation', 'Missing required parameters: file_description')
        
        #check all required parameters, if one does not exist a 404 error will be thrown
        messages_result = self.check_parameter(loc.keys(), ApiConstants.PROCESS_REQUEST_NODE_ATTRIBUTE_TYPE, messages_result)
        messages_result = self.check_parameter(loc.keys(), ApiConstants.PROCESS_REQUEST_NODE_ATTRIBUTE_STORAGE, messages_result)
        messages_result = self.check_parameter(loc.keys(), ApiConstants.PROCESS_REQUEST_NODE_ATTRIBUTE_PATH, messages_result)
        messages_result = self.check_parameter(loc.keys(), ApiConstants.PROCESS_REQUEST_NODE_ATTRIBUTE_FILENAME, messages_result)
        messages_result = self.check_parameter(loc.keys(), ApiConstants.PROCESS_REQUEST_NODE_ATTRIBUTE_OUTPATH, messages_result)
        # messages_result = self.check_parameter(loc.keys(), ApiConstants.PROCESS_REQUEST_NODE_ATTRIBUTE_PAGE_IMAGE_FILENAME, messages_result)
        messages_result = self.check_parameter(loc.keys(), ApiConstants.PROCESS_REQUEST_NODE_ATTRIBUTE_OCR_TABLE_JSON_FILENAME, messages_result)
        messages_result = self.check_parameter(loc.keys(), ApiConstants.PROCESS_REQUEST_NODE_ATTRIBUTE_OCR_CUSTOM_JSON_FILENAME, messages_result)
        messages_result = self.check_parameter(loc.keys(), ApiConstants.PROCESS_REQUEST_NODE_ATTRIBUTE_FORMULAR_TYPE, messages_result)
        
        
        #based on the received parameters, create the class containing all parameters required for processing
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
        
        return doc, messages_result
    
    
    def check_parameter(self, keys, param, messages: ProcessMessages) -> ProcessMessages:
        """Checks if a key exists. Used to check if the call to OCR a document has all parameters

        Args:
            keys ([list of strings]): [list of parameters sent to the service]
            param ([string]): [parameter name to check if exists]

        Raises:
            Http404: [the required parameter does not exist in the list of parameters received by the service]
        """
        if param not in keys:
            messages.add_error('process document parameter validation', 'Missing required parameters: file_description -> ' + 
                            param)
            
        return messages
            