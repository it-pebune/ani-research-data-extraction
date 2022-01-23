from typing import Tuple
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes, VisualFeatureTypes
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

from msrest.authentication import CognitiveServicesCredentials

import time
from NewDeclarationInQueue.preprocess.ocr_constants import OcrConstants

from NewDeclarationInQueue.processfiles.formatter.ocr_json_formatter import OcrJsonFormatter
from NewDeclarationInQueue.processfiles.process_messages import ProcessMessages
from NewDeclarationInQueue.processfiles.storage.storage_support import StorageSupport

class OcrService:
    pages: list
    computervision_client: ComputerVisionClient = None
    ocrJsonFormatter: OcrJsonFormatter = OcrJsonFormatter()
    
    def __init__(self, pages):
        self.pages = pages
    
    def create_computer_vision_object(self, cnt: OcrConstants):
        self.computervision_client = ComputerVisionClient(cnt.COMPUTER_VISION_ENDPOINT, 
                                    CognitiveServicesCredentials(cnt.COMPUTER_VISION_SUBSCRIPTION_KEY))
        
    def get_computer_vision(self, cnt: OcrConstants) -> ComputerVisionClient:
        if not self.computervision_client:
            self.create_computer_vision_object(cnt)
        
        return self.computervision_client
    
    def ocr_one_page(self, pageurl, message: ProcessMessages) -> Tuple[ProcessMessages, any]:
        try:
            # Call API with image and raw response (allows you to get the operation location)
            read_response = self.computervision_client.read(pageurl, raw=True)
            
            # Get the operation location (URL with ID as last appendage)
            read_operation_location = read_response.headers["Operation-Location"]
            # Take the ID off and use to get results
            operation_id = read_operation_location.split("/")[-1]
            
            # Call the "GET" API and wait for the retrieval of the results
            while True:
                read_result = self.computervision_client.get_read_result(operation_id)
                if read_result.status.lower () not in ['notstarted', 'running']:
                    break
                
                time.sleep(10)
                
            if read_result.status == OperationStatusCodes.succeeded:
                return message, read_result.analyze_result.read_results
            else:
                message.add_error('ocr one page service call', 'no result returned by the service')
                return message, None
        except Exception as exex:
            message.add_exception('ocr_one_page function call', exex)
    
        
    def ocr_service_call(self, storage: StorageSupport, output_path: str, ocr_json_filename: str, cnt: OcrConstants, message: ProcessMessages) -> ProcessMessages:
        client = self.get_computer_vision(cnt)
        if client is None:
           message.add_error('Computer vision creation', 'Computer vision service could not be created') 
           return message
       
        vpages = storage.get_pages_urls()
        
        dict_ocr = {'ocr_page_response': []}
        ncount = 1
        for pageurl in vpages:
            message, analyze_result = self.ocr_one_page(pageurl, message)
            if message.has_errors():
                return message
            
            if analyze_result:
                message, dict_ocr = \
                    self.ocrJsonFormatter.get_json_from_ocr_page_response(dict_ocr, ncount, analyze_result, message)
                
            ncount += 1
                
        message.add_message('ocr service call', 'service called for all pages', '')
        message = storage.save_ocr_json(output_path, ocr_json_filename, dict_ocr, message)
        
        return message
                  
    
