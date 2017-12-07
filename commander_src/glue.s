TEXT ·callCheckCore(SB), 0, $256-16
    MOVQ f_ptr+0(FP), AX
    MOVQ SP, BX
    ADDQ $256, SP
    ANDQ $~15, SP
    CALL AX
    MOVQ BX, SP 
    MOVQ AX, ret+8(FP)
    RET

TEXT ·callToggleEni(SB), 0, $256-16
    MOVQ f_ptr+0(FP), AX
    MOVQ SP, BX
    ADDQ $256, SP
    ANDQ $~15, SP
    CALL AX
    MOVQ BX, SP 
    MOVQ AX, ret+8(FP)
    RET

TEXT ·callSetVariableYield(SB), 0, $256-24
    MOVQ f_ptr+0(FP), AX
    MOVQ f_ptr+8(FP), DI
    MOVQ SP, BX
    ADDQ $256, SP
    ANDQ $~15, SP
    CALL AX
    MOVQ BX, SP 
    MOVQ AX, ret+8(FP)
    RET

TEXT ·callSetDtAmount(SB), 0, $256-24
    MOVQ f_ptr+0(FP), AX
    MOVQ f_ptr+8(FP), DI
    MOVQ SP, BX
    ADDQ $256, SP
    ANDQ $~15, SP
    CALL AX
    MOVQ BX, SP 
    MOVQ AX, ret+8(FP)
    RET

TEXT ·callDefuse(SB), 0, $256-40
    MOVQ f_ptr+0(FP), AX
    MOVQ f_ptr+8(FP), DI
    MOVQ f_ptr+16(FP), SI
    MOVQ f_ptr+24(FP), DX
    MOVQ SP, BX
    ADDQ $256, SP
    ANDQ $~15, SP
    CALL AX
    MOVQ BX, SP 
    MOVQ AX, ret+8(FP)
    RET
