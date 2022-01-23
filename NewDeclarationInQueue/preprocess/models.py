class DocumentType:
    DOC_WEALTH = 'DAvr'
    DOC_INTERESTS = 'DInt'
    DOCUMENT_TYPE_CHOICES = [
        (DOC_WEALTH, 'Declarație de Avere'),
        (DOC_INTERESTS, 'Declarație de Interese'),
    ]
    
class WelthFormular:
    DOCUMENT01 = 'Davere01'
    DOCUMENT02 = 'Davere02'
    
class InterestFormular:
    DOCUMENT01 = 'Dinterese01'
    DOCUMENT02 = 'Dinterese02'