TEXT ·trampoline(SB), 0, $256-16
    MOVQ f_ptr+0(FP), AX // Load the argument before messing with SP
    MOVQ SP, BX        // Save SP in a callee-saved registry
    ADDQ $256, SP      // Rollback SP to reuse this function's frame
    ANDQ $~15, SP      // Align the stack to 16-bytes
    CALL AX
    MOVQ BX, SP        // Restore SP
    MOVQ AX, ret+8(FP) // Place the return value on the stack
    RET


TEXT ·call_get_flag(SB), 0, $256-8
    MOVQ SP, BX        // Save SP in a callee-saved registry
    ANDQ $~15, SP      // Align the stack to 16-bytes
    ADDQ $32, SP
    MOVQ $0x41414141, 0(SP)
    MOVQ $0x42424242, 4(SP)
    MOVQ $0x43434343, 8(SP)
    MOVQ $0x44444444, 12(SP)
    MOVQ SP, DI
    MOVQ $8, SI
    MOVQ SP, DX
    ADDQ $8, DX
    MOVQ $8, CX
    CALL get_detonation_code(SB)
    MOVQ BX, SP        // Restore SP
    RET
