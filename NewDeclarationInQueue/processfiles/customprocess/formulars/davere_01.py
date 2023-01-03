

from typing import Tuple
from NewDeclarationInQueue.processfiles.customprocess.formulars.davere import DAvere
from NewDeclarationInQueue.processfiles.customprocess.search_text_line_parameter import SearchTextLineParameter
from NewDeclarationInQueue.processfiles.customprocess.table_config_detail import TableConfigDetail
from NewDeclarationInQueue.processfiles.tableobjects.art import Art
from NewDeclarationInQueue.processfiles.tableobjects.building import Building
from NewDeclarationInQueue.processfiles.tableobjects.debt import Debt
from NewDeclarationInQueue.processfiles.tableobjects.finance import Finance
from NewDeclarationInQueue.processfiles.tableobjects.gift import Gift
from NewDeclarationInQueue.processfiles.tableobjects.income import Income
from NewDeclarationInQueue.processfiles.tableobjects.investment import Investment
from NewDeclarationInQueue.processfiles.tableobjects.mobile import Mobile
from NewDeclarationInQueue.processfiles.tableobjects.parcel import Parcel
from NewDeclarationInQueue.processfiles.tableobjects.table_content_extractors.ocr_extractor import OcrExtractor
from NewDeclarationInQueue.processfiles.tableobjects.transport import Transport
#from NewDeclarationInQueue.processfiles.customprocess.text_with_special_ch import TextWithSpecialCharacters

from NewDeclarationInQueue.processfiles.process_messages import ProcessMessages


class Davere01(DAvere):
    """
        Class for a specific formular for Wealth Declaration
    """
    
    def __init__(self, no_of_pages: int):
        self.no_of_pages = no_of_pages
    
    
    def get_parcels(self, config: TableConfigDetail, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages,  int]:
        """
            Get the info from the table of the specific object
        Args:
            data (dict): table info from the Form Recognizer service
            n_page (int): page number where the parcel table is
            json (dict): output JSON info
            message (ProcessMessages): processing message collector

        Returns:
            Tuple[dict, ProcessMessages,  int]: response JSON for the specific object, processing messages 
                                                    and the page number where the table ends
        """
        tables, message, end_page_no = self.find_table_in_document_between_lines(data['ocr_form_response'], \
            n_page, self.no_of_pages, config.upper, config.lower, config.header, message)
        
        message, result = self.extract_table_info_to_json('parcels', tables, lambda x: Parcel(OcrExtractor()), message)
        if message.has_errors() or result is not None:
            json['parcels'] = result
            
        return json, message, (end_page_no if end_page_no > 0 else n_page)
    
    def get_buildings(self, config: TableConfigDetail, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        """
            Get the info from the table of the specific object
        Args:
            data (dict): table info from the Form Recognizer service
            n_page (int): page number where the parcel table is
            json (dict): output JSON info
            message (ProcessMessages): processing message collector

        Returns:
            Tuple[dict, ProcessMessages,  int]: response JSON for the specific object, processing messages 
                                                    and the page number where the table ends
        """
        
        tables, message, end_page_no = self.find_table_in_document_between_lines(data['ocr_form_response'], \
            n_page, self.no_of_pages, config.upper, config.lower, config.header, message)
        message, result = self.extract_table_info_to_json('buildings', tables, lambda x: Building(), message)
        if message.has_errors() or result is not None:
            json['buildings'] = result
            
        return json, message, (end_page_no if end_page_no > 0 else n_page)
    
    def get_transport(self, config: TableConfigDetail, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        tables, message, end_page_no = self.find_table_in_document_between_lines(data['ocr_form_response'], \
            n_page, self.no_of_pages, config.upper, config.lower, config.header, message)
        
        message, result = self.extract_table_info_to_json('transport', tables, lambda x: Transport(), message)
        if message.has_errors() or result is not None:
            json['transport'] = result
            
        return json, message, (end_page_no if end_page_no > 0 else n_page)
    
    
    def get_art(self, config: TableConfigDetail, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        """
            Get the info from the table of the specific object
        Args:
            data (dict): table info from the Form Recognizer service
            n_page (int): page number where the parcel table is
            json (dict): output JSON info
            message (ProcessMessages): processing message collector

        Returns:
            Tuple[dict, ProcessMessages,  int]: response JSON for the specific object, processing messages 
                                                    and the page number where the table ends
        """
        
        tables, message, end_page_no = self.find_table_in_document_between_lines(data['ocr_form_response'], \
            n_page, self.no_of_pages, config.upper, config.lower, config.header, message)
        
        message, result = self.extract_table_info_to_json('art', tables, lambda x: Art(), message)
        if message.has_errors() or result is not None:
            json['art'] = result
            
        return json, message, (end_page_no if end_page_no > 0 else n_page)
    
    def get_mobile(self, config: TableConfigDetail, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        """
            Get the info from the table of the specific object
        Args:
            data (dict): table info from the Form Recognizer service
            n_page (int): page number where the parcel table is
            json (dict): output JSON info
            message (ProcessMessages): processing message collector

        Returns:
            Tuple[dict, ProcessMessages,  int]: response JSON for the specific object, processing messages 
                                                    and the page number where the table ends
        """
        
        tables, message, end_page_no = self.find_table_in_document_between_lines(data['ocr_form_response'], \
            n_page, self.no_of_pages, config.upper, config.lower, config.header, message)
        
        message, result = self.extract_table_info_to_json('mobile', tables, lambda x: Mobile(), message)
        if message.has_errors() or result is not None:
            json['mobile'] = result
            
        return json, message, (end_page_no if end_page_no > 0 else n_page)
    
    def get_finances(self, config: TableConfigDetail, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        """
            Get the info from the table of the specific object
        Args:
            data (dict): table info from the Form Recognizer service
            n_page (int): page number where the parcel table is
            json (dict): output JSON info
            message (ProcessMessages): processing message collector

        Returns:
            Tuple[dict, ProcessMessages,  int]: response JSON for the specific object, processing messages 
                                                    and the page number where the table ends
        """
        
        tables, message, end_page_no = self.find_table_in_document_between_lines(data['ocr_form_response'], \
            n_page, self.no_of_pages, config.upper, config.lower, config.header, message)
        
        message, result = self.extract_table_info_to_json('finances', tables, lambda x: Finance(), message)
        if message.has_errors() or result is not None:
            json['finance'] = result
            
        return json, message, (end_page_no if end_page_no > 0 else n_page)
    
    def get_investments(self, config: TableConfigDetail, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        """
            Get the info from the table of the specific object
        Args:
            data (dict): table info from the Form Recognizer service
            n_page (int): page number where the parcel table is
            json (dict): output JSON info
            message (ProcessMessages): processing message collector

        Returns:
            Tuple[dict, ProcessMessages,  int]: response JSON for the specific object, processing messages 
                                                    and the page number where the table ends
        """
        
        tables, message, end_page_no = self.find_table_in_document_between_lines(data['ocr_form_response'], \
            n_page, self.no_of_pages, config.upper, config.lower, config.header, message)
        
        message, result = self.extract_table_info_to_json('investments', tables, lambda x: Investment(), message)
        if message.has_errors() or result is not None:
            json['investment'] = result
            
        return json, message, (end_page_no if end_page_no > 0 else n_page)
    
    def get_extra_finance_info(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        """
            Get text from a specific section
        Args:
            data (dict): text info from the Form Recognizer service
            n_page (int): page number where the parcel table is
            json (dict): output JSON info
            message (ProcessMessages): processing message collector

        Returns:
            Tuple[dict, ProcessMessages, int]: esponse JSON for the specific object, processing messages 
                                                    and the page number where the table ends
        """
        
        lines, end_page_no = self.find_lines_in_document_between_lines(data['ocr_form_response'], \
                            n_page, self.no_of_pages, \
                            '3. Alte active producatoare de venituri nete,', None, False, \
                            'NOTA:', None, False)
        
        result = self.extract_lines_info_to_json(lines)
        if result is not None and len(result) > 0:
            json['finance_extra_info'] = result
            
        return json, message, (end_page_no if end_page_no > 0 else n_page)
    
    def get_debt(self, config: TableConfigDetail, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        """
            Get the info from the table of the specific object
        Args:
            data (dict): table info from the Form Recognizer service
            n_page (int): page number where the parcel table is
            json (dict): output JSON info
            message (ProcessMessages): processing message collector

        Returns:
            Tuple[dict, ProcessMessages,  int]: response JSON for the specific object, processing messages 
                                                    and the page number where the table ends
        """
        
        tables, message, end_page_no = self.find_table_in_document_between_lines(data['ocr_form_response'],  \
            n_page, self.no_of_pages, config.upper, config.lower, config.header, message)
        
        message, result = self.extract_table_info_to_json('debt', tables, lambda x: Debt(), message)
        if message.has_errors() or result is not None:
            json['debt'] = result
            
        return json, message, (end_page_no if end_page_no > 0 else n_page)
    
    def get_gift(self, config: TableConfigDetail, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        """
            Get the info from the table of the specific object
        Args:
            data (dict): table info from the Form Recognizer service
            n_page (int): page number where the parcel table is
            json (dict): output JSON info
            message (ProcessMessages): processing message collector

        Returns:
            Tuple[dict, ProcessMessages,  int]: response JSON for the specific object, processing messages 
                                                    and the page number where the table ends
        """
        
        tables, message, end_page_no = self.find_table_in_document_between_lines(data['ocr_form_response'],  \
            n_page, self.no_of_pages, config.upper, config.lower, config.header, message)
        
        message, result = self.extract_table_info_one_level_to_json(tables, \
            config.first_level, lambda x: Gift(), message)
        if message.has_errors() or result is not None:
            json['gift'] = result
            
        return json, message, (end_page_no if end_page_no > 0 else n_page)
    
    def get_income(self, config: TableConfigDetail, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        """
            Get the info from the table of the specific object
        Args:
            data (dict): table info from the Form Recognizer service
            n_page (int): page number where the parcel table is
            json (dict): output JSON info
            message (ProcessMessages): processing message collector

        Returns:
            Tuple[dict, ProcessMessages,  int]: response JSON for the specific object, processing messages 
                                                    and the page number where the table ends
        """
        
        tables, message, end_page_no = self.find_table_in_document_between_lines(data['ocr_form_response'],  \
            n_page, self.no_of_pages, config.upper, config.lower, config.header, message)
        
        message, result = self.extract_table_info_two_level_to_json(tables, \
            config.second_level, config.first_level, lambda x: Income(), message)
        
        if message.has_errors() or result is not None:
            json['income'] = result
            
        return json, message, (end_page_no if end_page_no > 0 else n_page)
        