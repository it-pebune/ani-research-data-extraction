from NewDeclarationInQueue.processfiles.tableobjects.declaration_data import DeclarationData
from NewDeclarationInQueue.processfiles.tableobjects.table_in_document import TableInDocument


class Finance(TableInDocument):
    COL_ADM_INSTITUTION = 'adm_institution'
    COL_TYPE_OF_INVESTMENT = 'type_of_investment'
    COL_CURRENCY = 'currency'
    COL_YEAR_OF_OPENING = 'year_of_opening'
    COL_CURRENT_VALUE = 'current_value'

    adm_institution: DeclarationData = None
    type_of_investment: DeclarationData = None
    currency: DeclarationData = None
    year_of_opening: DeclarationData = None
    current_value: DeclarationData = None

    def __init__(self, adm_institution, type_of_investment, currency, year_of_opening, current_value):
        self.adm_institution = adm_institution
        self.type_of_investment = type_of_investment
        self.currency = currency
        self.year_of_opening = year_of_opening
        self.current_value = current_value

    def check_validity(self):
        return self.adm_institution is not None or self.type_of_investment is not None or self.currency is not None or \
                self.year_of_opening is not None or self.current_value is not None

    def to_string(self):
        return self.adm_institution.to_string() + ' - ' + self.type_of_investment.to_string() + ' - ' + self.currency.to_string() + ' - ' + \
            self.year_of_opening.to_string() + ' - ' + self.current_value

    def to_json(self):
        result = {
            self.COL_ADM_INSTITUTION:
                self.adm_institution.to_json() if self.adm_institution is not None else {},
            self.COL_TYPE_OF_INVESTMENT:
                self.type_of_investment.to_json() if self.type_of_investment is not None else {},
            self.COL_CURRENCY:
                self.currency.to_json() if self.currency is not None else {},
            self.COL_YEAR_OF_OPENING:
                self.year_of_opening.to_json() if self.year_of_opening is not None else {},
            self.COL_CURRENT_VALUE:
                self.current_value.to_json() if self.current_value is not None else {}
        }

        return result