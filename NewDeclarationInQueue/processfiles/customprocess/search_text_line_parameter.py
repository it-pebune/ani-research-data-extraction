

class SearchTextLineParameter:
    """
        Defines the parameters to search a line of text in the JSON returned by the Azure service
    """
    start_with_text: str
    contains_words: list
    all_words: bool
        
    def __init__(self, start_with_text: str, contains_words: list, all_words: bool):
        """
            Initialize the class

        Args:
            start_with_text (str): text with which the line starts
            contains_words (list): list of words that are contained in the line
            all_words (bool): if the two previous condition (start and contains) must be both true or only one
        """
        self.start_with_text = start_with_text
        self.contains_words = contains_words
        self.all_words = all_words
        
    def to_string(self):
        return self.start_with_text + ' - ' + \
            (",".join(self.contains_words) if self.contains_words is not None else '') + \
            ' - ' + str(self.all_words)