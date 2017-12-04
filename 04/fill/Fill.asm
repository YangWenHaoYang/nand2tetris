// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

	@last
	M = 0		// last = 0x0000
	@state
	M = 0		// state = 0x0000
	@SETSCREEN
	0; JMP

(LOOP)
	@KBD
	D = M
	@state
	M = D		// state = RAM[KBD]
	@SETSCREEN
	D; JEQ		// if no key, set screen zeros (white)
	@state
	M = -1		// if key pressed, set screen to all 1 bits (black)

(SETSCREEN)
	@state
	D = M
	@last
	D = D - M
	@LOOP
	D; JEQ		// do nothing if new state = old state
	
	@state
	D = M
	@last
	M = D		// last = state

	@SCREEN
	D = A
	@8192
	D = D + A
	D = D - 1	// upper limit of screen address
	@i
	M = D		// i = upper limit of screen address

(SETLOOP)
	@i
	D = M
	@LOOP
	D; JLT		// if i < 0 goto LOOP

	@state
	D = M
	@i
	A = M		// A = RAM[i] = value of variable 'i'
	M = D		// RAM[A] = state
	@i
	M = M - 1	// i = i -1
	@SETLOOP
	0; JMP
	
