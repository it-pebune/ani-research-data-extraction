

from typing import Tuple

from NewDeclarationInQueue.processfiles.process_messages import ProcessMessages


class OcrJsonFormatter:
    """ Formats the JSON received from simple OCR service in a more user friendly format
    """
    ROOT = 'ocr_page_response'
    NODE_PAGE_NO = 'page_no'
    NODE_PAGE = 'page'
    
    ATTRIBUTE_PAGE = 'page'
    ATTRIBUTE_LANGUAGE = 'language'
    ATTRIBUTE_ANGLE = 'angle'
    ATTRIBUTE_WIDTH = 'width'
    ATTRIBUTE_HEIGHT = 'height'
    NODE_LINES = 'lines'
    
    ATTRIBUTE_LINE_NO = 'line_no'
    ATTRIBUTE_BOUNDING_BOX = 'bounding_box'
    ATTRIBUTE_TEXT = 'text'
    
    NODE_WORDS = 'words'
    ATTRIBUTE_WORDS_BOUNDING_BOX = 'bounding_box'
    ATTRIBUTE_WORDS_TEXT = 'text'
    ATTRIBUTE_WORDS_CONFIDENCE = 'confidence'
    
    def __init__(self):
        pass
    
    
    def get_json_from_ocr_page_response(self, dict_ocr, page_no: int, result, message: ProcessMessages) -> Tuple[ProcessMessages, dict]:
        """ Get custom JSON from the JSON received from the simple OCR service. 
                We send to the service the image of the page and receive for each page a JSON file.

        Args:
            dict_ocr ([JSON Node]): custom JSON node to add the info for the current page to
            page_no (int): page number
            result ([type]): root of the received JSON file 
            message (ProcessMessages): collects messages from processing workflow

        Returns:
            Tuple[ProcessMessages, dict]: messages from the processing workflow for this page 
                                            and generated JSON info for this page
        """
        try:
            for res in result:
                dict_ocr[self.ROOT].append({self.NODE_PAGE_NO: str(page_no), self.NODE_PAGE: self.get_json_from_ocr_page(res)})
        except Exception as exex:
            message.add_exception('Generate custom json from OCR service json', exex)
            
        return message, dict_ocr
    
    def get_json_from_ocr_page(self, res) -> dict:
        """ Get JSON structure for a page

        Args:
            res ([JSON node]): JSON input for a page

        Returns:
            [dict]: custom generated JSON
        """
        dict_result = {self.ATTRIBUTE_PAGE: res.page, self.ATTRIBUTE_LANGUAGE: res.language, 
                    self.ATTRIBUTE_ANGLE: res.angle, 
                    self.ATTRIBUTE_WIDTH: res.width, self.ATTRIBUTE_HEIGHT: res.height, 
                    self.NODE_LINES: []}
        
        n_count = 1
        for line in res.lines:
            dict_result[self.NODE_LINES].append(self.get_json_from_ocr_line(line, n_count))
            n_count += 1
        return dict_result
    
    def get_json_from_ocr_line(self, line, no_line: int) -> dict:
        """ Generate custom JSON based on a line in the received JSON OCR file

        Args:
            line ([JSON node]): info about a line of text in the received JSON file
            no_line ([int]): number line in the document

        Returns:
            [dict]: custom JSON for the line
        """
        dict_line = {self.ATTRIBUTE_LINE_NO: str(no_line), self.ATTRIBUTE_BOUNDING_BOX: line.bounding_box, 
                     self.ATTRIBUTE_TEXT: line.text, self.NODE_WORDS: []}
        for word in line.words:
            dict_line[self.NODE_WORDS].append({self.ATTRIBUTE_WORDS_BOUNDING_BOX: word.bounding_box, \
                                    self.ATTRIBUTE_WORDS_TEXT: word.text, 
                                    self.ATTRIBUTE_WORDS_CONFIDENCE: word.confidence})
        return dict_line