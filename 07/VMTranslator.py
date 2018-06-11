from Parser import *
from CodeWriter import *
import sys, os

def translate(parser, codewriter):
    """Translate VM file into assembly file"""
    while parser.hasMoreCommands():
        if parser.commandType() == 'C_ARITHMETIC':
            codewriter.writeArithmetic(parser.arg1())
        elif parser.commandType() in ['C_PUSH', 'C_POP']:
            codewriter.writePushPop(parser.commandType(), parser.arg1(), parser.arg2())
        parser.advance()


if __name__ == '__main__':
    """Initializes the I/O files and drives the process"""
    if len(sys.argv) != 2:
        print('Usage: python VMTranslator.py inputFile.vm')
        sys.exit(1)
    else:
        filename = os.path.relpath(sys.argv[1])
        parser = Parser(filename)
        codewriter = CodeWriter(filename.replace('.vm', '.asm'))
        translate(parser, codewriter)
