@256
D=A
@SP
M=D
@.Sys.init$ret.0
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@SP
D=M
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(.Sys.init$ret.0)
(SimpleFunction.vm.SimpleFunction.test)
@2
D=A
@foo
M=D
(SimpleFunction.vm.SimpleFunction.test.init)
@SimpleFunction.vm.SimpleFunction.test.end
@foo
D=M
D;JLE
M=M-1
D=0
@SP
M=M+1
A=M-1
M=D
@SimpleFunction.vm.SimpleFunction.test.init
0;JMP
(SimpleFunction.vm.SimpleFunction.test.end)
@LCL
D=M
@0
A=A+D
D=M
@SP
M=M+1
A=M-1
M=D
@LCL
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
D=D+A
@SP
M=M+1
A=M-1
M=D
@SP
AM=M-1
D=M
D=!D
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@0
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
@ARG
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
@LCL
D=M
@endFrame
M=D
@5
A=D-A
D=M
@retAddr
M=D
@0
D=A
@ARG
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
@ARG
D=M+1
@SP
M=D
@endFrame
AM=M-1
D=M
@THAT
M=D
@endFrame
AM=M-1
D=M
@THIS
M=D
@endFrame
AM=M-1
D=M
@ARG
M=D
@endFrame
AM=M-1
D=M
@LCL
M=D
@retAddr
A=M
0;JMP