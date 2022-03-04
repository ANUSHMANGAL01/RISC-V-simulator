 .data 
ARRAY: .word 3, 4 , 55 ,6, 56, 67


# sample code

main: 
li x1, -36
addi x2, x1, 0x0000002f
lui x5, 0x11000
mv x4, x5
blt x1 ,x2,label2
label1    :  li x3, 40
label2    :  li x4, 3330
# checking the jump statements
j label5
label3    :  li x5, 40 
label5    :  li x6, 10


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


# main: 
# la x10, ARRAY
# li x1, 5
# lw x1, 0(x10)
# li x2, 10
# and x3, x1, x2   # 0
# or x4, x1, x2  # 15
# andi x5, x1, 6    # 4
# sll x6, x1, x2   # 5120
