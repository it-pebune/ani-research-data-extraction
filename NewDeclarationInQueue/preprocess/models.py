class DocumentType:
    DOC_WEALTH = 1
    DOC_INTERESTS = 2
    DOCUMENT_TYPE_CHOICES = [
        (DOC_WEALTH, 'Declarație de Avere'),
        (DOC_INTERESTS, 'Declarație de Interese'),
    ]
    
class WelthFormular:
    DOCUMENT01 = 1
    DOCUMENT02 = 2
    
class InterestFormular:
    DOCUMENT01 = 1
    DOCUMENT02 = 2