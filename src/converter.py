def nonint2decimal(left: str, right: str, entire: str) -> (str, bool | str):
    base = 16 if entire[1] == "x" else 2
    try:
        whole = int(left, base)
        part = int(right, base) / (base ** len(right))
        return str(whole + part), False
    except Exception as e:
        return None, f"{entire} is invalid"
    
    
def hex2bin(hex: str, flags: dict) -> (str, bool | str):
    expectedSize = flags["signlength"] if flags["mode"] == "signed" else int(flags["exponent"]) + int(flags["mantissa"])
    binary = None
    try:
        binary = bin(int(hex, 16))[2:]
    except Exception as e:
        return None, f"0x{hex}, is invalid"
    actualSize = len(binary)
    if expectedSize == actualSize:
        return binary, False
    if expectedSize > actualSize:
        return "0" * (expectedSize - actualSize) + binary, False
    if expectedSize < actualSize:
        return None, f"0x{hex} represents too many bits"
    
    
def bin2signedInt(entire: str, flags: dict) -> (str, bool | str): 
    binary, error = hex2bin(entire[2:], flags) if entire[1] == "x" else (entire[2:], False)
    if error != False:
        return None, error
    val = int(binary, 2)
    if binary[0] == "1":
        return str(val - 2 ** len(binary)), False
    else:
        return str(val), False


def bin2float(entire: str, flags: dict) -> (str, bool | str): #TODO TEST
    binary, error = hex2bin(entire[2:], flags) if entire[1] == "x" else (entire[2:], False)
    if error != False:
        return None, error
    expSize = flags["exponent"]
    manSize = flags["mantissa"]
    
    sign = -1 if bin[0] == "1" else 1
    exp = int(binary[1:(1+expSize)], 2)
    man = int(binary[(1+expSize):(1+expSize+manSize)], 2)
    bias = 2 ** (expSize - 1)
    return float(sign * man * (2 ** (exp - bias)))



def reportSignedInt(val: int | float, flags: dict) -> str:
    val = int(val)
    range = (-1 * 2**(flags["signlength"]-1), 2**(flags["signlength"]-1)-1)
    if val < range[0] or val > range[1]:
        return f"Signed Int {flags['signlength']}-bit: OVERFLOW!"
    if val < 0:
        val = 2 ** (flags['signlength']) + val
    bits = bin(val)
    bits = "0" * (flags["signlength"] - len(bits)) + bits
    return f"Signed Int {flags['signlength']}-bit: {bits}, {hex(int(bits, 2))}"

def reportStandard(val: int | float) -> str:
    binary, hexadecimal = None, None
    if type(val) == float:
        whole = int(val // 1)
        part = val % 1
        if val < 0 and part != 0:
            whole += 1
            part = 1 - part
        wholeBin = bin(whole)
        wholeHex = hex(whole)
        partBin = bin(int(part * 2**8))[2:]
        partBin = "0" * (8-len(partBin)) + partBin
        partHex = hex(int(part * 16**4))[2:]
        partHex = "0" * (4-len(partHex)) + partHex
        binary = f"{wholeBin}.{partBin}"
        hexadecimal = f"{wholeHex}.{partHex}"
    elif type(val) == int:
        binary = bin(val)
        hexadecimal = hex(val)
    return f"Standard Values: {val}, {binary}, {hexadecimal}"
    

def reportFloat(val, flags): #TODO
    return f"Float Values: TODO"
