
from typing import Tuple
from NewDeclarationInQueue.preprocess.models import DocumentType, InterestFormular, WelthFormular
from NewDeclarationInQueue.processfiles.customprocess.formulars.davere_01 import Davere01
from NewDeclarationInQueue.processfiles.customprocess.formulars.dinterese_01 import Dinterese01

from NewDeclarationInQueue.processfiles.process_messages import ProcessMessages


class TableExtractor:
    """
        Class to process each table obtained from the Azure Cognitive Services and
        generate a simplified structure
    """
    
    config_table: dict
    
    def __init__(self, cfg):
        self.config_table = cfg
    
    
    def extract_from_doc_to_json(self, declaration_type: str, formular_type: str, data: dict, message: ProcessMessages) -> Tuple[ProcessMessages, dict]:
        """ Extract simplified JSON structure from the JSON file received from the Form Recognizer service.
                This is the entry point for the processing that transforms the JSON received from the service
                to a simplified JSON

        Args:
            declaration_type (str): Declaration type: DAvr or DInt
            formular_type (str): Type of the formular, each declaration type can have document versions
                                    with different structures. They will be called Davere01...
            data (dict): JSON data from the Form Recognizer service (all data)
            message (ProcessMessages): collects process messages

        Returns:
            Tuple[ProcessMessages, dict]: process messages and the simplified JSON structure
        """
        
        json = {}
        
        # verify entry data 
        if data is None or 'ocr_form_response' not in data.keys():
            return json
        
        # get the correct formular based on declaration type and formular type
        formular = None
        if declaration_type == DocumentType.DOC_WEALTH:
            if formular_type == WelthFormular.DOCUMENT01:
                formular = Davere01(len(data['ocr_form_response']))
        else:
            if declaration_type == DocumentType.DOC_INTERESTS:
                if formular_type == InterestFormular.DOCUMENT01:
                    formular = Dinterese01(len(data['ocr_form_response']))
           
        # if no formular found, return     
        if formular is None:
            message.add_error('Formular not found', declaration_type + ' - ' + formular_type)
            return message, None
        else:
            message.add_message('Formular found', declaration_type + ' - ' + formular_type, '')
        
        # get each table in the formular and process it
        json, message = formular.process_all_tables(self.config_table, data, json, message)
        
        return message, json


