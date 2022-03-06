# Screenshots

![](Phase1/screenshots/1.PNG)

![](Phase1/screenshots/2.PNG)

![](Phase1/screenshots/3.PNG)

# Guidelines

### How to run my code?

- Clone the repo in your system
- make the desired .s or .asm file in folder
- Open gui.py
- Run gui.py
- Upload file using 'upload file' option in top left corner
- By default, the window will show the bubbleSort.asm file

### What to use as :

- ### Constants
  ##### Decimal and Hexadecimal values
- ### MemoryAddressLocation
  ##### The memory starts from the location 268500992 (which is 0x10010000 in hexadecimal) and ends at 268697599 (which is 0x1003ffff in hexadecimal). Each memory element is of four bytes. The user can either enter the decimal value for the memory or the hexadecimal value. 

### Points to note:

- We do not support the .section assembler directive. We only support .data, .text and .global
- The code must have the main function. Otherwise it will not run on our simulator.
- We do not support printing at console and taking inputs at runtime.
- In stepwise execution, the highlighted line will execute only after clicking the 'Run Stepwise' button. That means, that the line highlighted has not run yet.

### Errors to expect

- #### Syntactical errors specifying the line number in the code. 
- #### INSTRUCTION DOES NOT EXIST - Wrong opcode name.
- #### Logical error when given a wrong label name in the 'j' command.

# Arithmetic commands

## add

```
add register1 , register2 , register3
```

Adds the value of register2 and register3 and saves in register1.

## sub

```
sub register1 , register2 , register3
```

Subtracts the value of register3 from register2 and saves in register1.


## addi

```
addi register1 , register2 , <constant>
```

Adds the value of register2 and constant and saves in register1.


# Bitwise commands

## and

```
and register1 , register2 , register3
```

Does bitwise AND the values of register2 and register3 and saves in register1.

## or

```
or register1 , register2 , register3
```

Does bitwise OR the values of register2 and register3 and saves in register1.


## sll

```
sll register1 , register2 , register3
```

Bitwise shifts left the register2 value by the amount stored in register3 and saves in register1

## srl

```
srl register1 , register2 , register3
```

Bitwise shifts right the register2 value by the amount stored in register3 and saves in register1

## andi

```
andi register1 , register2 , <constant>
```

Does bitwise AND the values of register2 and the constant and saves in register1.

## ori

```
ori register1 , register2 , <constant>
```

Does bitwise OR the values of register2 and the constant and saves in register1.

# Load Commands

## li

```
li register , <constant>
```

Sets the value of the register to the given constant.

## lui

```
lui register , <constant>
```

Sets the upper 20 bits of the register to the given constant. Eg - lui x1, 0x10010

After executing this command, the value in x1 will be 0x10010000 which is 268500992 in decimal.

## la

```
la register , <Data_Label>
```

Stores the memory address of the given data label in the register. 


# Branch commands

## bne

```
bne register1  , register2 , <Label>
```

If register1 != register2 , this command jumps to the given label.

## beq

```
beq register1  , register2 , <Label>
```

If register1 == register2 , this command jumps to the given label.

## blt

```
blt register1  , register2 , <Label>
```

If register1 < register2 , this command jumps to the given label.

## bgt

```
bgt register1  , register2 , <Label>
```

If register1 > register2 , this command jumps to the given label.

## bge

```
bge register1  , register2 , <Label>
```

If register1 >= register2 , this command jumps to the given label.

## beqz

```
beqz register1 , <Label>
```

If register1 == 0 , this command jumps to the given label.

## bnez

```
bnez register1 , <Label>
```

If register1 != 0 , this command jumps to the given label.

## blez

```
blez register1 , <Label>
```

If register1 <= 0 , this command jumps to the given label.

# Jump commands

## j

```
j <Label>
```

Unconditional jump to the given label.

## jal

```
jal register , <Label>
```

Stores the next program counter (in our implementation, the global variable i) in the given register and jumps to the given label.

## jalr

```
jalr register1 , <constant>(register2) 
```

Stores the next program counter (in our implementation, the loop variable i) in the register1 and jumps to the program counter register2 + constant.

# Memory commands

## lw

```
lw register1 , <constant>(register2)
```

Sets the value of register1 to the value stored in the memory location constant + register2.

## sw

```
sw register1 , <constant>(register2)
```

Sets the value of memory at the location constant + register2 to the value of register1.

# Other commands

## mv

```
mv register1 , register2
```

Copies the value of register2 to register1.

## slt

```
slt register1 , register2 , register3
```

If register1 < register2 , this commands sets register1 to 1, otherwise 0.
