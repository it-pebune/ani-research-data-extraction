import json
import pprint

import camelot
from pdf_model.parse_lib.parse_raw_tables import parseRawTables
from pdf_model.parse_lib.parse_table_content import parseTable


class WealthDeclarationParser:

    def __init__(self, config):
        self.config = config
    
    def parse(self, filePath: str) -> None:
        try:
            tables = camelot.read_pdf(filePath, pages='all', line_scale=40)
            parsed_tables_with_configs = parseRawTables(tables, self.config)
            result = []
            for idx, table_with_config in enumerate(parsed_tables_with_configs):
                result.append(parseTable(table_with_config["header"], table_with_config['content'], self.config["table_{0}".format(idx + 1)]))
        except FileNotFoundError as e:
            print("File doesn't exist." + e.strerror)

        for parsed_table in result:
            print(parsed_table)
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(dict(parsed_table))

        return None
