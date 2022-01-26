

from typing import Tuple
from NewDeclarationInQueue.processfiles.customprocess.search_lines_in_pages import SearchLinesInPage
from NewDeclarationInQueue.processfiles.customprocess.search_table_in_pages import SearchTableInPages
from NewDeclarationInQueue.processfiles.customprocess.search_text_line_parameter import SearchTextLineParameter

from NewDeclarationInQueue.processfiles.process_messages import ProcessMessages


class FormularBase:
    """
        Base class for all formulars. Contains methods to find table info based on the text above
            and text below.
        The methods identify when a table goes over two pages or when it ends on a page and the 
            next table should be searched on the next page.
    """
    no_of_pages = -1
    
    def __init__(self, no_of_pages: int):
        """[summary]

        Args:
            no_of_pages (int): number of pages of the document
        """
        pass
    
    
    def find_table_in_document_between_lines(self, data: dict, page_no: int, max_pages_no: int, \
                    up_search: SearchTextLineParameter, low_search: SearchTextLineParameter, \
                    t_search: SearchTextLineParameter, message: ProcessMessages) -> Tuple[list, ProcessMessages, int]:
        """
            Find a table between two lines. The line are defined by the following two condition, at least one is required:
                The text the page starts with
                A vector of words to be contained in the line
                If the two conditions have to be both true or only one

        Args:
            data (dict): input JSON data obtained from the Form Recognizer service
            page_no (int): page number where the table is probably located 
                            (next page will be investigated also if the table is not found in this page)
            max_pages_no (int): maximum number of pages in the document
            upper_search (str): text with which the upper line starts
            upper_contains (list): list of words that is contained in the upper line
            upper_contains_all (bool): if the two above conditions must be met for the upper line or only one
            message (ProcessMessage): collector of the messages generated in the processing workflow

        Returns:
            Tuple[list, ProcessMessages, int]: output info from the table, processing messages, page where the table ends
        """
    
        upper_search = up_search
        lower_search = low_search
        table_column_search = t_search

        search = SearchTableInPages(page_no = page_no, upper_text_search = upper_search, \
                                   lower_text_search =lower_search, cell_search = table_column_search)
        tables, message, end_page_no = search.search_table(data, message)
        
        if (tables is None or len(tables) == 0) and end_page_no < max_pages_no:
            message.add_message('Look for table on the next page', str(page_no), 'find_table_in_document_between_lines')
            search.change_page(page_no + 1)
            tables, message, end_page_no = search.search_table(data, message)

        return tables, message, end_page_no 
    
    def find_lines_in_document_between_lines(self, data: dict, page_no: int, max_pages_no: int, \
                        upper_search_text: str, upper_search_contains: list, upper_search_all: bool, \
                        lower_search_text: str, lower_search_contains: list, lower_search_all: bool) -> Tuple[list, int]:
        """
            Find lines of text between two other lines of text
            
        Args:
            data (dict): input JSON data obtained from the Form Recognizer service
            page_no (int): page number where the table is probably located 
                            (next page will be investigated also if the table is not found in this page)
            max_pages_no (int): maximum number of pages in the document
            upper_search (str): text with which the upper line starts
            upper_search_contains (list): list of words that is contained in the upper line
            upper_search_all (bool): if the two above conditions must be met for the upper line or only one
            lower_search (str): text with which the lower line starts
            lower_search_contains (list): list of words that is contained in the lower line
            lower_search_all (bool): if the two above conditions must be met for the lower line or only one

        Returns:
            Tuple[list, int]: output info from the text and page where the text ends
        """
    
        upper_search = SearchTextLineParameter(upper_search_text, upper_search_contains, upper_search_all)
        lower_search = SearchTextLineParameter(lower_search_text, lower_search_contains, lower_search_all)

        search = SearchLinesInPage(page_no, upper_search, lower_search)
        lines, end_page_no = search.search_lines(data)
        
        if (lines is None or len(lines) == 0) and end_page_no < max_pages_no:
            search.change_page(page_no + 1)
            end_page_no = page_no + 1
            lines, end_page_no = search.search_lines(data)
        
        return lines, end_page_no
    
    def extract_table_info(self, tables: list, predicate) -> list:
        """
            Extract information from a table (that was already identified as a table)

        Args:
            tables (list): input JSON info corresponding to the table
            predicate ([type]): function to create the correct object for the table

        Returns:
            list: list of objects corresponding to the table
        """
        
        lt_objects = []
        
        if tables is None or len(tables) == 0:
            return lt_objects
        
        for table in tables:
            headings = [cell for cell in table['cells'] if cell['is_header'] == True]
            row = int(headings[0]['row']) + 1 if headings is not None and len(headings) > 0 else 0
            
            vect = [cell for cell in tables[0]['cells'] if int(cell['row']) == row]
            while vect is not None and len(vect) > 0:
                vect.sort(key=lambda x: x['column'])
                
                table_in_doc = predicate(None)
                table_in_doc.create_from_row([x['text'] for x in vect])
                if table_in_doc.check_validity() == True:
                    lt_objects.append(table_in_doc)

                row += 1
                vect = [cell for cell in tables[0]['cells'] if int(cell['row']) == row]
                
        return lt_objects
    
    def extract_table_info_to_json(self, sname: str, tables: list, predicate, message: ProcessMessages) -> Tuple[ProcessMessages, list]:
        """ 
            Transform the list of objects corresponding to a table to custom JSON
        
        Args:
            tables (list): list of objects corresponding to the table
            predicate ([type]): function to create the correct object corresponding to the table
            message (ProcessMessages): collector for the messages generated in the processing workflow

        Returns:
            Tuple[ProcessMessages, list]: processing messsages and custom JSON for the table
        """
        
        if tables is None:
            message.add_error('table not found ' + sname, 'extract_table_info_to_json')
            return message, None
        
        lt_objects = self.extract_table_info(tables, predicate)
        
        vect = []
        for p in lt_objects:
            vect.append(p.to_json())
            
        return message, vect
    
    def extract_lines_info_to_json(self, lines: list) -> str:
        """
            Creates a string with the received lines of text

        Args:
            lines (list): list of lines in the document received from the Azure service

        Returns:
            str: generated string based on the received lines of text
        """
        if lines is None:
            return None
        
        
        s_result = ''
        for line in lines:
            s_result = s_result + line + ' '
            
        return s_result
    
    def extract_table_info_one_level_to_json(self, tables: list, vlevel: list, predicate, message: ProcessMessages) -> Tuple[ProcessMessages, list]:
        """
            Extract table info form a table that has one level of detail in its structure

        Args:
            tables (list): list of objects corresponding to the table
            vlevel (list): header of each level in the table
            predicate ([type]): function to create the correct object corresponding to the table
            message (ProcessMessages): collector for the messages generated in the processing workflow

        Returns:
            Tuple[ProcessMessages, list]: processing messsages and custom JSON for the table
        """
        
        if tables is None:
            message.add_error('Table one level not found', 'extract_table_info_one_level_to_json')
            return message, None
        
        lt_objects = self.extract_table_info_one_level(tables, vlevel, predicate)
        
        vect = []
        for p in lt_objects:
            vect.append(p.to_json())
            
        return message, vect
    
    
    def extract_table_info_one_level(self, tables: list, vlevel: list, predicate) -> list:
        """
            Extract table info from a table that has one level of detail in its structure

        Args:
            tables (list): list of objects corresponding to the table
            vlevel (list): header of each level in the table
            predicate ([type]): function to create the correct object corresponding to the table

        Returns:
            list: list of objects containing the table informations
        """
        
        lt_objects = []
        
        if tables is None or len(tables) == 0:
            return lt_objects
        
        current_level = ''
        for table in tables:
            headings = [cell for cell in table['cells'] if cell['is_header'] == True]
            row = int(headings[0]['row']) + 1 if headings is not None and len(headings) > 0 else 0
            
            vect = [cell for cell in tables[0]['cells'] if int(cell['row']) == row]
            
            while vect is not None and len(vect) > 0:
                b_level_found = False
                vect.sort(key=lambda x: x['column'])
                
                for level in vlevel:
                    if level.check_contains(vect[0]['text']):
                    #if level in vect[0]['text']:
                        current_level = vect[0]['text']
                        row += 1
                        vect = [cell for cell in table['cells'] if int(cell['row']) == row]
                        b_level_found = True
                        break
                    
                if b_level_found:
                    continue
                
                table_in_doc = predicate(None)
                table_in_doc.create_from_row_one_level(current_level, [x['text'] for x in vect])
                if table_in_doc.check_validity() == True:
                    lt_objects.append(table_in_doc)

                row += 1
                vect = [cell for cell in table['cells'] if int(cell['row']) == row]
                
        return lt_objects
    
    
    
    def extract_table_info_two_level_to_json(self, tables: list, vlevel: list, vtwolevel: list, predicate, message: ProcessMessages) -> Tuple[ProcessMessages, list]:
        """
            Extract table info form a table that has two levels of detail in its structure

        Args:
            tables (list): list of objects corresponding to the table
            vlevel (list): header of each first level in the table
            vtwolevel (list): header of each second level in the table
            predicate ([type]): function to create the correct object corresponding to the table
            message (ProcessMessages): collector for the messages generated in the processing workflow

        Returns:
            Tuple[ProcessMessages, list]: processing messsages and custom JSON for the table
        """
        
        if tables is None:
            message.add_error('Table two levels not found', 'extract_table_info_two_level_to_json')
            return message, None
        
        lt_objects = self.extract_table_info_two_level(tables, vlevel, vtwolevel, predicate)
        
        vect = []
        for p in lt_objects:
            vect.append(p.to_json())
            
        return message, vect
    
    
    def extract_table_info_two_level(self, tables: list, vlevel: list, vtwolevel: list, predicate) -> list:
        """
            Extract table info from a table that has two levels of detail in its structure

        Args:
            tables (list): list of objects corresponding to the table
            vlevel (list): header of each first level in the table
            vtwolevel (list): header of each second level in the table
            predicate ([type]): function to create the correct object corresponding to the table

        Returns:
            list: list of objects containing the table informations
        """
        
        lt_objects = []
        
        if tables is None or len(tables) == 0:
            return lt_objects
        
        current_level = ''
        current_second_level = ''
        for table in tables:
            headings = [cell for cell in table['cells'] if cell['is_header'] == True]
            row = int(headings[0]['row']) + 1 if headings is not None and len(headings) > 0 else 0
            
            vect = [cell for cell in tables[0]['cells'] if int(cell['row']) == row]
            
            while vect is not None and len(vect) > 0:
                b_level_found = False
                vect.sort(key=lambda x: x['column'])
                
                for lev in vlevel:
                    if len(vect) > 0 and lev.check_contains(vect[0]['text']):
                #if vect[0]['text'] in vlevel:
                        current_level = vect[0]['text']
                        row += 1
                        vect = [cell for cell in table['cells'] if int(cell['row']) == row]
                        b_level_found = True
                        
                if b_level_found:
                    continue    
                    
                for level in vtwolevel:
                    if level.contains(vect[0]['text']):
                    #if level in vect[0]['text']:
                        current_second_level = vect[0]['text']
                        row += 1
                        vect = [cell for cell in table['cells'] if int(cell['row']) == row]
                        b_level_found = True
                        break
                    
                if b_level_found:
                    continue
                
                    
                table_in_doc = predicate(None)
                table_in_doc.create_from_row_two_level(current_level, current_second_level, [x['text'] for x in vect])
                if table_in_doc.check_validity() == True:
                    lt_objects.append(table_in_doc)

                row += 1
                vect = [cell for cell in table['cells'] if int(cell['row']) == row]
                
        return lt_objects