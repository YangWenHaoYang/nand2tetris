@111
D=A
@SP
M=M+1
A=M-1
M=D
@333
D=A
@SP
M=M+1
A=M-1
M=D
@888
D=A
@SP
M=M+1
A=M-1
M=D
@8
D=A
@StaticTest.8
A=M
D=D+A
@addr
M=D
@SP
AM=M-1
D=M
@addr
A=M
M=D
@3
D=A
@StaticTest.3
A=M
D=D+A
@addr
M=D
@SP
AM=M-1
D=M
@addr
A=M
M=D
@1
D=A
@StaticTest.1
A=M
D=D+A
@addr
M=D
@SP
AM=M-1
D=M
@addr
A=M
M=D
@StaticTest.3
D=M
@3
A=A+D
D=M
@SP
M=M+1
A=M-1
M=D
@StaticTest.1
D=M
@1
A=A+D
D=M
@SP
M=M+1
A=M-1
M=D
@SP
AM=M-1
D=M
@SP
AM=M-1
A=M
D=A-D
@SP
M=M+1
A=M-1
M=D
@StaticTest.8
D=M
@8
A=A+D
D=M
@SP
M=M+1
A=M-1
M=D
@SP
AM=M-1
D=M
@SP
AM=M-1
A=M
D=D+A
@SP
M=M+1
A=M-1
M=D
(END)
@END
0; JMP