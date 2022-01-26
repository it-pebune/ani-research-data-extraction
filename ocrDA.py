
import urllib.request, json 
from NewDeclarationInQueue.preprocess.document_location import DocumentLocation
from NewDeclarationInQueue.preprocess.models import DocumentType, InterestFormular, WelthFormular
from NewDeclarationInQueue.preprocess.ocr_constants import OcrConstants
from NewDeclarationInQueue.preprocess.api_constants import ApiConstants
from NewDeclarationInQueue.processfiles.customprocess.search_text_line_parameter import SearchTextLineParameter
from NewDeclarationInQueue.processfiles.customprocess.table_config_detail import TableConfigDetail
from NewDeclarationInQueue.processfiles.customprocess.text_with_special_ch import TextWithSpecialCharacters
from NewDeclarationInQueue.processfiles.ocr_worker import OcrWorker
from NewDeclarationInQueue.processfiles.process_messages import ProcessMessages


def get_env() -> OcrConstants:
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

def get_input() -> DocumentLocation:
    node = []
    with open(r"input.json") as json_data:
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

def get_summary_config_from_node(node) -> SearchTextLineParameter:
    line_starts = get_text_from_node(node['line_starts_with'])
    line_contains = get_contains_text_from_node(node['line_contains'])
    ball = node['all_words']
    
    return SearchTextLineParameter(line_starts, line_contains, ball)

def get_table_level(node) -> list:
    if node is None or len(node) == 0:
        return []
    
    vresult = []
    for level in node:
        vresult.append(get_summary_config_from_node(level))
       
    return vresult 

def get_table_config(node) -> TableConfigDetail:
    table_node = node['table']
    
    tab = TableConfigDetail()
    
    
    tab.upper = get_summary_config_from_node(table_node['upper'])
    tab.lower = get_summary_config_from_node(table_node['lower'])
    tab.header = get_summary_config_from_node(table_node['text_in_header'])    
    tab.first_level = get_table_level(node['first_level'])
    tab.second_level = get_table_level(node['second_level'])
    
    return tab
    

def get_formular_config() -> dict:
    node = []
    with open(r"config_davere_01.json") as json_data:
        node = json.load(json_data)
        json_data.close()
        
    config_tables = {}
    for table in node['tables']:
        config_tables[table['table']['name']] = get_table_config(table)
        
        
    return config_tables
        
        
        

ocr_cnt = get_env()
doc_loc = get_input()
process_messages = ProcessMessages('OCR Process')

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

config_tables = get_formular_config()

process_messages = ocr.process_custom_file(ocr_cnt, config_tables, ocr_dict, process_messages)
#process the document and obtain processing messages
#messages_result = ocr.process(cnt, messages_result)

#return the processing messages as JSON
#return messages_result.get_json()


s_message = process_messages.get_json()
print(json.dumps(s_message))