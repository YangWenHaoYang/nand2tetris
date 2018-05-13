import Parser
import Code
import SymbolTable
import sys, os, string


class HackAssembler:
    """ initializes and maintans symbol table """

    def __init__(self, filename):
        self.symbolTable = SymbolTable.SymbolTable()
        self.code = Code.Code()
        self.filename = filename
        self.outputFile = open(self.filename.replace('.asm', '.hack'), 'w')
        
    def firstPass(self):
        parser = Parser.Parser(self.filename)
        currAddr = 0
        while parser.hasMoreCommands():
            parser.advance()
            if parser.commandType() == 'Label':
                self.symbolTable.allocate(parser.symbol(), currAddr)
            else:
                currAddr += 1

    def secondPass(self):
        parser = Parser.Parser(self.filename)
        symbolAddr = 16
        while parser.hasMoreCommands():
            parser.advance()
            if parser.commandType() == 'A instruction':
                if not parser.symbol().isdigit() and \
                  not self.symbolTable.isContain(parser.symbol()):
                    self.symbolTable.allocate(parser.symbol(), symbolAddr)
                    symbolAddr += 1
                    

    def translate(self):
        parser = Parser.Parser(self.filename)
        while parser.hasMoreCommands():
            parser.advance()
            if parser.commandType() == 'A instruction':
                if parser.symbol().isdigit():
                    line = bin(int(parser.symbol()))[2:].zfill(16)
                    self.outputFile.write(line + '\n')
                else:
                    addr = self.symbolTable.getAddress(parser.symbol())
                    line = bin(int(addr))[2:].zfill(16)
                    self.outputFile.write(line + '\n')
            elif parser.commandType() == 'C instruction':
                line = '111' + self.code.getComp(parser.comp()) + \
                       self.code.getDest(parser.dest()) + self.code.getJump(parser.jump())
                self.outputFile.write(line + '\n')
        self.outputFile.close()

if __name__ == '__main__':
    """ initializes the I/O files and drives the process """
    if len(sys.argv) != 2:
        print('Usage: python HackAssembler.py inputFile.asm')
        sys.exit(1)
    else:
        assembler = HackAssembler(filename=sys.argv[1])
        assembler.firstPass()
        assembler.secondPass()
        assembler.translate()
        
        
