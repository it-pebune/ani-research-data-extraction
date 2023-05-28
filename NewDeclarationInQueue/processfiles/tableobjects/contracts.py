from NewDeclarationInQueue.processfiles.tableobjects.declaration_data import DeclarationData
from NewDeclarationInQueue.processfiles.tableobjects.table_in_document import TableInDocument


class Contracts(TableInDocument):
    COL_OWNER = 'owner'
    COL_INSITUTION = 'institution'
    COL_PROCEDURE = 'procedure'
    COL_CONTRACT_TYPE = 'contract_type'
    COL_DATE_OF_CONTRACT = 'date_of_contract'
    COL_DURATION = 'duration'
    COL_VALUE = 'value'
    COL_PERSON_TYPE = 'person_type'

    owner: DeclarationData = None
    institution: DeclarationData = None
    procedure: DeclarationData = None
    contract_type: DeclarationData = None
    date_of_contract: DeclarationData = None
    duration: DeclarationData = None
    value: DeclarationData = None
    person_type: DeclarationData = None

    def __init__(self,
                 owner,
                 institution,
                 procedure,
                 contract_type,
                 date_of_contract,
                 duration,
                 value,
                 person_type='unknown'):
        self.owner = owner
        self.institution = institution
        self.procedure = procedure
        self.contract_type = contract_type
        self.date_of_contract = date_of_contract
        self.duration = duration
        self.value = value
        self.person_type = person_type

    def check_validity(self):
        return self.owner is not None or self.institution is not None or \
                self.procedure is not None or self.contract_type is not None or \
                self.date_of_contract is not None or \
                self.duration is not None  or self.value is not None or self.person_type is not None

    def to_string(self):
        return self.owner.to_string() + ' - ' + self.institution.to_string() + ' - ' + self.procedure.to_string() + ' - ' + \
            self.contract_type.to_string() + ' - ' + self.date_of_contract.to_string() + ' - ' + \
            self.duration.to_string() + ' - ' + self.value + '-' + self.person_type

    def to_json(self):
        result = {
            self.COL_OWNER: self.owner.to_json() if self.owner is not None else {},
            self.COL_INSITUTION: self.institution.to_json() if self.institution is not None else {},
            self.COL_PROCEDURE: self.procedure.to_json() if self.procedure is not None else {},
            self.COL_CONTRACT_TYPE: self.contract_type.to_json() if self.contract_type is not None else {},
            self.COL_DATE_OF_CONTRACT: self.date_of_contract.to_json() if self.date_of_contract is not None else {},
            self.COL_DURATION: self.duration.to_json() if self.duration is not None else {},
            self.COL_VALUE: self.value.to_json() if self.value is not None else {},
            self.COL_PERSON_TYPE: self.person_type.to_json() if self.value is not None else {}
        }

        return result
