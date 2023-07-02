from NewDeclarationInQueue.processfiles.table_builders.art_builder import \
    ArtBuilder
from NewDeclarationInQueue.processfiles.table_builders.contracts_builder import ContractsBuilder
from NewDeclarationInQueue.processfiles.table_builders.man_party_builder import \
    ManagementPartyBuilder
from NewDeclarationInQueue.processfiles.table_builders.building_table_builder import \
    BuildingTableBuilder
from NewDeclarationInQueue.processfiles.table_builders.debt_builder import \
    DebtBuilder
from NewDeclarationInQueue.processfiles.table_builders.finance_builder import \
    FinanceBuilder
from NewDeclarationInQueue.processfiles.table_builders.gift_builder import \
    GiftBuilder
from NewDeclarationInQueue.processfiles.table_builders.income_builder import \
    IncomeBuilder
from NewDeclarationInQueue.processfiles.table_builders.investment_builder import \
    InvestmentBuilder
from NewDeclarationInQueue.processfiles.table_builders.man_commercial_builder import \
    ManCommercialBuilder
from NewDeclarationInQueue.processfiles.table_builders.member_quality_builder import MemberQualityBuilder
from NewDeclarationInQueue.processfiles.table_builders.mobile_builder import \
    MobileBuilder
from NewDeclarationInQueue.processfiles.table_builders.parcel_table_builder import \
    ParcelTableBuilder
from NewDeclarationInQueue.processfiles.table_builders.transport_builder import \
    TransportBuilder
from NewDeclarationInQueue.processfiles.tableobjects.man_professional import \
    ManProfessional
from pdf_model.parse_lib.parse_table_content import (parseSimpleTable, parseTableWithSpecialHeader,
                                                     parseTableWithSubcategories,
                                                     parseTableWithSubcategoriesWithSpecialHeader,
                                                     parseTableWithSubtablesAndSubcategories)

WealthDeclarationConfig = {
    "table_1": {
        "name": "parcels",
        "cols": [
            {
                "name": "adresa sau zona",
                # "format": {
                #     "startingPattern": "Tara:",
                #     "pattern": r'Tara: (\w+) Judet: (\w+) Localitate: (\w+)',
                #     "patternOutputField": ['country', 'county', 'locality']
                # },
                # "outputType": 'dict'
                "outputType": 'str'
            },
            {
                "name": "categoria*",
                "outputType": 'str'
            },
            {
                "name": "anul dobandirii",
                "outputType": 'str'
            },
            {
                "name": "suprafata",
                "outputType": 'str'
            },
            {
                "name": "cota-parte",
                "outputType": 'str'
            },
            {
                "name": "modul de dobandire",
                "outputType": 'str'
            },
            {
                "name": "titularul",
                "outputType": 'str'
            }
        ],
        "parseContentFunc": parseSimpleTable,
        "rowBuilder": ParcelTableBuilder
    },
    "table_2": {
        "name": "buildings",
        "cols": [
            {
                "name": "adresa sau zona",
                # "format": {
                #     "startingPattern": "Tara:",
                #     "pattern": r'Tara: (\w+) Judet: (\w+) Localitate: (\w+)',
                #     "patternOutputField": ['country', 'county', 'locality']
                # },
                # "outputType": 'dict'
                "outputType": 'str'
            },
            {
                "name": "categoria*",
                "outputType": 'str'
            },
            {
                "name": "Anul dobândirii",
                "outputType": 'str'
            },
            {
                "name": "Suprafata",
                "outputType": 'str'
            },
            {
                "name": "cota-parte",
                "outputType": 'str'
            },
            {
                "name": "modul de dobândire",
                "outputType": 'str'
            },
            {
                "name": "titularul",
                "outputType": 'str'
            }
        ],
        "parseContentFunc": parseSimpleTable,
        "rowBuilder": BuildingTableBuilder
    },
    "table_3": {
        "name": "transport",
        "cols": [{
            "name": "natura",
            "outputType": 'str'
        }, {
            "name": "marca",
            "outputType": 'str'
        }, {
            "name": "nr. de bucati",
            "outputType": 'str'
        }, {
            "name": "anul de fabricatie",
            "outputType": 'str'
        }, {
            "name": "modul de dobândire",
            "outputType": 'str'
        }],
        "parseContentFunc": parseSimpleTable,
        "rowBuilder": TransportBuilder
    },
    "table_4": {
        "name": "art",
        "cols": [{
            "name": "descriere sumară",
            "outputType": 'str'
        }, {
            "name": "anul dobândiri",
            "outputType": 'str'
        }, {
            "name": "valoarea estimata",
            "outputType": 'str'
        }],
        "parseContentFunc": parseSimpleTable,
        "rowBuilder": ArtBuilder
    },
    "table_5": {
        "name": "mobile",
        "cols": [{
            "name": "Natura bunului înstrăinat",
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

InterestDeclarationConfig = {
    "table_1": {
        "main_header": [
            "Asociat sau acţionar la societăţi comerciale, companii/societăţi naţionale, instituţii de credit, grupuri de interes economic, precum şi membru în asociaţii, fundaţii sau alte organizaţii neguvernamentale:"
        ],
        "name": "company_associate",
        "cols": [
            {
                "name": "company",
                # "format": {
                #     # "startingPattern": "Tara:",
                #     "pattern": r'Tara: (\w+) Judet: (\w+) Localitate: (\w+)',
                #     "patternOutputField": ['country', 'county', 'locality']
                # },
                # "outputType": 'dict'
                "outputType": 'str'
            },
            {
                "name": "position",
                "outputType": 'str'
            },
            {
                "name": "quantity",
                "outputType": 'str'
            },
            {
                "name": "total_value",
                "outputType": 'str'
            }
        ],
        # TODO
        "parseContentFunc": parseTableWithSpecialHeader,
        "rowBuilder": MemberQualityBuilder
    },
    "table_2": {
        "name": "management_commercial",
        "main_header": [
            "Calitatea de membru în organele de conducere, administrare şi control ale societăţilor comerciale, ale companiilor/societăţilor naţionale, ale instituţiilor de credit, ale grupurilor de interes economic, ale asociaţiilor sau fundaţiilor ori ale altor organizaţii neguvernamentale:"
        ],
        "cols": [
            {
                "name": "company",
                # "format": {
                #     "startingPattern": "Tara:",
                #     "pattern": r'Tara: (\w+) Judet: (\w+) Localitate: (\w+)',
                #     "patternOutputField": ['country', 'county', 'locality']
                # },
                "outputType": 'str'
            },
            {
                "name": "position",
                "outputType": 'str'
            },
            {
                "name": "value_of_shares",
                "outputType": 'str'
            }
        ],
        #TODO
        "parseContentFunc": parseTableWithSpecialHeader,
        "rowBuilder": ManCommercialBuilder
    },
    "table_3": {
        "main_header": ["Calitatea de membru în cadrul asociaţiilor profesionale şi/sau sindicale"],
        "header": False,
        "name": "management_professional",
        "cols": [{
            "name": "company",
            "outputType": 'str'
        }],
        "parseContentFunc": parseSimpleTable,
        "rowBuilder": ManProfessional
    },
    "table_4": {
        "main_header": [
            "Calitatea de membru în organele de conducere, administrare şi control, retribuite sau neretribuite, deţinute în cadrul partidelor politice, funcţia deţinută şi denumirea partidului politic"
        ],
        "header": False,
        "name": "management_party",
        "cols": [{
            "name": "party",
            "outputType": 'str'
        }],
        # TODO
        "parseContentFunc": parseSimpleTable,
        "rowBuilder": ManagementPartyBuilder
    },
    "table_5": {
        "main_header": [
            "Contracte, inclusiv cele de asistenţă juridică, consultanță juridică, consultanţă şi civile, obţinute ori aflate în derulare în timpul exercitării funcţiilor, mandatelor sau demnităţilor publice finanţate de la bugetul de stat, local şi din fonduri externe ori încheiate cu societăţi comerciale cu capital de stat sau unde statul este acţionar majoritar/minoritar:"
        ],
        "header": True,
        'subcategories': [
            'Titular', 'Soţ/soţie', 'Rude de gradul I ale titularului',
            'Societăţi comerciale/ Persoană fizică autorizată/ Asociaţii familiale/ Cabinete individuale, cabinete asociate, societăţi civile profesionale sau societăţi civile profesionale cu răspundere limitată care desfăşoară profesia de avocat/ Organizaţii neguvernamentale/ Fundaţii/ Asociaţi'
        ],
        "name": "contracts",
        "cols": [{
            "name": "5.1 Beneficiarul de contract: numele, prenumele / denumirea şi adresa",
            "outputType": 'str'
        }, {
            "name": "Instituţia contractantă: denumirea şi adresa",
            "outputType": 'str'
        }, {
            "name": "Procedura prin care a fost încredinţat contractul",
            "outputType": 'str'
        }, {
            "name": "Tipul contractului",
            "outputType": 'str'
        }, {
            "name": "Data încheierii contractului",
            "outputType": 'str'
        }, {
            "name": "Durata contractului",
            "outputType": 'str'
        }, {
            "name": "Valoarea totală a contractului",
            "outputType": 'str'
        }],
        # TODO
        "parseContentFunc": parseTableWithSubcategoriesWithSpecialHeader,
        "rowBuilder": ContractsBuilder
    },
    "table_6": {
        "main_header": ["Data completării Semnătura"],
        "name": "Date",
        "cols": [{
            "name": "Data completarii",
            "outputType": 'str'
        }
                 #          , {
                 #     "name": "Semnătura",
                 #     "outputType": 'str'
                 # }],
                ],
        "parseContentFunc": parseSimpleTable,
        "rowBuilder": None
    }
}
