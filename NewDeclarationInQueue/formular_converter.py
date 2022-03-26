import json
import urllib

from NewDeclarationInQueue.preprocess.document_location import DocumentLocation
from NewDeclarationInQueue.preprocess.models import DocumentType, InterestFormular, WelthFormular
from NewDeclarationInQueue.preprocess.ocr_constants import OcrConstants
from NewDeclarationInQueue.processfiles.customprocess.search_text_line_parameter import SearchTextLineParameter
from NewDeclarationInQueue.processfiles.customprocess.table_config_detail import TableConfigDetail
from NewDeclarationInQueue.processfiles.customprocess.text_with_special_ch import TextWithSpecialCharacters


class FormularConverter:
    
    def __init__(self):
        pass

    def get_formular_info(self, cnt: OcrConstants, doc: DocumentLocation) -> dict:
        s_formular_config = cnt.FORMULAR_CONFIG_AZURE_BASE + ('' if cnt.FORMULAR_CONFIG_AZURE_BASE.endswith('/') else '/') + \
        cnt.FORMULAR_CONFIG_PATH + ('' if cnt.FORMULAR_CONFIG_PATH.endswith('/') else '/') 
        
        if doc.type == DocumentType.DOC_WEALTH:
            if doc.formular_type == WelthFormular.DOCUMENT01:
                s_formular_config += 'config_davere_01.json'
        else:
            if doc.type == DocumentType.DOC_INTERESTS:
                if doc.formular_type == InterestFormular.DOCUMENT01:
                    s_formular_config += 'config_dinterese_01.json'

        s_formular_config += '?' + cnt.SAS_URL

        node = []
        with urllib.request.urlopen(s_formular_config) as json_data:
            node = json.load(json_data)
            json_data.close()
            
        config_tables = {}
        for table in node['tables']:
            config_tables[table['table']['name']] = self.get_table_config(table)
            
            
        return config_tables



    def get_table_config(self, node) -> TableConfigDetail:
        table_node = node['table']
        
        tab = TableConfigDetail()
        
        
        tab.upper = self.get_summary_config_from_node(table_node['upper'])
        tab.lower = self.get_summary_config_from_node(table_node['lower'])
        tab.header = self.get_summary_config_from_node(table_node['text_in_header'])    
        tab.first_level = self.get_table_level(node['first_level'])
        tab.second_level = self.get_table_level(node['second_level'])
        
        return tab



    def get_summary_config_from_node(self, node) -> SearchTextLineParameter:
        if (node is None or len(node) == 0):
            return None
            
        line_starts = self.get_text_from_node(node['line_starts_with'])
        line_contains = self.get_contains_text_from_node(node['line_contains'])
        ball = node['all_words']
        
        return SearchTextLineParameter(line_starts, line_contains, ball)

    def get_text_from_node(self, node) -> TextWithSpecialCharacters:
        if (node is None or len(node) == 0):
            return None
        
        main_string = node['text_no_diacritics']
        special_characters_string = node['text']
        
        return TextWithSpecialCharacters(main_string, None, False) \
                    if special_characters_string is None or len(special_characters_string) == 0 \
                    else TextWithSpecialCharacters(main_string, special_characters_string, True)
                    
    def get_contains_text_from_node(self, node) -> list:
        if node is None or len(node) == 0:
            return []
        
        vcontains = []
        for node_txt in node:
            vcontains.append(self.get_text_from_node(node_txt))
        return vcontains

    def get_table_level(self, node) -> list:
        if node is None or len(node) == 0:
            return []
        
        vresult = []
        for level in node:
            vresult.append(self.get_summary_config_from_node(level))
        
        return vresult 
    
    
    def get_formular_model_info(self, cnt: OcrConstants, doc: DocumentLocation, document_type: int) -> dict:
        s_formular_config = cnt.FORMULAR_CONFIG_AZURE_BASE + ('' if cnt.FORMULAR_CONFIG_AZURE_BASE.endswith('/') else '/') + \
        cnt.FORMULAR_MODEL_CONFIG_PATH + ('' if cnt.FORMULAR_MODEL_CONFIG_PATH.endswith('/') else '/') 
        
        if document_type == DocumentType.DOC_WEALTH:
            s_formular_config += 'config_cmodel_davere.json'
        else:
            if document_type == DocumentType.DOC_INTERESTS:
               s_formular_config += 'config_cmodel_dinterese.json'

        s_formular_config += '?' + cnt.SAS_URL

        node = []
        with urllib.request.urlopen(s_formular_config) as json_data:
            node = json.load(json_data)
            json_data.close()
            
        config_tables = {}
        for table in node['tables']:
            config_tables[table['table_id']] = table
            
            
        return config_tables
