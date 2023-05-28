from fuzzywuzzy import fuzz
from NewDeclarationInQueue.processfiles.table_builders.contracts_builder import ContractsBuilder

from pdf_model.parse_lib.helpers import isEmptyLine


def _parseMe(tables):
    raw_content = []
    for table in tables:
        raw_content += [[table.df[col][row] for col in range(len(table.cols))] for row in range(len(table.rows))]

    raw_content = [[word.replace('\n', ' ') for word in line] for line in raw_content]
    return raw_content


def parseRawTables2(tables, tables_config) -> list[dict]:
    x = _parseMe(tables)

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
                # print(next_line_combined)
                # print("score with following line", scoreWithFollowingLine, current_config["cols"])
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

        current_content.append(line)
        contor += 1

    return parsed_tables


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
