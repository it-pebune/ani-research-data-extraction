from NewDeclarationInQueue.processfiles.customprocess.search_text_line_parameter import SearchTextLineParameter


class TableConfigDetail:
    upper: SearchTextLineParameter
    lower: SearchTextLineParameter
    header: SearchTextLineParameter
    
    first_level: list
    second_level: list
    
    def __init__(self):
        pass