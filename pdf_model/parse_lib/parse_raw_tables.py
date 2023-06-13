from fuzzywuzzy import fuzz
from NewDeclarationInQueue.processfiles.table_builders.contracts_builder import ContractsBuilder
from camelot.core import Table

from pdf_model.parse_lib.helpers import isEmptyLine


def parseTables(tables: list[Table], table_configs: dict):
    table_idx = 1
    config_idx = 1
    result = []

    # check first table
    current_table = {
        "data": tables[0].data,
        "page": tables[0].page,
    }
    while table_idx < len(tables) and config_idx < len(table_configs):
        config_key = 'table_{0}'.format(config_idx + 1)
        previous_config_key = 'table_{0}'.format(config_idx)
        if config_key == 'table_6':
            import ipdb
            ipdb.set_trace()
        should_merge = shouldMergeTables(current_table, tables[table_idx], table_configs[config_key])
        if not should_merge:
            result.append({"table_content": current_table["data"], "table_config": table_configs[previous_config_key]})
            current_table = {
                "data": tables[table_idx].data,
                "page": tables[table_idx].page,
            }
            table_idx += 1
            config_idx += 1

        else:
            if isCombiningMoreAccurateMainHeader(current_table["data"][-1], tables[table_idx].data[0],
                                                 table_configs[previous_config_key]):
                current_table = combineWithLineMerge(current_table, tables[table_idx])
            elif isCombiningMoreAccurateHeader(current_table["data"][-1], tables[table_idx].data[0],
                                               table_configs[previous_config_key]):
                current_table = combineWithLineMerge(current_table, tables[table_idx])
            elif nextTableFirstRowHasEmptyLines(tables[table_idx].data[0]):
                current_table = combineWithLineMerge(current_table, tables[table_idx])
            else:
                current_table = combineWithoutLineMerge(current_table, tables[table_idx])

    for parsedTable in result:
        parsedTable['table_content'] = [
            [word.replace('\n', ' ') for word in line] for line in parsedTable['table_content']
        ]

    return result


def combineWithLineMerge(acc_table: dict, nextTable: Table) -> dict:
    endings_combined = _combineTwoLines(acc_table["data"][-1], nextTable.data[0])
    acc_table["data"][-1] = endings_combined
    acc_table["data"] = acc_table["data"] + nextTable.data[1:]
    acc_table["page"] = nextTable.page

    return acc_table


def combineWithoutLineMerge(acc_table: dict, nextTable: Table) -> dict:
    acc_table["data"] = acc_table["data"] + nextTable.data
    acc_table["page"] = nextTable.page

    return acc_table


def isCombiningMoreAccurateMainHeader(last_line, first_line, config):
    if not "main_header" in config or not config['main_header']:
        return False

    if not onlyFirstCellHasText(last_line):
        return False

    if not onlyFirstCellHasText(first_line):
        return False

    score = fuzz.ratio(last_line, config["main_header"])
    lines_combined = _combineTwoLines(last_line, first_line)
    score_combined = score = fuzz.ratio(lines_combined, config["main_header"])
    if score_combined > score and score_combined > 90:
        return True

    return False


def isCombiningMoreAccurateHeader(last_line, first_line, config):
    # if not "main_header" in config or not config['main_header']:
    #     return False

    score = computeHeaderScore(last_line, config['cols'])
    lines_combined = _combineTwoLines(last_line, first_line)
    score_combined = computeHeaderScore(lines_combined, config['cols'])
    if score_combined > score and score_combined > 90:
        return True

    return False


def nextTableFirstRowHasEmptyLines(first_line: list[str]) -> bool:
    return any(map(lambda cell: cell == "", first_line))


def shouldMergeTables(acc_table: dict, tableB: Table, table_configB: dict) -> bool:
    if len(acc_table["data"]) == 0 or len(tableB.data) == 0:
        return True

    if (len(acc_table["data"][0]) != len(tableB.data[0])) and len(acc_table["data"][-1]) != 1:
        return False

    # Consecutive tables on the same page shoud not be merged
    if acc_table["page"] == tableB.page:
        return False

    is_main_header, _ = _isMainHeader(tableB.data[0], table_configB)
    if is_main_header:
        return False

    # if the first line on the following page is header of table with main header
    # then we should merge it
    is_header = _isTableHeader(tableB.data[0], table_configB)
    if is_header:
        return "main_header" in table_configB

    return True


def _combineTwoLines(lineA: list[str], lineB: list[str]) -> list[str]:
    return [lineA[i] + ' ' + lineB[i] for i in range(len(lineA))]


def parseRawTable(scanned_tables) -> list[list[str]]:
    raw_content = []

    return raw_content


def _parseMe(tables):
    raw_content = []
    import ipdb
    ipdb.set_trace()
    for table in tables:
        raw_content += [[table.df[col][row] for col in range(len(table.cols))] for row in range(len(table.rows))]

    raw_content = [[word.replace('\n', ' ') for word in line] for line in raw_content]
    return raw_content


def parseRawTables2(tables, tables_config) -> list[dict]:
    x = _parseMe(tables)
    import ipdb
    ipdb.set_trace()
    parsed_tables: list[dict] = []
    contor: int = 0
    current_config = None
    current_main_header: list[str] = None
    current_header: list[str] = None
    current_content: list[list[str]] = []

    while contor < len(x):
        line = x[contor]
        is_main_header, table_config = _isMainHeader(line, tables_config)

        if is_main_header:
            # here we should append all the previous data
            if current_config:
                parsed_tables.append({
                    "main_header": current_main_header,
                    "header": current_header,
                    "content": current_content,
                    "config": current_config
                })

            # start processing the new table
            current_main_header = line
            current_config = table_config
            current_header = None
            current_content = []

            contor += 1
            continue

        # check if it is a header from a table with main header
        if current_main_header:
            if "header" in current_config and current_config["header"] == False:
                current_content.append(line)
                contor += 1
                continue

            header_score = computeHeaderScore(line, current_config["cols"])
            if contor + 1 < len(x) and len(line) == len(x[contor + 1]):
                next_line_combined = [line[i] + ' ' + x[contor + 1][i] for i in range(len(line))]
                scoreWithFollowingLine = computeHeaderScore(next_line_combined, current_config["cols"])
                if scoreWithFollowingLine > header_score and scoreWithFollowingLine > 90:
                    current_header = next_line_combined
                    contor += 2
                    continue

            if header_score > 90:
                current_header = line
                contor += 1
                continue

        # TODO UPDATE NAME
        # check if it is a header from a table without main header
        is_header, config = _isHeader2(line, tables_config)
        if is_header:
            # if we already have a header, then it means that a table with a new header is starting
            # we need to add things up
            if current_config:
                parsed_tables.append({
                    "main_header": current_main_header,
                    "header": current_header,
                    "content": current_content,
                    "config": current_config
                })

            # start processing the new table
            current_main_header = None
            current_header = line
            current_config = config
            current_content = []
            contor += 1
            continue

        # we need to check if the following line is part of the same one

        next_line_combined = [line[i] + ' ' + x[contor + 1][i] for i in range(len(line))]
        current_content.append(line)
        contor += 1

    return parsed_tables


def _shouldCombineWithNextLine(line_idx: int, raw_tables: list[list[str]]) -> bool:
    if line_idx + 1 >= len(raw_tables):
        return False

    line = raw_tables[line_idx]
    next_line = raw_tables[line_idx + 1]

    if len(line) != len(next_line):
        return False

    # maybe I should check if there is not a subcategory line


def _combineWithNextLine(line_idx: int, raw_tables: list[list[str]]) -> list[str]:
    line = raw_tables[line_idx]
    if line_idx + 1 >= len(raw_tables):
        return line

    return [line[i] + ' ' + raw_tables[line_idx + 1][i] for i in range(len(line))]


def computeHeaderScore(line, cols) -> float:
    if len(line) != len(cols):
        return 0.0

    score = 0.0
    for idx, cell_text in enumerate(line):
        score += fuzz.ratio(cell_text, cols[idx]["name"])

    return score / len(cols)


# TODO CHECK WHAT TO DO WITH THIS FUNCTION
def _parseRawTable(table) -> tuple[list[str], list[list[str]]]:
    header = [table.df[i][0] for i in range(len(table.cols))]
    header = list(map(lambda word: word.replace('\n', ' '), header))
    raw_content = [[table.df[col][row] for col in range(len(table.cols))] for row in range(1, len(table.rows))]
    raw_content = [[word.replace('\n', ' ') for word in line] for line in raw_content]
    print(header)
    print(raw_content)
    print('=======')
    return [header, raw_content]


def onlyFirstCellHasText(line: list[str]) -> bool:
    if len(line) < 1:
        return False

    return len(line[0]) > 0 and isEmptyLine(line[1:])


def _isMainHeader(line: list[str], config: dict) -> tuple[bool, dict]:
    if isEmptyLine(line):
        return False, None

    if not onlyFirstCellHasText(line):
        return False, None

    max_config_score = -1
    max_config_key = None
    for table_config_key, table_config in config.items():
        if 'main_header' not in table_config:
            continue

        score = fuzz.ratio(line[0], table_config["main_header"])
        if score > max_config_score and score > 90:
            max_config_score = score
            max_config_key = table_config_key

    if not max_config_key:
        return False, None

    return True, config[max_config_key]


def _isHeader2(line: list[str], config: dict) -> tuple[bool, dict, float]:
    if isEmptyLine(line):
        return False, None

    maxScore = -1
    max_score_config_key = None
    for table_config_key, table_config in config.items():
        if len(line) != len(table_config['cols']):
            continue

        score = computeHeaderScore(line, table_config['cols'])
        if score > maxScore and score > 70:
            max_score_config_key = table_config_key
            maxScore = score

    if max_score_config_key:
        return True, config[max_score_config_key]

    return False, None


def _isTableHeader(line: list[str], table_config: dict) -> bool:
    if isEmptyLine(line):
        return False

    if len(line) != len(table_config['cols']):
        return False

    score = computeHeaderScore(line, table_config['cols'])
    if score < 70:
        return False

    return True
