# sample code

# li x1, -36
# addi x2, x1, 0x0000002f
# lui x5, 0x11000
# mv x4, x5
# blt x1 ,x2,label2
# label1    :  li x3, 40
# label2    :  li x4, 3330
# checking the jump statements
# j label5
# label3    :  li x5, 40 
# label5    :  li x6, 10


# lui x1, 0x10020
# load upper part of register s0(20) with 0x10020

# lw x2, 0(x1)
# load s1 with the contents of memory address 0x10020000 = 7 

# lw x3, 4(x1)
# load s1 with the contents of memory address 0x10020004 = 10

# lw x4, 8(x1)
# load s1 with the contents of memory address 0x10020008 = 5    

# add x2, x2, x3   # add the first two numbers
# add x5, x2, x4   


func: 
add x3, x4, x5
addi x3, x3, 1
jalr x0, 0(x1)
main: 
li x1, 5
li x2, 5
li x3, 6
li x4, 7
li x5, 8
add x6, x1, x2
jal x1, func
add x7, x2, x3
