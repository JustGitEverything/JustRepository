OPERATORS = ["+", "-"]

temporary_var_count = 0


def add_immediate(val, le):
    if le == 1:
        return ["ADI " + val]
    elif le == 2:
        return ["MCA", "ADI " + str(int(val) % 2 ** 8), "MAC", "MDA", "ACI " + str(int(val) // 2 ** 8), "MAD"]
    else:
        raise Exception("Unknown Variable Type")


def sub_immediate(val, le):
    if le == 1:
        return ["SUI " + val]
    elif le == 2:
        return ["MCA", "SUI " + str(int(val) % 2 ** 8), "MAC", "MDA", "SCI " + str(int(val) // 2 ** 8), "MAD"]
    else:
        raise Exception("Unknown Variable Type")


def load_immediate(val, le):
    if le == 1:
        return ["LDI " + val]
    elif le == 2:
        return ["LDI " + str(int(val) % 2 ** 8), "MAC", "LDI " + str(int(val) // 2 ** 8), "MAD"]
    else:
        raise Exception("Unknown Variable Type")


def immediate_op(val, op, le):
    if op == "+":
        return add_immediate(val, le)
    elif op == "-":
        return sub_immediate(val, le)


def add(var, le):
    if le == 1:
        return ["ADD " + str(var[0])]
    elif le == 2:
        return ["MCA", "ADD " + str(var[0]), "MAC", "MDA", "ADC " + str(var[1]), "MAD"]
    else:
        raise Exception("Unknown Variable Type")


def sub(var, le):
    if le == 1:
        return ["SUB " + str(var[0])]
    elif le == 2:
        return ["MCA", "SUB " + str(var[0]), "MAC", "MDA", "SUC " + str(var[1]), "MAD"]
    else:
        raise Exception("Unknown Variable Type")


def normal_op(var, op, le):
    if op == "+":
        return add(var, le)
    elif op == "-":
        return sub(var, le)


def shift_left(var, le):
    if le == 1:
        return ["LDA " + str(var[0]), "ADD " + str(var[0]), "STA " + str(var[0])]
    elif le == 2:
        return ["LDA " + str(var[0]), "ADD " + str(var[0]), "STA " + str(var[0]),
                "LDA " + str(var[1]), "ADC " + str(var[1]), "STA " + str(var[1])]
    else:
        raise Exception("Unknown Variable Type")


def shift_right(var, le):
    if le == 1:
        return ["LDA " + str(var[0]), "SHR", "STA " + str(var[0])]
    elif le == 2:
        return ["LDA " + str(var[1]), "SHR", "STA " + str(var[1]),
                "LDA " + str(var[0]), "SRC", "STA " + str(var[0])]
    else:
        raise Exception("Unknown Variable Type")


def copy_val(pos1, pos2, le):
    if le == 1:
        return ["LDA " + str(pos1[0]), "STA " + str(pos2[0])]
    elif le == 2:
        return ["LDA " + str(pos1[0]), "STA " + str(pos2[0]), "LDA " + str(pos1[1]), "STA " + str(pos2[1])]
    else:
        raise Exception("Unknown Variable Type")


def load_val(pos, le):
    if le == 1:
        return ["LDA " + str(pos[0])]
    elif le == 2:
        return ["LDA " + str(pos[0]), "MAC", "LDA " + str(pos[1]), "MAD"]
    else:
        raise Exception("Unknown Variable Type")


def store_val(pos, le):
    if le == 1:
        return ["STA " + str(pos[0])]
    elif le == 2:
        return ["MCA", "STA " + str(pos[0]), "MDA", "STA " + str(pos[1])]
    else:
        raise Exception("Unknown Variable Type")


def store_ca(pos):
    return ["MCA", "STA " + str(pos), "MDA", "STA " + str(pos + 1)]


def load_ca(pos):
    return ["LDA " + str(pos), "MAC", "LDA " + str(pos + 1), "MAD"]


def function_call(ln, nm):
    d_res = []

    called_func = functions[nm]

    arg_c = len(called_func)

    if ln.find("(") == -1 or ln.find(")") == -1:  # or ln[ln.find("(") + 1:ln.find(")")].strip() == "":
        raise Exception("Invalid arguments for function call", line)

    psb_args = ln[ln.find("(") + 1:ln.find(")")]

    for argument in range(arg_c):
        # if argument is not last

        if argument != arg_c - 1:
            arg_end = psb_args.find(",")

            if arg_end == -1:
                raise Exception("Missing argument in function call", line)

            arg_n = psb_args[:arg_end].strip()
            d_res.extend(copy_val(variables[arg_n], variables[called_func[argument]],
                                  len(variables[called_func[argument]])))

            psb_args = psb_args[arg_end + 1:].strip()
        else:
            d_res.extend(copy_val(variables[psb_args], variables[called_func[argument]],
                                  len(variables[called_func[argument]])))

    d_res.append("JSR " + nm)

    return d_res


def get_par_content(lb):
    lin = lb.strip()

    p_count = 0

    for ci, c in enumerate(lin):
        if c == "(":
            p_count += 1
        elif c == ")":
            p_count -= 1

            if p_count == 0:
                return lin[1:ci], lin[ci + 1:]

    raise Exception("Number of closing parentheses does not match")


def only_func(funcs, lb):
    lin = lb.strip()

    if lin.find("(") == -1:
        return False

    for fu in funcs:
        if lin.startswith(fu):

            rst = lin[lin.find("(") + 1:-1]

            if not ("(" in rst or ")" in rst or "+" in rst or "-" in rst or "<<" in rst or ">>" in rst):
                return True

    return False


def find_first_operator(lb):
    for c_ind, c in enumerate(lb):
        if c in OPERATORS:
            return c_ind

    return - 1


def is_r_trivial(lb, vrs, fnc):
    lin = lb.strip()

    if lin.isdigit() or lin in vrs or lin == "" or only_func(fnc, lin):
        return True

    if lin[0] == "(" and lin[-1] == ")":
        return is_r_trivial(lin[1:-1], vrs, fnc)

    no_op = lin[1:].strip()

    if (lin[0] == "+") and is_r_trivial(no_op, vrs, fnc):
        return True

    if lin[0] in OPERATORS:
        i_t = no_op

        if no_op[0] == "(" and no_op[-1] == ")":
            i_t = no_op[1:-1].strip()

        if i_t.isdigit() or i_t in vrs or i_t == "" or only_func(fnc, i_t):
            return True

    return False


def is_trivial(lb, vrs):
    lin = lb.strip()

    if lin.isdigit() or lin in vrs or lin == "":
        return True

    return False


def trivialise(lb, vrs):
    lin = lb.replace("(", "").replace(")", "").replace("+", "").strip()

    if lin in vrs:
        return vrs[lin]

    return lin


def is_sep_char(c):
    if c == " " or c == "(" or c == ")" or c == "," or c in OPERATORS:
        return True
    return False


def do_addition(arg, le):
    if isinstance(arg, list):
        return add(arg, le)
    elif arg.strip().isdigit():
        return add_immediate(arg.strip(), le)

    raise Exception("Invalid argument for addition", arg)


def do_subtraction(arg, le):
    if isinstance(arg, list):
        return sub(arg, le)
    elif arg.strip().isdigit():
        return sub_immediate(arg.strip(), le)

    raise Exception("Invalid argument for addition", arg)


def do_loading(arg, le):
    if isinstance(arg, list):
        return load_val(arg, le)
    elif arg.strip().isdigit():
        return load_immediate(arg, le)

    raise Exception("Invalid argument for addition", arg)


def do_operation(arg, op, le):
    if op == "":
        return do_loading(arg, le)
    elif op == "+":
        return do_addition(arg, le)
    elif op == "-":
        return do_subtraction(arg, le)
    else:
        raise Exception("Invalid Operator", op, arg)


def extend_mem_pos(pos, le):
    return [pos + c for c in range(le)]


def brain(lb, vrs, fnc, le):
    global memory_pos

    lin = lb.strip()

    cur_r = []

    sng = ""

    op = ""

    c_i = 0
    while c_i < len(lin):
        c = lin[c_i]

        # skip over parentheses
        if c == "(":
            closing = find_matching_closing(lin, c_i)

            cur_r.extend(do_operation(extend_mem_pos(memory_pos, le), op, le))

            cur_r = store_val(extend_mem_pos(memory_pos, le), le) + cur_r

            memory_pos += le

            cur_r = brain(lin[c_i + 1:closing], vrs, fnc, le) + cur_r

            c_i = closing + 1

            sng = ""

            continue

        if c in OPERATORS:
            # load immediate zero if operator is first arg

            if lin[:c_i].strip() == "":
                cur_r = ["LDI 0", "MAC", "MAD"]

            op = c
            c_i += 1
            continue

        sng += c

        sng_s = sng.strip()

        # is function
        if sng_s in fnc and lin[c_i + 1:].strip()[0] == "(":
            # reserve space for function result

            ret_mem_pos = extend_mem_pos(memory_pos, le)
            memory_pos += le

            cur_r = ["JSR " + sng_s] + store_val(ret_mem_pos, le) + cur_r

            # do function argument

            closing = find_matching_closing(lin, c_i + 1)

            inner = lin[c_i + 2:closing]

            a_par_c = 0

            in_a_apr = False
            arg_count = 0
            last_comma = 0

            print("FUNCTION CALL", sng_s, functions[sng_s], inner)

            func_prepend = []

            # look for comma separated argument

            for i_c, a_c in enumerate(inner):
                if a_c == "(":
                    a_par_c += 1

                    in_a_apr = True
                elif a_c == ")":
                    a_par_c -= 1

                    if a_par_c == 0:
                        in_a_apr = False

                if inner.strip() != "" and (a_c == "," and not in_a_apr) or i_c + 1 == len(inner):
                    full_arg = inner[last_comma:] if i_c + 1 == len(inner) else inner[last_comma:i_c]

                    if is_trivial(full_arg, vrs):
                        cur_r = do_loading(trivialise(full_arg, vrs), le) + \
                            store_val(vrs[fnc[sng_s][arg_count]], le) + cur_r  # ps
                    else:
                        print("FA", full_arg)

                        func_prepend.extend(brain(full_arg, vrs, fnc, le))
                        print("FI", brain(full_arg, vrs, fnc, le), inner[last_comma:i_c])

                        arg_mem_pos = extend_mem_pos(memory_pos, le)
                        memory_pos += le

                        func_prepend.extend(store_val(arg_mem_pos, le))
                        cur_r = load_val(arg_mem_pos, le) + \
                            store_val(vrs[fnc[sng_s][arg_count]], le) + cur_r  # ps
                    print("FI", "STA", vrs[fnc[sng_s][arg_count]])

                    arg_count += 1

                    last_comma = i_c + 1

            print("FI JSR", sng_s)

            print("FI STA", extend_mem_pos(memory_pos, le))
            print("REC FUNC", inner)

            cur_r = func_prepend + cur_r

            # insert memory addr

            cur_r.extend(do_operation(ret_mem_pos, op, le))

            c_i = closing + 1

            sng = ""

            continue

        end_or_sep = c_i + 1 == len(lin) or (c_i + 1 < len(lin) and is_sep_char(lin[c_i + 1]))

        # is variable
        if sng_s in vrs and end_or_sep:
            cur_r.extend(do_operation(vrs[sng_s], op, le))

            sng = ""

        # is number
        if sng_s.isdigit() and end_or_sep:
            cur_r.extend(do_operation(sng_s, op, le))

            sng = ""

        c_i += 1

    return cur_r


def find_matching_closing(lb, par_i=0):
    p_c = 0

    for c_ind, c in enumerate(lb):
        if c_ind >= par_i:
            if c == "(":
                p_c += 1
            elif c == ")":
                p_c -= 1

                if p_c == 0:
                    return c_ind

    raise Exception("Closing parentheses missing", lb)


def is_function_call(ln, funcs):
    for fu in funcs:
        if ln.strip().startswith(fu):
            return fu

    return ""


with open("program.jl") as f:
    p = [x.strip() for x in f.readlines()]

print("p", p)

# append functions at end

res = []

function_code = []

function_start = 0

# other

memory_pos = 256

variables = {}

functions = {}
function_returns = {}

scopes = []
scope_index = 0


def create_short(nm, vl):
    global memory_pos

    variables[nm] = [memory_pos]

    if vl is not None:
        res.append("LDI " + vl)
        res.append("STA " + str(memory_pos))

    memory_pos += 1


def create_int(nm, vl):
    global memory_pos

    variables[nm] = [memory_pos, memory_pos + 1]

    if vl is not None:
        res.append("LDI " + str(int(vl) % (2 ** 8)))
        res.append("STA " + str(memory_pos))
        res.append("LDI " + str(int(vl) // (2 ** 8)))
        res.append("STA " + str(memory_pos + 1))

    memory_pos += 2


def get_arguments_and_types(arg_str):
    ret_args = []
    ret_types = []

    arg = ""
    name_start = ""

    arg_i = 0
    while arg_i < len(arg_str):
        arg = arg + arg_str[arg_i]

        if (name_start != "") and (arg_str[arg_i] == "," or arg_str[arg_i] == ")"):
            arg_name = arg.strip()[:-1].strip()

            if name_start == "short":
                ret_types.append("short")
            elif name_start == "int":
                ret_types.append("int")

            ret_args.append(arg_name)

            name_start = ""
            arg = ""

        if arg.strip() == "short" or arg.strip() == "int":
            name_start = arg.strip()
            arg = ""

        arg_i += 1

    if name_start != "":
        raise Exception("Missing closing parentheses", line)

    return ret_args, ret_types


def get_inside(stng):
    if stng.find("(") == -1 or stng.rfind(")") == -1:
        raise Exception("Parentheses not matching in", stng)

    return stng.strip()[stng.find("(") + 1:stng.rfind(")")]


for bl in p:
    line = bl.strip()

    # general

    if line == "":
        continue
    elif line[0] == "#":
        continue

    elif "}" in line:
        for i in range(line.count("}")):
            if len(scopes) == 0:
                raise Exception("Closing parentheses don't match")

            if scopes[-1] in functions:
                res.append("RSR")

                function_code.extend(res[function_start:])
                res = res[:function_start]
            elif scopes[-1][:2] == "if" and scopes[-1][2:].strip().isdigit():
                res.append("f endif " + scopes[-1][2:].strip())


            scopes.pop()

    elif "def" in line:
        function_start = len(res)

        argument_start = line.find("(")

        name = line[3:argument_start].strip()

        # find arguments

        if line.find(")") == -1:
            raise Exception("No closing parentheses found", line)

        possible_args = line.strip()[argument_start + 1:line.find(")") + 1]

        arguments, types = get_arguments_and_types(possible_args)

        functions[name] = arguments

        for a, t in zip(arguments, types):
            if t == "short":
                create_short(a, None)
            elif t == "int":
                create_int(a, None)

        if line.find(">") != -1:
            ret_signature = line[line.find(">") + 1:].strip()[:-1].strip()

            ret_sep = ret_signature.find(" ")

            ret_var = ret_signature[ret_sep + 1:].strip()
            ret_type = ret_signature[:ret_sep].strip()

            if ret_type == "short":
                create_short(ret_var, None)
            elif ret_type == "int":
                create_int(ret_var, None)

            function_returns[name] = ret_var

        res.append("f " + name)

        scopes.append(name)

    elif line.startswith("if"):
        inside = get_inside(line)

        # if "" in inside:

        print("INSIDE", inside)

        scopes.append("if " + str(scope_index))

        res.append("f " + "if " + str(scope_index))

        scope_index += 1

    elif is_function_call(line, functions) != "":
        name = is_function_call(line, functions)

        if line.startswith(name):
            res.extend(function_call(line, name))

    elif "<<" in line:
        for v in variables:
            if v in line:
                vp = variables[v]
                res.extend(shift_left(vp, len(vp)))

    elif ">>" in line:
        for v in variables:
            if v in line:
                vp = variables[v]
                res.extend(shift_right(vp, len(vp)))

    elif "print(" in line:
        if '"' in line:
            res.append("PRN " + line[7:-2])
        elif line[6:-1] not in variables:
            raise Exception("Variable", line[6:-1], "not found")
        else:
            res.append("PRN " + ("." if len(variables[line[6:-1]]) == 2 else "") + str(variables[line[6:-1]][0]))

    elif "halt" in line:
        res.append("BRK")

    # variable declarations

    elif "short" in line:
        eq = line.find("=")
        name = line[5:eq].strip()
        value = line[eq + 1:].strip()

        create_short(name, value)
    elif "int" in line:
        eq = line.find("=")
        name = line[3:eq].strip()
        value = line[eq + 1:].strip()

        create_int(name, value)

    # variable assignments

    elif "=" in line:
        des = -1

        for key in variables:
            if key in line:
                if line.startswith(key):
                    des = key

        if des == -1:
            raise Exception("Variable", line, "not found")

        rest = line[line.find("=") + 1:].strip()

        length = len(variables[des])

        temporary_var_count = 0

        #  res.extend(["LDI 0", "MAC", "MAD"])  # MIGHT BE NEEDED
        test = brain(rest, variables, functions, length)

        print("SUPERIOR", test)

        res.extend(test)
        res.extend(store_val(variables[des], length))

res.extend(function_code)

print("v", variables)
print("f", functions)
print("f rets", function_returns)
print("res", res)

print("END")

print(is_r_trivial("- 3", variables, functions))

with open('assembly.asm', mode='wt', encoding='utf-8') as mf:
    mf.write('\n'.join(res))
