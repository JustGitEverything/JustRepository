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


def find_matching_closing(lb):
    p_c = 0

    for c_ind, c in enumerate(lb):
        if c == "(":
            p_c += 1
        elif c == ")":
            p_c -= 1

            if p_c == 0:
                return c_ind

    raise Exception("Closing parentheses missing", lb)


def evaluate_expression(vs, funcs, lb, le):
    global temporary_var_count

    lin = lb.strip()

    cur_res = ""

    print("VARS", vs, "LIN", lin, "LE", le)

    if lin.isdigit() or lin in vs or lin == "" or only_func(funcs, lin):
        cur_res += lin
    elif lin.startswith("("):
        cont, rst = get_par_content(lin)

        print(lin, "TRUSTRIP", cont, "r", rst)

        cur_res += evaluate_expression(vs, funcs, cont, le)
        cur_res += evaluate_expression(vs, funcs, rst, le)

        # return cur_res
    else:
        print("WTHISE", lin)
        first_op = find_first_operator(lin)

        if first_op == -1:
            raise Exception("Error in expression", first_op)

        # next decomposition is function

        if lin.find("(") < first_op and lin.find("(") != -1:
            cur_res += "("

            end_f = find_matching_closing(lin)

            fst = lin[lin.find("(") + 1:end_f].strip()
            snd = lin[end_f + 1:].strip()

            print("BEFORE INNER", fst)

            # go through comma separated arguments

            c_ind = 0
            while c_ind < len(fst):
                c = fst[c_ind]

                if c == "(":
                    end_inner = find_matching_closing(fst)

                    inner_par = fst[c_ind + 1:end_inner]

                    c_ind = end_inner

                    temp_name = "v" + str(temporary_var_count)
                    temporary_var_count += 1

                    cur_res += temp_name

                    print("EVLLLLT", inner_par)

                    cur_res = temp_name + " = " + evaluate_expression(vs, funcs, inner_par, le) + "\n" + cur_res

                    print("INNER", inner_par, "|", end_inner, fst)
                else:
                    cur_res += c

                c_ind += 1

            print("WHY", fst, "|", snd)

            # add second part before closing pars

            cur_res += evaluate_expression(vs, funcs, snd, le)

            return cur_res

            # raise Exception("Incomplete Argument in function call")

        fst = lin[:first_op].strip()
        snd = lin[first_op + 1:].strip()

        print("LIN", fst, snd)
        if lin[first_op] == "+":  # or lin.startswith("-"):
            print("ERROR?", fst, "|", snd)
            cur_res += evaluate_expression(vs, funcs, fst, le)
            cur_res += " + "
            cur_res += evaluate_expression(vs, funcs, snd, le)
        elif lin[first_op] == "-":
            temp_name = "v" + str(temporary_var_count)
            temporary_var_count += 1

            print("CDCDCDC", snd, temp_name)

            cur_res = temp_name + " = " + evaluate_expression(vs, funcs, snd, le) + "\n" + cur_res  # ?
            cur_res += evaluate_expression(vs, funcs, fst, le)  #?
            cur_res += " - "
            cur_res += temp_name


    print("RETURNING", cur_res)

    return cur_res


def decompose_exp(var, exp, op, le):
    global memory_pos

    d_res = []

    if exp.strip() == "":
        return []

    if exp.isdigit():
        return immediate_op(exp.strip(), op, le)

    if exp.strip() in var:
        return normal_op(var[exp.strip()], op, le)

    if exp.find("(") != -1 and exp.find(")") != -1 and exp.find(")") == exp.rfind(")"):
        possible_func = exp[:exp.find("(")]

        if possible_func in functions:
            # store previous value, then compute function and operation

            if le == 1:
                d_res.append("STA " + str(memory_pos))
                first_mem = memory_pos
                memory_pos += 1
                d_res.append("LDI 0")

                d_res.extend(function_call(exp, possible_func))

                d_res.append("STA " + str(memory_pos))
                d_res.append("LDA " + str(first_mem))

                d_res.extend(normal_op([memory_pos], op, le))  # s

                memory_pos -= 1
            elif le == 2:
                d_res.extend(store_ca(memory_pos))
                first_mem = memory_pos
                memory_pos += 2

                d_res.extend(["LDI 0", "MAC", "MAD"])

                d_res.extend(function_call(exp, possible_func))

                d_res.extend(store_ca(memory_pos))
                d_res.extend(load_ca(first_mem))

                d_res.extend(normal_op([memory_pos, memory_pos + 1], op, le))  # s

                memory_pos -= 2
            else:
                raise Exception("Unknown Variable Type")

            return d_res

    stng = ""

    for ind, c in enumerate(exp):
        stng += c

        if c == "(":
            possible_f = stng.strip()[:-1]
            is_function = possible_f in functions

            # find matching parentheses

            end = - 1
            count = 0

            for p_ind, par in enumerate(exp):
                if par == "(":
                    count += 1
                if par == ")":
                    count -= 1

                    if count == 0:
                        end = p_ind

                        break

            if end == -1:
                raise Exception("No matching parentheses was found")

            if le == 1:
                d_res.append("STA " + str(memory_pos))
                first_mem = memory_pos
                memory_pos += 1
                d_res.append("LDI 0")

                if not is_function:
                    d_res.extend(decompose_exp(var, exp[ind + 1:end], "+", le))  # s
                else:
                    d_res.extend(function_call(possible_f + exp[ind:end + 1], possible_f))
                    d_res.extend(load_val(variables[function_returns[possible_f]], le))

                d_res.append("STA " + str(memory_pos))
                d_res.append("LDA " + str(first_mem))

                d_res.extend(normal_op([memory_pos], op, le))  # s

                memory_pos -= 1
            elif le == 2:
                d_res.extend(store_ca(memory_pos))
                first_mem = memory_pos
                memory_pos += 2

                d_res.extend(["LDI 0", "MAC", "MAD"])

                if not is_function:
                    d_res.extend(decompose_exp(var, exp[ind + 1:end], "+", le))  # s
                else:
                    d_res.extend(function_call(possible_f + exp[ind:end + 1], possible_f))
                    d_res.extend(load_val(variables[function_returns[possible_f]], le))

                d_res.extend(store_ca(memory_pos))
                d_res.extend(load_ca(first_mem))

                d_res.extend(normal_op([memory_pos, memory_pos + 1], op, le))  # s

                memory_pos -= 2
            else:
                raise Exception("Unknown Variable Type")

            # code after end of parentheses

            d_res.extend(decompose_exp(var, exp[end + 1:], "+", le))

            break

        if c in OPERATORS:
            first = exp[:ind].strip()
            second = exp[ind + 1:].strip()

            d_res.extend(decompose_exp(var, first, op, le))

            d_res.extend(decompose_exp(var, second, c, le))

            break

    return d_res


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

    res.append("LDI " + vl)
    res.append("STA " + str(memory_pos))

    memory_pos += 1


def create_int(nm, vl):
    global memory_pos

    variables[nm] = [memory_pos, memory_pos + 1]

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
                scopes.pop()

                function_code.extend(res[function_start:])
                res = res[:function_start]

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
                create_short(a, "0")
            elif t == "int":
                create_int(a, "0")

        if line.find(">") != -1:
            ret_signature = line[line.find(">") + 1:].strip()[:-1].strip()

            ret_sep = ret_signature.find(" ")

            ret_var = ret_signature[ret_sep + 1:].strip()
            ret_type = ret_signature[:ret_sep].strip()

            if ret_type == "short":
                create_short(ret_var, "0")
            elif ret_type == "int":
                create_int(ret_var, "0")

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

        if length == 1:
            res.extend(["LDI 0"])
            res.extend(decompose_exp(variables, rest, "+", 1))
            res.append("STA " + str(variables[des][0]))
        elif length == 2:
            res.extend(["LDI 0", "MAC", "MAD"])
            res.extend(decompose_exp(variables, rest, "+", 2))
            res.extend(["MCA", "STA " + str(variables[des][0])])
            res.extend(["MDA", "STA " + str(variables[des][1])])
        else:
            raise Exception("Unknown Variable Type")

        temporary_var_count = 0
        print("BETTER", evaluate_expression(variables, functions, rest, length))


res.extend(function_code)

print("v", variables)
print("f", functions)
print("f rets", function_returns)
print("res", res)

with open('assembly.asm', mode='wt', encoding='utf-8') as mf:
    mf.write('\n'.join(res))
