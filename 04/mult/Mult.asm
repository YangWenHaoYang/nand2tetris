// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

	@R0
	D = M
	@mul
	M = D		// mul = RAM[0]

	@R1
	D = M
	@n
	M = D		// n = RAM[1]

//	@R2
//	M = 0		// RAM[2] = 0

	@product
	M = 0		// product = 0

	@i
	M = 1		// i = 1

(LOOP)
	@n
	D = M
	@i
	D = M - D
	@STOP
	D; JGT		// if i > n goto STOP

	@mul
	D = M
	@product
	M = M + D	// product = product + mul

	@i
	M = M + 1	// i = i + 1

	@LOOP
	0; JMP

(STOP)
	@product
	D = M
	@R2
	M = D		// ROM[2] = product

(END)
	@END
	0; JMP
		
