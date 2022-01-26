

from typing import Tuple

from NewDeclarationInQueue.processfiles.customprocess.formulars.formular_base import FormularBase
from NewDeclarationInQueue.processfiles.customprocess.table_config_detail import TableConfigDetail
from NewDeclarationInQueue.processfiles.process_messages import ProcessMessages


class DAvere(FormularBase):
    """ 
        Base class for all the Wealth Declaration formulars. 
    """
    
    def __init__(self, no_of_pages: int):
        self.no_of_pages = no_of_pages
    
    def process_all_tables(self, config: dict, data: dict, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages]:
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
        json, message, n_count = self.get_parcels(config['parcels'], data, n_count, json, message)
        json, message, n_count = self.get_buildings(config['buildings'], data, n_count, json, message)
        json, message, n_count = self.get_transport(config['transport'], data, n_count, json, message)
        json, message, n_count = self.get_art(config['art'], data, n_count, json, message)
        json, message, n_count = self.get_mobile(config['mobile'], data, n_count, json, message)
        json, message, n_count = self.get_finances(config['finances'], data, n_count, json, message)
        json, message, n_count = self.get_investments(config['investments'], data, n_count, json, message)
        json, message, n_count = self.get_extra_finance_info(data, n_count, json, message)
        json, message, n_count = self.get_debt(config['debt'], data, n_count, json, message)
        json, message, n_count = self.get_gift(config['gift'], data, n_count, json, message)
        json, message, n_count = self.get_income(config['income'], data, n_count, json, message)
        
        return json, message
    
    #value:'upper: VII. Venituri ale declarantului si ale membrilor sai de familie -  - False - lower: Prezenta declaratie constituie act public si raspund potrivit legii penale -  - False'

    
    def get_parcels(self, config: TableConfigDetail, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages,  int]:
        pass
    
    def get_buildings(self, config: TableConfigDetail, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        pass
    
    def get_transport(self, config: TableConfigDetail, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        pass
    
    def get_art(self, config: TableConfigDetail, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        pass
    
    def get_mobile(self, config: TableConfigDetail, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        pass
    
    def get_finances(self, config: TableConfigDetail, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        pass
    
    def get_investments(self, config: TableConfigDetail, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        pass
    
    def get_extra_finance_info(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        pass
    
    def get_debt(self, config: TableConfigDetail, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        pass
    
    def get_gift(self, config: TableConfigDetail, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        pass
    
    def get_income(self, config: TableConfigDetail, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        pass
        