from src.compiler.tree.CommandNode import CommandNode


class ProgramNode:
    def __init__(self, memory_manager, register_manager, commands_object_array):
        self.memory_manager = memory_manager
        self.register_manager = register_manager
        self.commands_array = commands_object_array
        self.translate(commands_object_array)

    # TODO
    def get_machine_code(self):
        pass

    def __str__(self):
        return "Program: /*\n" + str(self.memory_manager) + ";\n" + print_commands(self.commands_array) + "\n*/"

    # TODO: building all commands based on specific objects.
    def translate(self, command_object_array: [CommandNode]):

        pass


def print_commands(commands: [CommandNode]):
    res = ""
    for comm in commands:
        res += str(comm) + "\n"
    return res
