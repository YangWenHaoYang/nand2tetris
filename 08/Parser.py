class Parser:
    """Parses each VM command into its lexical elements.
         * Handles the parsing of single .vm file
         * Reads a VM command, parses the command into its lexical
         components, and provides convenient access to these components
         * Ignores all white space and comments
    """
    
    def __init__(self, filename):
        """Opens the input file/stream and gets ready to prase it"""
        self.file = open(filename, 'r')
        self.advance()    # read first line or EOF
        

    def hasMoreCommands(self):
        """Returns True if there are more commands in the input,
        otherwise returns False"""
        return bool(self.current_command)

    def advance(self):
        """Reads the next command from the input and makes it the
           current command"""
        self.current_command = self.file.readline()
        while self.current_command:
            self.current_command = self.current_command.split('//')[0]
            self.current_command = self.current_command.strip()
            if not self.current_command:    # empty line
                self.current_command = self.file.readline()
            else:   # non-empty line
                break
        self.cmd_list = self.current_command.split()

    def commandType(self):
        """Returns a constant representing the type of the current
           command"""
        current_type = self.cmd_list[0]
        if current_type in ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']:
            return 'C_ARITHMETIC'
        if current_type in ['push', 'pop']:
            return 'C_' + current_type.upper()
        if current_type in ['goto', 'label', 'call', 'return', 'function']:
            return 'C_' + current_type.upper()
        if current_type == 'if-goto':
            return 'C_IF'

    def arg1(self):
        """Returns the first argument of the current command"""
        if self.commandType() == 'C_ARITHMETIC':
            return self.cmd_list[0]
        else:
            return self.cmd_list[1]

    def arg2(self):
        """Returns the second argument of the current command"""
        return int(self.cmd_list[2])
        
