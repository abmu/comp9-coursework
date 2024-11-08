MAX_CONSTANTS = 10

# Parse a formula, consult parseOutputs for return values.
def parse(fmla: str) -> int:
    match list(fmla):
        case [('P' | 'Q' | 'R' | 'S'), '(', ('x' | 'y' | 'z' | 'w'), ',', ('x' | 'y' | 'z' | 'w'), ')']:
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
        case ['E', ('x' | 'y' | 'z' | 'w'), *chars]:
            # a universally quantified formula
            sub_fmla = ''.join(chars)
            sub_fmla_output_index = parse(sub_fmla)
            if 1 <= sub_fmla_output_index <= 5:
                return 3
            return 0
        case ['A', ('x' | 'y' | 'z' | 'w'), *chars]:
            # an existentially quantified formula
            sub_fmla = ''.join(chars)
            sub_fmla_output_index = parse(sub_fmla)
            if 1 <= sub_fmla_output_index <= 5:
                return 4
            return 0
        case ['(', *chars, ')']:
            # a binary connective first order or propositional formula
            depth = 1
            for i, char in enumerate(chars):
                if char == '(':
                    depth += 1
                elif char == ')':
                    depth -= 1
                if depth == 1:
                    if i + 2 < len(chars) and chars[i:i+2] in (['/','\\'], ['\\','/'], ['=','>']):
                        left_fmla = ''.join(chars[:i])
                        left_fmla_output_index = parse(left_fmla)
                        right_fmla = ''.join(chars[i+2:])
                        right_fmla_output_index = parse(right_fmla)
                        if 1 <= left_fmla_output_index <= 5 and 1 <= right_fmla_output_index <= 5:
                            # a binary connective first order formula
                            return 5
                        if 6 <= left_fmla_output_index <= 8 and 6 <= right_fmla_output_index <= 8:
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
            if fmla[i:i+2] in (['/','\\'], ['\\','/'], ['=','>']):
                left_fmla = fmla[1:i]
                return left_fmla
    return ''

# Return the connective symbol of a binary connective formula
def con(fmla: str) -> str:
    return ''

# Return the RHS symbol of a binary connective formula
def rhs(fmla: str) -> str:
    depth = 0
    for i, char in enumerate(fmla):
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
        if depth == 1:
            if fmla[i:i+2] in (['/','\\'], ['\\','/'], ['=','>']):
                right_fmla = fmla[i+2:-1]
                return right_fmla
    return ''

# You may choose to represent a theory as a set or a list
def theory(fmla):#initialise a theory with a single formula in it
    return None

#check for satisfiability
def sat(tableau):
#output 0 if not satisfiable, output 1 if satisfiable, output 2 if number of constants exceeds MAX_CONSTANTS
    return 0

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
