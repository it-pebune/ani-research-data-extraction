from collections import defaultdict
import json
import re
from fuzzywuzzy import fuzz

from pdf_model.parse_lib.helpers import isEmptyLine


def parseRawTables(tables, config) -> list[dict]:
    parsed_tables = []

    for table in tables:
        header, raw_content = _parseRawTable(table)
        is_header, table_config = _isHeader(header, config)
        if is_header:
            parsed_tables.append({
                "header": header,
                "content": raw_content,
                "table_config": table_config
            })
        else:
            raw_content.insert(0, header)
            parsed_tables[-1]["content"].extend(raw_content)

    return parsed_tables

def _isHeader(line: list[str], config: dict) -> tuple[bool, dict]:
    if isEmptyLine(line):
        return False, None
    
    potential_headers: list[tuple[str, dict]] = []
    for table_key, table_config in config.items():
        if len(table_config['cols']) == len(line):
            potential_headers.append((table_key, table_config))
        
    maxScore = -1
    maxScoreIdx = -1
    for potential_idx, potential_config in enumerate(potential_headers):
        table_key, table_config = potential_config
        score = 0
        for idx, cell_text in enumerate(line):
            score += fuzz.ratio(cell_text, table_config["cols"][idx]["name"])
        if score > maxScore and score > 0.7:
            maxScoreIdx = potential_idx
    
    if maxScoreIdx != -1:
        return True, potential_headers[potential_idx][1]
    
    return False, None
                

def _parseRawTable(table) -> tuple[list[str], list[list[str]]]:
    header = [table.df[i][0] for i in range(len(table.cols))]
    header = list(map(lambda word: word.replace('\n', ' '), header))
    raw_content = [[table.df[col][row] for col in range(len(table.cols))] for row in range(1, len(table.rows))]
    raw_content = [[word.replace('\n', ' ') for word in line] for line in raw_content]
    
    return [header, raw_content]

