

from typing import Tuple

from NewDeclarationInQueue.processfiles.customprocess.search_lines_in_pages import SearchLinesInPage
from NewDeclarationInQueue.processfiles.customprocess.search_text_line_parameter import SearchTextLineParameter
from NewDeclarationInQueue.processfiles.process_messages import ProcessMessages


class SearchTableInPages:
    """
        Class to search tables in document
    """
    
    page_no = 0
    search_text_limit: SearchLinesInPage
    cell_search: SearchTextLineParameter
        
    def __init__(self, page_no: int, upper_text_search: SearchTextLineParameter, \
                    lower_text_search: SearchTextLineParameter, cell_search: SearchTextLineParameter):
        """
            Initialize the class with the necessary info for the processing

        Args:
            page_no (int): page number where the table is located
            upper_text_search (SearchTextLineParameter): parameters to search the upper line that defines the table position
            lowertext_search (SearchTextLineParameter): parameters to search the lower line that defines the table position
            cell_search (SearchTextLineParameter): parameters to search the first cell in the header of the table
        """
        
        self.page_no = page_no
        self.search_text_limit = SearchLinesInPage(page_no, upper_text_search, lower_text_search)
        self.cell_search = cell_search
        
    def change_page(self, new_page_no: int):
        """
            Change the page where the table is searched

        Args:
            new_page_no (int): new page number where the table should be searched
        """
        self.page_no = new_page_no
        self.search_text_limit.page_no = new_page_no
    
    def find_table_by_position(self, table_pages, page_no, bounding_box) -> list:
        """
            Fint the table by bounding box

        Args:
            table_pages ([list]): list of pages in the document
            page_no ([int]): page number where the table should be searched
            bounding_box ([list]): list of points that defines the bounding box of the table

        Returns:
            [list]: JSON information corresponding to the table
        """
        
        if page_no >= len(table_pages) or bounding_box is None:
            return None

        page = table_pages[page_no]
        found_table = None

        for table in page['form']['tables']:
            table_bounding_box =  table['bounding_box']
            if (abs(table_bounding_box[1] - bounding_box[1]) <= 0.5 and
                   table_bounding_box[5] >= bounding_box[5]):
                found_table = table
                break

        return found_table
        
    def search_table(self, data: dict, message: ProcessMessages) -> Tuple[list, ProcessMessages, int]:
        """
            Search a table in a document

        Args:
            data (dict): input JSON data of the doucment
            message (ProcessMessages): collects the messsages generated in the processing workflow

        Returns:
            Tuple[list, ProcessMessages, int]: JSON info corresponding to the searched information,
                                                    the processing messages and the page number where
                                                    the table was found
        """
        
        table_headers = []
        
        bOk = self.search_text_limit.get_limit_lines(data)
        if bOk == False:
            message.add_message('Text not found', self.search_text_limit.to_string(), 'search_table')
            return None, message, self.search_text_limit.end_page_no

        if self.search_text_limit.end_page_no < 0:
            txt = self.search_text_limit.find_line_between_lines(data, self.page_no, self.cell_search, \
                                                self.search_text_limit.n_min, self.search_text_limit.n_max)
            if txt is not None:
                tab = self.find_table_by_position(data, self.page_no, txt['bounding_box'])
                if tab is not None:
                    table_headers.append(tab)
        else:
            txt = self.search_text_limit.find_line_between_lines(data, self.page_no, self.cell_search, \
                                                self.search_text_limit.n_min, None)
            
            if txt is not None:
                tab = self.find_table_by_position(data, self.page_no, txt['bounding_box'])
                if tab is not None:
                    table_headers.append(tab)
                
            n_count = self.page_no + 1
            while n_count <= self.search_text_limit.end_page_no:
                txt = self.search_text_limit.find_line_between_lines(data, n_count, \
                                        self.cell_search, None, \
                                        (self.search_text_limit.n_max if n_count == self.search_text_limit.end_page_no else None))
                
                if txt is not None:
                    tab = self.find_table_by_position(data, n_count, txt['bounding_box'])
                    if tab is not None:
                        table_headers.append(tab)
                n_count += 1
            
        return table_headers, message, (self.search_text_limit.end_page_no if self.search_text_limit.end_page_no > 0 else self.page_no) 