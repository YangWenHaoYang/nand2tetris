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
        elif parser.commandType() == 'C_LABEL':
            codewriter.writeLabel(parser.arg1())
        elif parser.commandType() == 'C_GOTO':
            codewriter.writeGoto(parser.arg1())
        elif parser.commandType() == 'C_IF':
            codewriter.writeIf(parser.arg1())
        elif parser.commandType() == 'C_FUNCTION':
            codewriter.writeFunction(parser.arg1(), parser.arg2())
        elif parser.commandType() == 'C_CALL':
            codewriter.writeCall(parser.arg1(), parser.arg2())
        elif parser.commandType() == 'C_RETURN':
            codewriter.writeReturn()
        parser.advance()
        
def ListVmFile(path):
    ret = []
    if os.path.isfile(path):
        if path.endswith('.vm'):
            ret = [path]
    else:
        files = [os.path.join(path, file) for file in os.listdir(path)]
        for file in files:
            ret.extend(ListVmFile(file))
    return ret
        
if __name__ == '__main__':
    """Initializes the I/O files and drives the process"""
    if len(sys.argv) != 2:
        print('Usage: python VMTranslator.py <source-file>.vm or <source-dir>')
        sys.exit(1)
    else:
        inputpath = os.path.relpath(sys.argv[1])
        # get a list of VM files to be parsed
        inputfiles = ListVmFile(inputpath)
    
        if os.path.isfile(inputpath):
            outputfile =  '.'.join(inputpath.split('.')[:-1]) + '.asm'
        else:
            outputfile = os.path.join(inputpath, os.path.split(inputpath)[1]+'.asm')
        codewriter = CodeWriter(outputfile)
        has_sys_init = any(['Sys.vm' in inputfile for inputfile in inputfiles])
        if has_sys_init:
            codewriter.writeInit()
        for inputfile in inputfiles:
            parser = Parser(inputfile)
            codewriter.setFileName(inputfile)
            translate(parser, codewriter)
        codewriter.close()
            
