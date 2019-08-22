class ProgramNode:
    def __init__(self, declarationsNode, commandsNode):
        self.declarationsNode = declarationsNode
        self.commandsNode = commandsNode

    def get_machine_code(self):
        return self.commandsNode.get_machine_code

    def __str__(self):
        return "Program: /*" + str(self.declarationsNode) + "; " + str(self.commandsNode) + "*/"
