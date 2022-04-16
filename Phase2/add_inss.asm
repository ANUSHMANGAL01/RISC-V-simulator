# main:
# add x1, x2,x3
# lw x4,0(x1)
# add x11,x4,x18
# li x11, 0
# add x12,x11,x19

# main:
# add x1, x2,x3
# mv x4, x1  
# add x1,x9,x8
# add x11,x10,x18
# add x12,x11,x19
# sub x20, x12, x21
# addi x22, x23, 4


# main:
# add x1, x2, x3
# add x4, x5, x6
# sw x4, 0(x1)

# add x7, x2, x9
# sw x8, 4(x7)

# add x10, x11 ,x12

main:
add x1, x2, x3
add x4, x5, x6
beq x1, x4, label
label: 
add x10, x1, x12

# main:
# li x2, 268500994
# lw x1,0(x2)
# add x4, x1, x6
# add x1, x4, x1