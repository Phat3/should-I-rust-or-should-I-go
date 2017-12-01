TEXT ·trampoline(SB), 0, $256-16
    MOVQ f_ptr+0(FP), AX // Load the argument before messing with SP
    MOVQ SP, BX        // Save SP in a callee-saved registry
    ADDQ $256, SP      // Rollback SP to reuse this function's frame
    ANDQ $~15, SP      // Align the stack to 16-bytes
    CALL AX
    MOVQ BX, SP        // Restore SP
    MOVQ AX, ret+8(FP) // Place the return value on the stack
    RET
