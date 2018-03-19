import Parser
import CodeWriter
import sys, os, string

def translate(filename):
    """Translate VM file into assembly file"""
    parser = Parser.Parser(filename)
    codewriter = CodeWriter.CodeWriter(filename.replace('.vm', '.asm'))
    while parser.hasMoreCommands():
        parser.advance()
        if parser.commandType() == 'C_ARITHMETIC':
            codewriter.writeArithmetic(parser.arg1())
        elif parser.commandType() in ['C_PUSH', 'C_POP']:
            codewriter.writePushPop(parser.commandType(), parser.arg1(), parser.arg2())
    codewriter.close()


if __name__ == '__main__':
    """Initializes the I/O files and drives the process"""
    if len(sys.argv) != 2:
        print 'Usage: python VMTranslator.py inputFile.vm'
        sys.exit(1)
    else:
        translate(filename = sys.argv[1])
