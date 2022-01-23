

from typing import Tuple

from NewDeclarationInQueue.processfiles.customprocess.formulars.dinterese import DInterese
from NewDeclarationInQueue.processfiles.customprocess.tableobjects.member_quality import MemberQuality
from NewDeclarationInQueue.processfiles.process_messages import ProcessMessages


class Dinterese01(DInterese):
    """
        Class for a specific formular for Wealth Declaration
    """
    
    def __init__(self, no_of_pages: int):
        self.no_of_pages = no_of_pages
    
    def get_company_associate(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        tables, message, end_page_no = self.find_table_in_document_between_lines(data['ocr_form_response'], \
                    n_page, self.no_of_pages, \
                    '1. Asociat sau actionar la societàti comerciale,', None, False, \
                    '2. Calitatea de membru în organele de conducere', None, False, \
                    'Unitatea', None, False, message)
        
        message, result = self.extract_table_info_to_json(tables, lambda x: MemberQuality(), message)
        if message.has_errors() or result is not None:
            json['parcels'] = result
            
        return json, message, (end_page_no if end_page_no > 0 else n_page)
    
    def get_management_commercial(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        pass
    
    def get_management_association(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        lines, end_page_no = self.find_lines_in_document_between_lines(data['ocr_form_response'], \
                            n_page, self.no_of_pages, \
                            '1. Asociat sau actionar la societati comerciale', None, False, \
                            '2. Calitatea de membru in organe de conducere', None, False)
        
        result = self.extract_lines_info_to_json(lines)
        if result is not None and len(result) > 0:
            json['finance_extra_info'] = result
            
        return json, message, (end_page_no if end_page_no > 0 else n_page)
    
    def get_management_party(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        pass
    
    def get_contracts(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        pass
    
    #def get_parcels(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages,  int]:
    #    """
    #        Get the info from the table of the specific object
    #    Args:
    #        data (dict): table info from the Form Recognizer service
    #        n_page (int): page number where the parcel table is
    #        json (dict): output JSON info
    #        message (ProcessMessages): processing message collector

    #    Returns:
    #        Tuple[dict, ProcessMessages,  int]: response JSON for the specific object, processing messages 
    #                                                and the page number where the table ends
    #    """
    #    tables, message, end_page_no = self.find_table_in_document_between_lines(data['ocr_form_response'], \
    #                n_page, self.no_of_pages, \
    #                '1. Terenuri', None, False, \
    #                '*Categoriile indicate sunt:', ['agricol', 'forestier'], True, \
    #                'Adresa sau zona', None, False, message)
        
    #    message, result = self.extract_table_info_to_json(tables, lambda x: Parcel(), message)
    #    if message.has_errors() or result is not None:
    #        json['parcels'] = result
            
    #    return json, message, (end_page_no if end_page_no > 0 else n_page)
    
    
        