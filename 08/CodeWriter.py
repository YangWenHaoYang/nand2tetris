import os

class CodeWriter:
    """Generates assembly code from the parsed VM command"""
    
    SEGMENT_TABLE = {'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that': 'THAT'}
    
    def __init__(self, filename):
        """Opens the output file/stream and gets ready to write into it"""
        self.outputfile = open(filename, 'w')
        self.line_count = 0
        self.function_name = 'null'
        self.return_count = 0  # number of function calls


    def setFileName(self, fileName):
        """
        Informs the codeWriter that the translation of a new VM file
        has started (called by the main program of the VM translator)
        """
        fileName = os.path.split(fileName)[1]
        self.filename = '.'.join(fileName.split('.')[:-1])
        
    def writeln(self, content):
        self.outputfile.write(content + '\n')
        self.line_count += 1
        
        
    def writeInit(self):
        """
        Writes the assembly instructions that effect the bootstrap 
        code that initialize the VM. This code must be placed at the
        beginning of the generated *.asm file.
        """
        # SP=256
        self.writeln('@256')
        self.writeln('D=A')
        self.writeln('@SP')
        self.writeln('M=D')
        # call Sys.init
        self.writeCall("Sys.init", 0)
    
    
    def writeLabel(self, label = None):
        """
        Writes assembly code that effets the label command.
        """
        if label:
            label = self.function_name + '$' + label
        else:
            label = self.function_name
        self.writeln('(' + label + ')')
        self.line_count -= 1
    
    
    def writeGoto(self, label):
        """
        Writes assembly code that effects the goto command.
        """
        label = self.function_name + "$" + label
        self.writeln('@' + label)
        self.writeln('0;JMP')
    
    
    def writeIf(self, label):
        """
        Writes assembly code that effects if-goto command.
        """
        label = self.function_name + '$' + label
        self.popD()
        self.writeln('@' + label)
        self.writeln('D;JNE')
        
        
    def writeArithmetic(self, command):
        """Writes to the output file the assembly code that implements
           the given arithmetic command"""
        if command in ['not', 'neg']:
            self.writeln('@SP')
            self.writeln('A=M-1')
            if command == 'not':
                self.writeln('M=!M')
            else:  # command == 'neg'
                self.writeln('M=-M')
            return        
        self.writeln('@SP')
        self.writeln('M=M-1')
        self.writeln('A=M')
        self.writeln('D=M')
        self.writeln('A=A-1')
        if command == 'add':
            self.writeln('M=D+M')
        elif command == 'sub':
            self.writeln('M=M-D')
        elif command == 'and':
            self.writeln('M=D&M')
        elif command == 'or':
            self.writeln('M=D|M')
        elif command in ['eq', 'lt', 'gt']:
            self.writeln('D=M-D')
            self.writeln('@' + str(self.line_count+7))
            if command == 'eq':
                self.writeln('D; JEQ')
            elif command == 'lt':
                self.writeln('D; JLT')
            else:  # command == 'gt'
                self.writeln('D; JGT')
            self.writeln('@SP')
            self.writeln('A=M-1')
            self.writeln('M=0')
            self.writeln('@' + str(self.line_count+5))
            self.writeln('0; JMP')
            self.writeln('@SP')
            self.writeln('A=M-1')
            self.writeln('M=-1')
                
        
    def writePushPop(self, command, segment, index):
        """Writes to the output file the assembly code that implements
           the given command, where command is either C_PUSH or C_POP"""
        seg_pt = self.SEGMENT_TABLE.get(segment, None)
        if command == 'C_PUSH':
            if seg_pt:    # local, argument, this, that
                self.writeln('@' + seg_pt)
                self.writeln('D=M')
                self.writeln('@' + str(index))
                self.writeln('A=D+A')
                self.writeln('D=M')             
            elif segment == 'constant':
                self.writeln('@' + str(index))
                self.writeln('D=A')
            elif segment == 'static':
                self.writeln('@' + self.filename + '.' + str(index))
                self.writeln('D=M')
            elif segment == 'temp':
                self.writeln('@' + str(5+index))
                self.writeln('D=M')
            else:  # segment == 'pointer'
                if index == '0':
                    self.writeln('@THIS')
                else:
                    self.writeln('@THAT')
                self.writeln('D=M')
            self.pushD()
        else:  # command == 'C_POP'
            if seg_pt:    # local, argument, this, that
                self.writeln('@' + str(index))
                self.writeln('D=A')
                self.writeln('@' + seg_pt)
                self.writeln('D=D+M')
                self.writeln('@R13')
                self.writeln('M=D')
                self.popD()                
                self.writeln('@R13')
                self.writeln('A=M')
                self.writeln('M=D')
            elif segment == 'static':
                self.popD()
                self.writeln('@' + self.filename + '.' + str(index))
                self.writeln('M=D')
            elif segment == 'temp':
                self.popD()
                self.writeln('@' + str(5+index))
                self.writeln('M=D')
            else:  # segment == 'pointer'
                self.popD()
                if index == 0:
                    self.writeln('@THIS')
                else:
                    self.writeln('@THAT')
                self.writeln('M=D')
  
    
    def writeFunction(self, functionName, numVars):
        """
        Writes assembly code that effects the function command.
        """
        self.function_name = functionName
        self.return_count = 0
        # (functionName)
        self.writeLabel()
        # repeat nVars times: push 0
        self.writeln('@0')
        self.writeln('D=A')
        for _ in range(numVars):
            self.pushD()
    
    
    
    def writeCall(self, functionName, numArgs):
        """
        Writes assembly code that effects the call command.
        
        """
        # push returnAddress
        self.return_count += 1
        label = 'ret.' + str(self.return_count)
        self.writeln('@' + self.function_name + '$' + label)
        self.writeln('D=A')
        self.pushD()
        # push LCL, ARG, THIS, THAT
        for segment in ["LCL", "ARG", "THIS", "THAT"]:
            self.writeln('@' + segment)
            self.writeln('D=M')
            self.pushD()
        # ARG = SP - 5 - numArgs
        self.writeln('@SP')
        self.writeln('D=M')
        self.writeln('@' + str(int(numArgs)+5))
        self.writeln('D=D-A')
        self.writeln('@ARG')
        self.writeln('M=D')
        # LCL = SP
        self.writeln('@SP')
        self.writeln('D=M')
        self.writeln('@LCL')
        self.writeln('M=D')
        # goto functionName
        self.writeln('@' + functionName)
        self.writeln('0;JMP')
        # (returnAddress)
        self.writeLabel(label)
        
        
    
    def writeReturn(self):
        """
        Writes assembly code that effects the return command.
        """
        # endFrame = LCL
        self.writeln('@LCL')
        self.writeln('D=M')
        self.writeln('@R13')   # R13 = endFrame
        self.writeln('M=D')
        # retAddr = *(endFrame - 5)
        self.writeln('@5')
        self.writeln('A=D-A')
        self.writeln('D=M')
        self.writeln('@R14')    # R14 = retAddr
        self.writeln('M=D')
        # *ARG = pop()
        self.popD()
        self.writeln('@ARG')
        self.writeln('A=M')
        self.writeln('M=D')
        # SP = ARG + 1
        self.writeln('D=A')
        self.writeln('@SP')
        self.writeln('M=D+1')
        # THAT = *(endFrame - 1)
        # THIS = *(endFrame - 2)
        # ARG = *(endFrame - 3)
        # LCL = *(endFrame - 4)
        for segment in ['THAT', 'THIS', 'ARG', 'LCL']:
            self.writeln('@R13')
            self.writeln('AM=M-1')
            self.writeln('D=M')
            self.writeln('@' + segment)
            self.writeln('M=D')
        # goto retAddr
        self.writeln('@R14')
        self.writeln('A=M')
        self.writeln('0;JMP')
      
        
    def popD(self):
        self.writeln('@SP')
        self.writeln('AM=M-1')
        self.writeln('D=M')
        
    def pushD(self):
        self.writeln('@SP')
        self.writeln('M=M+1')
        self.writeln('A=M-1')
        self.writeln('M=D')

    def close(self):
        """Closes the output file"""
        self.outputfile.close()















    
