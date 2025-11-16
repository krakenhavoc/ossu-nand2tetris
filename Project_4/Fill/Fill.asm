// This file is derived from www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

//    screen_start = SCREEN
//    screed_end   = 24575
//
// LOOP (while True):
//    screen_addr = screen_start
//    if key == pressed goto BLACK_SCREEN
//    elif screen_addr >= screen_end goto LOOP
//    else
//        RAM[screen_addr] = 0
//        screen_addr = screen_addr + 1 // advances screen memory map index
//        goto LOOP 
//
// BLACK_SCREEN
//    if screen_addr >= screen_end goto LOOP
//    else
//        RAM[screen_addr] = -1
//        screen_addr = screen_addr + 1 // advances screen memory map index
//        goto BLACK_SCREEN
    


// Initialize pre-conditions

    @SCREEN
    D=A
    @screen_start
    M=D            // address = 16384 (base addr of screen)
    @24575
    D=A
    @screen_end
    M=D            // address = 24575 (last addr of screen)

(LOOP)

// Reset screen_addr
    @screen_start
    D=M
    @screen_addr
    M=D

// Evaluate keyboard event
    @KBD
    D=M
    @BLACK_SCREEN
    D;JNE  // if key == pressed goto BLACK_SCREEN

(WHITE_SCREEN)
    @screen_end
    D=M
    @screen_addr
    D=D-M
    @LOOP
    D;JLE // if screen_addr >= screen_end goto LOOP

    @screen_addr
    D=M   // holds current screen index
    A=M   // loads current screen index addr
    M=0   // RAM[screen_addr] = 0
    
    @screen_addr
    M=D+1 // screen_addr = screen_addr + 1 // advances screen memory map index

    @WHITE_SCREEN
    0;JMP // goto WHITE_SCREEN

(BLACK_SCREEN)
    @screen_end
    D=M
    @screen_addr
    D=D-M
    @LOOP
    D;JLE // if screen_addr >= screen_end goto LOOP

    @screen_addr
    D=M   // holds current screen index
    A=M   // loads current screen index addr
    M=-1  // RAM[screen_addr] = -1
    
    @screen_addr
    M=D+1 // screen_addr = screen_addr + 1 // advances screen memory map index

    @BLACK_SCREEN
    0;JMP // goto BLACK_SCREEN

@LOOP
0;JMP // Infinite LOOP