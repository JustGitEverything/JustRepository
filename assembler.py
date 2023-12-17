cd = {"NOP": '00', "LDA": '01', "LDI": '02', "ADD": '03', "ADI": '04', "SUB": '05', "SUI": '06', "STA": '07',
      "JMP": '08', "JPO": '09', "JPZ": '0a', "JPN": '0b', "JPP": '0c', "JSR": '0d', "RSR": '0e', "JPS": '0f',
      "SHR": '10', "SRC": '11', "SVA": '12', "ADC": '13', "ACI": '14', "SUC": '15', "SCI": '16',
      "LDX": '18', "LDY": '19',
      "MAC": '20', "MAD": '21', "MCA": '22', "MDA": '23', "LDC": '24', "LDD": '25',
      "BRK": 'ff', "PRN": 'pp'}


def hx(n):
    return "{:02x}".format(n)


def nt(n):
    return int("0x" + n, 16)


def assemble(file_name="assembly.asm"):
    ram = [hx(0x00) for _ in range(2 ** 16)]
    pointers = {}

    with open(file_name) as f:
        p = [x.strip() for x in f.readlines()]

    ind = 0

    for i, command in enumerate(p):
        if command.replace(" ", "") == "" or command.replace(" ", "")[0] == "#":
            continue

        if command[0] == "f":
            pointers[command[1:].replace(" ", "")] = ind

            continue

        cmd = command[:3]

        if "PRN" == cmd:
            ram[ind] = cd["PRN"] + command[3:]

            ind += 1

            continue
        elif cmd in ["BRK", "NOP", "SHR", "SRC", "RSR", "MAC", "MAD", "MCA", "MDA"]:
            ram[ind] = cd[cmd]

            ind += 1

            continue
        elif cmd in ["JMP", "JPO", "JPZ", "JPN", "JPP", "JSR", "JPS"]:
            point = command[3:].replace(" ", "")

            ram[ind] = cd[cmd]
            ram[ind + 1] = point
            ram[ind + 2] = point + " 2"

            ind += 3

            continue

        arg = int(command[3:])

        if cmd in ["LDA", "ADD", "SUB", "STA", "SVA", "ADC", "SUC"]:
            ram[ind] = cd[cmd]
            ram[ind + 1] = hx(arg % 2 ** 8)
            ram[ind + 2] = hx(arg // 2 ** 8)

            ind += 3
        elif cmd in ["LDI", "ADI", "SUI", "ACI", "SCI"]:
            ram[ind] = cd[cmd]
            ram[ind + 1] = hx(arg)

            ind += 2
        else:
            raise Exception("Command", cmd, "not found, in line", i)

    print("pointers", pointers)
    print("ram", ram[:100])

    for i, r in enumerate(ram):
        if r in pointers:
            ram[i] = hx(pointers[r] % 2 ** 8)
            ram[i + 1] = hx(pointers[r] // 2 ** 8)
        elif len(r) != 2 and r[:2] != cd["PRN"]:
            raise Exception("Pointer", r, "not found in program")

    with open('final.ram', mode='wt', encoding='utf-8') as mf:
        mf.write('\n'.join(ram))
