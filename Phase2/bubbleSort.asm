.data
Array: .word 6,7,3,2,9,8, 56, 344,23,2,45
Arraysize: .word 11
.text
main:
andi x10, x10, 0
andi x11, x11, 0
andi x13, x13, 0
andi x14, x14, 0
andi x15, x15, 0
andi x16, x16, 0
la x10, Array
la x11, Arraysize
lw x11, 0(x11)
andi x11, x11, -1
andi x1, x1, 0  #taking and
outerloop:
    bge x0, x11, outerend
    andi x12, x12, 0
    addi x12, x12, 1
    innerloop:
        bge x12, x11, innerend
        lw x13, 0(x10)
        lw x15, 4(x10)
        bgt x13, x15, swap
        addi x10, x10, 4
        addi x12, x12, 1
        # j innerloop
    swap:
       mv x16, x13 
       mv x13, x15 
       mv x15, x16 
       sw x13, 0(x10) 
       sw x15, 4(x10)
       addi x10, x10, 4 
       addi x12, x12, 1
       # j innerloop
    innerend:
        la x10, Array
        addi x11, x11, -1
        # j outerloop
    outerend:
        li x31, 9999 
