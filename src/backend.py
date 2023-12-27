import re as regex
from converter import nonint2decimal, bin2float, bin2signedInt, reportFloat, reportSignedInt, reportStandard


def calculate(expression: str) -> (float | int, dict, bool | str):
    expression = expression.lower().replace("\n", "")
    if expression == "":
        return None, None, "No expression entered"

    # Step 1: get any flags
    expression, flags = parseFlags(expression)

    # Step 2: convert bin and hex nonintegers to decimal
    matches = list(regex.finditer(r"0[xb]([0-9a-z]+)\.([0-9a-z]+)", expression))
    for match in matches:
        replacement, error = nonint2decimal(match.group(1), match.group(2), match.group(0))
        if error != False:
            return None, None, error
        expression = expression.replace(match.group(0), replacement)


    # Step 3: convert unsigned ints, signed ints, and floats to decimal
    instances = regex.findall(r"0[xb][0-9a-z]+", expression)
    match (flags["mode"]):
        case "unsigned":
            for instance in instances:
                try:
                    replacement = str(int(instance, 0))
                    expression = expression.replace(instance, replacement)
                except Exception as e:
                    return None, None, f"{instance} is invalid"
        case "signed":
            for instance in instances:
                replacement, error = bin2signedInt(instance, flags)
                if error != False:
                    return None, None, error
                expression = expression.replace(instance, replacement)
        case "float":
            for instance in instances:
                replacement, error = bin2float(instance, flags)
                if error != False:
                    return None, None, error
                expression = expression.replace(instance, replacement)
    
    # Step 4: flag any unauthorized characters
    invalidChars = regex.findall(r"[^+\-\/\*\.\%0-9 ]", expression)
    if len(invalidChars) > 0:
        return None, None, f"Invalid characters were entered: {invalidChars}"
            
    # Step 4: evaluate and return results
    try: 
        return eval(expression), flags, False
    except Exception as e:
        return None, None, "Could not evaluate expression"


def parseFlags(expression: str) -> (str, dict):
    match = regex.search(r"s(\d+)", expression)
    if match:
        expression = expression.replace(match.group(0), "")
        return expression, {"mode": "signed", "signlength": int(match.group(1))}
    match = regex.search(r"f(\d+),(\d+)", expression)
    if match:
        expression = expression.replace(match.group(0), "")
        return expression, {"mode": "float", "exponent": int(match.group(1)), "mantissa": int(match.group(2))}
    return expression, {"mode": "unsigned"}


def generateOutput(val: int | float, flags: dict) -> str:
    out = reportStandard(val) + "\n"
    if flags["mode"] == "signed":
        out += reportSignedInt(val, flags)
    elif flags["mode"] == "float":
        out += reportFloat(val, flags)
    return out


class HistoryLog:
    def __init__(this) -> None:
        this.lastExp = None
        this.history = "START OF HISTORY"
    
    def addEntry(this, report: str, expression: str) -> None:
        if expression != this.lastExp:
            this.history = f"{expression}\n{report}\n{'_'*40}\n{this.history}"
            this.lastExp = expression
    
    def getHistory(this) -> str:
        return this.history
    

def getReadme() -> str:
    try:
        text = None
        with open("README.md") as readme:
            text = readme.read()
        index = text.find("How to use")
        return text[index:]
    except Exception as e:
        return "COULD NOT OPEN README"
