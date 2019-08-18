from src.register_machine.register_parser import read_file
import random


def run_machine(file):
    commands = read_file(file)
    print(commands)

    memory = []
    registers = [0, 0, 0, 0, 0, 0, 0, 0]
    comm_NO = 0
    time_of_processing = 0

    for i in range(8):
        registers[i] = random.randint(0, 100)

    command_tuple = commands[comm_NO]
    print("HERE!!!")
    while command_tuple[0] != 'HALT':
        command_tuple = commands[comm_NO]

        if command_tuple[0] == "GET":
            print("? ", end='')
            registers[command_tuple[1]] = input()
            time_of_processing += 100
            comm_NO = comm_NO + 1

        elif command_tuple[0] == "PUT":
            print("> " + str(registers[command_tuple[1]]))
            time_of_processing += 100
            comm_NO = comm_NO + 1

        elif command_tuple[0] == "LOAD":
            registers[command_tuple[1]] = memory[registers[0]]
            time_of_processing += 50
            comm_NO = comm_NO + 1

        elif command_tuple[0] == "STORE":
            mem_index = registers[0]
            if len(memory) <= mem_index:
                curr_index = len(memory)
                while curr_index <= mem_index:
                    memory.append(random.randint(0, 100000))
                    curr_index += 1
            else:
                memory[mem_index] = registers[command_tuple[1]]

            memory[mem_index] = registers[command_tuple[1]]
            time_of_processing += 50
            comm_NO = comm_NO + 1

        elif command_tuple[0] == "COPY":
            registers[command_tuple[1]] = registers[command_tuple[2]]
            time_of_processing += 5
            comm_NO = comm_NO + 1

        elif command_tuple[0] == "ADD":
            registers[command_tuple[1]] += registers[command_tuple[2]]
            time_of_processing += 5
            comm_NO = comm_NO + 1

        elif command_tuple[0] == "SUB":
            if registers[command_tuple[1]] >= registers[command_tuple[2]]:
                registers[command_tuple[1]] -= registers[command_tuple[2]]
            else:
                registers[command_tuple[1]] = 0
            time_of_processing += 5
            comm_NO = comm_NO + 1

        elif command_tuple[0] == "HALF":
            registers[command_tuple[1]] = int(registers[command_tuple[1]] / 2)
            time_of_processing += 1
            comm_NO = comm_NO + 1

        elif command_tuple[0] == "INC":
            registers[command_tuple[1]] += 1
            time_of_processing += 1
            comm_NO = comm_NO + 1

        elif command_tuple[0] == "DEC":
            registers[command_tuple[1]] += 1
            if registers[command_tuple[1]] > 0:
                registers[command_tuple[1]] -= 1
            time_of_processing += 1
            comm_NO = comm_NO + 1

        elif command_tuple[0] == "JUMP":
            comm_NO = command_tuple[1]
            time_of_processing += 1

        elif command_tuple[0] == "JZERO":
            if registers[command_tuple[1]] == 0:
                comm_NO = command_tuple[2]
            else:
                comm_NO += 1
            time_of_processing += 1

        elif command_tuple[0] == "JODD":
            if registers[command_tuple[1]] % 2 != 0:
                comm_NO = command_tuple[2]
            else:
                comm_NO += 1
            time_of_processing += 1

        print(str(command_tuple[0]))
    print("HERE!!!")


run_machine('register_code.txt')

'''

void run_machine( std::vector< std::tuple<int,int,int> > & program )
{
  std::map<long long,long long> pam;

  long long r[8];
  int lr;

  long long t;

  std::cout << "Uruchamianie programu." << std::endl;
  lr = 0;
  srand( time(NULL) );
  for(int i = 0; i<8; i++ ) r[i] = rand();
  t = 0;
  while( std::get<0>(program[lr])!=HALT )	// HALT
  {
    switch( std::get<0>(program[lr]) )
    {
      case GET:		std::cout << "? "; std::cin >> r[std::get<1>(program[lr])]; t+=100; lr++; break;
      case PUT:		std::cout << "> " << r[std::get<1>(program[lr])] << std::endl; t+=100; lr++; break;
      case LOAD:	r[std::get<1>(program[lr])] = pam[r[0]]; t+=50; lr++; break;
      case STORE:	pam[r[0]] = r[std::get<1>(program[lr])]; t+=50; lr++; break;
      case COPY:	r[std::get<1>(program[lr])] = r[std::get<2>(program[lr])] ; t+=5; lr++; break;
      case ADD:		r[std::get<1>(program[lr])] += r[std::get<2>(program[lr])] ; t+=5; lr++; break;
      case SUB:		if( r[std::get<1>(program[lr])] >= r[std::get<2>(program[lr])] )
                          r[std::get<1>(program[lr])] -= r[std::get<2>(program[lr])];
                        else
                          r[std::get<1>(program[lr])] = 0;
                        t+=5; lr++; break;
      case HALF:	r[std::get<1>(program[lr])] >>= 1; t+=1; lr++; break;
      case INC:		r[std::get<1>(program[lr])]++ ; t+=1; lr++; break;
      case DEC:		if( r[std::get<1>(program[lr])]>0 ) r[std::get<1>(program[lr])]--; t+=1; lr++; break;
      case JUMP: 	lr = std::get<2>(program[lr]); t+=1; break;
      case JZERO:	if( r[std::get<1>(program[lr])]==0 ) lr = std::get<2>(program[lr]); else lr++; t+=1; break;
      case JODD:	if( r[std::get<1>(program[lr])] % 2 != 0 ) lr = std::get<2>(program[lr]); else lr++; t+=1; break;
      default: break;
    }
    if( lr<0 || lr>=(int)program.size() )
    {
      std::cerr << "Błąd: Wywołanie nieistniejącej instrukcji nr " << lr << "." << std::endl;
      exit(-1);
    }
  }
  std::cout << "Skończono program (koszt: " << t << ")." << std::endl;
}

'''
