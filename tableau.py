MAX_CONSTANTS = 10

# Parse a formula, consult parseOutputs for return values.
def parse(fmla: str) -> int:
    match list(fmla):
        case [('p' | 'q' | 'r' | 's')]:
            return 6
        case ['~', *chars]:
            if parse(''.join(chars)) != 0:
                return 7
            return 0
        case ['(', *chars, ')']:
            depth = 1
            for i, char in enumerate(chars):
                if char == '(':
                    depth += 1
                elif char == ')':
                    depth -= 1
                if depth == 1:
                    if i + 2 <= len(chars) and chars[i:i+2] in (['/','\\'], ['\\','/'], ['=','>']):
                        left_chars = chars[:i]
                        right_chars = chars[i+2:]
                        if parse(left_chars) != 0 and parse(right_chars) != 0:
                            return 8
                        return 0
            return 0
        case _:
            return 0

# Return the LHS of a binary connective formula
def lhs(fmla):
    return ''

# Return the connective symbol of a binary connective formula
def con(fmla):
    return ''

# Return the RHS symbol of a binary connective formula
def rhs(fmla):
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

# f = open('input.txt')

# parseOutputs = ['not a formula',
#                 'an atom',
#                 'a negation of a first order logic formula',
#                 'a universally quantified formula',
#                 'an existentially quantified formula',
#                 'a binary connective first order formula',
#                 'a proposition',
#                 'a negation of a propositional formula',
#                 'a binary connective propositional formula']

# satOutput = ['is not satisfiable', 'is satisfiable', 'may or may not be satisfiable']



# firstline = f.readline()

# PARSE = False
# if 'PARSE' in firstline:
#     PARSE = True

# SAT = False
# if 'SAT' in firstline:
#     SAT = True

# for line in f:
#     if line[-1] == '\n':
#         line = line[:-1]
#     parsed = parse(line)

#     if PARSE:
#         output = "%s is %s." % (line, parseOutputs[parsed])
#         if parsed in [5,8]:
#             output += " Its left hand side is %s, its connective is %s, and its right hand side is %s." % (lhs(line), con(line) ,rhs(line))
#         print(output)

#     if SAT:
#         if parsed:
#             tableau = [theory(line)]
#             print('%s %s.' % (line, satOutput[sat(tableau)]))
#         else:
#             print('%s is not a formula.' % line)

print(parse('((p=>q)=>~~~~~)q)'))