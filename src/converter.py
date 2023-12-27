import struct

def nonint2decimal(left: str, right: str, entire: str) -> (str, bool | str):
    base = 16 if entire[1] == "x" else 2
    try:
        whole = int(left, base)
        part = int(right, base) / (base ** len(right))
        return str(whole + part), False
    except Exception as e:
        return None, f"{entire} is invalid"
    
    
def hex2bin(hex: str, flags: dict) -> (str, bool | str):
    expectedSize = flags["signlength"] if flags["mode"] == "signed" else int(flags["exponent"]) + int(flags["mantissa"]) + 1
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
    if val >= 2**(flags["signlength"]):
        return None, f"{entire} is too many bits"
    elif val >= 2**(flags["signlength"]-1):
        return str(val - 2 ** flags["signlength"]), False
    else:
        return str(val), False


def bin2float(entire: str, flags: dict) -> (str, bool | str):
    expSize = flags["exponent"]
    manSize = flags["mantissa"]
    binary, error = hex2bin(entire[2:], flags) if entire[1] == "x" else (entire[2:], False)
    if error != False:
        return None, error
    binary = fixLength(int(entire, 0), expSize + manSize + 1, 2)
    if binary is None:
        return None, f"{entire} is too large"
    sign = -1 if binary[0] == "1" else 1
    exp = int(binary[1:(1+expSize)], 2)
    man = binary[(1+expSize):(1+expSize+manSize)]
    man, _ = nonint2decimal("1", man, f"0b1.{man}")
    bias = 2 ** (expSize - 1) - 1
    result = str(sign * float(man) * (2 ** (exp - bias)))
    if result.find("e") != -1:
        return None, f"the result is out of bounds"
    return result, False

def fixLength(input: int, length: int, base: int) -> str:
    output = bin(input)[2:] if base == 2 else hex(input)[2:]
    if len(output) > length:
        return None
    return "0" * (length - len(output)) + output




def reportSignedInt(val: int | float, flags: dict) -> str:
    length = flags["signlength"]
    val = int(val)
    range = (-1 * 2**(length-1), 2**(length-1)-1)
    if val < range[0] or val > range[1]:
        return f"Signed Int {length}-bit: OVERFLOW!"
    if val < 0:
        val = 2 ** (length) + val
    bits = fixLength(val, length, 2)
    hexlen = int(length / 4) if length % 4 == 0 else int(length // 4 + 1)
    hexadecimal = fixLength(val, hexlen, 16)
    return f"Signed Int {length}-bit:\n  0b{bits}\n  0x{hexadecimal}"

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
        partBin = bin(int(part * 2**12))[2:]
        partBin = "0" * (12-len(partBin)) + partBin
        partHex = hex(int(part * 16**8))[2:]
        partHex = "0" * (8-len(partHex)) + partHex
        binary = f"{wholeBin}.{partBin}"
        hexadecimal = f"{wholeHex}.{partHex}"
        if val < 0 and val > -1:
            binary = f"-{binary}"
            hexadecimal = f"-{hexadecimal}"
    elif type(val) == int:
        binary = bin(val)
        hexadecimal = hex(val)
    return f"Standard Values:\n  {val}\n  {binary}\n  {hexadecimal}"
    

def reportFloat(val: int | float, flags: dict) -> str:
    expSize = flags["exponent"]
    manSize = flags["mantissa"]
    header = f"Float ({expSize}-bit exponent, {manSize}-bit mantissa):"

    if expSize > 8 or manSize > 23:
        return f"{header}\n  Up to single precision is supported (f8,23)"
    floatBytes = struct.pack("!f", val)
    sign = floatBytes[0] >> 7
    exponent = ((floatBytes[0] & 0b01111111) << 1) | (floatBytes[1] >> 7)
    mantissa = ((floatBytes[1] & 0b01111111) << 16) | (floatBytes[2] << 8) | floatBytes[3]

    exponent = exponent + 2**(expSize-1) - 2**7
    exponent = fixLength(exponent, expSize, 2)
    if exponent is None:
        return f"{header} OVERFLOW"

    mantissa =  fixLength(mantissa, 23, 2)
    manTrunc = mantissa[0:manSize]
    if len(manTrunc) != len(mantissa) and mantissa[manSize] == "1":
        manTrunc = int(manTrunc, 2) + 0b1
        manTrunc = fixLength(manTrunc, manSize, 2)
    mantissa = manTrunc

    length = expSize + manSize + 1
    hexlen = int(length / 4) if length % 4 == 0 else int(length // 4 + 1)
    binary = f"0b{sign}{exponent}{mantissa}"
    hexadecimal = fixLength(int(binary, 2), hexlen, 16)
    return f"{header}\n  {binary}\n  0x{hexadecimal}"