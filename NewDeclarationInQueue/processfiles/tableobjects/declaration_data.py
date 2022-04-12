


class DeclarationData:
    text = ''
    page_number = 0
    confidence = 0.0
    bounding_box = [] # this should be a vector of dict, so it is easily transformed in json
    
        
    def __init__(self):
        pass
    
    def create_from_row(self, obj) -> bool:
        if obj is None:
            return False
        
        value_data = obj['value_data']
        if value_data is None:
            return False
        
        self.text = obj['value']
        self.page_number = value_data['page_number']
        self.confidence = obj['confidence']
        self.bounding_box = value_data['bounding_box']
        
        return True
    
        
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