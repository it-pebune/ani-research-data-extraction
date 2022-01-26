

from typing import Tuple

from NewDeclarationInQueue.processfiles.customprocess.search_text_line_parameter import SearchTextLineParameter


class SearchLinesInPage:
    """
        Search the lines in a page that are between two other lines
        Output parameters:
            bounding box of the upper line
            bounding box of the lower line
            line number of the uppler line
            line number of the lower line
            page number where the selected section ends (can be higher than the page where the search started)
    """
    
    # intput
    page_no = 0
    upper_text_search: SearchTextLineParameter
    lower_text_search: SearchTextLineParameter
    
    
    # output
    upper_limit_table = None
    lower_limit_table = None
    n_min = -1
    n_max = -1
    end_page_no = -1
    
        
    def __init__(self, page_no: int, upper_text_search: SearchTextLineParameter, lower_text_search: SearchTextLineParameter):
        """

        Args:
            page_no (int): page of the document where the lines have to be searched
            upper_text_search (SearchTextLineParameter): parameters to find the upper text
            lower_text_search (SearchTextLineParameter): parameters to find the lower text
        """
        self.page_no = page_no
        self.upper_text_search = upper_text_search
        self.lower_text_search = lower_text_search
        
    def to_string(self):
        return 'upper: ' + (self.upper_text_search.to_string() if self.upper_text_search is not None else '') + ' - ' + \
            'lower: ' + (self.lower_text_search.to_string() if self.lower_text_search is not None else '')
        
    def change_page(self, new_page_no: int):
        self.page_no = new_page_no
        
        
    def get_position_of_line(self, line_pages: list, page_no: int, param: SearchTextLineParameter) -> Tuple[dict, int]:
        """
            Get position of a line in a page
        Args:
            line_pages (list): list of pages in the returned JSON from the Azure Form Recognizer service
            page_no (int): page number to search the table in
            param (SearchTextLineParameter): parameters that define the line to be found

        Returns:
            Tuple[dict, int]: line found to satisfy the conditions, the page number where this line is
        """
        if page_no >= len(line_pages) or \
            (param.start_with_text is None and (param.contains_words is None or len(param.contains_words) == 0)):
            return None, -1

        page = line_pages[page_no]
        n_count = 0
        for line in page['form']['lines']:
            bStartsWith = False
            bContains = True if param.all_words else False

            if param.start_with_text is not None:
                if param.check_start(line['text']):
                #line['text'].startswith(param.start_with_text):
                    bStartsWith = True
            else:
                bStartsWith = True


            if param.contains_words is not None and len(param.contains_words) > 0:
                bContains = param.check_contains(line['text'])
                #for word in param.contains_words:
                    #bContainsOneWord = word in line['text']
                    #bContains = (bContains and bContainsOneWord) if param.all_words else (bContains or bContainsOneWord)
            else:
                bContains = True

            if bStartsWith and bContains:
                return line, n_count

            n_count += 1

        return None, -1
    
    def find_line_between_lines(self, line_pages: list, page_no: int, param: SearchTextLineParameter, min_line_no: int, max_line_no: int) -> dict:
        """ Given two lines (defined by position)

        Args:
            line_pages ([list]): list of pages in the JSON received by the Azure service
            page_no ([int]): number of page to search the lines between
            param (SearchTextLineParameter): parameters to find the line
            min_line_no (int): minimum number of line to start the search from
            max_line_no (int): maximum number of line to end the search to

        Returns:
            [dict]: found line that satisfies the conditions
        """
        if page_no >= len(line_pages):
            return None

        page = line_pages[page_no]
        n_count = 0

        for line in page['form']['lines']:
            if (min_line_no is not None or max_line_no is not None) and \
                ((min_line_no is not None and n_count < min_line_no) or (max_line_no is not None and n_count > max_line_no)):
                n_count += 1
                continue

            #if line['text'].startswith(param.start_with_text):
            #    return line
            if param.check_start(line['text']):
                return line
            
            n_count += 1

        return None
         
    def get_limit_lines(self, line_pages: list) -> bool:
        """
            Get the upper and lower lines, as they are defined by the parameters. Set the output parameters.

        Args:
            line_pages ([list]): list of pages from the JSON obtained from the Azure service

        Returns:
            [bool]: if the limits were found or not
        """
        self.upper_limit_table, self.n_min = self.get_position_of_line(line_pages, self.page_no, self.upper_text_search)
        if self.upper_limit_table is None:
            return False
        
        self.lower_limit_table, self.n_max = self.get_position_of_line(line_pages, self.page_no, self.lower_text_search)
        
        #ncount = 1
        while self.lower_limit_table is None and self.end_page_no < len(line_pages):
            if self.lower_limit_table is None:
                self.end_page_no = self.page_no + 1 #ncount
                #ncount += 1
                self.lower_limit_table, self.n_max = self.get_position_of_line(line_pages, self.end_page_no, self.lower_text_search)
                if self.lower_limit_table is None:
                    break
        return True
    
    def search_lines(self, data:dict) -> Tuple[list, int]:
        """
            Search the lines between the upper and lower lines, as defined in the input data in this class.

        Args:
            data (dict): JSON data as received from the service. Keys form and lines contain the lines.

        Returns:
            Tuple[list, int]: found lines between the upper and lower limit and the page number where the search ended
        """
        
        lines = []
        
        bOk = self.get_limit_lines(data)
        if bOk == False:
            return None, self.end_page_no
        
        n_page_count = self.page_no
        b_one = False
        while not b_one and (self.end_page_no < 0 or n_page_count < self.end_page_no):
            page = data[n_page_count]

            n_count = 0
            for line in page['form']['lines']: 
                if n_count <= self.n_min + 1 or n_count >= self.n_max:
                    n_count += 1
                    continue
                    
                lines.append(line['text'])
                n_count += 1
                
            n_page_count += 1
            
            if self.end_page_no < 0:
                b_one = True
            
        return lines, (self.end_page_no if self.end_page_no > 0 else self.page_no)
    
    
    
    