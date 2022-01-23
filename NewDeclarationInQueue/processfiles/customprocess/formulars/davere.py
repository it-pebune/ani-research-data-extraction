

from typing import Tuple

from NewDeclarationInQueue.processfiles.customprocess.formulars.formular_base import FormularBase
from NewDeclarationInQueue.processfiles.process_messages import ProcessMessages


class DAvere(FormularBase):
    """ 
        Base class for all the Wealth Declaration formulars. 
    """
    
    def __init__(self, no_of_pages: int):
        self.no_of_pages = no_of_pages
    
    def process_all_tables(self, data: dict, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages]:
        """ This is the base class for all Welth formulars and it contains the order of tables in the formular
                and a function for each table to process. Only this function is implemented in this class,
                all the others are overwritten in the different formulars, to allow for different texts.

        Args:
            data (dict): input JSON obtained from the Form Recognition service
            json (dict): output JSON (simplified)
            message (ProcessMessages): collect the process message

        Returns:
            Tuple[dict, ProcessMessages]: the output JSON and the messages generated from the processing workflow
        """
        
        n_count = 0
        json, message, n_count = self.get_parcels(data, n_count, json, message)
        json, message, n_count = self.get_buildings(data, n_count, json, message)
        json, message, n_count = self.get_transport(data, n_count, json, message)
        json, message, n_count = self.get_art(data, n_count, json, message)
        json, message, n_count = self.get_mobile(data, n_count, json, message)
        json, message, n_count = self.get_finances(data, n_count, json, message)
        json, message, n_count = self.get_investments(data, n_count, json, message)
        json, message, n_count = self.get_extra_finance_info(data, n_count, json, message)
        json, message, n_count = self.get_debt(data, n_count, json, message)
        json, message, n_count = self.get_gift(data, n_count, json, message)
        json, message, n_count = self.get_income(data, n_count, json, message)
        
        return json, message
    
    def get_parcels(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages,  int]:
        pass
    
    def get_buildings(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        pass
    
    def get_transport(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        pass
    
    def get_art(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        pass
    
    def get_mobile(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        pass
    
    def get_finances(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        pass
    
    def get_investments(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        pass
    
    def get_extra_finance_info(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        pass
    
    def get_debt(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        pass
    
    def get_gift(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        pass
    
    def get_income(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        pass
        