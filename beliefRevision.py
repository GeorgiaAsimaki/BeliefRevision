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
        # Negate the statement and convert it to CNF form

        negated_statement = apply_demorgan(Not(statement))
        s = to_cnf(negated_statement)

        base = self.beliefs

        # Extract clauses from the base
        clauses = []

        for b in base:
            bc = cnf_to_clauses(b, 'base') # translate beliefs to a list of specific form
            clauses.extend(bc)

        # Add the negated statement clauses to the clauses list
        s_clause = cnf_to_clauses(s, 'statement')

        clauses.extend(s_clause)

        #this list stores the pairs that have already been resolved
        resolved = []
        #this list stores the origin of the resolvement, i.e. the pair that resolved and produced clause i is in origin[i]
        origin = []
        for i in range(len(clauses)):
            origin.append([]) #append empty lists as origins for the initial clauses

        while True:
            n = len(clauses)

            change = False
            entails = False

            #the set that has all the pairs that can be resolved
            set = []
            for i in range(n):
                for j in range(i + 1, n):
                    s = [clauses[i], clauses[j]]
                    if(s not in resolved): #if it hasn't already been resolved
                        if((clauses[i] not in origin[j]) and (clauses[j] not in origin[i])):
                            #here it checks that one of the parts of the pair has been resolved from the other. if so, it shouldn't create a new pair to add to the set
                            set.append(s)
            #go through the pairs of the set and check their resolvements
            for s in set:
                a=s[0]
                b=s[1]
                res, found = resolution(a, b)
                #res is the resolvement
                #found is a flag that is True when a resolvement has been found
                if (found):
                    change = True
                    if res == [[]]:
                        #if resolvement is empty
                        entails = True
                        print("entails")
                        return True
                        break
                    else:
                        resolved.append(s)

                        clauses.extend(res)
                        for i in res:
                            origina = origin[clauses.index(a)]
                            originb = origin[clauses.index(b)]
                            origin.append([a, b, origina, originb])


            if not change or entails or len(set)==0:
                if not entails:
                    print("Not entails")
                    return False
                break



    
    

