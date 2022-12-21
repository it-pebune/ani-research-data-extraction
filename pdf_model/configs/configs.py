from pdf_model.parse_lib.parse_table_content import (
    parseSimpleTable, parseTableWithSubcategories,
    parseTableWithSubtablesAndSubcategories
    )

WealthDeclarationConfig = {
    "table_1": {
        "name": "Terenuri",
        "cols": [
            {
                "name": "Adresa sau zona",
                "format": {
                    "startingPattern": "Tara:",
                    "pattern": r'Tara: (\w+) Judet: (\w+) Localitate: (\w+)',
                    "patternOutputField": ['country', 'county', 'locality']
                },
                "outputType": 'dict'
            } ,
            {"name": "Categoria", "raw_name": "Categoria*", "outputType": 'str'},
            {"name": "Anul dobandirii", "raw_name": "Anul dobândirii", "outputType": 'str'},
            {"name": "Suprafata", "raw_name": "Suprafaţa", "outputType": 'str'},
            {"name": "Cota-parte", "raw_name": "Cota- parte", "outputType": 'str'},
            {"name": "Modul de dobandire", "raw_name": "Modul de dobândire", "outputType": 'str'},
            {"name": "Titularul", "raw_name": "Titularul", "outputType": 'str'}
        ],
        "parseContentFunc": parseSimpleTable
    },
    "table_2": {
        "name": "Cladiri",
        "cols": [
            {
                "name": "Adresa sau zona",
                "format": {
                    "startingPattern": "Tara:",
                    "pattern": r'Tara: (\w+) Judet: (\w+) Localitate: (\w+)',
                    "patternOutputField": ['country', 'county', 'locality']
                },
                "outputType": 'dict'
            } ,
            {"name": "Categoria", "raw_name": "Categoria*", "outputType": 'str'},
            {"name": "Anul dobandirii", "raw_name": "Anul dobândirii", "outputType": 'str'},
            {"name": "Suprafata", "raw_name": "Suprafaţa", "outputType": 'str'},
            {"name": "Cota-parte", "raw_name": "Cota- parte", "outputType": 'str'},
            {"name": "Modul de dobandire", "raw_name": "Modul de dobândire", "outputType": 'str'},
            {"name": "Titularul", "raw_name": "Titularul", "outputType": 'str'}
        ],
        "parseContentFunc": parseSimpleTable
    },
    "table_3": {
        "name": "Autovehicule/autoturisme, tractoare, maşini agricole, şalupe, iahturi şi alte mijloace de transport care sunt supuse înmatriculării, potrivit legii",
        "cols": [
            {"name": "Natura", "raw_name": "Natura", "outputType": 'str'} ,
            {"name": "Marca", "raw_name": "Marca", "outputType": 'str'},
            {"name": "Nr. Bucati", "raw_name": "Nr. de bucăţi", "outputType": 'str'},
            {"name": "Anul de fabricatie", "raw_name": "Anul de fabricaţie", "outputType": 'str'},
            {"name": "Modul de dobandire", "raw_name": "Modul de dobândire", "outputType": 'str'}
        ],
        "parseContentFunc": parseSimpleTable
    },
    "table_4": {
        "name": "Bunuri sub formă de metale preţioase, bijuterii, obiecte de artă şi de cult, colecţii de artă şi numismatică, obiecte care fac parte din patrimoniul cultural naţional sau universal, a căror valoare însumată depăşeşte 5.000 de euro",
        "cols": [
            {"name": "Descriere sumara", "raw_name": "Descriere sumară", "outputType": 'str'} ,
            {"name": "Anul dobandiriii", "raw_name": "Anul dobândiri", "outputType": 'str'},
            {"name": "Valoarea estimata", "raw_name": "Valoarea estimata", "outputType": 'str'}
        ],
        "parseContentFunc": parseSimpleTable
    },
    "table_5": {
        "name": "Bunuri mobile, a căror valoare depăşeşte 3.000 de euro fiecare, şi bunuri imobile înstrăinate în ultimele 12 luni",
        "cols": [
            {"name": "Natura bunului instrainat", "raw_name": "Natura bunului înstrăinat", "outputType": 'str'} ,
            {"name": "Data instrainarii", "raw_name": "Data înstrăinării", "outputType": 'str'},
            {"name": "Persoana care s-a instrainat", "raw_name": "Persoana catre care s-a înstrăinat", "outputType": 'str'},
            {"name": "Forma instrainarii", "raw_name": "Forma înstrăinării", "outputType": 'str'},
            {"name": "Valoarea", "raw_name": "Valoarea", "outputType": 'str'}
        ],
        "parseContentFunc": parseSimpleTable
    },
    "table_6": {
        "name": "Conturi şi depozite bancare, fonduri de investiţii, forme echivalente de economisire şi investire, inclusiv cardurile de credit, dacă valoarea însumată a tuturor acestora depăşeşte 5.000 de euro",
        "cols": [
            {
                "name": "Instituţia care administrează şi adresa acesteia", 
                "raw_name": "Instituţia care administrează şi adresa acesteia", 
                "outputType": 'str'
            },
            {"name": "Tipul", "raw_name": "Tipul*", "outputType": 'str'},
            {"name": "Valuta", "raw_name": "Valuta", "outputType": 'str'},
            {"name": "Deschis in anul", "raw_name": "Deschis în anul", "outputType": 'str'},
            {"name": "Sold/valoarea la zi", "raw_name": "Sold/valoare la zi", "outputType": 'str'}
        ],
        "parseContentFunc": parseSimpleTable
    },
    "table_7": {
        "name": "Plasamente, investiţii directe şi împrumuturi acordate, dacă valoarea de piaţă însumată a tuturor acestora depăşeşte 5.000 de euro",
        "cols": [
            {
                "name": "Emitent titlu/societatea în care persoana este acţionar sau asociat/beneficiar de împrumut", 
                "outputType": 'str'} ,
            {"name": "Tipul", "raw_name": "Tipul*'", "outputType": 'str'},
            {"name": "Număr de titluri/ cota de participare", "raw_name": "Număr de titluri/ cota de participare", "outputType": 'str'},
            {"name": "Valoarea totală la zi", "raw_name": "Valoarea totală la zi", "outputType": 'str'}
        ],
        "parseContentFunc": parseSimpleTable
    },
    "table_8": {
        "name": "Alte active producătoare de venituri nete, care însumate depăşesc echivalentul a 5.000 de euro pe an",
        "cols": [
            {"name": "Descriere", "raw_name": "Descriere","outputType": 'str'} ,
            {"name": "Valoarea", "raw_name": "Valoare", "outputType": 'str'},
            {"name": "Valuta", "raw_name": "Valuta","outputType": 'str'}
        ],
        "parseContentFunc": parseSimpleTable
    },
    "table_9": {
        "name": "Debite, ipoteci, garanţii emise în beneficiul unui terţ, bunuri achiziţionate în sistem leasing şi alte asemenea bunuri, dacă valoarea însumată a tuturor acestora depăşeşte 5.000 de euro",
        "cols": [
            {"name": "Creditor","raw_name": "Creditor", "outputType": 'str'} ,
            {"name": "Contractat in anul", "raw_name": "Creditor", "outputType": 'str'},
            {"name": "Scadent in anul", "raw_name": "Creditor", "outputType": 'str'},
            {"name": "Valoarea", "raw_name": "Creditor", "outputType": 'str'}
        ],
        "parseContentFunc": parseSimpleTable
    },
    "table_10": {
        "name": "Cadouri, servicii sau avantaje primite gratuit sau subvenţionate faţă de valoarea de piaţă, din partea unor persoane, organizaţii, societăţi comerciale, regii autonome, companii/societăţi naţionale sau instituţii publice româneşti sau străine, inclusiv burse, credite, garanţii, decontări de cheltuieli, altele decât cele ale angajatorului, a căror valoare individuală depăşeşte 500 de euro*",
        "cols": [
            {"name": "Cine a realizat venitul", "outputType": 'str'} ,
            {"name": "Sursa venitului: numele, adresa", "outputType": 'str'},
            {"name": "Serviciul prestat/Obiectul generator de venit", "outputType": 'str'},
            {"name": "Venitul anual încasat", "outputType": 'str'}
        ],
        "parseContentFunc": parseTableWithSubcategories
    },
    "table_11": {
        "name": "Venituri ale declarantului şi ale membrilor săi de familie, realizate în ultimul an fiscal încheiat (potrivit art. 41 din Legea nr. 571/2003 privind Codul fiscal, cu modificările şi completările ulterioare)",
        "cols": [
            {"name": "Cine a realizat venitul", "outputType": 'str'} ,
            {"name": "Sursa venitului: numele, adresa", "outputType": 'str'},
            {"name": "Serviciul prestat/Obiectul generator de venit", "outputType": 'str'},
            {"name": "Venitul anual încasat", "outputType": 'str'}
        ],
        "parseContentFunc": parseTableWithSubtablesAndSubcategories
    },
    "table_12": {
        "name": "Date",
        "cols": [
            {"name": "Data completarii", "outputType": 'str'} ,
            {"name": "Semnătura", "outputType": 'str'}
        ],
        "parseContentFunc": parseSimpleTable
    }
}