# Multiformat Calculator

## Description

This program is a multiple operations calculator, that can process numbers in decimal, binary and hexadecimal, and can process representations of signed integers and floating point numbers of custom length.

## Installation

Option 1: Install the `.exe` file

Option 2: clone the repo, create a python virtual environment, install `requirements.txt`, run `frontend.py`

## How to use

Enter an expression to evaluate in the "Enter Expression" box. Binary and hexadecimal must be preceded by 0b and 0x, respectively. A flag can be added at the end of the expression to change how binary and hexadecimal is interpreted and displayed. Check "Show History" to show calculator history.

**Valid Operators:** +, -, *, /, %, **

**Formats and Flags:** 

- **Standard**, no flag needed. Values are displayed and interpreted in a normal manner. Binary and hex fractions can be represented like `-0x123.abc`
- **Signed integer**, flag: `s[length]`, example for an 8-bit signed int: `s8`. Binary and hex values are assumed to be signed ints of the specified length. The result will also be in this format. 
- **Float**, flag: `f[exponent length],[mantissa length]`, example for a single precision float `f8,23`. Binary and hex values are assumed to be floats with the specified exponent and mantissa length. The result will also be in this format. 

Note: standard values can be in the same expression as signed ints or floats.

**Key Binds:**

_Enter_ solves the inputted expression
_Control-W_ closes the calculator
_Control-D_ clears the calculator
