from gettext import find

# File Handling
file = open("assemblyFile.asm", "r")
lines = file.readlines();
file.close()

global i
i=0
MEMORY = [0]*1024*2
MEMORY[10] =10;
INSTR_MEMORY = {}
LABELS = {}
REGISTERS = {'x0': 0, 'x1': 0, 'x2': 10, 'x3': 0, 'x4': 0, 'x5': 0, 'x6': 0, 'x7': 0, 'x8': 0,
             'x9': 0, 'x10': 0, 'x11': 0, 'x12': 0, 'x13': 0, 'x14': 0, 'x15': 0, 'x16': 0, 'x17': 0,
             'x18': 0, 'x19': 0, 'x20': 0, 'x21': 0, 'x22': 0, 'x23': 0, 'x24': 0, 'x25': 0, 'x26': 0, 'x27': 0,
             'x28': 0, 'x29': 0, 'x30': 0, 'x31': '0'}
ASSEMBLER_DIRECTIVES = {".text": 0 ,".data": 0}

def handle_add(line):
    reg =line.split(',');
    reg = list(map(str.strip, reg))
    REGISTERS[reg[0]]=REGISTERS[reg[1]]+REGISTERS[reg[2]]

def handle_addi(line):
    reg =line.split(',');
    reg = list(map(str.strip, reg))
    REGISTERS[reg[0]]=REGISTERS[reg[1]]+int(reg[2])

def handle_sub(line):
    reg =line.split(',');
    reg = list(map(str.strip, reg))
    REGISTERS[reg[0]]=REGISTERS[reg[1]]-REGISTERS[reg[2]]

def handle_slt(line):
    reg =line.split(',');
    reg = list(map(str.strip, reg))
    if(REGISTERS[reg[1]]<REGISTERS[reg[2]]):
        REGISTERS[reg[0]]=1
    else:
        REGISTERS[reg[0]]=0

def handle_lw(line):
    reg =line.split(',');
    reg = list(map(str.strip, reg))
    arg = reg[1]
    offset=int(arg[0:arg.find('(')].strip())
    arg=arg[arg.find('(')+1 : arg.find(')')]
    ma = REGISTERS[arg]+offset;
    REGISTERS[reg[0]]=MEMORY[ma] 

def handle_li(line):
    reg =line.split(',');
    reg = list(map(str.strip, reg))
    const = int(reg[1])
    REGISTERS[reg[0]]=const 

def handle_sw(line):
    reg =line.split(',');
    reg = list(map(str.strip, reg))
    arg = reg[1]
    offset=int(arg[0:arg.find('(')].strip())
    arg=arg[arg.find('(')+1 : arg.find(')')]
    ma = REGISTERS[arg]+offset;
    MEMORY[ma]=REGISTERS[reg[0]]

def handle_bne(line):
    global i
    reg =line.split(',');
    reg = list(map(str.strip, reg))
    if(REGISTERS[reg[0]]!=REGISTERS[reg[1]]):
        i=LABELS[reg[2]]-1;

def handle_beq(line):
    global i
    reg =line.split(',');
    reg = list(map(str.strip, reg))
    if(REGISTERS[reg[0]]==REGISTERS[reg[1]]):
        i=LABELS[reg[2]]-1;

def handle_blt(line):
    global i
    reg =line.split(',');
    reg = list(map(str.strip, reg))
    if(REGISTERS[reg[0]] < REGISTERS[reg[1]]):
        i=LABELS[reg[2]]-1;

def handle_bge(line):
    global i
    reg =line.split(',');
    reg = list(map(str.strip, reg))
    if(REGISTERS[reg[0]] >= REGISTERS[reg[1]]):
        i=LABELS[reg[2]]-1;

def handle_beqz(line):
    global i
    reg =line.split(',');
    reg = list(map(str.strip, reg))
    if(REGISTERS[reg[0]] == 0):
        i=LABELS[reg[1]]-1;

def handle_j(line):
    global i
    label = line.strip()
    i=LABELS[label]-1

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
    if(opcode == "j"):
        handle_j(line)
        return

def remove_side_comment(line):
    if(line.find('#')>0):
        line=line[0 : line.find('#')]
    return line

def find_labels():
    j=0
    while j < len(lines):
        line=lines[j].strip()
        label=""
        if(line.find(':')>0):
            label=line[0:line.find(':')].strip()
        if(label!=""):
            LABELS[label]=j
            line=line[line.find(':')+1:].strip()
            lines[j]=line
        j+=1

find_labels()

while i < len(lines):
    line=lines[i].strip()
    if line[0]=='#':
        i+=1
        continue
    line = remove_side_comment(line)
    opcode = line[0 : line.find(' ')].strip()
    callFunction(opcode,line[line.find(' '):].strip())
    i+=1

print(REGISTERS)
print(LABELS)

#   add rd , r1 , r2
#   addi rd , r1 , c
#   sub rd , r1 , r2 
#   slt rd , r1 , r2
#   lw  rd, offset(r1)   
#   sw  rs, offset(r1) 
#   li rd, c
#   bne r1,r2,LABEL
#   beq r1,r2,LABEL
#   blt r1,r2,LABEL
#   bgt r1,r2,LABEL
#   beqz r1,LABEL
#   j LABEL