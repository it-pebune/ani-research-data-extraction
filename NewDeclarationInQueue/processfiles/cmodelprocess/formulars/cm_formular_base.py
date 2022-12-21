
from multiprocessing.dummy import Array
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
    
    def load_from_model(self, raw_model: dict):
        self.cmformular = raw_model
        self.form_type = raw_model[self.FORM_TYPE]
        self.form_confidence = raw_model[self.FORM_CONFIDENCE]
        self.page_range = raw_model[self.PAGE_RANGE]
        
    
    def get_labels(self, tab_config, fields, slabel_name) -> Tuple[int, int]:
        slabels = tab_config[slabel_name]
        
        if slabels is None:
            return 0, 0
        
        vlabels =  slabels.split(',')
        
        start_y = 0
        start_page = 0
        for stab in vlabels:
            tab = fields[stab]
            
            if tab is not None and tab['value_data'] is not None:
                bb = tab['value_data']['bounding_box']
                pag = tab['value_data']['page_number']
                
                if pag > start_page:
                    start_page = pag
                
                if bb is not None and len(bb) > 3:
                    y = bb[1]['y']
                    if y > start_y:
                        start_y = y
            
        
        return start_page, start_y
        
        
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
    
    def identify_raw_tables(self, raw_tables: list, page_label_start: int, y_label_start: int, 
                            page_label_end: int, y_label_end: int, predicate) -> list:
        found_raw_tables = []
        
        #table on one page only (both labels are on the same page)
        if page_label_start == page_label_end:
            for raw_table in raw_tables:
                # raw table is on the correct page and it is after the start label but before the end label
                if raw_table.page_number == page_label_start and raw_table.y_start > y_label_start and raw_table.y_end < y_label_end:
                    found_raw_tables.append(raw_table)
                    
        else:
            #table is on several pages (start label is one page, end label is on another page)
            for raw_table in raw_tables:
                # take tables on the start page, after the start label
                if raw_table.page_number == page_label_start and raw_table.y_start > y_label_start:
                    found_raw_tables.append(raw_table)
                    
                # take all tables in intermediary pages (between page of start label and page of end label)
                if raw_table.page_number > page_label_start and raw_table.page_number < page_label_end:
                    found_raw_tables.append(raw_table)
                    
                # take tables on the end page, above the end label
                if raw_table.page_number == page_label_end and raw_table.y_start < y_label_end:
                    found_raw_tables.append(raw_table)
                    

        header = [ v['text'] for v in found_raw_tables[0].raw_tab['cells'] if v['row_index'] == 0 ] if len(found_raw_tables) > 0  else None
        
        cells_result = []
        max_row = 0
        for tab in found_raw_tables:
            cells = [ c for c in tab.raw_tab['cells'] if len(c['text']) > 0 and c['text'] not in header ]
            if len(cells) > 0:
                for c in cells: c['row_index'] += max_row        
                max_row = max(c['row_index'] for c in cells)
            cells_result += cells
        
        v_obj_row = []
        for i in range(0, max_row + 1):
            vrow = [v for v in cells_result if v['row_index'] == i]
            vrow.sort(key = lambda v: v['column_index'])
            if (vrow is not None and len(vrow) > 0): 
                obj_row = predicate(None)
                obj_row.create_from_cells(vrow)
                v_obj_row.append(obj_row)
            
        
        return v_obj_row
        
    
    def identify_one_table(self, table_name: str, out_json_node_name: str, predicate, \
            config_formular: dict, fields: dict, raw_tables: list, json_root: dict, raw_json_root: dict,
            message: ProcessMessages) -> Tuple[ProcessMessages, dict, dict]:
        
        try:
            config, v_tables, message = self.get_config_and_value_tables(table_name, config_formular, fields, message)
            if message.has_errors():
                return message, json_root, raw_json_root      
            
            page_label_start, y_label_start = self.get_labels(config, fields, 'label_start')
            page_label_end, y_label_end = self.get_labels(config, fields, 'label_end')
            
            # raw json from tables
            v_raw_results = self.identify_raw_tables(raw_tables, page_label_start, y_label_start, page_label_end, y_label_end, predicate) 
            vect = []
            for p in v_raw_results:
                vect.append(p.to_json())
                
            if vect is not None and len(vect) > 0:
                raw_json_root[out_json_node_name] = vect
            else:
                raw_json_root[out_json_node_name] = []
            
            # json from tables identified by the model
            v_results = []
            for table in v_tables:
                v_results = self.get_objects_from_model_table(config, table, v_results, predicate)
                
            vect = []
            for p in v_results:
                vect.append(p.to_json())
                
            if vect is not None and len(vect) > 0:
                json_root[out_json_node_name] = vect
            else:
                json_root[out_json_node_name] = []
        except Exception as exex:
            message.add_exception('Error reading the model ' + table_name, exex)
            
        return message, json_root, raw_json_root
    
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
        
    def identify_all_data(self, config_formular: dict, raw_tables: list, message: ProcessMessages) -> Tuple[dict, dict, ProcessMessages]:
        return message
    
    def identify_id_data(self, message: ProcessMessages) -> ProcessMessages:
        pass
    
    def identify_tables(self, config_formular: dict, raw_tables: list, message: ProcessMessages) -> Tuple[dict, ProcessMessages]:
        pass
        
        
