class Parser:
    """Parses each VM command into its lexical elements.
         * Handles the parsing of single .vm file
         * Reads a VM command, parses the command into its lexical
         components, and provides convenient access to these components
         * Ignores all white space and comments
    """
    
    def __init__(self, filename):
        """Opens the input file/stream and gets ready to prase it"""
        self.inFile = open(filename, 'r')
        self.commands = []
        self.currPos = 0
        self.numCom = 0
        for line in self.inFile.readlines():
            line = line.split('//')[0].strip('\n')
            if line != '':
                self.commands.append(line)
                self.numCom += 1

    def hasMoreCommands(self):
        """Returns True if there are more commands in the input,
        otherwise returns False"""
        if self.currPos < self.numCom:
            return True
        else:
            return False

    def advance(self):
        """Reads the next command from the input and makes it the
           current command"""
        if self.hasMoreCommands():
            self.currCom = self.commands[self.currPos]
            self.currPos += 1

    def commandType(self):
        """Returns a constant representing the type of the current
           command"""
        currType = self.currCom.split()[0]
        if currType in ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']:
            return 'C_ARITHMETIC'
        if currType in ['push', 'pop']:
            return 'C_' + currType.upper()

    def arg1(self):
        """Returns the first argument of the current command"""
        if self.commandType() == 'C_ARITHMETIC':
            return self.currCom.split()[0]
        elif self.commandType() in ['C_PUSH', 'C_POP']:
            return self.currCom.split()[1]

    def arg2(self):
        """Returns the second argument of the current command"""
        if self.commandType() in ['C_PUSH', 'C_POP']:
            return self.currCom.split()[2]
        
