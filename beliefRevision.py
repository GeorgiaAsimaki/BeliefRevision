from sympy.logic.boolalg import to_cnf, Not, And, Or
from sympy import sympify

from utils import cnf_to_clauses,resolution,apply_demorgan

class BeliefBase:
    def __init__(self):
        #self.beliefs = {"a", "d|b"} # it should be cnf formed
        self.beliefs = set()

    def display(self):
        return self.beliefs

    def expansion(self, statement):
        cnf = to_cnf(statement)
        cnf = str(cnf)

        self.beliefs.add(cnf)


    def contraction(self, statement):
        if statement in self.beliefs:
            self.beliefs.remove(statement)

    def check_entailment(self,statement):
        # 1. Negate the statement and convert it to CNF form
        # print(statement)
        negated_statement = apply_demorgan(Not(statement))
        # print("Negated statement:", negated_statement)
        s = to_cnf(negated_statement)
        # print("CNF form of negated statement:", s)

        # 2. Initialize a base set with beliefs
        # base = {"D | R", "B"}  # Example beliefs as SymPy expressions
        base = self.beliefs

        # 3. Extract clauses from the base
        clauses = []
        # print("base",base)
        for b in base:
            bc = cnf_to_clauses(b, 'base')
            # print("bc",bc)
            clauses.extend(bc)

        # Add this line before s_clause assignment
        # print("Negated statement CNF form:", s)
        # 4. Add the negated statement clauses to the clauses list
        s_clause = cnf_to_clauses(s, 'statement')
        # print(s_clause)

        # Add this line after s_clause assignment
        # print("Negated statement clauses:", s_clause)

        clauses.extend(s_clause)

        # print("cl",clauses)
        # print(len(clauses))
        resolved = []
        origin = []
        for i in range(len(clauses)):
            origin.append([])

        while True:
            n = len(clauses)
            # print("start")
            change = False
            entails = False

            set = []
            for i in range(n):
                for j in range(i + 1, n):
                    s = [clauses[i], clauses[j]]
                    if(s not in resolved):
                        if((clauses[i] not in origin[j]) and (clauses[j] not in origin[i])):
                            set.append(s)

            # print(set)



            for s in set:
                a=s[0]
                b=s[1]
                # print("a.b : ",a,b)
                res, found = resolution(a, b)
                if (found):
                    change = True

                    if res == [[]]:
                        entails = True
                        print("entails")
                        return True
                        break
                    else:
                        # print('in')
                        #clauses.remove(a)
                        #clauses.remove(b)

                        resolved.append(s)
                        '''
                        for s in set:
                            if (s[0] == a or s[0] == b or s[1] == a or s[1] == b):
                                set.remove(s)
                        '''
                        clauses.extend(res)
                        for i in res:
                            origina = origin[clauses.index(a)]
                            originb = origin[clauses.index(b)]
                            origin.append([a, b, origina, originb])
                        '''
                        if a in clauses:
                            clauses.remove(a)
                        if b in clauses:
                            clauses.remove(b)
                        '''


            if not change or entails or len(set)==0:
                if not entails:
                    print("Not entails")
                    return False
                break



    
    

