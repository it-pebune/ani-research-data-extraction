

from typing import Tuple

from NewDeclarationInQueue.processfiles.customprocess.formulars.formular_base import FormularBase
from NewDeclarationInQueue.processfiles.process_messages import ProcessMessages


class DInterese(FormularBase):
    """ 
        Base class for all the Interest Declaration formulars. 
    """
    
    def __init__(self, no_of_pages: int):
        self.no_of_pages = no_of_pages
    
    def process_all_tables(self, data: dict, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages]:
        """ This is the base class for all Interest formulars and it contains the order of tables in the formular
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
        json, message, n_count = self.get_company_associate(data, n_count, json, message)
        json, message, n_count = self.get_management_commercial(data, n_count, json, message)
        json, message, n_count = self.get_management_association(data, n_count, json, message)
        json, message, n_count = self.get_management_party(data, n_count, json, message)
        json, message, n_count = self.get_contracts(data, n_count, json, message)
        
        
        return json, message
    
    def get_company_associate(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        pass
    
    def get_management_commercial(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        pass
    
    def get_management_association(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        pass
    
    def get_management_party(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        pass
    
    def get_contracts(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        pass
    
    
    
    
        