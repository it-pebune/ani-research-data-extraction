class DeclarationData:
    text = ''
    page_number = 0
    confidence = 0.0
    bounding_box = []  # this should be a vector of dict, so it is easily transformed in json

    def __init__(self, content: str, page_number: int, confidence: float, bounding_box):
        self.text = content
        self.page_number = page_number
        self.confidence = confidence
        self.bounding_box = bounding_box

    def check_validity(self):
        return len(self.text) > 0

    def to_string(self):
        return self.text
    
    def create_from_cell(self, cell: dict) -> bool:
        if 'text' not in cell or 'page_number' not in cell or 'confidence' not in cell or 'bounding_box' not in cell:
            return False
        
        self.text = cell['text']
        self.page_number = cell['page_number']
        self.confidence = cell['confidence']
        self.bounding_box = cell['bounding_box']
        
        return True
    
    def create_from_row(self, row) -> bool:
        
        if row is None or 'value' not in row or 'confidence' not in row:
            return False
        
        if row['value_data'] is None or 'page_number' not in row['value_data'] or 'bounding_box' not in row['value_data']:
            return False
        
        
        self.text = row['value']
        self.page_number = row['value_data']['page_number']
        self.confidence = row['confidence']
        self.bounding_box = row['value_data']['bounding_box']
        
        return True

    def to_json(self):
        result = {
            'text': self.text,
            'page_number': self.page_number,
            'confidence': self.confidence,
            'bounding_box': self.bounding_box
        }

        return result
