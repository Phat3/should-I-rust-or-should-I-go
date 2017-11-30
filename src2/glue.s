TEXT ·trampoline(SB), 0, $2048
    MOVQ SP, BX        // Save SP in a callee-saved registry
    ADDQ $2048, SP     // Rollback SP to reuse this function's frame
    ANDQ $~15, SP      // Align the stack to 16-bytes
    CALL hello(SB)
    MOVQ BX, SP        // Restore SP
    RET
