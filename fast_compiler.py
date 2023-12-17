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


def trivialise(lb):
    lin = lb.strip()

    return lin.replace("(", "").replace(")", "")


def fast_evaluate(lb, vrs, fnc, le):
    global temporary_var_count

    print("WHAT CALL?")

    lin = lb.strip()

    cur_res = ""
    prepend = ""

    par_count = 0
    current_par_content = ""
    first_par_started = False

    last_argument = ""

    c_ind = 0
    while c_ind < len(lin):
        c = lin[c_ind]

        if c == "(":
            par_count += 1

            if not first_par_started:
                if last_argument in fnc:
                    print("FUNCTION", last_argument)

                    fnc_start = c_ind
                    fnc_end = find_matching_closing(lin, fnc_start)

                    fast_eval = fast_evaluate(lin[fnc_start + 1:fnc_end], vrs, fnc, le)

                    cur_res += cur_res[:-len(last_argument)] + "v_" + str(temporary_var_count)

                    inner_eval = fast_evaluate(fast_eval[1], vrs, fnc, le)

                    print("INNER EVAL", inner_eval[0], "|", inner_eval[1], "FE", fast_eval[1])

                    # cur_res += "(" + fast_eval[1] + ")"
                    prepend += inner_eval[0]
                    prepend += fast_eval[0]
                    prepend += str(temporary_var_count) + "=" + inner_eval[1] + "\n"
                    print("SHOULD BE PREP", temporary_var_count, "|", prepend)
                    temporary_var_count += 1

                    c_ind = fnc_end + 1

                    continue
                else:
                    first_par_started = True
        elif c == ")":
            par_count -= 1

            if par_count == 0:
                first_par_started = False

                # check for triviality

                if is_r_trivial(current_par_content[1:], vrs, fnc):
                    cur_res += trivialise(current_par_content[1:])
                else:
                    cur_res += "v_" + str(temporary_var_count)

                    print("SUB cl", temporary_var_count, current_par_content[1:], "triv", is_r_trivial(current_par_content[1:], vrs, fnc), trivialise(current_par_content[1:]))

                    prepend += str(temporary_var_count) + "=" + trivialise(current_par_content[1:]) + "\n"

                    temporary_var_count += 1

                current_par_content = ""

                c_ind += 1

                continue

        if first_par_started:
            current_par_content += c
        else:
            cur_res += c

        # for function calls

        if (c in OPERATORS) or (c == " ") or (c == "(") or (c == ")"):
            last_argument = ""
        else:
            last_argument += c

        c_ind += 1

    print("CUR_RES", cur_res, "cur_cont", current_par_content)

    return prepend, cur_res


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
        # print("BETTER", evaluate_expression(variables, functions, rest, length, ""))

        test = fast_evaluate(rest, variables, functions, length)

        print("SUPERIOR \n", test[0] + test[1])


res.extend(function_code)

print("v", variables)
print("f", functions)
print("f rets", function_returns)
print("res", res)

print("END")

print(is_r_trivial("- 3", variables, functions))

with open('assembly.asm', mode='wt', encoding='utf-8') as mf:
    mf.write('\n'.join(res))
