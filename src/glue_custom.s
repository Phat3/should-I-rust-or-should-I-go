TEXT ·custom(SB), 0, $256-8
    MOVQ SP, BX
    ANDQ $~15, SP
    SUBQ $16, SP
    MOVQ SP, DI
    CALL get_code_1(SB)
    MOVQ AX, R12
    MOVQ SP, DI
    ADDQ $8, DI
    CALL get_code_2(SB)
    MOVQ (AX), DX
    MOVQ $8, CX
    MOVQ (R12), DI
    MOVQ $8, SI
    CALL get_detonation_code(SB)
    MOVQ BX, SP
    MOVQ AX, ret+8(FP)
    RET
