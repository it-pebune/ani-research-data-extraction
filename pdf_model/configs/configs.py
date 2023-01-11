from NewDeclarationInQueue.processfiles.table_builders.art_builder import ArtBuilder
from NewDeclarationInQueue.processfiles.table_builders.building_table_builder import BuildingTableBuilder
from NewDeclarationInQueue.processfiles.table_builders.debt_builder import DebtBuilder
from NewDeclarationInQueue.processfiles.table_builders.finance_builder import FinanceBuilder
from NewDeclarationInQueue.processfiles.table_builders.gift_builder import GiftBuilder
from NewDeclarationInQueue.processfiles.table_builders.income_builder import IncomeBuilder
from NewDeclarationInQueue.processfiles.table_builders.investment_builder import InvestmentBuilder
from NewDeclarationInQueue.processfiles.table_builders.mobile_builder import MobileBuilder
from NewDeclarationInQueue.processfiles.table_builders.parcel_table_builder import ParcelTableBuilder
from NewDeclarationInQueue.processfiles.table_builders.transport_builder import TransportBuilder
from pdf_model.parse_lib.parse_table_content import (parseSimpleTable, parseTableWithSubcategories,
                                                     parseTableWithSubtablesAndSubcategories)

WealthDeclarationConfig = {
    "table_1": {
        "name": "parcels",
        "cols": [{
            "name": "address",
            "format": {
                "startingPattern": "Tara:",
                "pattern": r'Tara: (\w+) Judet: (\w+) Localitate: (\w+)',
                "patternOutputField": ['country', 'county', 'locality']
            },
            "outputType": 'dict'
        }, {
            "name": "cateogory",
            "outputType": 'str'
        }, {
            "name": "year_of_purchase",
            "outputType": 'str'
        }, {
            "name": "surface",
            "outputType": 'str'
        }, {
            "name": "quota",
            "outputType": 'str'
        }, {
            "name": "type_of_aquisition",
            "outputType": 'str'
        }, {
            "name": "owner",
            "outputType": 'str'
        }],
        "parseContentFunc": parseSimpleTable,
        "rowBuilder": ParcelTableBuilder
    },
    "table_2": {
        "name": "buildings",
        "cols": [{
            "name": "address",
            "format": {
                "startingPattern": "Tara:",
                "pattern": r'Tara: (\w+) Judet: (\w+) Localitate: (\w+)',
                "patternOutputField": ['country', 'county', 'locality']
            },
            "outputType": 'dict'
        }, {
            "name": "category",
            "outputType": 'str'
        }, {
            "name": "year_of_purchase",
            "outputType": 'str'
        }, {
            "name": "surface",
            "outputType": 'str'
        }, {
            "name": "quota",
            "outputType": 'str'
        }, {
            "name": "type_of_aquisition",
            "outputType": 'str'
        }, {
            "name": "owner",
            "outputType": 'str'
        }],
        "parseContentFunc": parseSimpleTable,
        "rowBuilder": BuildingTableBuilder
    },
    "table_3": {
        "name": "transport",
        "cols": [{
            "name": "type_of_transport",
            "outputType": 'str'
        }, {
            "name": "model",
            "outputType": 'str'
        }, {
            "name": "number_of_pieces",
            "outputType": 'str'
        }, {
            "name": "year_of_production",
            "outputType": 'str'
        }, {
            "name": "type_of_aquisition",
            "outputType": 'str'
        }],
        "parseContentFunc": parseSimpleTable,
        "rowBuilder": TransportBuilder
    },
    "table_4": {
        "name": "art",
        "cols": [{
            "name": "short_description",
            "outputType": 'str'
        }, {
            "name": "year_of_aquisition",
            "outputType": 'str'
        }, {
            "name": "estimated_value",
            "outputType": 'str'
        }],
        "parseContentFunc": parseSimpleTable,
        "rowBuilder": ArtBuilder
    },
    "table_5": {
        "name": "mobile",
        "cols": [{
            "name": "",
            "outputType": 'str'
        }, {
            "name": "Data instrainarii",
            "outputType": 'str'
        }, {
            "name": "Persoana care s-a instrainat",
            "outputType": 'str'
        }, {
            "name": "Forma instrainarii",
            "outputType": 'str'
        }, {
            "name": "Valoarea",
            "outputType": 'str'
        }],
        "parseContentFunc": parseSimpleTable,
        "rowBuilder": MobileBuilder
    },
    "table_6": {
        "name": "finance",
        "cols": [{
            "name": "Instituţia care administrează şi adresa acesteia",
            "outputType": 'str'
        }, {
            "name": "Tipul",
            "outputType": 'str'
        }, {
            "name": "Valuta",
            "outputType": 'str'
        }, {
            "name": "Deschis in anul",
            "outputType": 'str'
        }, {
            "name": "Sold/valoarea la zi",
            "outputType": 'str'
        }],
        "parseContentFunc": parseSimpleTable,
        "rowBuilder": FinanceBuilder
    },
    "table_7": {
        "name": "investment",
        "cols": [{
            "name": "Emitent titlu/societatea în care persoana este acţionar sau asociat/beneficiar de împrumut",
            "outputType": 'str'
        }, {
            "name": "Tipul",
            "outputType": 'str'
        }, {
            "name": "Număr de titluri/ cota de participare",
            "outputType": 'str'
        }, {
            "name": "Valoarea totală la zi",
            "outputType": 'str'
        }],
        "parseContentFunc": parseSimpleTable,
        "rowBuilder": InvestmentBuilder
    },
    "table_8": {
        "name": "investment_others",
        "cols": [{
            "name": "Descriere",
            "outputType": 'str'
        }, {
            "name": "Valoarea",
            "outputType": 'str'
        }, {
            "name": "Valuta",
            "outputType": 'str'
        }],
        "parseContentFunc": parseSimpleTable,
        "rowBuilder": None
    },
    "table_9": {
        "name": "debts",
        "cols": [{
            "name": "Creditor",
            "outputType": 'str'
        }, {
            "name": "Contractat in anul",
            "outputType": 'str'
        }, {
            "name": "Scadent in anul",
            "outputType": 'str'
        }, {
            "name": "Valoarea",
            "outputType": 'str'
        }],
        "parseContentFunc": parseSimpleTable,
        "rowBuilder": DebtBuilder
    },
    "table_10": {
        "name": "gifts",
        "cols": [{
            "name": "Cine a realizat venitul",
            "outputType": 'str'
        }, {
            "name": "Sursa venitului: numele, adresa",
            "outputType": 'str'
        }, {
            "name": "Serviciul prestat/Obiectul generator de venit",
            "outputType": 'str'
        }, {
            "name": "Venitul anual încasat",
            "outputType": 'str'
        }],
        "parseContentFunc": parseTableWithSubcategories,
        "rowBuilder": GiftBuilder
    },
    "table_11": {
        "name": "income",
        "cols": [{
            "name": "Cine a realizat venitul",
            "outputType": 'str'
        }, {
            "name": "Sursa venitului: numele, adresa",
            "outputType": 'str'
        }, {
            "name": "Serviciul prestat/Obiectul generator de venit",
            "outputType": 'str'
        }, {
            "name": "Venitul anual încasat",
            "outputType": 'str'
        }],
        "parseContentFunc": parseTableWithSubtablesAndSubcategories,
        "rowBuilder": IncomeBuilder
    },
    "table_12": {
        "name": "Date",
        "cols": [{
            "name": "Data completarii",
            "outputType": 'str'
        }, {
            "name": "Semnătura",
            "outputType": 'str'
        }],
        "parseContentFunc": parseSimpleTable,
        "rowBuilder": None
    }
}