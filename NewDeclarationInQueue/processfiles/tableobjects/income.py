from NewDeclarationInQueue.processfiles.tableobjects.declaration_data import DeclarationData
from NewDeclarationInQueue.processfiles.tableobjects.table_in_document import TableInDocument


class Income(TableInDocument):
    COL_INCOME_TYPE = 'income_type'
    COL_PERSON_TYPE = 'person_type'
    COL_OWNER = 'owner'
    COL_SOURCE = 'source'
    COL_SERVICE = 'service'
    COL_YEAR_INCOME = 'year_income'

    income_type: DeclarationData = None
    person_type: DeclarationData = None
    owner: DeclarationData = None
    source: DeclarationData = None
    service: DeclarationData = None
    year_income: DeclarationData = None

    def __init__(self, owner, source, service, year_income, income_type=None, person_type=None):
        self.owner = owner
        self.source = source
        self.service = service
        self.year_income = year_income
        self.person_type = person_type
        self.income_type = income_type

    def check_validity(self):
        return self.owner is not None or \
                self.source is not None or self.service is not None  or self.year_income is not None

    def to_string(self):
        return self.income_type.to_string() + ' - ' + self.person_type.to_string() + ' - ' + \
            self.owner.to_string() + ' - ' + \
            self.source.to_string() + ' - ' + self.service.to_string() + ' - ' + self.year_income

    def to_json(self):
        result = {
            self.COL_INCOME_TYPE: self.income_type.to_json() if self.income_type is not None else {},
            self.COL_PERSON_TYPE: self.person_type.to_json() if self.person_type is not None else {},
            self.COL_OWNER: self.owner.to_json() if self.owner is not None else {},
            self.COL_SOURCE: self.source.to_json() if self.source is not None else {},
            self.COL_SERVICE: self.service.to_json() if self.service is not None else {},
            self.COL_YEAR_INCOME: self.year_income.to_json() if self.year_income is not None else {}
        }

        return result
