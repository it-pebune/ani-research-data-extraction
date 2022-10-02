class RawTable:
    raw_tab: dict
    page_number: int
    y_start: int
    y_end: int
    
    def __init__(self, raw_tab):
        self.raw_tab = raw_tab
        
        if 'page_number' in raw_tab:
            self.page_number = raw_tab['page_number']
            
        if 'bounding_box' in raw_tab:
            bb = raw_tab['bounding_box']
            if bb is not None and len(bb) > 3:
                self.y_start = bb[1]['y']
                self.y_end = bb[2]['y']