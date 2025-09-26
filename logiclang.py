from random import choice 
propositions = {}
current_line = 0
def valid_name(s): return s and s[0].isalpha() and all(c.isalnum() or c=='_' for c in s)
def func_or_var_def(txt:str):
    txt = txt.replace(" ", "")
    global current_line
    if '(' in txt:
        if not txt.endswith(')'): raise Exception(f"Malformed function name '{txt}' at line {current_line}")
        i = txt.index('(')
        f = txt[:i].strip()
        if not valid_name(f.replace(" ", '')): raise Exception(f"Invalid function name '{f}' at line {current_line}")
        args = [a.strip() for a in txt[i+1:-1].split(',') if a.strip()]
        if not args: raise Exception(f"Function '{f}' has no arguments at line {current_line}")
        for a in args:
            if not valid_name(a.replace(" ", '')): raise Exception(f"Invalid argument '{a}' in '{txt}' at line {current_line}")
        return ('func',f,args)
    elif ')' in txt or ',' in txt:
        raise Exception(f"Malformed name '{txt}' at line {current_line}")
    else:
        if not valid_name(txt.replace(" ", '')): raise Exception(f"Invalid variable name '{txt}' at line {current_line}")
        return ('var', txt)
def func_or_var(txt:str,typ=None):
    txt = txt.replace(" ", "")
    global current_line
    if txt == "true" or txt == "True": return ('bool', True)
    if txt == "false" or txt == "False": return ('bool', False)
    if '(' in txt:
        if not txt.endswith(')'): raise Exception(f"Malformed function name '{txt}' at line {current_line}")
        i = txt.index('(')
        f = txt[:i].strip()
        if not valid_name(f.replace(" ", '')): raise Exception(f"Invalid function name '{f}' at line {current_line}")
        args = [a.strip() for a in txt[i+1:-1].split(',') if a.strip()]
        if not args: raise Exception(f"Function '{f}' has no arguments at line {current_line}")
        for a in args:
            try:
                body_parser(a)
            except Exception as e:
                raise Exception(f"Invalid argument '{a}' in '{txt}' at line {current_line}: {e}")
        if f in propositions:
            fargs = propositions[f][2]
            if len(args) != len(fargs):
                raise Exception(f"a function {f} needs {len(fargs)} argument, but got {args} at line {current_line}")
            args = [(fargs[i],args[i]) for i in range(len(fargs))]
            args = sorted(args,key=lambda k: len(k[0]))[::-1]
            funcbody:str = propositions[f][4]
            for i in range(len(fargs)):
                funcbody = funcbody.replace(args[i][0],args[i][1])
            return body_parser(funcbody)        
        else:raise Exception(f"Undefined function {f} at line {current_line}")
    elif ')' in txt or ',' in txt:
        raise Exception(f"Malformed name '{txt}' at line {current_line}")
    else:
        if not valid_name(txt.replace(" ", '')): raise Exception(f"Invalid variable name '{txt}' at line {current_line}")
        if txt in propositions:
            if typ!='func':return propositions[txt][3]
            else: raise Exception(f"Undefined function's variable {txt} at line {current_line}")
        return ('var', txt)

def body_parser(txt:str,typ=None):
    txt = txt.replace(" ", "")
    if len(txt) == 0:
        raise Exception(f"Unexpectxted end of expression at line {current_line}")
    while txt.startswith('(') and txt.endswith(')'):
        depth = 0
        matched = True
        for i in range(len(txt)):
            if txt[i] == '(':
                depth += 1
            elif txt[i] == ')':
                depth -= 1
                if depth == 0 and i != len(txt) - 1:
                    matched = False
                    break
        if matched:
            txt = txt[1:-1]
        else:
            break
    def find_main_op(txt, op):
        depth = 0
        for i in range(len(txt)):
            if txt[i] == '(':
                depth += 1
            elif txt[i] == ')':
                depth -= 1
            elif depth == 0 and txt[i:i+len(op)] == op:
                return i
        return -1

    for op in ['<->', '->', '|', '&']:
        i = find_main_op(txt, op)
        if i != -1:
            return [op, body_parser(txt[:i],typ), body_parser(txt[i+len(op):],typ)]

    if txt[0] == '~':
        return ['~', body_parser(txt[1:],typ)]
    else:
        return func_or_var(txt,typ)

def txt_or_logic(txt:str):
    try:
        syntax_tree = body_parser(txt)
        return syntax_tree_to_logic(syntax_tree)
    except:
        return txt

def parse(txt:str):
    global current_line
    current_line += 1
    syntax_tree = []
    current_branch = syntax_tree
    query = False
    txt = txt.split('#', 1)[0].strip()
    if txt.lower().strip() == 'repl':
        repl()
    if txt.lower().startswith("writeln"):
        print(txt_or_logic(txt[7:].strip()))
        return None
    if txt.lower().startswith("write"):
        print(txt_or_logic(txt[5:].strip()),end=" ")
        return None
    txt = txt.replace(' ','')
    if txt == '':return None
    if txt[0] == '?':
        query = True
        txt = txt[1:].replace(' ', '')
        if txt.startswith("sat"):
            syntax_tree = ["sat", body_parser(txt[3:])]
        elif txt.startswith("valid"):
            syntax_tree = ["valid", body_parser(txt[5:])]
        elif txt.startswith("contr"):
            syntax_tree = ["contr", body_parser(txt[5:])]
        elif txt.startswith("models"):
            syntax_tree = ["models", body_parser(txt[6:])]
        elif txt.startswith("countermodels"):
            syntax_tree = ["countermodels", body_parser(txt[13:])]
        elif txt.startswith("model"):
            syntax_tree = ["model", body_parser(txt[5:])]
        elif txt.startswith("countermodel"):
            syntax_tree = ["countermodel", body_parser(txt[12:])]
        elif txt.startswith("eval"):
            syntax_tree = ["eval", body_parser(txt[4:])]
        elif txt.startswith("table"):
            syntax_tree = ["table", body_parser(txt[5:])]
        else:
            raise Exception(f"Unexpected query at line {current_line}")
    else:
        txt = txt.replace(' ','')
        if ':=' not in txt:raise Exception(f"Missing ':=' at line {current_line}")
        txt = txt.split(':=')
        if txt[0] == '':raise Exception(f"Empty left side of := at line {current_line}")
        if txt[1] == '':raise Exception(f"Empty right side of := at line {current_line}")
        current_branch.append(':=')
        current_branch.append(func_or_var_def(txt[0]))
        txt = txt[1]
        typ = current_branch[-1][0]
        current_branch.append(body_parser(txt,typ))
    return ("def" if not query else "query",syntax_tree)

def find_vars(tree):
    vars_found = []
    seen = set()
    def helper(node):
        if isinstance(node, tuple):
            if node[0] == 'var':
                varname = node[1]
                if varname not in seen:
                    seen.add(varname)
                    vars_found.append(varname)
        elif isinstance(node, list):
            for item in node:
                helper(item)
    if isinstance(tree, tuple) and tree[0] in ('def', 'query'):
        if isinstance(tree[1], list) and len(tree[1]) > 2:
            helper(tree[1][2])
        elif isinstance(tree[1], list) and len(tree[1]) == 2:
            helper(tree[1][1])
        else:
            helper(tree[1])
    else:
        helper(tree)

    return vars_found

def syntax_tree_to_lambda(syntax_tree):
    ops = {'|':"or",'&':"and",'->':'<=',"<->":'=='}
    if isinstance(syntax_tree, tuple):
        if syntax_tree[0] == "bool":
            return str(syntax_tree[1])
        if syntax_tree[0] == 'var':
            return syntax_tree[1]
    elif isinstance(syntax_tree, list):
        if not syntax_tree:
            return ""
        op = syntax_tree[0]
        if op =='~':
            return f"(not({syntax_tree_to_lambda(syntax_tree[1])}))"
        if op in ['|', '&', '->', '<->']:
            return f"({syntax_tree_to_lambda(syntax_tree[1])} {ops[op]} {syntax_tree_to_lambda(syntax_tree[2])})"
    return str(syntax_tree)

def syntax_tree_to_logic(syntax_tree):
    if isinstance(syntax_tree, tuple):
        if syntax_tree[0] == "bool":
            return str(syntax_tree[1])
        if syntax_tree[0] == 'var':
            return syntax_tree[1]
    elif isinstance(syntax_tree, list):
        if not syntax_tree:
            return ""
        op = syntax_tree[0]
        if op =='~':
            return f"(~({syntax_tree_to_logic(syntax_tree[1])}))"
        if op in ['|', '&', '->', '<->']:
            return f"({syntax_tree_to_logic(syntax_tree[1])}{op}{syntax_tree_to_logic(syntax_tree[2])})"
    return str(syntax_tree).replace(" ", "")

def all_bool_combinations(n):
    for i in range(2**n):
        vals = []
        for j in range(n):
            vals.append(bool((i >> j) & 1))
        yield vals

def valid(f,args):
    if len(args) > 8:
        for _ in range(100):
            if not f(*[choice([True,False]) for _ in range(len(args))]):
                return False
    for i in all_bool_combinations(len(args)):
        if not f(*i):
            return False
    return True

def contr(f,args):
    if len(args) > 8:
        for _ in range(100):
            if f(*[choice([True,False]) for _ in range(len(args))]):
                return False
    for i in all_bool_combinations(len(args)):
        if f(*i):
            return False
    return True

def sat(f,args):return not contr(f,args)

def model(f,args):
    if len(args) > 8:
        for _ in range(100):
            values = [choice([True,False]) for _ in range(len(args))]
            if f(*values):
                return f'{', '.join([f'{args[i]} : {values[i]}' for i in range(len(args))])}'
    for values in all_bool_combinations(len(args)):
        if f(*values):
            return f'{', '.join([f'{args[i]} : {values[i]}' for i in range(len(args))])}'
    return None

def countermodel(f,args):
    if len(args) > 8:
        for _ in range(100):
            values = [choice([True,False]) for _ in range(len(args))]
            if not f(*values):
                return f'{', '.join([f'{args[i]} : {values[i]}' for i in range(len(args))])}'
    for values in all_bool_combinations(len(args)):
        if not f(*values):
            return f'{', '.join([f'{args[i]} : {values[i]}' for i in range(len(args))])}'
    return None

def evall(f,args):
    vals = []
    for i in args:
        inp = input(f"{i} := ")
        if inp in ["True",'true']:
            vals.append(True)
        elif inp in ["False",'false']:
            vals.append(False)
        else:raise Exception(f"Unexpected input: {inp}")
    return f(*vals)

def models(f,args):
    for values in all_bool_combinations(len(args)):
        if f(*values):
            yield f'{', '.join([f'{args[i]} : {values[i]}' for i in range(len(args))])}'

def countermodels(f,args):
    for values in all_bool_combinations(len(args)):
        if not f(*values):
            yield f'{', '.join([f'{args[i]} : {values[i]}' for i in range(len(args))])}'

def print_truth_table(rows):
    var_names = [var for var, _ in rows[0]]
    col_widths = {var: len(var) for var in var_names}
    for row in rows:
        for var, val in row:
            val_str = str(val)
            col_widths[var] = max(col_widths[var], len(val_str))
    header = " | ".join(var.ljust(col_widths[var]) for var in var_names)
    separator = "-+-".join('-' * col_widths[var] for var in var_names)
    print(header)
    print(separator)
    for row in rows:
        row_str = " | ".join(str(val).ljust(col_widths[var]) for var, val in row)
        print(row_str)


def interpret(parsed_txt):
    if parsed_txt == None:
        pass
    else :
        if parsed_txt[0] == 'query':
            syntax_tree = parsed_txt[1][1]
            args = find_vars(syntax_tree)
            f = eval(f'lambda {','.join(args)}:'+syntax_tree_to_lambda(syntax_tree))
            if parsed_txt[1][0] == 'sat':
                print(sat(f,args))
            elif parsed_txt[1][0] == 'contr':
                print(contr(f,args))
            elif parsed_txt[1][0] == 'valid':
                print(valid(f,args))
            elif parsed_txt[1][0] == 'model':
                print(model(f,args))
            elif parsed_txt[1][0] == 'countermodel':
                print(countermodel(f,args))
            elif parsed_txt[1][0] == 'eval':
                print(evall(f,args))
            elif parsed_txt[1][0] == 'table':
                l = []
                for vals in all_bool_combinations(len(args)):
                    l1 = []
                    for i in range(len(args)):
                        l1.append((args[i],vals[i]))
                    l1.append((syntax_tree_to_logic(syntax_tree),f(*vals)))
                    l.append(l1)
                    l1 =[]
                print_truth_table(l)
            elif parsed_txt[1][0] == 'models':
                for i in models(f,args):
                    print(i)
            elif parsed_txt[1][0] == 'countermodels':
                for i in countermodels(f,args):
                    print(i)
            else:raise Exception(f"Unexpected query {parsed_txt[1][0]} at line {current_line}")
        else:
            syntax_tree = parsed_txt[1]
            typ = syntax_tree[1][0]
            name = syntax_tree[1][1]
            if typ == 'func':
                args = syntax_tree[1][2]
                found_args = find_vars(syntax_tree)
                if name in found_args:found_args.remove(name)
                if not set(args) == set(found_args):
                    raise Exception(f"Function '{name}' has unused or missing parameters at line {current_line}")
                py_func = f'lambda {','.join(args)}:'+syntax_tree_to_lambda(syntax_tree[2])
                f = eval(py_func)
                propositions[name] = (typ,f,args,syntax_tree[2],syntax_tree_to_logic(syntax_tree[2]))
            else:
                args = find_vars(syntax_tree)
                if name in args:args.remove(name)
                py_func = f'lambda {','.join(args)}:'+syntax_tree_to_lambda(syntax_tree[2])
                f = eval(py_func)
                propositions[name] = (typ,f,args,syntax_tree[2], syntax_tree_to_logic(syntax_tree[2]))

            
def repl():
    print("Welcome to LogicLang REPL. Type 'exit' to quit.")
    while True:
        try:
            line = input(">>> ").strip()
            if line.lower().strip()== 'repl':
                continue
            elif line.startswith("writeln"):
                pass
            elif line.lower().startswith("write"):
                line = line.replace("write",'writeln')
            elif line.lower() == "exit":
                break
            if not line:
                continue
            interpret(parse(line))
        except Exception as e:
            print(f"Error: {e}")

def main():
    import sys
    import os
    if len(sys.argv) > 1:
        filename = sys.argv[1]

        if not filename.endswith('.logic'):
            print(f"Error: Invalid file extension. Expected '.logic', got '{filename}'")
            sys.exit(1)

        if not os.path.isfile(filename):
            print(f"Error: File '{filename}' not found.")
            sys.exit(1)

        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                try:
                    interpret(parse(line))
                except Exception as e:
                    print(f"Error: {e}")
                    sys.exit(1)
    else:repl()

if __name__ == "__main__":
    main()
