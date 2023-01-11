from NewDeclarationInQueue.processfiles.tableobjects.declaration_data import DeclarationData
from NewDeclarationInQueue.processfiles.tableobjects.table_in_document import TableInDocument


class Investment(TableInDocument):
    COL_ISSUER = 'issuer'
    COL_TYPE_OF_INVESTMENT = 'type_of_investment'
    COL_NUMBER_OF_SHARES = 'number_of_shares'
    COL_CURRENT_VALUE = 'current_value'

    issuer: DeclarationData = None
    type_of_investment: DeclarationData = None
    number_of_shares: DeclarationData = None
    current_value: DeclarationData = None

    def __init__(self, issuer: DeclarationData, type_of_investment: DeclarationData, number_of_shares: DeclarationData,
                 current_value: DeclarationData):
        self.issuer = issuer
        self.type_of_investment = type_of_investment
        self.number_of_shares = number_of_shares
        self.current_value = current_value

    def check_validity(self):
        return self.issuer is not None or self.type_of_investment is not None or self.number_of_shares is not None or \
                self.current_value is not None

    def to_string(self):
        return self.issuer.to_string() + ' - ' + self.type_of_investment.to_string() + ' - ' + self.number_of_shares.to_string() + ' - ' + \
            self.current_value

    def to_json(self):
        result = {
            self.COL_ISSUER:
                self.issuer.to_json() if self.issuer.to_json() is not None else {},
            self.COL_TYPE_OF_INVESTMENT:
                self.type_of_investment.to_json() if self.type_of_investment is not None else {},
            self.COL_NUMBER_OF_SHARES:
                self.number_of_shares.to_json() if self.number_of_shares is not None else {},
            self.COL_CURRENT_VALUE:
                self.current_value.to_json() if self.current_value is not None else {}
        }

        return result