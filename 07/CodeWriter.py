class CodeWriter:
    """Generates assembly code from the parsed VM command"""
    
    def __init__(self, filename):
        """Opens the output file/stream and gets ready to write into it"""
        self.outputFile = open(filename, 'w')
        self.filename = filename.split('.')[0]
        self.popD = '@SP\nAM=M-1\nD=M\n'
        self.popA = '@SP\nAM=M-1\nA=M\n'
        self.pushD = '@SP\nM=M+1\nA=M-1\nM=D\n'
        self.counter = 0

    def writeArithmetic(self, command):
        """Writes to the output file the assembly code that implements
           the given arithmetic command"""
        label = self.filename + str(self.counter)
        codeToWrite = self.popD
        if command in ['add', 'sub', 'eq', 'gt', 'lt', 'and', 'or']:
            codeToWrite += self.popA
            if command == 'add':
                codeToWrite += 'D=D+A\n'
            elif command == 'sub':
                codeToWrite += 'D=A-D\n'
            elif command == 'eq':
                codeToWrite += 'D=D-A\n@'+label+'.EQUAL\nD;JEQ\nD=0\n@'+label+'.END\n0;JMP\n('+label+'.EQUAL)\nD=-1\n('+label+'.END)\n'
            elif command == 'gt':
                codeToWrite += 'D=A-D\n@'+label+'.GT\nD;JGT\nD=0\n@'+label+'.END\n0;JMP\n('+label+'.GT)\nD=-1\n('+label+'.END)\n'
            elif command == 'lt':
                codeToWrite += 'D=A-D\n@'+label+'.LT\nD;JLT\nD=0\n@'+label+'.END\n0;JMP\n('+label+'.LT)\nD=-1\n('+label+'.END)\n'
            elif command == 'and':
                codeToWrite += 'D=D&A\n'
            elif command == 'or':
                codeToWrite += 'D=D|A\n'
        else:
            if command == 'neg':
                codeToWrite += 'D=-D\n'
            elif command == 'not':
                codeToWrite += 'D=!D\n'
        codeToWrite += self.pushD
        self.counter += 1
        self.outputFile.write(codeToWrite)
                
    def writePushPop(self, command, segment, index):
        """Writes to the output file the assembly code that implements
           the given command, where command is either C_PUSH or C_POP"""
        memMappedSeg = {'argument':'ARG', 'local':'LCL', 'this':'THIS', 'that':'THAT',
                        'static':self.filename+'.'+str(index)}
        codeToWrite = ''
        if command == 'C_PUSH':
            if segment in ['local', 'argument', 'this', 'that', 'static']:
                codeToWrite += '@'+memMappedSeg[segment]+'\nD=M\n@'+str(index)+'\nA=A+D\nD=M\n'
            elif segment == 'pointer':
                if index == '0':
                    codeToWrite += '@THIS\nD=M\n'
                elif index == '1':
                    codeToWrite += '@THAT\nD=M\n'
            elif segment == 'constant':
                codeToWrite += '@'+str(index)+'\nD=A\n'
            elif segment == 'temp':
                codeToWrite += '@'+str(5+int(index))+'\nD=M\n'
            codeToWrite += self.pushD
        else:
            if segment in ['local', 'argument', 'this', 'that', 'static']:
                codeToWrite += '@'+str(index)+'\nD=A\n@'+memMappedSeg[segment]+'\nA=M\nD=D+A\n@addr\nM=D\n'+self.popD+'@addr\nA=M\nM=D\n'
            elif segment == 'pointer':
                codeToWrite += self.popD
                if index == '0':
                    codeToWrite += '@THIS\nM=D\n'
                elif index == '1':
                    codeToWrite += '@THAT\nM=D\n'
            elif segment == 'temp':
                codeToWrite += self.popD+'@'+str(5+int(index))+'\nM=D\n'
        self.outputFile.write(codeToWrite)

    def close(self):
        """Closes the output file"""
        end = '(END)\n@END\n0; JMP\n'
        self.outputFile.write(end)
        self.outputFile.close()















    
