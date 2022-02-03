

from typing import Tuple

from NewDeclarationInQueue.processfiles.customprocess.formulars.formular_base import FormularBase
from NewDeclarationInQueue.processfiles.customprocess.table_config_detail import TableConfigDetail
from NewDeclarationInQueue.processfiles.customprocess.table_stop_header import TableStopHeader
from NewDeclarationInQueue.processfiles.customprocess.tableobjects.associate import Associate
from NewDeclarationInQueue.processfiles.customprocess.tableobjects.contracts import Contracts
from NewDeclarationInQueue.processfiles.customprocess.tableobjects.man_commercial import ManCommercial
from NewDeclarationInQueue.processfiles.customprocess.tableobjects.man_professional import ManProfessional
from NewDeclarationInQueue.processfiles.process_messages import ProcessMessages


class DInterese(FormularBase):
    """ 
        Base class for all the Interest Declaration formulars. 
    """
    
    def __init__(self, no_of_pages: int):
        self.no_of_pages = no_of_pages
    
    
    def process_all_tables(self, config: dict, data: dict, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages]:
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
        
        n_upper_page = 0
        n_upper_line = 1
        n_lower_page = 0
        n_lower_line = 0
        
        line_asociate, n_upper_page, n_upper_line, massage = self.get_header_from_lines(config['asociat'], \
            data['ocr_form_response'], n_upper_page, n_upper_line, 'asociat', message)  
        line_company, n_lower_page, n_lower_line, massage = self.get_header_from_lines(config['company_comm'], \
            data['ocr_form_response'], n_upper_page, n_upper_line, 'company_comm', message)
        json, message = self.get_header_from_tables(line_asociate, line_company, \
            data['ocr_form_response'], n_upper_page, n_lower_page, \
            'asociat', 4, True, lambda x: Associate(), json, message)
         
        n_upper_page = n_lower_page
        n_upper_line = n_lower_line
        line_management, n_lower_page, n_lower_line, massage = self.get_header_from_lines(config['management_comm'], \
            data['ocr_form_response'], n_upper_page, n_lower_page, 'management_comm', message)
        json, message = self.get_header_from_tables(line_company, line_management, \
            data['ocr_form_response'], n_upper_page, n_lower_page, \
            'company_comm', 3, True, lambda x: ManCommercial(), json, message)
        
        n_upper_page = n_lower_page
        n_upper_line = n_lower_line
        line_party, n_lower_page, n_lower_line, massage = self.get_header_from_lines(config['management_party'], \
            data['ocr_form_response'], n_upper_page, n_lower_page, 'management_party', message)
        json, message = self.get_header_from_one_line_table(line_management, line_party, \
            data['ocr_form_response'], n_upper_page, n_lower_page, 'management_comm', json, message)
        
        n_upper_page = n_lower_page
        n_upper_line = n_lower_line
        line_contracts, n_lower_page, n_lower_line, massage = self.get_header_from_lines(config['contracts'], \
            data['ocr_form_response'], n_upper_page, n_lower_page, 'contracts', message)
        json, message = self.get_header_from_one_line_table(line_party, line_contracts, \
            data['ocr_form_response'], n_upper_page, n_lower_page, 'management_party', json, message)
        
        n_upper_page = n_lower_page
        n_upper_line = n_lower_line
        json, message = self.get_header_from_tables(line_party, line_contracts, \
            data['ocr_form_response'], n_upper_page, \
            100, 'contracts', 7, True, lambda x: Contracts(), json, message)
        
        
        
        return json, message
    
    def get_header_from_tables(self, header_line: dict, footer_line: dict, \
        pages: list, n_upper_page: int, n_lower_page: int, sname: str, no_columns: int,  \
        b_skip_header: bool, predicate, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages]:
        
        
        v_objects = None
        if header_line is None or len(header_line) == 0:
            message.add_error('get_header_from_tables', 'upper line not found ' + sname)
            return None, message
        
        n_count_page = 0
        n_count_column = 0
        v_line = []
        for page in pages:
            if n_count_page < n_upper_page:
                n_count_page += 1
                continue
            
            bfirst = False
            for table in page['form']['tables']:
                for cell in table['cells']:
                    if cell['bounding_box'][1] > header_line['bounding_box'][1] and \
                        ((footer_line is None or cell['bounding_box'][1] < footer_line['bounding_box'][1]) or \
                            n_count_page < n_lower_page ) and \
                        (footer_line is None or cell['text'] != footer_line['text']):
                            if bfirst == False and b_skip_header == True:
                                bfirst = True
                                continue
                            
                            if n_count_column < no_columns:
                                v_line.append(cell['text'])
                                n_count_column += 1
                            
                            if n_count_column == no_columns - 1:
                                if v_objects is None and b_skip_header == True:
                                    v_objects = []
                                else:
                                    obj = predicate(None)
                                    obj.create_from_row(v_line)
                                    if obj.check_validity():
                                        if v_objects is None:
                                            v_objects = []
                                        v_objects.append(obj)
                                    
                                v_line = []
                                n_count_column = 0
                            
                    else:
                        continue
                    
                
            n_count_page += 1
            if n_count_page > n_lower_page:
                break
        
        json[sname] = []            
        if v_objects is not None and len(v_objects) > 0:
            for obj in v_objects:
                json[sname].append(obj.to_json())
                
        return json, message
        
        
    def get_header_from_one_line_table(self, header_line: dict, footer_line: dict, \
        pages: list, n_upper_page: int, n_lower_page: int, sname: str, \
        json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages]:
        
        if header_line is None or len(header_line) == 0:
            message.add_error('get_header_from_one_line_table', 'upper line not found ' + sname)
            return None, message
        
        n_count_page = 0
        v_line = []
        for page in pages:
            if n_count_page < n_upper_page:
                n_count_page += 1
                continue
            
            for line in page['form']['lines']:
                if line['bounding_box'][1] > header_line['bounding_box'][1] and \
                    ((footer_line is None or line['bounding_box'][1] < footer_line['bounding_box'][1]) or \
                        n_count_page < n_lower_page ) and \
                    (footer_line is None or line['text'] != footer_line['text']):
                        
                        v_line.append(line['text'])
                else:
                    continue
                    
                
            n_count_page += 1
            if n_count_page > n_lower_page:
                break
                    
        json[sname] = []            
        if len(v_line) > 0:
            for sobj in v_line:
                json[sname].append({'line': sobj})
                
        return json, message
        

    def get_header_from_lines(self, config: TableConfigDetail, pages: list, n_page: int, \
        n_line: int, sname: str, message: ProcessMessages) -> Tuple[dict, int, int, ProcessMessages]:
        
        line_stop  = None
        param = config.header
        if param is None:
            message.add_error('no parameter found ' + sname)
            return None, n_page, n_line, message
        
        n_count_page = 0
        n_count_line = 0
        for page in pages:
            if n_count_page < n_page:
                n_count_page += 1
                continue
            
            n_count_line = 0
            for line in page['form']['lines']:
                if n_count_line < n_line:
                    n_count_line += 1
                    continue
                
                bStartsWith =  param.check_start(line['text']) \
                    if param is not None else False
                    
                bContains = param.check_contains(line['text']) \
                    if param.contains_words is not None and len(param.contains_words) > 0 \
                    else False
                    
                if bStartsWith or bContains:
                    line_stop = line
                    break
                
                n_count_line += 1
                
            if line_stop is not None:
                break
            
            n_count_page += 1
            n_line = 0
        
        if line_stop is not None:
            return line_stop, n_count_page, n_count_line, message
        else:
            message.add_message('get_header_from_lines', 'table not found: ' + sname, '')
            return None, n_page, 0, message
        
    
        
    
    def get_next_table(self, tab: TableStopHeader, count: int) -> int:
        return tab.n_table if tab is not None else count
    
    
    def get_company_associate(self, config: TableConfigDetail,  data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        pass
    
    def get_management_commercial(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        pass
    
    def get_management_association(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        pass
    
    def get_management_party(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        pass
    
    def get_contracts(self, data: dict, n_page: int, json: dict, message: ProcessMessages) -> Tuple[dict, ProcessMessages, int]:
        pass
    
    
    
    
        