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
            result = {}
            for idx, table_with_config in enumerate(parsed_tables_with_configs):
                table_config = self.config["table_{0}".format(idx + 1)]
                if not table_config["rowBuilder"]:
                    continue
                result[table_config["name"]] = parseTable(table_with_config['content'], table_config)
        except FileNotFoundError as e:
            print("File doesn't exist." + e.strerror)

        r = {}
        for table_name, table_content in result.items():
            r[table_name] = [line.to_json() for line in table_content]

        print(json.dumps(r, indent=4))
        return None
