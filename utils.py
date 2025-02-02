from sympy.logic.boolalg import to_cnf, Not, And, Or
from sympy import sympify, Symbol


def extract_literals(expr):
    literals = []
    if expr.func == Not:
        literals.append(~expr.args[0])
    else:
        literals.append(expr)
    return literals


def cnf_to_clauses(cnf_formula,origin):
    '''
    The functionality of this function is to turn a formula that is in this form e.g a^b|c to this form [[a],[b,c]]
    so that the elemnts of the list are the parts of the conjuction and each of them is a list of the literals that appear at the disjunctions (since it is in cnf form).
    '''

    cnf_expr = to_cnf(cnf_formula)
    clauses = []

    if cnf_expr is None:
        return clauses  # Return an empty list if cnf_expr is None

    if cnf_expr.func == Or:  # If it's a disjunction (Or)
        subcl =[]
        for arg in cnf_expr.args:
            clause_literals = extract_literals(arg)
            subcl.extend(clause_literals)
        clauses.append(subcl)
    elif cnf_expr.func == And:  # If it's a conjunction (And)
        clause_literals = []
        for arg in cnf_expr.args:
            if (arg.func == Or):
                clause_literals.extend(cnf_to_clauses(arg, origin))
            else:
                clause_literals.append(extract_literals(arg))
        clauses.extend(clause_literals)  # Append all literals to a single clause
    else:  # If it's neither Or nor And, leave it as is
        clause_literals = extract_literals(cnf_expr)
        if clause_literals:  # Check if the list is not empty
            if len(clause_literals)==1:
                clauses.append(clause_literals)
            else:
                clauses.extend(clause_literals)  # Treat it as a single clause

    return clauses



def resolution(a,b):
    '''
    This function finds the resolvements of a pair a,b
    and returns found = True if there is a resolvement else found=False and the resolvement in res
    '''
    res = []
    found = False
    for la in a:
        for lb in b:
            if (la==Not(sympify(lb)) or lb==Not(sympify(la))):
                #remove instances of la and lb
                a_new = [i for i in a if i != la]
                b_new = [i for i in b if i != lb]
                ab = a_new+b_new
                #remove duplicates
                result =list(set(ab))
                res.append(result)
                found = True

    return res,found #True means I couldn't remove something

def apply_demorgan(expr):
    if isinstance(expr, Not):  # Check if it's a negation
        arg = expr.args[0]
        if isinstance(arg, Or):  # Apply De Morgan's law for negated disjunction
            result = And(*[Not(sub_expr) for sub_expr in arg.args])
            return result
        elif isinstance(arg, And):  # Apply De Morgan's law for negated conjunction
            result = Or(*[Not(sub_expr) for sub_expr in arg.args])
            return result
        elif isinstance(arg, Not):  # Remove double negation
            result = arg.args[0]
            return result
        elif isinstance(arg, Symbol):  # If it's a symbol, return the negation
            return Not(arg)
    elif isinstance(expr, Or):  # Apply De Morgan's law for disjunction
        result = And(*[apply_demorgan(sub_expr) for sub_expr in expr.args])
        return result
    elif isinstance(expr, And):  # Apply De Morgan's law for conjunction
        result = Or(*[apply_demorgan(sub_expr) for sub_expr in expr.args])
        return result
    else:
        return expr



