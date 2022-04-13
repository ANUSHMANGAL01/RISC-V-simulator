from gettext import find

# Global variables
global stages
stages = ["IF", "ID", "EX", "ME", "WB"]
global i, MEMORY ,REGISTERS, LABELS, ASSEMBLER_DIRECTIVES,PROCESSED_LINES,lines
global pipeline_matrix
pipeline_matrix = []
global instructions_registers
instructions_registers=[]

def check_data_dependency():
    global i
    if len(instructions_registers)==0 or len(instructions_registers)==1:
        return 0

    current_registers = instructions_registers[len(instructions_registers)-1]
    previous_registers = instructions_registers[len(instructions_registers)-2]
    if(previous_registers[0] in current_registers and previous_registers[0] !=current_registers[0]):
        return 1

    if(len(instructions_registers)==2):
        return 0

    prev_previous_registers = instructions_registers[0]
    if(prev_previous_registers[0] in current_registers and prev_previous_registers[0] !=current_registers[0]):
        return 2
    
    return 0


# File Handling
file = open("add_inss.asm", "r")
lines = file.readlines();
file.close()

# String to store the path of the new file in case of a new file upload
new_file_name = "add_inss.asm"

i=0
# We will take the base address for user to store in memory to be 0x10010000 which is 268500992
# Each element in the MEMORY array below if for four bytes. Since we are only dealing here with lw and sw commands, this won't cause any problem
#  If the user enters any address of memory to refer it, we will divide it by four to get the correct address in the MEMORY array below
# Also, in the memory, we will storing the numbers in decimal format only
MEMORY = [0]*32768
MEM_POINTER = 268500992  # MEMORY[0]
# MEM_POINTER = 268500996 next. This will access MEMORY[1]
# MEMORY[16384] = 7
# MEMORY[16385] = 10
# MEMORY[16386] = 5
#  The above locations for MEMORY have been initialised just for testing purpose. They will not be there in the final version


LABELS = {}
REGISTERS = {'x0': 0, 'x1': 0, 'x2': 0, 'x3': 0, 'x4': 0, 'x5': 0, 'x6': 0, 'x7': 0, 'x8': 0,
             'x9': 0, 'x10': 0, 'x11': 0, 'x12': 0, 'x13': 0, 'x14': 0, 'x15': 0, 'x16': 0, 'x17': 0,
             'x18': 0, 'x19': 0, 'x20': 0, 'x21': 0, 'x22': 0, 'x23': 0, 'x24': 0, 'x25': 0, 'x26': 0, 'x27': 0,
             'x28': 0, 'x29': 0, 'x30': 0, 'x31': 0}
ASSEMBLER_DIRECTIVES = {".text": 0 ,".data": 0}
PROCESSED_LINES=[]

def clear_reg():
    global REGISTERS
    REGISTERS = {'x0': 0, 'x1': 0, 'x2': 0, 'x3': 0, 'x4': 0, 'x5': 0, 'x6': 0, 'x7': 0, 'x8': 0,
                'x9': 0, 'x10': 0, 'x11': 0, 'x12': 0, 'x13': 0, 'x14': 0, 'x15': 0, 'x16': 0, 'x17': 0,
                'x18': 0, 'x19': 0, 'x20': 0, 'x21': 0, 'x22': 0, 'x23': 0, 'x24': 0, 'x25': 0, 'x26': 0, 'x27': 0,
                'x28': 0, 'x29': 0, 'x30': 0, 'x31': '0'}

class Error(Exception):
    """Base class for other exceptions"""
    pass

class SyntaxError(Error):
    """Raised when there is some syntax error in the input code"""
    pass
class LogicalError(Error):
    """Raised when there is some logical error in the input code"""
    pass

def clear_mem():
    global MEMORY
    MEMORY = [0]*32768

def clear_labels():
    global LABELS
    LABELS={}

def clear_assembler_dir():
    global ASSEMBLER_DIRECTIVES
    ASSEMBLER_DIRECTIVES = {".text": 0 ,".data": 0}

def clear_processed_lines():
    global PROCESSED_LINES
    PROCESSED_LINES=[]

def clear_all():
    global i,lines, MEM_POINTER
    lines=[]
    i=0
    MEM_POINTER = 268500992
    clear_reg()
    clear_mem()
    clear_labels()
    clear_assembler_dir()
    clear_processed_lines()

def getIndex(my_list, key):
    if(key in my_list):
        return my_list.index(key)
    else:
        return -1

def hexadecimal_to_decimal(hex_string):
    hex_string= hex_string[2:]   # removing the first two "0x"
    res = "{0:032b}".format(int(hex_string, 16))
    # print(res)
    # print(type(res))
    if(res[0]=='1'):
        res = get_complement(res)
        return int(res, 2) * -1
    else:
        return int(res, 2)    

def get_complement(binary_string):
    i=len(binary_string) - 1
    new_string=""
    while(i>=0 and binary_string[i]=='0'):
        new_string='0' + new_string
        i-=1
    # print(new_string)
    if(i<0):
        return new_string
    
    new_string = '1'+new_string
    i-=1
    while(i>=0):
        if(binary_string[i]=='0'):
            new_string='1'+new_string
        else:
            new_string='0'+new_string
        i-=1
    return new_string

def isConstantAndNeededLength(word, length):
    if(len(word)==0):
        return False
    if(word[0]=='-' or word[0]=='+'):
        word = word[1:]
        if word.isnumeric():
            return True
        else:
            return False   # hexadecimal numbers don't need a negative sign
    if len(word)>1:
        if((word[1]=='x' or word[1]=='X')):
            if(len(word)!=length):
                return False
            word = word[0] + word[2:]
            for character in word:
                if not ((character>='0' and character<='9') or (character>='a' and character<='f') or (character>='A' and character<='F')):
                    return False
            return True
    if word.isnumeric():
        return True
    else:
        return False

def fillMatrixForRegisterInstructions():
    global i, pipeline_matrix, instructions_registers, stages
    if(len(pipeline_matrix)==0):
        pipeline_matrix.append(stages)
        return

    if(check_data_dependency()==0):
        prev_index = getIndex(pipeline_matrix[len(pipeline_matrix)-1], "IF")
        to_add = ["  "]*(prev_index+1)
        lastRow = pipeline_matrix[len(pipeline_matrix)-1]
        stages_pointer=0
        while(stages_pointer<5):
            if(len(to_add)>len(lastRow)-1):
                while(stages_pointer<5):
                    to_add.append(stages[stages_pointer])
                    stages_pointer+=1
                break
            if( lastRow[len(to_add)] =="ST"):
                to_add.append("ST")
                continue
            to_add.append(stages[stages_pointer])
            stages_pointer+=1   

    elif(check_data_dependency()==1):
        prev_index = getIndex(pipeline_matrix[len(pipeline_matrix)-1], "IF")
        to_add = ["  "]*(prev_index+1)
        lastRow = pipeline_matrix[len(pipeline_matrix)-1]
        stages_pointer=0
        for ele in lastRow:
            if(lastRow.index(ele)<prev_index):
                continue
            if(ele == "  " or ele=="IF"): 
                continue
            if(len(to_add) > getIndex(pipeline_matrix[len(pipeline_matrix)-1], "WB")):
                break
            if(ele =="ST"):
                to_add.append("ST")
                continue
            if(stages_pointer==2):
                to_add.append("ST")
                continue
            to_add.append(stages[stages_pointer])
            stages_pointer+=1
        while(stages_pointer<5):
            to_add.append(stages[stages_pointer])
            stages_pointer+=1 
    elif(check_data_dependency()==2):
        prev_index = getIndex(pipeline_matrix[len(pipeline_matrix)-1], "IF")
        to_add = ["  "]*(prev_index+1)
        prev_prev_WB_index = getIndex(pipeline_matrix[len(pipeline_matrix)-2], "WB")
        lastRow = pipeline_matrix[len(pipeline_matrix)-1]
        stages_pointer=0
        while(stages_pointer<2):
            if(lastRow[len(to_add)] =="ST"):
                to_add.append("ST")
                continue
            to_add.append(stages[stages_pointer])
            stages_pointer+=1
        while(len(to_add)<=prev_prev_WB_index):
            to_add.append("ST")
        while(stages_pointer<5):
            if(lastRow[len(to_add)] =="ST"):
                to_add.append("ST")
                continue
            to_add.append(stages[stages_pointer])
            stages_pointer+=1
    pipeline_matrix.append(to_add)
    print(pipeline_matrix)

def handle_add(line):
    global i, pipeline_matrix, instructions_registers, stages
    reg =line.split(',')
    reg = list(map(str.strip, reg))

    if(len(instructions_registers)==3):
        del instructions_registers[0]
    instructions_registers.append((reg))

    if len(reg)!=3 or not (reg[0] in REGISTERS and reg[1] in REGISTERS and reg[2] in REGISTERS):
        raise SyntaxError('Syntax error found in line %d. The register name is wrong.' %i)
    REGISTERS[reg[0]]=REGISTERS[reg[1]]+REGISTERS[reg[2]]
    REGISTERS['x0'] = 0
    fillMatrixForRegisterInstructions()


def handle_addi(line):
    global i, pipeline_matrix, instructions_registers, stages
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    const =0
    if(len(instructions_registers)==3):
        del instructions_registers[0]
    instructions_registers.append((reg))

    if len(reg)!=3 or not (reg[0] in REGISTERS and reg[1] in REGISTERS and isConstantAndNeededLength(reg[2], 10)):
        raise SyntaxError('Syntax error found in line %d. The register name is wrong or the constant value is wrong.' %i)
    if reg[2].find("0x")<0:   #means we did not find "0x"
        const = int(reg[2])       
    else:
        const= hexadecimal_to_decimal(reg[2]) 
    REGISTERS[reg[0]]=REGISTERS[reg[1]]+const
    REGISTERS['x0'] = 0
    fillMatrixForRegisterInstructions()

def handle_sub(line):
    global i, pipeline_matrix, instructions_registers, stages
    reg =line.split(',')
    reg = list(map(str.strip, reg))

    if(len(instructions_registers)==3):
        del instructions_registers[0]
    instructions_registers.append((reg))
    if len(reg)!=3 or not (reg[0] in REGISTERS and reg[1] in REGISTERS and reg[2] in REGISTERS):
        raise SyntaxError('Syntax error found in line %d. The register name is wrong.' %i)
    REGISTERS[reg[0]]=REGISTERS[reg[1]]-REGISTERS[reg[2]]
    REGISTERS['x0'] = 0
    fillMatrixForRegisterInstructions()

def handle_slt(line):
    global i, pipeline_matrix, instructions_registers, stages
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    if(len(instructions_registers)==3):
        del instructions_registers[0]
    instructions_registers.append((reg))
    if len(reg)!=3 or not (reg[0] in REGISTERS and reg[1] in REGISTERS and reg[2] in REGISTERS):
        raise SyntaxError('Syntax error found in line %d. The register name is wrong.' %i)
    if(REGISTERS[reg[1]]<REGISTERS[reg[2]]):
        REGISTERS[reg[0]]=1
    else:
        REGISTERS[reg[0]]=0
    REGISTERS['x0'] = 0
    fillMatrixForRegisterInstructions()

def handle_lw(line):
    global i
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    arg = reg[1]
    offset=(arg[0:arg.find('(')].strip())
    arg=arg[arg.find('(')+1 : arg.find(')')]
    if len(reg)!=2 or not (reg[0] in REGISTERS and arg in REGISTERS and isConstantAndNeededLength(offset, 0)):
        raise SyntaxError('Syntax error found in line %d.' %i)
    offset = int(offset)
    ma = REGISTERS[arg]+offset
    REGISTERS[reg[0]]=MEMORY[(ma-268500992)//4]
    REGISTERS['x0'] = 0

def handle_li(line):
    global i
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    if len(reg)!=2 or not (reg[0] in REGISTERS and isConstantAndNeededLength(reg[1], 10)):
        raise SyntaxError('Syntax error found in line %d. The register name is wrong or the constant value is wrong.' %i)
    if reg[1].find("0x")<0:   #means we did not find "0x"
        const = int(reg[1])
        REGISTERS[reg[0]]=const
    else:
        REGISTERS[reg[0]]=hexadecimal_to_decimal(reg[1]) 
    REGISTERS['x0'] = 0

def handle_lui(line):
    global i
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    if len(reg)!=2 or not (reg[0] in REGISTERS and isConstantAndNeededLength(reg[1], 7)):
        raise SyntaxError('Syntax error found in line %d. The register name is wrong or the constant value is wrong.' %i)
    if reg[1].find("0x")<0:   #means we did not find "0x"
        const = int(reg[1])
        REGISTERS[reg[0]]=const*16*16*16    # Because we have to store it in upper half
    else:
        REGISTERS[reg[0]]=hexadecimal_to_decimal(reg[1]+"000") 
    REGISTERS['x0'] = 0

def handle_sw(line):
    global i
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    arg = reg[1]
    offset=(arg[0:arg.find('(')].strip())
    arg=arg[arg.find('(')+1 : arg.find(')')]
    if len(reg)!=2 or not (reg[0] in REGISTERS and arg in REGISTERS and isConstantAndNeededLength(offset, 0)):
        raise SyntaxError('Syntax error found in line %d.' %i)
    offset = int(offset)
    ma = REGISTERS[arg]+offset;
    MEMORY[(ma-268500992)//4]=REGISTERS[reg[0]]
    REGISTERS['x0'] = 0

def handle_bne(line):
    global i
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    if len(reg)!=3 or not (reg[0] in REGISTERS and reg[1] in REGISTERS and reg[2] in LABELS):
        raise SyntaxError('Syntax error found in line %d. The register or the label name is wrong.' %i)
    if(REGISTERS[reg[0]]!=REGISTERS[reg[1]]):
        i=LABELS[reg[2]]-1
    REGISTERS['x0'] = 0

def handle_beq(line):
    global i
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    if len(reg)!=3 or not (reg[0] in REGISTERS and reg[1] in REGISTERS and reg[2] in LABELS):
        raise SyntaxError('Syntax error found in line %d. The register or the label name is wrong.' %i)
    if(REGISTERS[reg[0]]==REGISTERS[reg[1]]):
        i=LABELS[reg[2]]-1
    REGISTERS['x0'] = 0

def handle_blt(line):
    global i
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    if len(reg)!=3 or not (reg[0] in REGISTERS and reg[1] in REGISTERS and reg[2] in LABELS):
        raise SyntaxError('Syntax error found in line %d. The register or the label name is wrong.' %i)
    if(REGISTERS[reg[0]] < REGISTERS[reg[1]]):
        i=LABELS[reg[2]]-1
    REGISTERS['x0'] = 0
def handle_bgt(line):
    global i
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    if len(reg)!=3 or not (reg[0] in REGISTERS and reg[1] in REGISTERS and reg[2] in LABELS):
        raise SyntaxError('Syntax error found in line %d. The register or the label name is wrong.' %i)
    if(REGISTERS[reg[0]] > REGISTERS[reg[1]]):
        i=LABELS[reg[2]]-1
    REGISTERS['x0'] = 0

def handle_bge(line):
    global i
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    if len(reg)!=3 or not (reg[0] in REGISTERS and reg[1] in REGISTERS and reg[2] in LABELS):
        raise SyntaxError('Syntax error found in line %d. The register or the label name is wrong.' %i)
    if(REGISTERS[reg[0]] >= REGISTERS[reg[1]]):
        i=LABELS[reg[2]]-1
    REGISTERS['x0'] = 0

def handle_beqz(line):
    global i
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    if len(reg)!=2 or not (reg[0] in REGISTERS and reg[1] in LABELS):
        raise SyntaxError('Syntax error found in line %d. The register or the label name is wrong.' %i)
    if(REGISTERS[reg[0]] == 0):
        i=LABELS[reg[1]]-1
    REGISTERS['x0'] = 0

def handle_bnez(line):
    global i
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    if len(reg)!=2 or not (reg[0] in REGISTERS and reg[1] in LABELS):
        raise SyntaxError('Syntax error found in line %d. The register or the label name is wrong.' %i)
    if(REGISTERS[reg[0]] != 0):
        i=LABELS[reg[1]]-1
    REGISTERS['x0'] = 0

def handle_blez(line):
    global i
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    if len(reg)!=2 or not (reg[0] in REGISTERS and reg[1] in LABELS):
        raise SyntaxError('Syntax error found in line %d. The register or the label name is wrong.' %i)
    if(REGISTERS[reg[0]] <= 0):
        i=LABELS[reg[1]]-1
    REGISTERS['x0'] = 0

def handle_j(line):
    global i
    label = line.strip()
    if not (label in LABELS):
        raise LogicalError('Logical error found in line %d. The label name is wrong.' %i)
    i=LABELS[label]-1
    REGISTERS['x0'] = 0

def handle_mv(line):
    global i, pipeline_matrix, instructions_registers, stages
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    if(len(instructions_registers)==3):
        del instructions_registers[0]
    instructions_registers.append((reg))
    if len(reg)!=2 or not (reg[0] in REGISTERS and reg[1] in REGISTERS):
        raise SyntaxError('Syntax error found in line %d. The register name is wrong.' %i)
    REGISTERS[reg[0]]=REGISTERS[reg[1]]
    REGISTERS['x0'] = 0
    fillMatrixForRegisterInstructions()

def handle_jal(line):
    global i
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    if len(reg)!=2 or not (reg[0] in REGISTERS and reg[1] in LABELS):
        raise SyntaxError('Syntax error found in line %d. The register or the label name is wrong.' %i)
    REGISTERS[reg[0]] = i    # now when this will be called, i will be given this value and will be incrememented in the main while loop
    i=LABELS[reg[1]]-1
    REGISTERS['x0'] = 0

def handle_jalr(line):
    global i
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    arg = reg[1]
    offset=(arg[0:arg.find('(')].strip())
    arg=arg[arg.find('(')+1 : arg.find(')')]
    if len(reg)!=2 or not (reg[0] in REGISTERS and arg in REGISTERS and isConstantAndNeededLength(offset, 0)):
        raise SyntaxError('Syntax error found in line %d.' %i)
    offset = int(offset)
    REGISTERS[reg[0]] = i
    i = REGISTERS[arg] + offset 
    REGISTERS['x0'] = 0

def handle_andi(line):
    global i, pipeline_matrix, instructions_registers, stages
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    const =0
    if(len(instructions_registers)==3):
        del instructions_registers[0]
    instructions_registers.append((reg))
    if len(reg)!=3 or not (reg[0] in REGISTERS and reg[1] in REGISTERS and isConstantAndNeededLength(reg[2], 10)):
        raise SyntaxError('Syntax error found in line %d. The register name is wrong or the constant value is wrong.' %i)
    if reg[2].find("0x")<0:   #means we did not find "0x"
        const = int(reg[2])       
    else:
        const= hexadecimal_to_decimal(reg[2]) 
    REGISTERS[reg[0]]=REGISTERS[reg[1]] & const
    REGISTERS['x0'] = 0
    fillMatrixForRegisterInstructions()

def handle_ori(line):
    global i, pipeline_matrix, instructions_registers, stages
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    const =0
    if(len(instructions_registers)==3):
        del instructions_registers[0]
    instructions_registers.append((reg))
    if len(reg)!=3 or not (reg[0] in REGISTERS and reg[1] in REGISTERS and isConstantAndNeededLength(reg[2], 10)):
        raise SyntaxError('Syntax error found in line %d. The register name is wrong or the constant value is wrong.' %i)
    if reg[2].find("0x")<0:   #means we did not find "0x"
        const = int(reg[2])       
    else:
        const= hexadecimal_to_decimal(reg[2]) 
    REGISTERS[reg[0]]=REGISTERS[reg[1]] | const
    REGISTERS['x0'] = 0
    fillMatrixForRegisterInstructions()

def handle_or(line):
    global i, pipeline_matrix, instructions_registers, stages
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    if(len(instructions_registers)==3):
        del instructions_registers[0]
    instructions_registers.append((reg))
    if len(reg)!=3 or not (reg[0] in REGISTERS and reg[1] in REGISTERS and reg[2] in REGISTERS):
        raise SyntaxError('Syntax error found in line %d. The register name is wrong.' %i)
    REGISTERS[reg[0]]=REGISTERS[reg[1]] | REGISTERS[reg[2]]
    REGISTERS['x0'] = 0
    fillMatrixForRegisterInstructions()

def handle_and(line):
    global i, pipeline_matrix, instructions_registers, stages
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    if(len(instructions_registers)==3):
        del instructions_registers[0]
    instructions_registers.append((reg))
    if len(reg)!=3 or not (reg[0] in REGISTERS and reg[1] in REGISTERS and reg[2] in REGISTERS):
        raise SyntaxError('Syntax error found in line %d. The register name is wrong.' %i)
    REGISTERS[reg[0]]=REGISTERS[reg[1]] & REGISTERS[reg[2]]
    REGISTERS['x0'] = 0
    fillMatrixForRegisterInstructions()

def handle_sll(line):
    global i, pipeline_matrix, instructions_registers, stages
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    if(len(instructions_registers)==3):
        del instructions_registers[0]
    instructions_registers.append((reg))
    if len(reg)!=3 or not (reg[0] in REGISTERS and reg[1] in REGISTERS and reg[2] in REGISTERS):
        raise SyntaxError('Syntax error found in line %d. The register name is wrong.' %i)
    REGISTERS[reg[0]]=REGISTERS[reg[1]] << REGISTERS[reg[2]]
    REGISTERS['x0'] = 0
    fillMatrixForRegisterInstructions()

def handle_srl(line):
    global i, pipeline_matrix, instructions_registers, stages
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    if(len(instructions_registers)==3):
        del instructions_registers[0]
    instructions_registers.append((reg))
    if len(reg)!=3 or not (reg[0] in REGISTERS and reg[1] in REGISTERS and reg[2] in REGISTERS):
        raise SyntaxError('Syntax error found in line %d. The register name is wrong.' %i)
    REGISTERS[reg[0]]=REGISTERS[reg[1]] >> REGISTERS[reg[2]]
    REGISTERS['x0'] = 0
    fillMatrixForRegisterInstructions()

def handle_la(line):
    global i
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    if len(reg)!=2 or not (reg[0] in REGISTERS and reg[1] in LABELS):
        raise SyntaxError('Syntax error found in line %d. The register or the label name is wrong.' %i)
    REGISTERS[reg[0]] = LABELS[reg[1]]    # now when this will be called, i will be given this value and will be incrememented in the main while loop
    REGISTERS['x0'] = 0

def callFunction(opcode,line):
    global i
    if(opcode == "add"):
        handle_add(line)
        return
    if(opcode == "addi"):
        handle_addi(line)
        return
    if(opcode == "sub"):
        handle_sub(line)
        return    
    if(opcode == "slt"):
        handle_slt(line)
        return
    if(opcode == "lw"):
        handle_lw(line)
        return
    if(opcode == "sw"):
        handle_sw(line)
        return
    if(opcode == "li"):
        handle_li(line)
        return
    if(opcode == "lui"):
        handle_lui(line)
        return
    if(opcode == "bne"):
        handle_bne(line)
        return
    if(opcode == "beq"):
        handle_beq(line)
        return
    if(opcode == "blt"):
        handle_blt(line)
        return
    if(opcode == "bgt"):
        handle_bgt(line)
        return
    if(opcode == "bge"):
        handle_bge(line)
        return
    if(opcode == "beqz"):
        handle_beqz(line)
        return
    if(opcode == "bnez"):
        handle_bnez(line)
        return
    if(opcode == "blez"):
        handle_blez(line)
        return
    if(opcode == "j"):
        handle_j(line)
        return
    if(opcode == "jal"):
        handle_jal(line)
        return
    if(opcode == "jalr"):
        handle_jalr(line)
        return
    if(opcode == "mv"):
        handle_mv(line)
        return
    if(opcode == "andi"):
        handle_andi(line)
        return
    if(opcode == "ori"):
        handle_ori(line)
        return
    if(opcode == "or"):
        handle_or(line)
        return
    if(opcode == "and"):
        handle_and(line)
        return
    if(opcode == "sll"):
        handle_sll(line)
        return
    if(opcode == "srl"):
        handle_srl(line)
        return
    if(opcode == "la"):
        handle_la(line)
        return
    
    raise SyntaxError('Syntax error found in line %d. The opcode name is wrong. It is ' %i)

def remove_side_comment(line):
    if(line.find('#')>0):
        line=line[0 : line.find('#')]
    return line

#  only handling word right now
def handle_data(line, j):
    global MEM_POINTER, PROCESSED_LINES, LABELS
    while not line[0]=='.':
        line = line.strip()
        label=""
        if(line.find(':')>0):
            label=line[0:line.find(':')].strip()
            line=line[line.find(':')+1:].strip()
            LABELS[label] = MEM_POINTER
        d_type = line[0: line.find(' ')]
        line = line[line.find(" ")+1: ]
        values = line.split(",")
        if(d_type==".word"):
            for value in values:
                MEMORY[(MEM_POINTER-268500992)//4] = int(value)
                MEM_POINTER+=4
        else:
            pass  
        j+=1  
        line=PROCESSED_LINES[j]
    while(line[0]=='.'):
        if(line.find(".word")==0):
            line = line[line.find(" ")+1: ]
            values = line.split(",")
            for value in values:
                MEMORY[(MEM_POINTER-268500992)//4] = int(value)
                MEM_POINTER+=4
        j+=1
        line=PROCESSED_LINES[j]
    return j

def find_labels(j):
    
    while j < len(PROCESSED_LINES):
        line=PROCESSED_LINES[j].strip()
        if(line[0]=='.' and line.find(".data") ==0):
            if(line[5:].strip()==""):
                j = handle_data(PROCESSED_LINES[j+1], j+1)
                
            else:
                j = handle_data(line[5:], j)
                
            continue
        label=""
        if(line.find(':')>0):
            label=line[0:line.find(':')].strip()
        if(label!=""):
            LABELS[label]=j
            line=line[line.find(':')+1:].strip()
            PROCESSED_LINES[j]=line
        j+=1

# Removing white spaces and comments
def process_lines():
    global PROCESSED_LINES
    j=0
    while j < len(lines):
        line=lines[j].strip()
        if line=="":
            j+=1
            continue
        if(line[0]=='#'):
            j+=1
            continue
        else:
            line = remove_side_comment(line)
            PROCESSED_LINES.append(line)
            j+=1


def load_code():
    global lines
    file = open(new_file_name, "r")
    lines = file.readlines();
    file.close()
    process_lines()

# Lines are intially processed
process_lines()

def main():
    global i,lines,REGISTERS,MEMORY,LABELS
    find_labels(0)
    i= LABELS["main"]
    # print(i)
    while i < len(PROCESSED_LINES):
        line=PROCESSED_LINES[i].strip()
        if line=='' :
            i+=1
            continue
        line = remove_side_comment(line)
        opcode = line[0 : line.find(' ')].strip()
        callFunction(opcode,line[line.find(' '):].strip())
        i+=1
    print(REGISTERS)
    print(MEMORY[0:10])

# main()

def run_one_by_one(line_number):
    global PROCESSED_LINES, i
    i = line_number
    line = PROCESSED_LINES[line_number].strip()
    if line == "":
        i+=1
        return
    opcode = line[0 : line.find(' ')].strip()
    callFunction(opcode,line[line.find(' '):].strip())
    i+=1
    print(REGISTERS)
    print(MEMORY[0:10])

# Function to run the code with a different file
def run():
    global lines
    clear_all()
    file = open(new_file_name, "r")
    lines = file.readlines();
    file.close()
    process_lines()
    main()

if __name__ =="__main__":
    main()
#   add rd , r1 , r2
#   addi rd , r1 , c
#   sub rd , r1 , r2 
#   slt rd , r1 , r2
#   lw  rd, offset(r1)   
#   sw  rs, offset(r1) 
#   li rd, c
#   lui rd, c
#   bne r1,r2,LABEL
#   beq r1,r2,LABEL
#   blt r1,r2,LABEL
#   bgt r1,r2,LABEL
#   bge r1,r2,LABEL
#   beqz r1,LABEL
#   bnez r1,LABEL
#   blez r1,LABEL
#   j LABEL
#   mv , rd, rs
#   jal rd, label
#   jalr x0, 0(x1)
#   andi rd, rs1, imm
#   ori rd, rs1, imm
#   or rd, rs1, rs2
#   and rd, rs1, rs2
#   sll rd , r1 , r2
#   srl rd , r1 , r2
#   la rd, data_label