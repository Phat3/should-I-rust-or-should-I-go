TEXT ·custom(SB), 0, $512-8
    MOVQ SP, BX
    ANDQ $~15, SP
    SUBQ $32, SP
    MOVQ $0x4d6f3679, (SP)
    MOVQ $0x6d4c5159, 4(SP)
    MOVQ $0x6a446f55, 8(SP)
    MOVQ $0x49646d55, 12(SP)
    MOVQ $0x35356265, 16(SP)
    MOVQ $1726387586, DI
    MOVQ SP, SI
    MOVQ $20, DX
    CALL set_detonation_code(SB)
    MOVQ BX, SP
    MOVQ AX, ret+8(FP)
    RET
