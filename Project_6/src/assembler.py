import sys, csv

# Reference - C-instruction syntax: 111 a c1 c2 c3 c4 c5 c6 d1 d2 d3 j1 j2 j3
# a: 0 for A register, 1 for M (memory at address A) instruction[3]
# c1-c6: computation bits instruction[4:10]
# d1-d3: destination bits instruction[10:13]
# j1-j3: jump bits instruction[13:]
# Build Symbol Table
# Predefined symbols
# Variable symbols
# Labels
# Instruction parsing
# Take in assembly file
# Read line by line
# Strip comments and whitespace
# Translate A-instructions
# Translate C-instructions
# Decimal to Binary conversion
# Output binary file
###########
# CONSTANTS
###########
DEST_TABLE = {
    'null'  : '000',
    'M'     : '001',
    'D'     : '010',
    'MD'    : '011',
    'A'     : '100',
    'AM'    : '101',
    'AD'    : '110',
    'AMD'   : '111'
}
COMP_TABLE = {
    '0'     : '101010',
    '1'     : '111111',
    '-1'    : '111010',
    'D'     : '001100',
    'A'     : '110000',
    'M'     : '110000',
    '!D'    : '001101',
    '!A'    : '110001',
    '!M'    : '110001',
    '-D'    : '001111',
    '-A'    : '110011',
    '-M'    : '110011',
    'D+1'   : '011111',
    'A+1'   : '110111',
    'M+1'   : '110111',
    'D-1'   : '001110',
    'A-1'   : '110010',
    'M-1'   : '110010',
    'D+A'   : '000010',
    'D+M'   : '000010',
    'D-A'   : '010011',
    'D-M'   : '010011',
    'A-D'   : '000111',
    'M-D'   : '000111',
    'D&A'   : '000000',
    'D&M'   : '000000',
    'D|A'   : '010101',
    'D|M'   : '010101'
}
JUMP_TABLE = {
    'null'  : '000',
    'JGT'   : '001',
    'JEQ'   : '010',
    'JGE'   : '011',
    'JLT'   : '100',
    'JNE'   : '101',
    'JLE'   : '110',
    'JMP'   : '111'
}

# File > File
# Consumes Assembly file '.asm' and produces Machine Code file '.hack'
def main(fileName=sys.argv[1]):
    # Read line by line
    # Strip comments and whitespace
    # Determine label, variable, or instruction type
    symbolTable = symbol_table_manager(initialize=True)
    parsedFilePath = parser(fileName, symbolTable)
    print(parsedFilePath)
    return 0

# Produces symbolTable
# !!! File Dictionary String > String
def symbol_table_manager(initialize=False, st={}):
    if initialize:
        with open('../data/symbol_table.csv', mode='r') as stFile:
            reader = csv.reader(stFile)
            next(reader, None)  # skip header row
            st = {rows[0]: rows[1] for rows in reader}
    return st

# File Dictionary Integer > String
# Consumes fn=fileName, st=symbolTable
# Produces parsedFilePath
def parser(fn, st, i):

    if fn[-3:] == 'asm' and i == 0:
        tempFileName = fn + '.temp'
        with open(fn, 'r') as sourceFile, open(tempFileName, 'w') as tempFile:
            for line in sourceFile:
                strippedLine = line.split('//')[0].strip()  # Remove comments and whitespace
                if strippedLine:
                    decodedLine = decoder(strippedLine, st)  # Only write non-empty lines
                    tempFile.write(decodedLine + '\n')
        destFileName = tempFileName
    else:
        destFileName = fn.replace('.asm.temp', '.hack')
    
    return destFileName

# String Dictionary > String  ## For v1. v2 will need more parameters to handle custom symbols
# Consumes instruction, st=symbolTable and Produces binaryInstruction
def decoder(instruction, st):
    binaryInstruction = [''] * 16  # Initialize a list of 16 characters

    match instruction[0]:
        case '@':  # A-instruction
            binaryInstruction[0] = '0'
    
    if binaryInstruction[0] == '0': # A-instruction
        address = instruction[1:]
        value = int(address)
        binaryInstruction = '0' + format(value, '015b')
    else:  # C-instruction
        binaryInstruction[0:3] = ['1', '1', '1']
        dest, comp, jump = '', '', ''
        if '=' in instruction:
            parts = instruction.split('=')
            dest = parts[0]
            comp = parts[1]
            binaryInstruction[3]     = '0' if 'A' in comp else '1'
            binaryInstruction[4:10]  = COMP_TABLE[comp]
            binaryInstruction[10:13] = DEST_TABLE[dest]
            binaryInstruction[13:]   = JUMP_TABLE['null']

    return ''.join(binaryInstruction)


if __name__ == '__main__':
    main()
