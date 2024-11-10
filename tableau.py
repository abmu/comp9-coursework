MAX_CONSTANTS = 10
CONSTS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

class NoConstsException(Exception):
    pass

# Parse a formula, consult parseOutputs for return values
# Index 1-5 first order logic formula
# Index 6-8 propositional formula
def parse(fmla: str) -> int:
    match list(fmla):
        case [('P' | 'Q' | 'R' | 'S'), '(', x, ',', y, ')'] if x in {'x', 'y', 'z', 'w'} | set(CONSTS) and y in {'x', 'y', 'z', 'w'} | set(CONSTS):
            # an atom
            return 1
        case [('p' | 'q' | 'r' | 's')]:
            # a proposition
            return 6
        case ['~', *chars]:
            # a negation of a first order logic or propositional formula
            sub_fmla = ''.join(chars)
            sub_fmla_output_index = parse(sub_fmla)
            if 1 <= sub_fmla_output_index <= 5:
                # a negation of a first order logic formula
                return 2
            elif 6 <= sub_fmla_output_index <= 8:
                # a negation of a propositional formula
                return 7
            return 0
        case ['A', ('x' | 'y' | 'z' | 'w'), *chars]:
            # a universally quantified formula
            sub_fmla = ''.join(chars)
            sub_fmla_output_index = parse(sub_fmla)
            if 1 <= sub_fmla_output_index <= 5:
                return 3
            return 0
        case ['E', ('x' | 'y' | 'z' | 'w'), *chars]:
            # an existentially quantified formula
            sub_fmla = ''.join(chars)
            sub_fmla_output_index = parse(sub_fmla)
            if 1 <= sub_fmla_output_index <= 5:
                return 4
            return 0
        case ['(', *chars, ')']:
            # a binary connective first order logic or propositional formula
            depth = 1
            for i, char in enumerate(chars):
                if char == '(':
                    depth += 1
                elif char == ')':
                    depth -= 1
                if depth == 1:
                    if i + 2 < len(chars) and chars[i:i+2] in (['/','\\'], ['\\','/'], ['=','>']):
                        lhs_fmla = ''.join(chars[:i])
                        lhs_fmla_output_index = parse(lhs_fmla)
                        rhs_fmla = ''.join(chars[i+2:])
                        rhs_fmla_output_index = parse(rhs_fmla)
                        if 1 <= lhs_fmla_output_index <= 5 and 1 <= rhs_fmla_output_index <= 5:
                            # a binary connective first order logic formula
                            return 5
                        if 6 <= lhs_fmla_output_index <= 8 and 6 <= rhs_fmla_output_index <= 8:
                            # a binary connective propositional formula
                            return 8
                        return 0
            return 0
        case _:
            # not a formula
            return 0

# Return the LHS of a binary connective formula
def lhs(fmla: str) -> str:
    depth = 0
    for i, char in enumerate(fmla):
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
        if depth == 1:
            if fmla[i:i+2] in ('/\\', '\\/', '=>'):
                lhs_fmla = fmla[1:i]
                return lhs_fmla
    return ''

# Return the connective symbol of a binary connective formula
def con(fmla: str) -> str:
    depth = 0
    for i, char in enumerate(fmla):
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
        if depth == 1:
            if fmla[i:i+2] in ('/\\', '\\/', '=>'):
                con = fmla[i:i+2]
                return con
    return ''

# Return the RHS of a binary connective formula
def rhs(fmla: str) -> str:
    depth = 0
    for i, char in enumerate(fmla):
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
        if depth == 1:
            if fmla[i:i+2] in ('/\\', '\\/', '=>'):
                rhs_fmla = fmla[i+2:-1]
                return rhs_fmla
    return ''

# You may choose to represent a theory as a set or a list
# Initialise a theory with a single formula in it
def theory(fmla: str) -> list[str]:
    return [fmla]

# Check for satisfiability - output 0 if not satisfiable, output 1 if satisfiable, output 2 if number of constants exceeds MAX_CONSTANTS
def sat(tableau: list[list[str]]) -> int:
    consts = CONSTS.copy()
    while tableau:
        theory = tableau.pop(0)
        if _is_expanded(theory) and not _is_contradictory(theory):
            return 1
        else:
            # Pick non-literal formula in theory
            for fmla in theory:
                if not _is_literal(fmla):
                    break
            if _is_literal(fmla):
                continue
            try:
                expansion_type, fmla_1, fmla_2 = _expand_fmla(fmla, consts, theory)
            except NoConstsException:
                return 2
            match expansion_type:
                case 'alpha':
                    new_theory = theory.copy()
                    new_theory.remove(fmla)
                    new_theory.append(fmla_1)
                    if fmla_2 != '':
                        new_theory.append(fmla_2)
                    if not _is_contradictory(new_theory) and not _is_contained(new_theory, tableau):
                        tableau.append(new_theory)
                case 'beta':
                    new_theory_1 = theory.copy()
                    new_theory_1.remove(fmla)
                    new_theory_1.append(fmla_1)
                    if not _is_contradictory(new_theory_1) and not _is_contained(new_theory_1, tableau):
                        tableau.append(new_theory_1)
                    new_theory_2 = theory.copy()
                    new_theory_2.remove(fmla)
                    new_theory_2.append(fmla_2)
                    if not _is_contradictory(new_theory_2) and not _is_contained(new_theory_2, tableau):
                        tableau.append(new_theory_2)
                case 'delta':
                    new_theory = theory.copy()
                    new_theory.remove(fmla)
                    new_theory.append(fmla_1)
                    if not _is_contradictory(new_theory) and not _is_contained(new_theory, tableau):
                        tableau.append(new_theory)
                case 'gamma':
                    new_theory = theory.copy()
                    new_theory.remove(fmla)
                    new_theory.append(fmla_1)
                    new_theory.append(fmla) # keep gamma formula, but move it to the end of the list representation of the theory (fair schedule)
                    if not _is_contradictory(new_theory) and not _is_contained(new_theory, tableau):
                        tableau.append(new_theory)
    return 0

def _is_literal(fmla: str) -> bool:
    output_index = parse(fmla)
    if output_index in (1,6): # an atom or proposition
        return True
    elif output_index in (2,7): # a negation of first order logic or propositional formula
        sub_fmla = fmla[1:]
        sub_fmla_output_index = parse(sub_fmla)
        return sub_fmla_output_index in (1,6)
    return False

def _is_expanded(theory: list[str]) -> bool:
    for fmla in theory:
        if not _is_literal(fmla):
            return False
    return True

def _is_contradictory(theory: list[str]) -> bool:
    for fmla in theory:
        if f'~{fmla}' in theory:
            return True
    return False

def _is_contained(theory: list[str], tableau: list[list[str]]) -> bool:
    theory = set(theory)
    for t in tableau:
        if set(t) == theory:
            return True
    return False

def _replace_var(fmla: str, var: str, const: str) -> str:
    new_fmla = fmla[2:]
    ignore = False
    depth = 0
    for i, char in enumerate(new_fmla):
        # Variables within a nested quantifier which uses the same variable should be ignored
        if char in ('A', 'E') and new_fmla[i+1] == var:
            ignore = True
            continue
        if not ignore:
            if char == var:
                new_fmla = new_fmla[:i] + const + new_fmla[i+1:]
        else:
            if char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
            if depth == 0:
                if i + 2 <= len(new_fmla) and new_fmla[i:i+2] in ('/\\', '\\/', '=>'):
                    ignore = False
    return new_fmla

def _expand_fmla(fmla: str, consts: list[str], theory: list[str]) -> tuple[str, str, str]:
    output_index = parse(fmla)
    if output_index in (2,7): # a negation of first order logic or propositional formula
        sub_fmla = fmla[1:]
        sub_fmla_output_index = parse(sub_fmla)
        if sub_fmla_output_index in (2,7):
            return 'alpha', sub_fmla[1:], ''
        elif output_index == 3:
            var = fmla[1]
            try:
                const = consts.pop(0)
            except IndexError:
                raise NoConstsException(f'Error whilst expanding delta formula! Ran out of new constants. (Max {MAX_CONSTANTS})')
            new_fmla = _replace_var(fmla, var, const)
            return 'delta', f'~{new_fmla}', ''
        elif output_index == 4:
            # var = fmla[1]
            # for const in CONSTS:
            #     new_fmla = _replace_var(fmla, var, const)
            #     if new_fmla not in theory:
            #         return 'gamma', f'~{new_fmla}', ''
            # raise NoConstsException(f'Error whilst expanding gamma formula! Unable to try any more constants. (Max {MAX_CONSTANTS})')
        elif sub_fmla_output_index in (5,8):
            lhs_sub_fmla = lhs(sub_fmla)
            sub_fmla_con = con(sub_fmla)
            rhs_sub_fmla = rhs(sub_fmla)
            if sub_fmla_con == '\\/':
                return 'alpha', f'~{lhs_sub_fmla}', f'~{rhs_sub_fmla}'
            elif sub_fmla_con == '=>':
                return 'alpha', lhs_sub_fmla, f'~{rhs_sub_fmla}'
            elif sub_fmla_con == '/\\':
                return 'beta', f'~{lhs_sub_fmla}', f'~{rhs_sub_fmla}'
    elif output_index == 3: # a universally quantified formula
        # var = fmla[1]
        # for const in CONSTS:
        #     new_fmla = _replace_var(fmla, var, const)
        #     if new_fmla not in theory:
        #         return 'gamma', new_fmla, ''
        # raise NoConstsException(f'Error whilst expanding gamma formula! Unable to try any more constants. (Max {MAX_CONSTANTS})')
    elif output_index == 4: # an existentially quantified formula
        var = fmla[1]
        try:
            const = consts.pop(0)
        except IndexError:
            raise NoConstsException(f'Error whilst expanding delta formula! Ran out of new constants. (Max {MAX_CONSTANTS})')
        new_fmla = _replace_var(fmla, var, const)
        return 'delta', new_fmla, ''
    elif output_index in (5,8): # a binary connective first order logic or propositional formula
        lhs_fmla = lhs(fmla)
        fmla_con = con(fmla)
        rhs_fmla = rhs(fmla)
        if fmla_con == '/\\':
            return 'alpha', lhs_fmla, rhs_fmla
        elif fmla_con == '\\/':
            return 'beta', lhs_fmla, rhs_fmla
        elif fmla_con == '=>':
            return 'beta', f'~{lhs_fmla}', rhs_fmla
    return '', '', ''


#------------------------------------------------------------------------------------------------------------------------------:
#                   DO NOT MODIFY THE CODE BELOW. MODIFICATION OF THE CODE BELOW WILL RESULT IN A MARK OF 0!                   :
#------------------------------------------------------------------------------------------------------------------------------:

f = open('input.txt')

parseOutputs = ['not a formula',
                'an atom',
                'a negation of a first order logic formula',
                'a universally quantified formula',
                'an existentially quantified formula',
                'a binary connective first order formula',
                'a proposition',
                'a negation of a propositional formula',
                'a binary connective propositional formula']

satOutput = ['is not satisfiable', 'is satisfiable', 'may or may not be satisfiable']



firstline = f.readline()

PARSE = False
if 'PARSE' in firstline:
    PARSE = True

SAT = False
if 'SAT' in firstline:
    SAT = True

for line in f:
    if line[-1] == '\n':
        line = line[:-1]
    parsed = parse(line)

    if PARSE:
        output = "%s is %s." % (line, parseOutputs[parsed])
        if parsed in [5,8]:
            output += " Its left hand side is %s, its connective is %s, and its right hand side is %s." % (lhs(line), con(line) ,rhs(line))
        print(output)

    if SAT:
        if parsed:
            tableau = [theory(line)]
            print('%s %s.' % (line, satOutput[sat(tableau)]))
        else:
            print('%s is not a formula.' % line)
