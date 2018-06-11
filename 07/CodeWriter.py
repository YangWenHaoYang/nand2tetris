class CodeWriter:
    """Generates assembly code from the parsed VM command"""
    
    SEGMENT_TABLE = {'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that': 'THAT'}
    
    def __init__(self, filename):
        """Opens the output file/stream and gets ready to write into it"""
        self.outputfile = open(filename, 'w')
        self.filename = filename.split('.')[0]
        self.line_count = 0

    def writeln(self, content):
        self.outputfile.write(content + '\n')
        self.line_count += 1
              
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













    
