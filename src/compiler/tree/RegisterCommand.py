from enum import Enum
from src.compiler.RegisterManager import parse_register_to_str
from src.compiler.RegisterManager import register_manager


class RegisterParametersError(Exception):
    message = "You typed arguments to register command in wrong order."


class RegisterCommandType(Enum):
    GET = "GET"
    PUT = "PUT"
    LOAD = "LOAD"
    STORE = "STORE"
    INC = "INC"
    DEC = "DEC"
    HALF = "HALT"
    COPY = "COPY"
    ADD = "ADD"
    SUB = "SUB"
    JUMP = "JUMP"
    JZERO = "JZERO"
    JODD = "JODD"
    HALT = "HALT"

    def __str__(self):
        return str(self.value)


# TODO: Change signature of __init__. arguments could be of any type, including Register(). But I must check if are specified and both can be optional
# TODO: I'm not sure, but probably I finished refactoring it. I should test it first.
class RegisterCommand:
    value: str = ""
    command_type: RegisterCommandType
    command_arg_1: str
    command_arg_2: str

    def __init__(self, command_type: RegisterCommandType, command_arg_1=None, command_arg_2=None):
        if not command_arg_1 and command_arg_2:
            raise RegisterParametersError()

        if command_type == RegisterCommandType.GET or command_type == RegisterCommandType.PUT or \
                command_type == RegisterCommandType.LOAD or command_type == RegisterCommandType.STORE or \
                command_type == RegisterCommandType.INC or command_type == RegisterCommandType.DEC or \
                command_type == RegisterCommandType.HALF or command_type == RegisterCommandType.COPY or \
                command_type == RegisterCommandType.ADD or command_type == RegisterCommandType.SUB or \
                command_type == RegisterCommandType.JZERO or command_type == RegisterCommandType.JODD:
            command_arg_1 = command_arg_1.name_str
            # command_arg_1 = parse_register_to_str(int(command_arg_1))

        if command_type == RegisterCommandType.COPY or command_type == RegisterCommandType.ADD or \
                command_type == RegisterCommandType.SUB:
            command_arg_2 = command_arg_2.name_str
            # command_arg_2 = parse_register_to_str(command_arg_2)

        if command_arg_1:
            command_arg_1 = " " + str(command_arg_1)
        if command_arg_2:
            command_arg_2 = " " + str(command_arg_2)
        self.value = str(command_type) + str(command_arg_1) + str(command_arg_2) + "\n"
        self.command_arg_1 = str(command_arg_1)
        self.command_arg_2 = str(command_arg_2)

    def __str__(self):
        return self.value


def connect_all_commands(commands: [RegisterCommand]) -> ([RegisterCommand], str):
    index = 0
    output_str = ""

    while index < len(commands):
        command = commands[index]
        if command.command_type == RegisterCommandType.JUMP:
            commands[index].value = str(command.command_type) + " " + str(int(command.command_arg_1) + index) + "\n"
        elif command.command_type == RegisterCommandType.JODD or command.command_type == RegisterCommandType.JZERO:
            commands[index].value = str(command.command_type) + " " + command.command_arg_1 + str(int(command.command_arg_1) + index) + "\n"
        output_str += command.value
        index += 1
    return commands, output_str


def concat_commands(commands_1: [RegisterCommand], commands_2: [RegisterCommand]) -> [RegisterCommand]:
    for comm in commands_2:
        commands_1.append(comm)
    return commands_1


def make_number_commands(reg, number):
    reg_help = register_manager.get_free_registers(1)
    effect: [RegisterCommand] = [RegisterCommand(RegisterCommandType.SUB, reg, reg),
                                 RegisterCommand(RegisterCommandType.SUB, reg_help, reg_help),
                                 RegisterCommand(RegisterCommandType.INC, reg_help)]
    res = 0
    iq = 1

    while 2 * iq < number:
        iq = 2 * iq
        effect.append(RegisterCommand(RegisterCommandType.ADD, reg_help, reg_help))

    while res != number:
        while res + iq > number:
            iq = iq / 2
            effect.append(RegisterCommand(RegisterCommandType.HALF, reg_help))
        res += iq
    effect.append(RegisterCommand(RegisterCommandType.ADD, reg, reg_help))
    return effect


def addition_commands(reg, reg_help):
    reg_help.free()
    return [RegisterCommand(RegisterCommandType.ADD, reg, reg_help)]


def substraction_commands(reg, reg_help):
    reg_help.free()
    return [RegisterCommand(RegisterCommandType.SUB, reg, reg_help)]


def multiplication_commands(reg_1, reg_2):
    result: [RegisterCommand] = []
    regs = register_manager.get_free_registers(3)
    reg_3 = regs[0]
    reg_4 = regs[1]
    reg_5 = regs[2]
    result.append(RegisterCommand(RegisterCommandType.SUB, reg_4, reg_4))
    result.append(RegisterCommand(RegisterCommandType.JZERO, reg_1, "32"))
    result.append(RegisterCommand(RegisterCommandType.JZERO, reg_1, "31"))

    result.append(RegisterCommand(RegisterCommandType.SUB, reg_3, reg_3))

'''
put(result, SUB, reg4, reg4);
put(result, JZERO, reg1, "32");
put(result, JZERO, reg2, "31");

put(result, SUB, reg3, reg3);
put(result, INC, reg3, "");
put(result, COPY, reg5, reg2);
put(result, INC, reg2, "");
put(result, SUB, reg2, reg3);
put(result, JZERO, reg2, "7");

put(result, DEC, reg2, "");
put(result, JZERO, reg2, "7");

put(result, COPY, reg2, reg5);
put(result, ADD, reg1, reg1);
put(result, ADD, reg3, reg3);
put(result, JUMP, "-9", "");

put(result, HALF, reg3, "");
put(result, HALF, reg1, "");
put(result, COPY, reg2, reg5);
put(result, SUB, reg2, reg3);
put(result, ADD, reg4, reg1);
put(result, JZERO, reg2, "13");

put(result, COPY, reg5, reg2);
put(result, INC, reg2, "");
put(result, SUB, reg2, reg3);
put(result, JZERO, reg2, "5");

put(result, COPY, reg2, reg5);
put(result, SUB, reg2, reg3);
put(result, ADD, reg4, reg1);
put(result, JUMP, "-8", "");

put(result, COPY, reg2, reg5);
put(result, HALF, reg3, "");
put(result, HALF, reg1, "");
put(result, JUMP, "-11", "");

put(result, COPY, reg1, reg4);

release_register(reg2, "1008");
release_register(reg3, "1009");
release_register(reg4, "1010");
release_register(reg5, "1011");

return result;
}





map < long
long, tuple < long
long, string, string > >
*division_MR(string
key1, string
key2) {

string
reg1 = get_reg(key1);
string
reg2 = get_reg(key2);
map < long
long, tuple < long
long, string, string > >
*result = new
map < long
long, tuple < long
long, string, string > >;

string
reg3 = get_from_register_manager();
register_register(reg3, "");
string
reg4 = get_from_register_manager();
register_register(reg4, "");
string
reg5 = get_from_register_manager();
register_register(reg5, "");

put(result, SUB, reg4, reg4);
put(result, JZERO, reg1, "31");
put(result, JZERO, reg2, "30");

put(result, SUB, reg3, reg3);
put(result, INC, reg3, "");
put(result, COPY, reg5, reg1);
put(result, INC, reg1, "");
put(result, SUB, reg1, reg2);
put(result, JZERO, reg1, "7");

put(result, DEC, reg1, "");
put(result, JZERO, reg1, "7");

put(result, COPY, reg1, reg5);
put(result, ADD, reg2, reg2);
put(result, ADD, reg3, reg3);
put(result, JUMP, "-9", "");

put(result, HALF, reg3, "");
put(result, HALF, reg2, "");
put(result, COPY, reg1, reg5);
put(result, SUB, reg1, reg2);
put(result, ADD, reg4, reg3);
put(result, JZERO, reg3, "12");

put(result, COPY, reg5, reg1);
put(result, INC, reg1, "");
put(result, SUB, reg1, reg2);
put(result, JZERO, reg1, "4");

put(result, DEC, reg1, "");
put(result, ADD, reg4, reg3);
put(result, JUMP, "-7", "");

put(result, COPY, reg1, reg5);
put(result, HALF, reg3, "");
put(result, HALF, reg2, "");
put(result, JUMP, "-10", "");

put(result, COPY, reg1, reg4);

release_register(reg2, "1208");
release_register(reg3, "1209");
release_register(reg4, "1210");
release_register(reg5, "1211");

return result;
}




map < long
long, tuple < long
long, string, string > >
*modulation_MR(string
key1, string
key2) {

string
reg1 = get_reg(key1);
string
reg2 = get_reg(key2);
map < long
long, tuple < long
long, string, string > >
*result = new
map < long
long, tuple < long
long, string, string > >;

string
reg3 = get_from_register_manager();
register_register(reg3, "");
string
reg4 = get_from_register_manager();
register_register(reg4, "");
string
reg5 = get_from_register_manager();
register_register(reg5, "");

put(result, SUB, reg4, reg4);
put(result, JZERO, reg1, "31");
put(result, JZERO, reg2, "30");

put(result, SUB, reg3, reg3);
put(result, INC, reg3, "");
put(result, COPY, reg5, reg1);
put(result, INC, reg1, "");
put(result, SUB, reg1, reg2);
put(result, COPY, reg4, reg5);
put(result, JZERO, reg1, "7");

put(result, DEC, reg1, "");
put(result, JZERO, reg1, "20");

put(result, COPY, reg1, reg5);
put(result, ADD, reg2, reg2);
put(result, ADD, reg3, reg3);
put(result, JUMP, "-9", "");

put(result, HALF, reg3, "");
put(result, HALF, reg2, "");
put(result, COPY, reg1, reg5);
put(result, JZERO, reg3, "13");

put(result, COPY, reg5, reg1);
put(result, INC, reg1, "");
put(result, SUB, reg1, reg2);
put(result, JZERO, reg1, "4");

put(result, DEC, reg1, "");
put(result, SUB, reg4, reg2);
put(result, JUMP, "-6", "");

put(result, COPY, reg1, reg5);
put(result, HALF, reg3, "");
put(result, HALF, reg2, "");
put(result, JUMP, "-11", "");

put(result, SUB, reg4, reg4);
put(result, COPY, reg1, reg4);

release_register(reg2, "1208");
release_register(reg3, "1209");
release_register(reg4, "1210");
release_register(reg5, "1211");

return result;
}

'''