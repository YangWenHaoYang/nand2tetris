class Parser:
    """ unpack each instruction into its underlying fields """
    
    def __init__(self, inFile):
        self.inFile = open(inFile, 'r')

        self.commands = []
        self.currPos = 0
        self.numCom = 0
        for line in self.inFile.readlines():
            line = filter(lambda ch:ch not in ' ', line).split('//')[0].strip('\n')
            if line != '':
                self.commands.append(line)
                self.numCom += 1


    def hasMoreCommands(self):
        if self.currPos < self.numCom:
            return True
        else:
            return False

    def advance(self):
        if self.hasMoreCommands():
            self.currCom = self.commands[self.currPos]
            self.currPos += 1

    def commandType(self):
        if self.currCom[0] == '@':
            return 'A instruction'
        elif self.currCom[0] == '(':
            return 'Label'
        else:
            return 'C instruction'
    
    def dest(self):
        if self.commandType() == 'C instruction':
            temp = self.currCom.split('=')
            if len(temp) > 1:
                return temp[0]
            else:
                return 'null'

    def comp(self):
        if self.commandType() == 'C instruction':
            temp = self.currCom.split('=')
            if len(temp) > 1:
                temp2 = temp[1].split(';')
                return temp2[0]
            else:
                temp3 = temp[0].split(';')
                return temp3[0]
                        

    def jump(self):
        if self.commandType() == 'C instruction':
            temp = self.currCom.split(';')
            if len(temp) > 1:
                return temp[1]
            else:
                return 'null'

    def symbol(self):
        if self.commandType() == 'A instruction':
            return self.currCom[1:]
        elif self.commandType() == 'Label':
            return self.currCom[1:len(self.currCom)-1]

    
    
