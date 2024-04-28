from sympy.logic.boolalg import to_cnf, Not, And, Or
from sympy import sympify

from utils import cnf_to_clauses,resolution,apply_demorgan

class BeliefBase:
    def __init__(self):
        #self.beliefs = {"a", "d|b"} # it should be cnf formed
        self.beliefs = set()
        self.sorted = set()

    def get_beliefs(self):
        """
        Get beliefs from BeliefBase.
        """
        return {belief.belief for belief in self.beliefs}

    def get_beliefs_with_priorities(self):
        """
        Get beliefs with priorities from BeliefBase.
        """
        beliefs_with_priorities = [(belief.belief, belief.priority) for belief in self.beliefs]
        return beliefs_with_priorities

    def display(self):
        beliefs_str = "\n".join(str(belief) for belief in self.beliefs)
        return beliefs_str

    def checkOrder(self,b):
        self.sort()
        #check if the order is more than the least important belief
        if b.priority<self.sorted[0][1]:
            return False
        else:
            #check if the base that includes beliefs with higher order entails the negation of the statement
                #if yes we cannot continue, otherwise we can
            base = BeliefBase()
            base.beliefs =self.beliefs
            base.sort()
            sorted=base.sorted

            beliefs_to_remove = [belief for belief in sorted if belief[1] <= b.priority]
            for belief_tuple in beliefs_to_remove:
                belief_to_remove = next(belief for belief in base.beliefs if belief.belief == belief_tuple[0])
                base.beliefs.remove(belief_to_remove)

            entails = base.check_entailment(Not(sympify(b.belief)))
            # if entails=True then I cannot add it
            if entails:
                return False
            else:
                return True


    def revision(self,belief):
        # 1.check entailment for degrees>=order
            # if the base that includes degrees more or equal to the order that the statement has then we can continue
            # otherwise it cannot be added
        p = self.checkOrder(belief)
        if p:
            # check for the maximal base subset that doesn't entail the negation of the statement

        else:
            print('Cannot be added due to low priority')
            return


    def sort(self):
        # Create a list of tuples (belief, priority)
        beliefs_with_priorities = self.get_beliefs_with_priorities()

        # Sort the list of tuples based on priority
        beliefs_with_priorities.sort(key=lambda x: x[1])

        # Update beliefs with sorted list of beliefs
        self.sorted = beliefs_with_priorities


        return self.sorted

    def expansion(self, belief):
        self.beliefs.add(belief)


    def contraction(self, statement):
        if statement in self.beliefs:
            self.beliefs.remove(statement)

    def check_entailment(self,statement):
        # Negate the statement and convert it to CNF form

        negated_statement = apply_demorgan(Not(statement))
        s = to_cnf(negated_statement)

        base = self.get_beliefs()

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

class Belief:
    def __init__(self):
        # self.beliefs = {"a", "d|b"} # it should be cnf formed
        self.belief = ''
        self.priority = 0

    def __str__(self):
        return f"Belief: {self.belief} with Priority: {self.priority}"


