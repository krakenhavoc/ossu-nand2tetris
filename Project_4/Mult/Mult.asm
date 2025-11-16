// This file is derived from www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.

// RAM[2] = RAM[0] * RAM[1], where x = R0; y = R1; result = R2 

// result = 0
// for (i = 0; i < y; i++ ) {
//    result = x + x
// }

// Init LOOP pre-conditions
    @i
    M=0 // i = 0

    @result
    M=0 // result = 0

// Evaluate LOOP condition
(LOOP)
    @R1
    D=M
    @i
    D=D-M
    @STOP
    D;JLE // if i > y; STOP

// LOOP Logic
    @result
    D=M
    @R0
    D=D+M
    @result
    M=D    // result = result + x
    @i
    M=M+1  // i++
    @LOOP
    0;JMP

    (STOP)
    @result
    D=M
    @R2
    M=D  // R2 = result

(END)
    @END
    0;JMP