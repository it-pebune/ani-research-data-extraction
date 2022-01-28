from ast import Tuple
import logging
import json
import os, uuid

from azure.storage.queue import (
        QueueService,
        QueueMessageFormat
)


import azure.functions as func
import urllib

from NewDeclarationInQueue.preprocess.api_constants import ApiConstants
from NewDeclarationInQueue.preprocess.document_location import DocumentLocation
from NewDeclarationInQueue.preprocess.models import DocumentType, InterestFormular, WelthFormular
from NewDeclarationInQueue.preprocess.ocr_constants import OcrConstants
from NewDeclarationInQueue.processfiles.customprocess.search_text_line_parameter import SearchTextLineParameter
from NewDeclarationInQueue.processfiles.customprocess.table_config_detail import TableConfigDetail
from NewDeclarationInQueue.processfiles.customprocess.text_with_special_ch import TextWithSpecialCharacters
from NewDeclarationInQueue.processfiles.ocr_worker import OcrWorker
from NewDeclarationInQueue.processfiles.process_messages import ProcessMessages


def main(msg: func.QueueMessage) -> None:
    process_messages = ProcessMessages('OCR Process', msg.id)
    
    ocr_constants = get_constats()
    ocr_file, process_messages = get_file_info(msg, process_messages)
    
    ocr_formular = get_formular_info(ocr_constants, ocr_file)
    
    process_messages_json = process_document(ocr_file, ocr_constants, ocr_formular, process_messages)
    
    save_in_output_queue(process_messages_json)
    
    
def get_formular_info(cnt: OcrConstants, doc: DocumentLocation) -> dict:
    s_formular_config = cnt.FORMULAR_CONFIG_AZURE_BASE + ('' if cnt.FORMULAR_CONFIG_AZURE_BASE.endswith('/') else '/') + \
    cnt.FORMULAR_CONFIG_PATH + ('' if cnt.FORMULAR_CONFIG_PATH.endswith('/') else '/') 
    
    if doc.type == DocumentType.DOC_WEALTH:
        if doc.formular_type == WelthFormular.DOCUMENT01:
            s_formular_config += 'config_davere_01.json'
    else:
        if doc.formular_type == DocumentType.DOC_INTERESTS:
            if doc.formular_type == InterestFormular.DOCUMENT01:
                s_formular_config += 'config_dinterese_01.json'

    s_formular_config += '?' + cnt.SAS_URL

    node = []
    with urllib.request.urlopen(s_formular_config) as json_data:
        node = json.load(json_data)
        json_data.close()
        
    config_tables = {}
    for table in node['tables']:
        config_tables[table['table']['name']] = get_table_config(table)
        
        
    return config_tables


def get_table_config(node) -> TableConfigDetail:
    table_node = node['table']
    
    tab = TableConfigDetail()
    
    
    tab.upper = get_summary_config_from_node(table_node['upper'])
    tab.lower = get_summary_config_from_node(table_node['lower'])
    tab.header = get_summary_config_from_node(table_node['text_in_header'])    
    tab.first_level = get_table_level(node['first_level'])
    tab.second_level = get_table_level(node['second_level'])
    
    return tab

def get_summary_config_from_node(node) -> SearchTextLineParameter:
    line_starts = get_text_from_node(node['line_starts_with'])
    line_contains = get_contains_text_from_node(node['line_contains'])
    ball = node['all_words']
    
    return SearchTextLineParameter(line_starts, line_contains, ball)

def get_text_from_node(node) -> TextWithSpecialCharacters:
    main_string = node['text_no_diacritics']
    special_characters_string = node['text']
    
    return TextWithSpecialCharacters(main_string, None, False) \
                if special_characters_string is None or len(special_characters_string) == 0 \
                else TextWithSpecialCharacters(main_string, special_characters_string, True)
                
def get_contains_text_from_node(node) -> list:
    if node is None or len(node) == 0:
        return []
    
    vcontains = []
    for node_txt in node:
        vcontains.append(get_text_from_node(node_txt))
    return vcontains

def get_table_level(node) -> list:
    if node is None or len(node) == 0:
        return []
    
    vresult = []
    for level in node:
        vresult.append(get_summary_config_from_node(level))
       
    return vresult 
    
def save_in_output_queue(msg: dict):
    connect_str = os.getenv("AZURE_CONNECTION_STRING")
    queue_service = QueueService(connection_string=connect_str)
    output_queue = 'outputqueueprocess'
    queue_service.put_message(output_queue, json.dumps(msg))
        
def get_file_info(msg: func.QueueMessage, messages_result: ProcessMessages) -> Tuple(DocumentLocation, ProcessMessages):   
    message_str = msg.get_body().decode('utf-8')
    data = json.loads(message_str)
    
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
    
    return doc, messages_result
        
def get_constats() -> OcrConstants:
    cnt = OcrConstants()
    cnt.STORAGE_TYPE_AZURE = os.getenv("STORAGE_TYPE_AZURE")
    cnt.STORAGE_AZURE_BASE = os.getenv("STORAGE_AZURE_BASE")
    cnt.SAS_URL = os.getenv("SAS_URL")
    cnt.AZURE_CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
    cnt.AZURE_SHARE_NAME = os.getenv("AZURE_SHARE_NAME")
    cnt.COMPUTER_VISION_SUBSCRIPTION_KEY = os.getenv("COMPUTER_VISION_SUBSCRIPTION_KEY")
    cnt.COMPUTER_VISION_ENDPOINT = os.getenv("COMPUTER_VISION_ENDPOINT")
    cnt.COMPUTER_VISION_FORM_SUBSCRIPTION_KEY = os.getenv("COMPUTER_VISION_FORM_SUBSCRIPTION_KEY")
    cnt.COMPUTER_VISION_FORM_ENDPOINT = os.getenv("COMPUTER_VISION_FORM_ENDPOINT")
    cnt.FORMULAR_CONFIG_AZURE_BASE = os.getenv("FORMULAR_CONFIG_AZURE_BASE")
    cnt.FORMULAR_CONFIG_PATH = os.getenv("FORMULAR_CONFIG_PATH")
    cnt.FORMULAR_CONFIG_AZURE_BASE = os.getenv("FORMULAR_CONFIG_AZURE_BASE")
    cnt.FORMULAR_CONFIG_PATH = os.getenv("FORMULAR_CONFIG_PATH")
    return cnt

def process_document(doc: DocumentLocation, cnt: OcrConstants, ocr_formular: dict, messages_result: ProcessMessages) -> dict:
    #create the worker and send it the parameters for processing
    ocr = OcrWorker(doc)
    #process the document and obtain processing messages
    messages_result = ocr.process(cnt, ocr_formular, messages_result)
    
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