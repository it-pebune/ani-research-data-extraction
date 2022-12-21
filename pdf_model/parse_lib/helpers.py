def isEmptyLine(line: list): 
    emptyString = all(map(lambda x: x == "", line))
    dashedLineString = all(map(lambda x: x == "-", line))
    return emptyString or dashedLineString