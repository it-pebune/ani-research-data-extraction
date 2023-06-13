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


def computeHeaderScore(line, cols) -> float:
    if len(line) != len(cols):
        return 0.0

    score = 0.0
    for idx, cell_text in enumerate(line):
        score += fuzz.ratio(cell_text, cols[idx]["name"])

    return score / len(cols)


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


def _isTableHeader(line: list[str], table_config: dict) -> bool:
    if isEmptyLine(line):
        return False

    if len(line) != len(table_config['cols']):
        return False

    score = computeHeaderScore(line, table_config['cols'])
    if score < 70:
        return False

    return True
