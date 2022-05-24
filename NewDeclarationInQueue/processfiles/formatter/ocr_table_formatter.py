
from typing import Tuple

from NewDeclarationInQueue.processfiles.process_messages import ProcessMessages


class OcrTableFormatter:
    """ Generate a custom generated JSON file for a response from
            Form Recognizer Cognitive Service
    """
    ROOT = 'ocr_form_response'
    NODE_PAGE = 'ocr_form_response'
    ATTRIBUTE_PAGE_NO = 'page_no'
    ATTRIBUTE_FORM = 'form'
    ATTRIBUTE_TEXT_ANGLE = 'text_angle'
    ATTRIBUTE_WIDTH = 'width'
    ATTRIBUTE_HEIGHT = 'height'
    ATTRIBUTE_UNIT = 'unit'
    NODE_TABLES = 'tables'
    NODE_LINES = 'lines'
    ATTRIBUTE_PAGE_NUMBER = 'page_number'
    NODE_CELLS = 'cells'
    ATTRIBUTE_TEXT = 'text'
    ATTRIBUTE_ROW = 'row'
    ATTRIBUTE_COLLUMN = 'column'
    ATTRIBUTE_ROW_SPAN = 'row_span'
    ATTRIBUTE_COLUMN_SPAN = 'column_span'
    ATTRIBUTE_BOUNDING_BOX = 'bounding_box'
    ATTRIBUTE_CONFIDENCE = 'confidence'
    ATTRIBUTE_IS_HEADER = 'is_header'
    ATTRIBUTE_IS_FOOTER = 'is_footer'
    NODE_WORDS = 'words'
    ATTRIBUTE_WORD_TEXT = 'text'
    ATTRIBUTE_WORD_BOUNDING_BOX = 'bounding_box'
    ATTRIBUTE_WORD_CONFIDENCE = 'confidence'
    ATTRIBUTE_WORD_KIND = 'kind'
    
    
    
    def get_vector_from_points(self, vpoints):
        """ Get a vector from the points obtained from the service JSON file

        Args:
            vpoints ([list of points]): a list of points that has to be transformed in a vector of double values

        Returns:
            [vector of double]: resulting list of numbers
        """
        v = []
        
        for point in vpoints:
            v.append(point.x)
            v.append(point.y)
        
        return v
    
    
    def __init__(self):
        pass
    
    #TODO: save the file exactly how it comes from the OCR service
    def get_json_from_form_recognizer_response(self, message: ProcessMessages, pages: any) -> Tuple[ProcessMessages, dict]:
        """ Generate custom JSON from the JSON received from form recognizer service. 
                This is the entry point for the processing happening in this class.

        Args:
            message (ProcessMessages): collects processing messages
            pages (JSON node): the JSON received from the service

        Returns:
            Tuple[ProcessMessages, dict]: processing messages and the generated custom JSON structure
        """
        dict_ocr = {self.ROOT: []}
        ncount = 1
        
        for page in pages:
            dict_tables_page = self.get_form_for_page(page)
            dict_ocr[self.NODE_PAGE].append({self.ATTRIBUTE_PAGE_NO: ncount, self.ATTRIBUTE_FORM: dict_tables_page})
            ncount += 1
            
        return message, dict_ocr
    
    def get_form_for_page(self, form) -> dict:
        """ Generate custom JSON for a page obtained from the azure service

        Args:
            form ([JSON node]): input JSON structure for a page

        Returns:
            [dict]: custom JSON for a page
        """
        dict_form = {self.ATTRIBUTE_TEXT_ANGLE: form.text_angle, self.ATTRIBUTE_WIDTH: form.width, \
                    self.ATTRIBUTE_HEIGHT: form.height, self.ATTRIBUTE_UNIT: form.unit, 
                    self.NODE_TABLES: [], self.NODE_LINES: []}
        
        for table in form.tables:
            dict_form[self.NODE_TABLES].append(self.get_json_from_table(table))
            
        for line in form.lines:
            dict_form[self.NODE_LINES].append(self.get_json_from_line(line))
            
        return dict_form
    
    def get_json_from_line(self, line) -> dict:
        """ get custom JSON for a line in the input document

        Args:
            line ([JSON node]): a line from the input document

        Returns:
            [dict]: generated custom JSON
        """
        dict_line = {self.ATTRIBUTE_PAGE_NUMBER: line.page_number, 'kind': line.kind, 
                     self.ATTRIBUTE_TEXT: line.text,
                     self.ATTRIBUTE_BOUNDING_BOX: self.get_vector_from_points(line.bounding_box),
                     self.NODE_WORDS: []}
        
        if None != line.words:
            for word in line.words:
                dict_line[self.NODE_WORDS].append(self.get_json_words(word))
        
        return dict_line
    
    def get_json_from_table(self, table):
        """ Generate custom JSON for a table identified in the form recognizer service

        Args:
            table ([JSON node]): JSON information about a table

        Returns:
            [dict]: custom JSON generated for a table
        """
        dict_table = {self.ATTRIBUTE_PAGE_NUMBER: table.page_number, 
                      self.ATTRIBUTE_BOUNDING_BOX: self.get_vector_from_points(table.bounding_box),
                      self.NODE_CELLS: []}
        
        for cell in table.cells:
            dict_table[self.NODE_CELLS].append(self.get_json_cell(cell))
        
        return dict_table
    
    def get_json_cell(self, cell) -> dict:
        """ Generate custom JSON for a cell in a table identified by form recognizer service

        Args:
            cell ([JSON node]): input JSON information about a cell 

        Returns:
            dict: custom JSON generated for a cell in a table
        """
        dict_cell = {self.ATTRIBUTE_TEXT: cell.text, self.ATTRIBUTE_ROW: cell.row_index, 
                        self.ATTRIBUTE_COLLUMN: cell.column_index, 
                        self.ATTRIBUTE_ROW_SPAN: cell.row_span, 
                        self.ATTRIBUTE_COLUMN_SPAN: cell.column_span,
                        self.ATTRIBUTE_BOUNDING_BOX: self.get_vector_from_points(cell.bounding_box), 
                        self.ATTRIBUTE_CONFIDENCE: cell.confidence, 
                        self.ATTRIBUTE_IS_HEADER: cell.is_header, 
                        self.ATTRIBUTE_IS_FOOTER: cell.is_footer,
                        self.NODE_WORDS: []}
        
        if None != cell.field_elements:
            for word in cell.field_elements:
                dict_cell[self.NODE_WORDS].append(self.get_json_words(word))
        
        return dict_cell
    
    def get_json_words(self, word) -> dict:
        """ Get custom JSON for words identified in the input JSON

        Args:
            word ([JSON node]): input information about a word

        Returns:
            dict: custom JSON describing a word
        """
        dict_word = {"text": word.text, "bounding_box": self.get_vector_from_points(word.bounding_box), \
                    "confidence": word.confidence, "kind": word.kind}

        return dict_word
    
    def get_json_words(self, word) -> dict:
        """ Get custom JSON for words identified in the input JSON

        Args:
            word ([JSON node]): input information about words

        Returns:
            dict: custom JSON describing words
        """
        dict_word = {self.ATTRIBUTE_WORD_TEXT: word.text, 
                        self.ATTRIBUTE_WORD_BOUNDING_BOX: self.get_vector_from_points(word.bounding_box), 
                        self.ATTRIBUTE_WORD_CONFIDENCE: word.confidence, 
                        self.ATTRIBUTE_WORD_KIND: word.kind}

        return dict_word