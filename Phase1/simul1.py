from gettext import find

# File Handling
file = open("assemblyFile.asm", "r")
lines = file.readlines();
file.close()

global i
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
             'x28': 0, 'x29': 0, 'x30': 0, 'x31': '0'}
ASSEMBLER_DIRECTIVES = {".text": 0 ,".data": 0}
PROCESSED_LINES=[]

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


def handle_add(line):
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    REGISTERS[reg[0]]=REGISTERS[reg[1]]+REGISTERS[reg[2]]
    REGISTERS['x0'] = 0

def handle_addi(line):
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    const =0
    if reg[2].find("0x")<0:   #means we did not find "0x"
        const = int(reg[2])       
    else:
        const= hexadecimal_to_decimal(reg[2]) 
    REGISTERS[reg[0]]=REGISTERS[reg[1]]+const
    REGISTERS['x0'] = 0

def handle_sub(line):
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    REGISTERS[reg[0]]=REGISTERS[reg[1]]-REGISTERS[reg[2]]
    REGISTERS['x0'] = 0

def handle_slt(line):
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    if(REGISTERS[reg[1]]<REGISTERS[reg[2]]):
        REGISTERS[reg[0]]=1
    else:
        REGISTERS[reg[0]]=0
    REGISTERS['x0'] = 0

def handle_lw(line):
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    arg = reg[1]
    offset=int(arg[0:arg.find('(')].strip())
    arg=arg[arg.find('(')+1 : arg.find(')')]
    ma = REGISTERS[arg]+offset
    REGISTERS[reg[0]]=MEMORY[(ma-268500992)//4] 
    REGISTERS['x0'] = 0

def handle_li(line):
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    if reg[1].find("0x")<0:   #means we did not find "0x"
        const = int(reg[1])
        REGISTERS[reg[0]]=const
    else:
        REGISTERS[reg[0]]=hexadecimal_to_decimal(reg[1]) 
    REGISTERS['x0'] = 0

def handle_lui(line):
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    if reg[1].find("0x")<0:   #means we did not find "0x"
        const = int(reg[1])
        REGISTERS[reg[0]]=const*16*16*16    # Because we have to store it in upper half
    else:
        REGISTERS[reg[0]]=hexadecimal_to_decimal(reg[1]+"000") 
    REGISTERS['x0'] = 0

def handle_sw(line):
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    arg = reg[1]
    offset=int(arg[0:arg.find('(')].strip())
    arg=arg[arg.find('(')+1 : arg.find(')')]
    ma = REGISTERS[arg]+offset;
    MEMORY[(ma-268500992)//4]=REGISTERS[reg[0]]
    REGISTERS['x0'] = 0

def handle_bne(line):
    global i
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    if(REGISTERS[reg[0]]!=REGISTERS[reg[1]]):
        i=LABELS[reg[2]]-1
    REGISTERS['x0'] = 0

def handle_beq(line):
    global i
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    if(REGISTERS[reg[0]]==REGISTERS[reg[1]]):
        i=LABELS[reg[2]]-1
    REGISTERS['x0'] = 0

def handle_blt(line):
    global i
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    if(REGISTERS[reg[0]] < REGISTERS[reg[1]]):
        i=LABELS[reg[2]]-1
    REGISTERS['x0'] = 0

def handle_bge(line):
    global i
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    if(REGISTERS[reg[0]] >= REGISTERS[reg[1]]):
        i=LABELS[reg[2]]-1
    REGISTERS['x0'] = 0

def handle_beqz(line):
    global i
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    if(REGISTERS[reg[0]] == 0):
        i=LABELS[reg[1]]-1
    REGISTERS['x0'] = 0

def handle_bnez(line):
    global i
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    if(REGISTERS[reg[0]] != 0):
        i=LABELS[reg[1]]-1
    REGISTERS['x0'] = 0

def handle_blez(line):
    global i
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    if(REGISTERS[reg[0]] <= 0):
        i=LABELS[reg[1]]-1
    REGISTERS['x0'] = 0

def handle_j(line):
    global i
    label = line.strip()
    i=LABELS[label]-1
    REGISTERS['x0'] = 0

def handle_mv(line):
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    REGISTERS[reg[0]]=REGISTERS[reg[1]]
    REGISTERS['x0'] = 0

def handle_jal(line):
    global i
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    REGISTERS[reg[0]] = i    # now when this will be called, i will be given this value and will be incrememented in the main while loop
    i=LABELS[reg[1]]-1
    REGISTERS['x0'] = 0

def handle_jalr(line):
    global i
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    arg = reg[1]
    offset=int(arg[0:arg.find('(')].strip())
    arg=arg[arg.find('(')+1 : arg.find(')')]
    REGISTERS[reg[0]] = i
    i = REGISTERS[arg] + offset 
    REGISTERS['x0'] = 0

def handle_andi(line):
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    const =0
    if reg[2].find("0x")<0:   #means we did not find "0x"
        const = int(reg[2])       
    else:
        const= hexadecimal_to_decimal(reg[2]) 
    REGISTERS[reg[0]]=REGISTERS[reg[1]] & const
    REGISTERS['x0'] = 0

def handle_ori(line):
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    const =0
    if reg[2].find("0x")<0:   #means we did not find "0x"
        const = int(reg[2])       
    else:
        const= hexadecimal_to_decimal(reg[2]) 
    REGISTERS[reg[0]]=REGISTERS[reg[1]] | const
    REGISTERS['x0'] = 0
def handle_or(line):
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    REGISTERS[reg[0]]=REGISTERS[reg[1]] | REGISTERS[reg[2]]
    REGISTERS['x0'] = 0
def handle_sll(line):
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    REGISTERS[reg[0]]=REGISTERS[reg[1]] << REGISTERS[reg[2]]
    REGISTERS['x0'] = 0
def handle_srl(line):
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    REGISTERS[reg[0]]=REGISTERS[reg[1]] >> REGISTERS[reg[2]]
    REGISTERS['x0'] = 0
def handle_la(line):
    global i
    reg =line.split(',')
    reg = list(map(str.strip, reg))
    REGISTERS[reg[0]] = LABELS[reg[1]]    # now when this will be called, i will be given this value and will be incrememented in the main while loop
    REGISTERS['x0'] = 0

def callFunction(opcode,line):
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
    if(opcode == "sll"):
        handle_sll(line)
        return
    if(opcode == "srl"):
        handle_srl(line)
        return
    if(opcode == "la"):
        handle_la(line)
        return

def remove_side_comment(line):
    if(line.find('#')>0):
        line=line[0 : line.find('#')]
    return line

#  only handling word right now
def handle_data(line):
    global MEM_POINTER
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
            MEMORY[(MEM_POINTER-268500992)//4] = value
            MEM_POINTER+=4
    else:
        pass       
        
    

def find_labels(j):
    
    while j < len(lines):
        line=lines[j].strip()
        if line=="":
            j+=1
            continue
        if(line[0]=='#'):
            j+=1
            continue
        if(line[0]=='.' and line.find(".data") ==0):
            if(line[5:].strip()==""):
                handle_data(lines[j+1])
                j+=2
            else:
                handle_data(line[5:])
                j+=1
            continue
        label=""
        if(line.find(':')>0):
            label=line[0:line.find(':')].strip()
        if(label!=""):
            LABELS[label]=j
            line=line[line.find(':')+1:].strip()
            lines[j]=line
        j+=1

# Removing white spaces and comments
def process_lines():
    j=0
    while j < len(lines):
        line=lines[j].strip()
        if line=="":
            j+=1
            continue;
        if(line[0]=='#'):
            j+=1
            continue;
        else:
            PROCESSED_LINES.append(line)
            j+=1


process_lines()
find_labels(0)
i= LABELS["main"]
# print(i)
while i < len(lines):
    line=lines[i].strip()
    if line=="":
        i+=1
        continue
    if line[0]=='#':
        i+=1
        continue
    line = remove_side_comment(line)
    opcode = line[0 : line.find(' ')].strip()
    callFunction(opcode,line[line.find(' '):].strip())
    i+=1

print(REGISTERS)
print(MEMORY[0:10])

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
#   la rd, data_label