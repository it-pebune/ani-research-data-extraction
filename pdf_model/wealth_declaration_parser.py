import json
import camelot
from pdf_model.parse_lib.parse_raw_tables import parseRawTables2, parseTables
from pdf_model.parse_lib.parse_table_content import parseTable


class WealthDeclarationParser:

    def __init__(self, config):
        self.config = config

    def parse(self, filePath: str) -> None:
        try:
            tables = camelot.read_pdf(filePath, pages='all', line_scale=40)
            # parsed_tables = parseRawTables2(tables, self.config)
            parsed_tables = parseTables(tables, self.config)

            result = {}
            for _, table_with_config in enumerate(parsed_tables):
                table_config = table_with_config['table_config']
                if not table_config['rowBuilder']:
                    continue
                result[table_config['name']] = parseTable(table_with_config['table_content'], table_config)

        except FileNotFoundError as e:
            print("File doesn't exist." + e.strerror)

        r = {}
        for table_name, table_content in result.items():
            r[table_name] = [line.to_json() for line in table_content]

        # print(json.dumps(r, indent=4))
        return r
