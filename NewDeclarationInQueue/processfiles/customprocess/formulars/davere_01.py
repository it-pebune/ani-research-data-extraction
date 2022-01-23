

from typing import Tuple
from NewDeclarationInQueue.processfiles.customprocess.formulars.davere import DAvere
from NewDeclarationInQueue.processfiles.customprocess.tableobjects.art import Art
from NewDeclarationInQueue.processfiles.customprocess.tableobjects.building import Building
from NewDeclarationInQueue.processfiles.customprocess.tableobjects.debt import Debt
from NewDeclarationInQueue.processfiles.customprocess.tableobjects.finance import Finance
from NewDeclarationInQueue.processfiles.customprocess.tableobjects.gift import Gift
from NewDeclarationInQueue.processfiles.customprocess.tableobjects.income import Income
from NewDeclarationInQueue.processfiles.customprocess.tableobjects.investment import Investment
from NewDeclarationInQueue.processfiles.customprocess.tableobjects.mobile import Mobile
from NewDeclarationInQueue.processfiles.customprocess.tableobjects.parcel import Parcel
from NewDeclarationInQueue.processfiles.customprocess.tableobjects.transport import Transport

from NewDeclarationInQueue.processfiles.process_messages import ProcessMessages


class Davere01(DAvere):
    """
        Class for a specific formular for Wealth Declaration
    """
    
    def __init__(self, no_of_pages: int):
        self.no_of_pages = no_of_pages
    
    
    def get_parcels(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages,  int]:
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
                    n_page, self.no_of_pages, \
                    '1. Terenuri', None, False, \
                    '*Categoriile indicate sunt:', ['agricol', 'forestier'], True, \
                    'Adresa sau zona', None, False, message)
        
        message, result = self.extract_table_info_to_json(tables, lambda x: Parcel(), message)
        if message.has_errors() or result is not None:
            json['parcels'] = result
            
        return json, message, (end_page_no if end_page_no > 0 else n_page)
    
    def get_buildings(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
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
                            n_page, self.no_of_pages, \
                            '2. Cladiri', None, False, \
                            '*Categoriile indicate sunt:', ['apartament', 'casa de locuit'], True, \
                            'Adresa sau zona', None, False, message)
        message, result = self.extract_table_info_to_json(tables, lambda x: Building(), message)
        if message.has_errors() or result is not None:
            json['buildings'] = result
            
        return json, message, (end_page_no if end_page_no > 0 else n_page)
    
    def get_transport(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        tables, message, end_page_no = self.find_table_in_document_between_lines(data['ocr_form_response'], \
                            n_page, self.no_of_pages, \
                            'II. Bunuri mobile', None, False, \
                            '2. Bunuri sub forma de metale pretioase', None, False, \
                            'Natura', None, False, message)
        
        message, result = self.extract_table_info_to_json(tables, lambda x: Transport(), message)
        if message.has_errors() or result is not None:
            json['transport'] = result
            
        return json, message, (end_page_no if end_page_no > 0 else n_page)
    
    
    def get_art(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
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
                            n_page, self.no_of_pages, \
                            '2. Bunuri sub forma de metale pretioase', None, False, \
                            'III. Bunuri mobile, a caror valoare depaşeste', None, False, \
                            'Descriere sumarã', None, False, message)
        
        message, result = self.extract_table_info_to_json(tables, lambda x: Art(), message)
        if message.has_errors() or result is not None:
            json['art'] = result
            
        return json, message, (end_page_no if end_page_no > 0 else n_page)
    
    def get_mobile(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
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
                            n_page, self.no_of_pages, \
                            'III. Bunuri mobile, a caror valoare depaşeste', None, False, \
                            'IV. Active financiare', None, False, \
                            'Natura bunului', None, False, message)
        
        message, result = self.extract_table_info_to_json(tables, lambda x: Mobile(), message)
        if message.has_errors() or result is not None:
            json['mobile'] = result
            
        return json, message, (end_page_no if end_page_no > 0 else n_page)
    
    def get_finances(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
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
                            n_page, self.no_of_pages, \
                            'IV. Active financiare', None, False, \
                            '*Categoriile indicate sunt', ['cont curent sau echivalente', 'depozit bancar sau echivalente'], True, \
                            'Institutia care administreazã', None, False, message)
        
        message, result = self.extract_table_info_to_json(tables, lambda x: Finance(), message)
        if message.has_errors() or result is not None:
            json['finance'] = result
            
        return json, message, (end_page_no if end_page_no > 0 else n_page)
    
    def get_investments(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
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
                            n_page, self.no_of_pages, \
                            '2. Plasamente, investitii directe si împrumuturi acordate', None, False, \
                            '*Categoriile indicate sunt', ['hârtii de valoare detinute', 'actiuni sau parti sociale'], True, \
                            'Emitent titlu/societatea', None, False, message)
        
        message, result = self.extract_table_info_to_json(tables, lambda x: Investment(), message)
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
    
    def get_debt(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
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
                            n_page, self.no_of_pages, \
                            'V. Datorii', None, False, \
                            'VI. Cadouri, servicii sau avantaje primite gratuit sau', None, False, \
                            'Creditor', None, False, message)
        
        message, result = self.extract_table_info_to_json(tables, lambda x: Debt(), message)
        if message.has_errors() or result is not None:
            json['debt'] = result
            
        return json, message, (end_page_no if end_page_no > 0 else n_page)
    
    def get_gift(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
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
                            n_page, self.no_of_pages, \
                            'VI. Cadouri, servicii sau avantaje primite gratuit sau', None, False, \
                            '*Se excepteazã de la declarare cadourile şi tratatiile uzuale primite', None, False, \
                            'Cine a realizat venitul', None, False, message)
        
        message, result = self.extract_table_info_one_level_to_json(tables, \
                        ['.1. Titular', '.2. Sot/sotie', '.3. Copii'], \
                        lambda x: Gift(), message)
        if message.has_errors() or result is not None:
            json['gift'] = result
            
        return json, message, (end_page_no if end_page_no > 0 else n_page)
    
    def get_income(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
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
                            n_page, self.no_of_pages, \
                            'VII. Venituri ale declarantului si ale membrilor sai de familie', None, False, \
                            'Prezenta declaratie constituie act public si raspund potrivit legii penale', None, False, \
                            'Cine a realizat venitul', None, False, message)
        
        message, result = self.extract_table_info_two_level_to_json(tables, \
                            ['1. Venituri din salarii', '2. Venituri din activitati independente',  \
                            '3. Venituri din cedarea folosintei bunurilor', \
                            '4. Venituri din investitii',  \
                            '5. Venituri din pensii',  \
                            '6. Venituri din activitati agricole',  \
                            '7. Venituri din premii si din jocuri de noroc',  \
                            '8. Venituri din alte surse'], \
                            ['.1. Titular', '.2. Sot/sotie', '.3. Copii'], \
                            lambda x: Income(), message)
        if message.has_errors() or result is not None:
            json['income'] = result
            
        return json, message, (end_page_no if end_page_no > 0 else n_page)
        