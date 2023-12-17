from assembler import nt

import assembler
# import VGA

assembler.assemble()  # "asm_programs/full_divide.asm")

cd = assembler.cd
rd = dict((v, k) for k, v in cd.items())


ram = [0 for _ in range(2 ** 16)]
v_ram = [0 for _ in range(2 ** 16)]

# flags

zero_flag = 0
neg_flag = 0
pos_flag = 0
overflow_flag = 0

shift_flag = 0


# registers

a_reg = 0
b_reg = 0

c_reg = 0
d_reg = 0

x_reg = 0
y_reg = 0

prg_c = 0
stk_c = 0


def set_flags():
    global a_reg
    global zero_flag
    global neg_flag
    global pos_flag
    global overflow_flag

    if a_reg > 255:
        a_reg = a_reg % 256
        overflow_flag = 1
    else:
        overflow_flag = 0

    zero_flag = 1 if a_reg == 0 else 0
    neg_flag = 1 if a_reg >= 128 else 0
    pos_flag = 1 if a_reg < 128 else 0


with open("final.ram") as f:
    eeprom = [x.strip() for x in f.readlines()]

for i in range(300):
    instruction = eeprom[prg_c]

    if cd["NOP"] == instruction:
        prg_c += 1
    elif cd["PRN"] in instruction:
        if instruction[3:] == "UPD":
            pass  # VGA.draw_ram(v_ram)

        if instruction[3:].isdigit():
            print("PRINT address", instruction[3:], " : ", ram[int(instruction[3:])], "")
        elif instruction[3] == ".":
            x_r = ram[int(instruction[4:])]
            y_r = ram[int(instruction[4:]) + 1]
            sign = -1 if (y_r // 128 == 1) else 1
            print("PRINT", instruction[3:], "|", (sign - 1) * 2 ** 14 + x_r + 2 ** 8 * (y_r % 128),
                  "|", x_r, y_r, "")
        else:
            print("PRINT", instruction[3:], "")

        prg_c += 1

        continue
    elif cd["BRK"] == instruction:
        print("PROGRAM TERMINATED, with", i, "steps")
        break
    elif rd[instruction] in ["LDA", "ADD", "SUB", "STA", "SVA", "ADC", "SUC"]:
        x_reg = nt(eeprom[prg_c + 1])
        y_reg = nt(eeprom[prg_c + 2])

        if cd["LDA"] == instruction:
            a_reg = ram[x_reg + y_reg * 2 ** 8]
        elif cd["ADD"] == instruction:
            b_reg = ram[x_reg + y_reg * 2 ** 8]
            a_reg = a_reg + b_reg
            set_flags()
        elif cd["SUB"] == instruction:
            b_reg = ram[x_reg + y_reg * 2 ** 8]
            a_reg = a_reg + (256 - b_reg)
            set_flags()
        elif cd["STA"] == instruction:
            ram[x_reg + y_reg * 2 ** 8] = a_reg
        elif cd["SVA"] == instruction:
            v_ram[x_reg + y_reg * 2 ** 8] = a_reg

            # VGA.draw_ram(v_ram)
        elif cd["ADC"] == instruction:
            b_reg = ram[x_reg + y_reg * 2 ** 8]
            a_reg = a_reg + b_reg + overflow_flag
            set_flags()
        elif cd["SUC"] == instruction:
            b_reg = ram[x_reg + y_reg * 2 ** 8]
            a_reg = a_reg + (255 - b_reg) + overflow_flag
            set_flags()

        prg_c += 3
    elif cd["LDI"] == instruction:
        a_reg = nt(eeprom[prg_c + 1])

        prg_c += 2
    elif cd["ADI"] == instruction:
        b_reg = nt(eeprom[prg_c + 1])
        a_reg = a_reg + b_reg

        prg_c += 2

        set_flags()
    elif cd["SUI"] == instruction:
        b_reg = nt(eeprom[prg_c + 1])
        a_reg = a_reg + (256 - b_reg)

        prg_c += 2

        set_flags()
    elif cd["ACI"] == instruction:
        b_reg = nt(eeprom[prg_c + 1])
        a_reg = a_reg + b_reg + overflow_flag

        prg_c += 2

        set_flags()
    elif cd["SCI"] == instruction:
        b_reg = nt(eeprom[prg_c + 1])
        a_reg = a_reg + (255 - b_reg) + overflow_flag

        prg_c += 2

        set_flags()

    elif instruction in [cd["JMP"], cd["JPO"], cd["JPZ"], cd["JPN"], cd["JPP"], cd["JSR"], cd["JPS"]]:
        # print(rd[instruction], "zf", zero_flag, "of", overflow_flag, "nf", neg_flag, "pf", pos_flag, "sf", shift_flag)

        if instruction == cd["JPO"]:
            if overflow_flag == 0:
                prg_c += 3
                continue
        elif instruction == cd["JPZ"]:
            if zero_flag == 0:
                prg_c += 3
                continue
        elif instruction == cd["JPN"]:
            if neg_flag == 0:
                prg_c += 3
                continue
        elif instruction == cd["JPP"]:
            if pos_flag == 0:
                prg_c += 3
                continue
        elif instruction == cd["JPS"]:
            if shift_flag == 0:
                prg_c += 3
                continue

        prg_c += 1
        x_reg = nt(eeprom[prg_c])
        prg_c += 1
        y_reg = nt(eeprom[prg_c])

        if instruction == cd["JSR"]:
            prg_c += 1

            ram[stk_c] = prg_c % 256
            stk_c += 1
            ram[stk_c] = prg_c // 256
            stk_c += 1

        prg_c = x_reg + y_reg * 2 ** 8
    elif cd["RSR"] == instruction:
        stk_c -= 1
        y_reg = ram[stk_c]
        stk_c -= 1
        x_reg = ram[stk_c]

        prg_c = x_reg + y_reg * 2 ** 8
    elif cd["SHR"] == instruction:
        if int(a_reg / 2) == a_reg / 2:
            shift_flag = 0
        else:
            shift_flag = 1

        a_reg = a_reg // 2

        prg_c += 1
    elif cd["SRC"] == instruction:
        old_flag = shift_flag

        if int(a_reg / 2) == a_reg / 2:
            shift_flag = 0
        else:
            shift_flag = 1

        a_reg = a_reg // 2 + old_flag * 128

        prg_c += 1

    elif rd[instruction] in ["MAC", "MAD", "MCA", "MDA"]:
        if cd["MAC"] == instruction:
            c_reg = a_reg
        elif cd["MAD"] == instruction:
            d_reg = a_reg
        elif cd["MCA"] == instruction:
            a_reg = c_reg
        elif cd["MDA"] == instruction:
            a_reg = d_reg

        prg_c += 1

    else:
        raise Exception("Command", rd[instruction], "not found, in line", prg_c)

    # print(rd[instruction], "a", a_reg, "b", b_reg, "c", c_reg, "d", d_reg, "x", x_reg, "y", y_reg, "zf", zero_flag,
    #      "of", overflow_flag, "sf", shift_flag, "stack", ram[:256], "\n  pg", prg_c, "sc", stk_c, "ram", ram[256:400])
