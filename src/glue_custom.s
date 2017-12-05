TEXT ·custom(SB), 0, $256-8
    MOVQ SP, BX
    ANDQ $~15, SP
    SUBQ $16, SP
    MOVQ SP, DI
    MOVQ $1454620416, SI
    CALL get_token(SB)
    MOVQ $1454620416, DI
    MOVQ (AX), SI
    MOVQ $20, DX
    CALL get_detonation_code(SB)
    MOVQ BX, SP
    MOVQ AX, ret+8(FP)
    RET
