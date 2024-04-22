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
    cnf_expr = to_cnf(cnf_formula)
    clauses = []

    if cnf_expr is None:
        return clauses  # Return an empty list if cnf_expr is None

    if cnf_expr.func == Or:  # If it's a disjunction (Or)
        subcl =[]
        for arg in cnf_expr.args:
            clause_literals = extract_literals(arg)
            if origin=='base':
                clauses.extend(clause_literals)  # Append literals directly to the clause
            else:
                subcl.extend(clause_literals)
        if origin == 'statement':
            clauses.append(subcl)
    elif cnf_expr.func == And:  # If it's a conjunction (And)
        clause_literals = []
        for arg in cnf_expr.args:
            clause_literals.append(extract_literals(arg))
        clauses.extend(clause_literals)  # Append all literals to a single clause
    else:  # If it's neither Or nor And, leave it as is
        clause_literals = extract_literals(cnf_expr)
        if clause_literals:  # Check if the list is not empty
            if len(clause_literals)==1 and origin=='statement':
                clauses.append(clause_literals)
            else:
                clauses.extend(clause_literals)  # Treat it as a single clause

    return clauses



'''
# Example usage:
cnf_formula = "A & ~B | C"
clauses = cnf_to_clauses(cnf_formula,'statement')
print("Clauses:")
for clause in clauses:
    print(clause)
'''

def resolution(a,b):
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
            #print("Applied De Morgan's law for negated disjunction:", result)
            return result
        elif isinstance(arg, And):  # Apply De Morgan's law for negated conjunction
            result = Or(*[Not(sub_expr) for sub_expr in arg.args])
            #print("Applied De Morgan's law for negated conjunction:", result)
            return result
        elif isinstance(arg, Not):  # Remove double negation
            result = arg.args[0]
            #print("Removed double negation:", result)
            return result
        elif isinstance(arg, Symbol):  # If it's a symbol, return the negation
            return Not(arg)
    elif isinstance(expr, Or):  # Apply De Morgan's law for disjunction
        result = And(*[apply_demorgan(sub_expr) for sub_expr in expr.args])
        #print("Applied De Morgan's law for disjunction:", result)
        return result
    elif isinstance(expr, And):  # Apply De Morgan's law for conjunction
        result = Or(*[apply_demorgan(sub_expr) for sub_expr in expr.args])
        #print("Applied De Morgan's law for conjunction:", result)
        return result
    else:
        return expr

#for testing purposes
def check_entailment(statement):
    # 1. Negate the statement and convert it to CNF form
    #print(statement)
    negated_statement = apply_demorgan(Not(statement))
    #print("Negated statement:", negated_statement)
    s = to_cnf(negated_statement)
    #print("CNF form of negated statement:", s)


    # 2. Initialize a base set with beliefs
    base = {"D | R", "B"}  # Example beliefs as SymPy expressions

    # 3. Extract clauses from the base
    clauses = []
    #print("base",base)
    for b in base:
        bc = cnf_to_clauses(b,'base')
        #print("bc",bc)
        clauses.append(bc)

    # Add this line before s_clause assignment
    #print("Negated statement CNF form:", s)
    # 4. Add the negated statement clauses to the clauses list
    s_clause = cnf_to_clauses(s,'statement')
    #print(s_clause)


    # Add this line after s_clause assignment
    #print("Negated statement clauses:", s_clause)

    clauses.extend(s_clause)


    #print("cl",clauses)
    #print(len(clauses))

    while True:
        n = len(clauses)
        #print("start")
        change = False
        entails = False

        set = []
        for i in range(n):
            for j in range(i + 1, n):
                set.append([clauses[i], clauses[j]])

        #print(set)

        for a,b in set:
            #print("a.b : ",a,b)
            res,found = resolution(a, b)
            if(found):
                change = True
                if res==[[]]:
                    entails =True
                    print("entails")
                    break
                else:
                    #print('in')
                    clauses.remove(a)
                    clauses.remove(b)
                    clauses.extend(res)
                    for s in set:
                        if (s[0]==a or s[0]==b or s[1]==a or s[1]==b):
                            set.remove(s)

        if not change or entails:
            if not entails:
                print("Not entails")
            break


#check_entailment("A|B|C&D")

