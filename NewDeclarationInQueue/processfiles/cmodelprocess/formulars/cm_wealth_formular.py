

from typing import Tuple
from NewDeclarationInQueue.processfiles.cmodelprocess.formulars.cm_formular_base import CmFormularBase
from NewDeclarationInQueue.processfiles.process_messages import ProcessMessages
from NewDeclarationInQueue.processfiles.tableobjects.art import Art
from NewDeclarationInQueue.processfiles.tableobjects.building import Building
from NewDeclarationInQueue.processfiles.tableobjects.debt import Debt
from NewDeclarationInQueue.processfiles.tableobjects.finance import Finance
from NewDeclarationInQueue.processfiles.tableobjects.gift import Gift
from NewDeclarationInQueue.processfiles.tableobjects.income import Income
from NewDeclarationInQueue.processfiles.tableobjects.investment import Investment
from NewDeclarationInQueue.processfiles.tableobjects.mobile import Mobile
from NewDeclarationInQueue.processfiles.tableobjects.parcel import Parcel
from NewDeclarationInQueue.processfiles.tableobjects.transport import Transport


class CmWealthFormular(CmFormularBase):
    FIELD_NAME = "NumePrenume"
    FIELD_JOB_TITLE = "Functie"
    FIELD_INSTITUTION = "Institutie"
    FIELD_ADDRESS = "Domiciliu"
    FIELD_DOCUMENT_DATE = "Date of filling"
    
    TABLE_PARCELS = "Parcels"
    TABLE_BUILDINGS = "Buildings"
    TABLE_TRANSPORT = "Transport"
    TABLE_ART = "Art"
    TABLE_MOBILE = "Mobile items"
    TABLE_FINANCE = "Finance"
    TABLE_INVESTMENT = "Investement"
    TABLE_DEBT = "Debt"
    TABLE_GIFT = "Gift"
    TABLE_INCOME = "Income"
    
    FIELD_OTHER_INCOME = "Other net incomes"

    
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
            message, json = self.identify_one_table(self.TABLE_PARCELS, 'parcels', lambda x: Parcel(), \
                config_formular, fields, json, message)
            message, json = self.identify_one_table(self.TABLE_BUILDINGS, 'buildings', lambda x: Building(), \
                config_formular, fields, json, message)
            message, json = self.identify_one_table(self.TABLE_TRANSPORT, 'transport', lambda x: Transport(), \
                config_formular, fields, json, message)
            message, json = self.identify_one_table(self.TABLE_ART, 'art', lambda x: Art(), \
                config_formular, fields, json, message)
            message, json = self.identify_one_table(self.TABLE_MOBILE, 'mobile', lambda x: Mobile(), \
                config_formular, fields, json, message)
            message, json = self.identify_one_table(self.TABLE_FINANCE, 'finance', lambda x: Finance(), \
                config_formular, fields, json, message)
            message, json = self.identify_one_table(self.TABLE_INVESTMENT, 'investment', lambda x: Investment(), \
                config_formular, fields, json, message)
            message, json = self.identify_one_table(self.TABLE_DEBT, 'debt', lambda x: Debt(), \
                config_formular, fields, json, message)
            message, json = self.identify_one_table(self.TABLE_GIFT, 'gift', lambda x: Gift(), \
                config_formular, fields, json, message)
            message, json = self.identify_one_table(self.TABLE_INCOME, 'income', lambda x: Income(), \
                config_formular, fields, json, message)
            
            json['finance_extra_info'] = self.get_field_value(fields[self.FIELD_OTHER_INCOME])
            json[self.FIELD_NAME] = self.name
            json[self.FIELD_JOB_TITLE] = self.job_title
            json[self.FIELD_INSTITUTION] = self.institution
            json[self.FIELD_ADDRESS] = self.address
            json[self.FIELD_DOCUMENT_DATE] = self.doc_date
        except Exception as exex:
            message.add_exception('Error reading the model', exex)
                  
        return json, message
        
        
    
    