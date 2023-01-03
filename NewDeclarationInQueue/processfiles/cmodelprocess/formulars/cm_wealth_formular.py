

from typing import Tuple
from NewDeclarationInQueue.processfiles.cmodelprocess.formulars.cm_formular_base import CmFormularBase
from NewDeclarationInQueue.processfiles.process_messages import ProcessMessages
from NewDeclarationInQueue.processfiles.table_builders.art_builder import ArtBuilder
from NewDeclarationInQueue.processfiles.table_builders.building_table_builder import BuildingTableBuilder
from NewDeclarationInQueue.processfiles.table_builders.debt_builder import DebtBuilder
from NewDeclarationInQueue.processfiles.table_builders.finance_builder import FinanceBuilder
from NewDeclarationInQueue.processfiles.table_builders.gift_builder import GiftBuilder
from NewDeclarationInQueue.processfiles.table_builders.income_builder import IncomeBuilder
from NewDeclarationInQueue.processfiles.table_builders.investment_builder import InvestmentBuilder
from NewDeclarationInQueue.processfiles.table_builders.mobile_builder import MobileBuilder
from NewDeclarationInQueue.processfiles.table_builders.parcel_table_builder import ParcelTableBuilder
from NewDeclarationInQueue.processfiles.table_builders.transport_builder import TransportBuilder
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
    
    def identify_all_data(self, config_formular: dict, raw_tables: list, message: ProcessMessages) -> Tuple[dict, dict, ProcessMessages]:
        message = self.identify_id_data(message)
        json, raw_json, message = self.identify_tables(config_formular, raw_tables, message)
        return json, raw_json, message
    
    def identify_id_data(self, message: ProcessMessages) -> ProcessMessages:
        fields = self.cmformular["fields"]
        
        self.name = self.get_field_value(fields[self.FIELD_NAME])
        self.job_title = self.get_field_value(fields[self.FIELD_JOB_TITLE])
        self.institution = self.get_field_value(fields[self.FIELD_INSTITUTION])
        self.address = self.get_field_value(fields[self.FIELD_ADDRESS])
        self.doc_date = self.get_field_value(fields[self.FIELD_DOCUMENT_DATE])
        
        return message
        
        
    def identify_tables(self, config_formular: dict, raw_tables: list, message: ProcessMessages) -> Tuple[dict, dict, ProcessMessages]:
        fields = self.cmformular["fields"]
        
        json = {}
        raw_json = {}
        try:
            message, json, raw_json = self.identify_one_table(self.TABLE_PARCELS, 'parcels', lambda x: ParcelTableBuilder(OcrExtractor()), \
                config_formular, fields, raw_tables, json, raw_json, message)
            message, json, raw_json = self.identify_one_table(self.TABLE_BUILDINGS, 'buildings', lambda x: BuildingTableBuilder(OcrExtractor()), \
                config_formular, fields, raw_tables, json, raw_json, message)
            message, json, raw_json = self.identify_one_table(self.TABLE_TRANSPORT, 'transport', lambda x: TransportBuilder(OcrExtractor()), \
                config_formular, fields, raw_tables, json, raw_json, message)
            message, json, raw_json = self.identify_one_table(self.TABLE_ART, 'art', lambda x: ArtBuilder(OcrExtractor()), \
                config_formular, fields, raw_tables, json, raw_json, message)
            message, json, raw_json = self.identify_one_table(self.TABLE_MOBILE, 'mobile', lambda x: MobileBuilder(OcrExtractor()), \
                config_formular, fields, raw_tables, json, raw_json, message)
            message, json, raw_json = self.identify_one_table(self.TABLE_FINANCE, 'finance', lambda x: FinanceBuilder(OcrExtractor()), \
                config_formular, fields, raw_tables, json, raw_json, message)
            message, json, raw_json = self.identify_one_table(self.TABLE_INVESTMENT, 'investment', lambda x: InvestmentBuilder(OcrExtractor()), \
                config_formular, fields, raw_tables, json, raw_json, message)
            message, json, raw_json = self.identify_one_table(self.TABLE_DEBT, 'debt', lambda x: DebtBuilder(OcrExtractor()), \
                config_formular, fields, raw_tables, json, raw_json, message)
            message, json, raw_json = self.identify_one_table(self.TABLE_GIFT, 'gift', lambda x: GiftBuilder(OcrExtractor()), \
                config_formular, fields, raw_tables, json, raw_json, message)
            message, json, raw_json = self.identify_one_table(self.TABLE_INCOME, 'income', lambda x: IncomeBuilder(OcrExtractor()), \
                config_formular, fields, raw_tables, json, raw_json, message)
            
            json = self.add_finance_extra_to_json(json, fields)
            raw_json = self.add_finance_extra_to_json(raw_json, fields)
        except Exception as exex:
            print("---------Found excception-------", exex)
            message.add_exception('Error reading the model', exex)
                  
        return json, raw_json, message
    
    def add_finance_extra_to_json(self, root: dict, fields) -> dict:
        root['finance_extra_info'] = self.get_field_value(fields[self.FIELD_OTHER_INCOME])
        root[self.FIELD_NAME] = self.name
        root[self.FIELD_JOB_TITLE] = self.job_title
        root[self.FIELD_INSTITUTION] = self.institution
        root[self.FIELD_ADDRESS] = self.address
        root[self.FIELD_DOCUMENT_DATE] = self.doc_date
        
        return root
        
        
    
    