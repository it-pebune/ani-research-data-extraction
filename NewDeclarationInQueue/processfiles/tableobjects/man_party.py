from NewDeclarationInQueue.processfiles.tableobjects.declaration_data import DeclarationData
from NewDeclarationInQueue.processfiles.tableobjects.table_in_document import TableInDocument


class ManParty(TableInDocument):
    COL_PARTY = 'party'

    party: DeclarationData = None

    def __init__(self, party):
        self.party = party

    def check_validity(self):
        return self.party is not None

    def to_string(self):
        return self.party.to_string()

    def to_json(self):
        result = {self.COL_PARTY: self.party.to_json() if self.party is not None else {}}

        return result
