

from NewDeclarationInQueue.processfiles.customprocess.text_with_special_ch import TextWithSpecialCharacters


class SearchTextLineParameter:
    """
        Defines the parameters to search a line of text in the JSON returned by the Azure service
    """
    start_with_text: TextWithSpecialCharacters
    contains_words: list
    all_words: bool
        
    def __init__(self, start_with_text: TextWithSpecialCharacters, contains_words: list, all_words: bool):
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
        
    def check_start(self, scompare: str) -> bool:
        return self.start_with_text.startswith(scompare)
    
    def check_contains(self, scompare: str) -> bool:
        return self.start_with_text.contains(scompare)
    
    def check_contains(self, scompare: str) -> bool:
        bresult = True
        
        for word in self.contains_words:
            bok = word.contains(scompare)
            bresult = (bresult or bok) if self.all_words == False else (bresult and bok)
        
        return bresult
        
    def to_string(self):
        return self.start_with_text.main_string + ' - ' + \
            (",".join([x.main_string for x in self.contains_words]) if self.contains_words is not None else '') + \
            ' - ' + str(self.all_words)