from src.compiler.tree.CommandNode import CommandNode, str_comms


class ProgramNode:
    def __init__(self, memory_manager, commandsNode):
        self.memory_manager = memory_manager
        self.commandsNode = commandsNode

    # TODO
    def get_machine_code(self):
        return self.commandsNode.get_machine_code

    def __str__(self):
        return "Program: /*\n" + str(self.memory_manager) + ";\n" + print_commands(self.commandsNode) + "\n*/"


# TODO: building all commands based on specific objects.
def print_commands(commands):
    res = ""
    for comm in commands:
        res += str(comm) + "\n"
    return res
