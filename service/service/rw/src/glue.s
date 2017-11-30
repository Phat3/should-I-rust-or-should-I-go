TEXT ·trampoline(SB), 0, $2048
    MOVQ SP, BX 
    ADDQ $2048, SP
    ANDQ $~15, SP
    CALL hello(SB)
    MOVQ BX, SP
    RET

