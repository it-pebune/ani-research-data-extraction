class TextWithSpecialCharacters:
    
    main_string: str
    sch_string: str
    has_sch: bool
    
    def __init__(self, main: str, sch: str, bsch: bool):
        self.main_string = main
        self.sch_string = sch
        self.has_sch = bsch

    def contains(self, scompare: str) -> bool:
        if not self.has_sch:
            return (self.main_string in scompare)
        
        return (self.sch_string in scompare.encode('ascii','replace').decode("utf-8") or \
            #self.main_string in scompare.replace('ă', 'a').replace('â', 'a').replace('î', 'i').replace('ș', 's').replace('ț', 't'))
            self.main_string in scompare)
        
    def startswith(self, scompare: str) -> bool:
        if not self.has_sch:
            return scompare.startswith(self.main_string)
        
        
        return (scompare.encode('ascii','replace').decode("utf-8").startswith(self.sch_string) or \
            scompare.startswith(self.main_string))
            #scompare.replace('ä', 'a').replace('ă', 'a').replace('ã', 'a').replace('à', 'a').replace('â', 'a').replace('î', 'i').replace('ş', 's').replace('ț', 't').startswith(self.main_string))

