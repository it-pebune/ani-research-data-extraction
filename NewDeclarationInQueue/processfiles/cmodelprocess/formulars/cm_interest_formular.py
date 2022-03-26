

from typing import Tuple
from NewDeclarationInQueue.processfiles.cmodelprocess.formulars.cm_formular_base import CmFormularBase
from NewDeclarationInQueue.processfiles.process_messages import ProcessMessages
from NewDeclarationInQueue.processfiles.tableobjects.associate import Associate
from NewDeclarationInQueue.processfiles.tableobjects.contracts import Contracts
from NewDeclarationInQueue.processfiles.tableobjects.man_commercial import ManCommercial
from NewDeclarationInQueue.processfiles.tableobjects.man_professional import ManProfessional
from NewDeclarationInQueue.processfiles.tableobjects.member_quality import MemberQuality


class CmInterestFormular(CmFormularBase):
    FIELD_NAME = "NumePrenume"
    FIELD_JOB_TITLE = "Functie"
    FIELD_INSTITUTION = "Institutie"
    FIELD_ADDRESS = "Domiciliu"
    FIELD_DOCUMENT_DATE = "Date of document"
    
    TABLE_PARTY = "PartyManagement"
    TABLE_CONTRACTS = "Contracts"
    TABLE_ASSOCIATIONS = "Association"
    TABLE_SHARES = "CompanyShares"
    TABLE_COMPANY = "ManagementCompany"
    
    
    def __init__(self):
        pass
    
    def identify_all_data(self, config_formular: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages]:
        message = self.identify_id_data(message)
        json, message = self.identify_tables(config_formular, message)
        return json, message
    
    def identify_id_data(self, message: ProcessMessages) -> ProcessMessages:
        fields = self.cmformular["fields"]
        
        self.name = self.get_field_value(fields[self.FIELD_NAME])
        self.job_title = self.get_field_value(fields[self.FIELD_JOB_TITLE])
        self.institution = self.get_field_value(fields[self.FIELD_INSTITUTION])
        self.address = self.get_field_value(fields[self.FIELD_ADDRESS])
        self.doc_date = self.get_field_value(fields[self.FIELD_DOCUMENT_DATE])
        
        return message
    
    
    def identify_tables(self, config_formular: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages]:
        fields = self.cmformular["fields"]
        
        json = {}
        try:
            message, json = self.identify_one_table(self.TABLE_PARTY, 'party', lambda x: ManProfessional(), \
                config_formular, fields, json, message)
            message, json = self.identify_one_table(self.TABLE_CONTRACTS, 'contracts', lambda x: Contracts(), \
                config_formular, fields, json, message)
            message, json = self.identify_one_table(self.TABLE_ASSOCIATIONS, 'asociations', lambda x: ManProfessional(), \
                config_formular, fields, json, message)
            message, json = self.identify_one_table(self.TABLE_SHARES, 'company_shares', lambda x: MemberQuality(), \
                config_formular, fields, json, message)
            message, json = self.identify_one_table(self.TABLE_COMPANY, 'man_companies', lambda x: ManCommercial(), \
                config_formular, fields, json, message)
            
            json[self.FIELD_NAME] = self.name
            json[self.FIELD_JOB_TITLE] = self.job_title
            json[self.FIELD_INSTITUTION] = self.institution
            json[self.FIELD_ADDRESS] = self.address
            json[self.FIELD_DOCUMENT_DATE] = self.doc_date
        except Exception as exex:
            message.add_exception('Error reading the model', exex)
                  
        return json, message