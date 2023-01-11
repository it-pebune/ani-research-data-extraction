


class DeclarationData:
    text = ''
    page_number = 0
    confidence = 0.0
    bounding_box = [] # this should be a vector of dict, so it is easily transformed in json
        
    def __init__(self, content: str, page_number: int, confidence: float, bounding_box):
        self.text = content 
        self.page_number = page_number
        self.confidence = confidence
        self.bounding_box = bounding_box
        
    def check_validity(self):
        return len(self.text) > 0
    
    def to_string(self):
        return self.text
    
    def to_json(self):
        result = {
            'text': self.text,
            'page_number': self.page_number,
            'confidence': self.confidence,
            'bounding_box': self.bounding_box
        }
        
        return result