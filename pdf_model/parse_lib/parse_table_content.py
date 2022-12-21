import json
import re
from collections import defaultdict


SubcategoryReg = r'([\d]+)\.([\d]+)\.? ([\w|\s]+)'
SubtableReg = r'([\d]+)\.? ([\w|\s]+)'


def _parseCellWithFormatting(cell_content: str, format_config: dict) -> str:
    if "startingPattern" in format_config:
        pos = cell_content.find(format_config["startingPattern"])
        if pos != -1:
            cell_content = cell_content[pos:]

    m = re.match(format_config["pattern"], cell_content, re.M|re.I)
    if not m:
        print("WTF", cell_content)
    parsed_cell_content = {}
    for [idx, field] in enumerate(format_config["patternOutputField"]):
        parsed_cell_content[field] = m.group(idx+1)
    
    return parsed_cell_content


def _parseLine(line: list[str], columns_config) -> list[dict]:
    if len(line) != len(columns_config):
        print("ERROR missmatch lines and columns")
        return []

    row_content = []
    for idx, config in enumerate(columns_config):
        cell_text = line[idx]
        parsed_cell = {
            "name": config["name"],
            "raw_cell": cell_text,
            "outputType": config["outputType"]
        }
        cell_text = cell_text.replace('\n', ' ')
        
        if "format" in config:
            parsed_cell_text = _parseCellWithFormatting(cell_text, config["format"])
        else:
            parsed_cell_text = cell_text

        parsed_cell["output"] = parsed_cell_text
        row_content.append(parsed_cell)
    
    return row_content    


def parseSimpleTable(header, raw_content, config) -> dict:
    content = [];
    
    for row in raw_content:
        parsed_line = _parseLine(row, config["cols"])
        content.append(parsed_line)
        
    return {"NO_CATEGORY": content}


def onlyFirstCellHasText(line: list[int]):
    non_empty_cells = 0
    for cell_text in line:
        if cell_text != "":
            non_empty_cells += 1
    return non_empty_cells == 1 and line[0] != ""

def isTableSubcategory(line: list, curr_subtable: int) -> bool:
    if not onlyFirstCellHasText(line):
        return False
    
    subcategory_cell = line[0]
    m = re.match(SubcategoryReg, subcategory_cell, re.M|re.I)
    if not m:
        print("ERROR not match", line)
        return False
    
    if len(m.groups()) == 3 and int(m[1]) == curr_subtable:
        return True
    else:
        import ipdb
        ipdb.set_trace()
        print("ERROR", m.groups(), subcategory_cell)
        return False
    

def extractTableSubcategory(line: list) -> str:
    m = re.match(SubcategoryReg, line[0], re.M|re.I)
    if not m:
        print("wtf extract", line)
    return m[3]
    


def isEmptyLine(line: list) -> bool:
    return all(map(lambda x: x == "", line))
    

def parseTableWithSubcategories(header, raw_content, config: dict) -> dict:
    content = defaultdict(list)
    current_category = None
    current_subtable_idx = 1
    
    for line in raw_content:
        if isTableSubcategory(line, current_subtable_idx):
            current_category = extractTableSubcategory(line)
            content[current_category] = []
        else:
            content[current_category].append(line)
            
    return content

def extractSubTableName(line: list) -> str:
    m = re.match(SubtableReg, line[0], re.M|re.I)
    if not m:
        print("ERROR - should be subtable", line)
        return None
    return m[2]

def _isSubtable(line: list, currentSubtable: int) -> bool:
    if not onlyFirstCellHasText(line):
        return False
    
    subtable_cell = line[0]
    m = re.match(SubtableReg, subtable_cell, re.M|re.I)
    if not m:
        return False
    
    if len(m.groups()) == 2 and int(m[1]) == currentSubtable+1:
        return True
    else:
        print("ERROR - should be subtable", line, m)
        return False



def parseTableWithSubtablesAndSubcategories(header, raw_content, config) -> dict:
    content = {}
    current_subtable, current_table_idx = None, 0
    current_category = None, None
    for line in raw_content:
        if _isSubtable(line, current_table_idx): 
            current_subtable = extractSubTableName(line)
            current_category = None
            current_table_idx += 1
            content[current_subtable] = {}
        elif isTableSubcategory(line, current_table_idx):
            current_category = extractTableSubcategory(line)
            content[current_subtable][current_category] = []
        else:
            if current_subtable not in content:
                print("ERROR - invalid table format - missing subtable", raw_content, content, current_subtable)
            if current_category not in content[current_subtable]:
                print("ERROR - invalid table format - missing category", raw_content, content, current_category)    
            content[current_subtable][current_category].append(_parseLine(line, config["cols"]))

    return content


def parseTable(header, raw_content, config):
    print("Processing table with Header:", header)
    parseContentFunc = config["parseContentFunc"]
    content = parseContentFunc(header, raw_content, config)
    # print("Content", content)
    return content
