
from typing import Tuple
from NewDeclarationInQueue.processfiles.process_messages import ProcessMessages
from NewDeclarationInQueue.processfiles.tableobjects.declaration_data import DeclarationData


class CmFormularBase:
    FORM_TYPE = "form_type"
    FORM_CONFIDENCE = "form_type_confidence"
    PAGE_RANGE = "page_range"
    
    cmformular: dict
    form_type: str
    form_confidence: float
    page_range: dict
    
    name: str
    job_title: str
    institution: str
    address: str
    doc_date: str
    
    def __init__(self):
        pass
    
    def get_field_value(self, value_data: dict) -> str:
        if not value_data:
            return None
        
        return value_data["value"]
    
    def load_from_model(self, dict):
        self.cmformular = dict
        self.form_type = dict[self.FORM_TYPE]
        self.form_confidence = dict[self.FORM_CONFIDENCE]
        self.page_range = dict[self.PAGE_RANGE]
        
        
    def get_config_and_value_tables(self, table_config_name: str, config_formular: dict, fields: dict, message: ProcessMessages) \
        -> Tuple[dict, list, ProcessMessages]:
            
        config = config_formular[table_config_name]
        if config is None:
            message.add_error('Configuration table not found ' + table_config_name)
            return None, None, message
        
        v_model_tables = config['model_table_names'].split(',')
        v_tables = []
        for table_name in v_model_tables:
            tab = fields[table_name]
            if tab is None:
                message.add_error('Model table not found: ' + table_name)
            else:
                if tab['value'] is not None and len(tab['value']) > 0:
                    v_tables.append(tab)
                    
                    
        return config, v_tables, message
    
    def identify_one_table(self, table_name: str, out_json_node_name: str, perdicate, \
            config_formular: dict, fields: dict, json_root: dict, message: ProcessMessages) -> Tuple[ProcessMessages, dict]:
        
        try:
            config, v_tables, message = self.get_config_and_value_tables(table_name, config_formular, fields, message)
            if message.has_errors():
                return message, json_root      
            
            v_results = []
            for table in v_tables:
                v_results = self.get_objects_from_model_table(config, table, v_results, perdicate)
                
            vect = []
            for p in v_results:
                vect.append(p.to_json())
                
            if vect is not None and len(vect) > 0:
                json_root[out_json_node_name] = vect
            else:
                json_root[out_json_node_name] = []
        except Exception as exex:
            message.add_exception('Error reading the model ' + table_name, exex)
            
        return message, json_root
    
    def get_objects_from_model_table(self, config: dict, table: dict, v_result: list, predicate) -> list:
        rows = table['value']
        for row in rows:
            row_data = row['value']
            
            v_value = []
            for column_name in config['columns'].split(','):
                declaration_data = DeclarationData()
                obj = row_data[column_name] if column_name in row_data.keys() else None
                if declaration_data.create_from_row(obj):
                    v_value.append(declaration_data)
                    
                
            obj_row = predicate(None) 
            obj_row.create_from_row(v_value)
            v_result.append(obj_row)
                    
        return v_result
        
    def identify_all_data(self, config_formular: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages]:
        return message
    
    def identify_id_data(self, message: ProcessMessages) -> ProcessMessages:
        pass
    
    def identify_tables(self, config_formular: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages]:
        pass
        
        
