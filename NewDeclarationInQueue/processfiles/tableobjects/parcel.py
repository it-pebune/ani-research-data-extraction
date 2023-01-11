from NewDeclarationInQueue.processfiles.tableobjects.declaration_data import DeclarationData
from NewDeclarationInQueue.processfiles.tableobjects.table_in_document import TableInDocument


class Parcel(TableInDocument):
    COL_ADDRESS = 'address'
    COL_CATEGORY = 'category'
    COL_YEAR_OF_PURCHASE = 'year_of_purchase'
    COL_SURFACE = 'surface'
    COL_QUOTA = 'quota'
    COL_TYPE_OF_AQUISITION = 'type_of_aquisition'
    COL_OWNER = 'owner'

    address: DeclarationData = None
    category: DeclarationData = None
    year_of_purchase: DeclarationData = None
    surface: DeclarationData = None
    quota: DeclarationData = None
    type_of_aquisition: DeclarationData = None
    owner: DeclarationData = None

    def __init__(self, address, category, year_of_purchase, surface, quota, type_of_aquisition, owner):
        self.address = address
        self.category = category
        self.year_of_purchase = year_of_purchase
        self.surface = surface
        self.quota = quota
        self.type_of_aquisition = type_of_aquisition
        self.owner = owner

    def check_validity(self):
        return self.address is not None or self.category is not None or self.year_of_purchase is not None or \
                self.surface is not None or self.quota is not None or self.type_of_aquisition is not None or \
                self.owner is not None

    def to_string(self):
        return self.address.to_string() + ' - ' + self.category.to_string() + ' - ' + self.year_of_purchase.to_string() + ' - ' + \
            self.surface.to_string() + ' - ' + self.quota.to_string() + ' - ' + self.type_of_aquisition.to_string() + ' - ' + \
            self.owner

    def to_json(self):
        result = {
            self.COL_ADDRESS:
                self.address.to_json() if self.address is not None else {},
            self.COL_CATEGORY:
                self.category.to_json() if self.category is not None else {},
            self.COL_YEAR_OF_PURCHASE:
                self.year_of_purchase.to_json() if self.year_of_purchase is not None else {},
            self.COL_SURFACE:
                self.surface.to_json() if self.surface is not None else {},
            self.COL_QUOTA:
                self.quota.to_json() if self.quota is not None else {},
            self.COL_TYPE_OF_AQUISITION:
                self.type_of_aquisition.to_json() if self.type_of_aquisition is not None else {},
            self.COL_OWNER:
                self.owner.to_json() if self.owner is not None else {}
        }

        return result
