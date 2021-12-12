import re

def getSubstringBetweenStringFromFile(file_path, split_begin, split_end):
    output = ''
    with open(file_path) as file:
        buffer = file.read()
        start = buffer.find(split_begin) + len(split_begin)
        end = buffer.find(split_end)
        output = buffer[start:end]

        file.close()
    
    return output

def getTrailingInt(inputStr):
    m = re.search(r'\d+$', inputStr)
    return int(m.group()) if m else None

def getTrailingFloat(inputStr):
    m = re.search(r'\d+.\d+$', inputStr)
    return float(m.group()) if m else None