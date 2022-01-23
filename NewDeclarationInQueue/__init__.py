import logging
import json
import os, uuid

from azure.storage.queue import (
        QueueService,
        QueueMessageFormat
)


import azure.functions as func

from NewDeclarationInQueue.preprocess.api_constants import ApiConstants
from NewDeclarationInQueue.preprocess.document_location import DocumentLocation
from NewDeclarationInQueue.preprocess.ocr_constants import OcrConstants
from NewDeclarationInQueue.processfiles.ocr_worker import OcrWorker
from NewDeclarationInQueue.processfiles.process_messages import ProcessMessages


def main(msg: func.QueueMessage) -> None:
    ocr_constants = OcrConstants()
    ocr_constants.STORAGE_TYPE_AZURE = os.getenv("STORAGE_TYPE_AZURE")
    ocr_constants.STORAGE_AZURE_BASE = os.getenv("STORAGE_AZURE_BASE")
    ocr_constants.SAS_URL = os.getenv("SAS_URL")
    ocr_constants.AZURE_CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
    ocr_constants.AZURE_SHARE_NAME = os.getenv("AZURE_SHARE_NAME")
    ocr_constants.COMPUTER_VISION_SUBSCRIPTION_KEY = os.getenv("COMPUTER_VISION_SUBSCRIPTION_KEY")
    ocr_constants.COMPUTER_VISION_ENDPOINT = os.getenv("COMPUTER_VISION_ENDPOINT")
    ocr_constants.COMPUTER_VISION_FORM_SUBSCRIPTION_KEY = os.getenv("COMPUTER_VISION_FORM_SUBSCRIPTION_KEY")
    ocr_constants.COMPUTER_VISION_FORM_ENDPOINT = os.getenv("COMPUTER_VISION_FORM_ENDPOINT")
    
    connect_str = os.getenv("AZURE_CONNECTION_STRING")
    queue_service = QueueService(connection_string=connect_str)
    output_queue = 'outputqueueprocess'


    logging.info('Python queue trigger function processed a queue item: %s',
                 msg.get_body().decode('utf-8'))
    
    message_str = msg.get_body().decode('utf-8')
    data = json.loads(message_str)
    
    process_messages = ProcessMessages('OCR Process')
    process_messages_json = process_document(data, ocr_constants, process_messages)
    
    queue_service.put_message(output_queue, json.dumps(process_messages_json))
    
    


def process_document(data: dict, cnt: OcrConstants, messages_result: ProcessMessages) -> dict:
    #check if parameters for processing info exists in request
    loc = (data[ApiConstants.PROCESS_REQUEST_NODE_FILE_DESCRIPTION] 
            if ApiConstants.PROCESS_REQUEST_NODE_FILE_DESCRIPTION in data.keys() else None)

    #if it does not exist, return 404 error
    if None == loc:
        messages_result.add_error('process document parameter validation', 'Missing required parameters: file_description')
    
    #check all required parameters, if one does not exist a 404 error will be thrown
    messages_result = check_parameter(loc.keys(), ApiConstants.PROCESS_REQUEST_NODE_ATTRIBUTE_TYPE, messages_result)
    messages_result = check_parameter(loc.keys(), ApiConstants.PROCESS_REQUEST_NODE_ATTRIBUTE_STORAGE, messages_result)
    messages_result = check_parameter(loc.keys(), ApiConstants.PROCESS_REQUEST_NODE_ATTRIBUTE_PATH, messages_result)
    messages_result = check_parameter(loc.keys(), ApiConstants.PROCESS_REQUEST_NODE_ATTRIBUTE_FILENAME, messages_result)
    messages_result = check_parameter(loc.keys(), ApiConstants.PROCESS_REQUEST_NODE_ATTRIBUTE_OUTPATH, messages_result)
    messages_result = check_parameter(loc.keys(), ApiConstants.PROCESS_REQUEST_NODE_ATTRIBUTE_PAGE_IMAGE_FILENAME, messages_result)
    messages_result = check_parameter(loc.keys(), ApiConstants.PROCESS_REQUEST_NODE_ATTRIBUTE_OCR_TABLE_JSON_FILENAME, messages_result)
    messages_result = check_parameter(loc.keys(), ApiConstants.PROCESS_REQUEST_NODE_ATTRIBUTE_OCR_CUSTOM_JSON_FILENAME, messages_result)
    messages_result = check_parameter(loc.keys(), ApiConstants.PROCESS_REQUEST_NODE_ATTRIBUTE_FORMULAR_TYPE, messages_result)
    
    
    #based on the received parameters, create the class containing all parameters required for processing
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
    
    #create the worker and send it the parameters for processing
    ocr = OcrWorker(doc)
    #process the document and obtain processing messages
    messages_result = ocr.process(cnt, messages_result)
    
    #return the processing messages as JSON
    return messages_result.get_json()

def check_parameter(keys, param, messages: ProcessMessages) -> ProcessMessages:
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