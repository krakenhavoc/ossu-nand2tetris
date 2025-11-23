import sys
import csv

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
    symbolTable = symbol_table_manager(initialize=True)
    parsedFilePath = parser(fileName, symbolTable)
    print(parsedFilePath)
    # print(symbolTable)
    return 0

# Boolean Dictionary String String > Dictionary
def symbol_table_manager(initialize=False, st=None, k=None, v=None):
    if initialize:
        with open('/Users/luke/devops/repos/LabXP/ossu-nand2tetris/Project_6/data/symbol_table.csv', mode='r') as stFile:
            reader = csv.reader(stFile)
            next(reader, None)  # skip header row
            st = {rows[0]: rows[1] for rows in reader}

        return st

    if st is None:
        return {}

    if k is None or v is None:
        return st

    st[k] = v
    return st

# File Dictionary Integer > String
# Consumes fn=fileName, st=symbolTable, i=iteration; Produces parsedFilePath
def parser(fn, st, i=0):

    if i == 0:  # Initial pass | strips whitespace, comments, and loads labels
        tempFileName = fn.replace('.asm', '.asm.temp')
        lineCounter = 0

        with open(fn, 'r') as sourceFile, open(tempFileName, 'w') as tempFile:
            for line in sourceFile:
                strippedLine = line.split('//')[0].strip()
                if not strippedLine:
                    continue

                if strippedLine[0] == '(':  # Load symbol table with label
                    label = strippedLine.split(')')[0][1:]
                    st = symbol_table_manager(st=st, k=label, v=lineCounter)
                    continue

                tempFile.write(strippedLine + '\n')
                lineCounter += 1

        return parser(fn=tempFileName, st=st, i=1)

    elif i == 1:  # Second pass | loads custom variables
        tempFileName = fn.replace('.asm.temp', '.asm.temp2')
        memAddr = 16

        with open(fn, 'r') as sourceFile, open(tempFileName, 'w') as tempFile:
            for line in sourceFile:
                strippedLine = line.strip()
                if strippedLine[0] == '@':
                    try:
                        int(strippedLine[1:])
                        tempFile.write(line)
                        continue
                    except ValueError:
                        custom_var = strippedLine[1:]

                    if custom_var not in st:
                        st = symbol_table_manager(st=st, k=custom_var, v=memAddr)
                        memAddr += 1

                    tempFile.write('@' + str(st[custom_var]) + '\n')
                    continue

                tempFile.write(line)

        return parser(fn=tempFileName, st=st, i=2)

    else:  # Final pass | writes machine code
        destFileName = fn.replace('.asm.temp2', '.hack')

        with open(fn, 'r') as sourceFile, open(destFileName, 'w') as destFile:
            for line in sourceFile:
                destFile.write(decoder(line.strip(), st) + '\n')

    return destFileName

# String Dictionary > String 
# Consumes instruction, st=symbolTable and Produces binaryInstruction
def decoder(instruction, st):
    binaryInstruction = [''] * 16  # Initialize a list of 16 characters

    if instruction[0] == '@':  # A-instruction
        address = instruction[1:]
        value = int(address)
        binaryInstruction = '0' + format(value, '015b')
        return ''.join(binaryInstruction)

    # C-instruction
    dest, comp, jump = 'null', '0', 'null'

    if '=' in instruction:
        parts = instruction.split('=')
        dest = parts[0]
        comp = parts[1]
    elif ';' in instruction:
        parts = instruction.split(';')
        comp = parts[0]
        jump = parts[1]

    binaryInstruction[0:3] = ['1', '1', '1']
    binaryInstruction[3] = '1' if 'M' in comp else '0'
    binaryInstruction[4:10] = COMP_TABLE[comp]
    binaryInstruction[10:13] = DEST_TABLE[dest]
    binaryInstruction[13:] = JUMP_TABLE[jump]

    return ''.join(binaryInstruction)

if __name__ == '__main__':
    main()
