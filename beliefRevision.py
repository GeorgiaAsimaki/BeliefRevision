from sympy.logic.boolalg import to_cnf, Not, And, Or
from sympy import sympify
from itertools import combinations

from utils import cnf_to_clauses,resolution,apply_demorgan


class BeliefBase:
    def __init__(self):
        #self.beliefs = {"a", "d|b"} # it should be cnf formed
        self.beliefs = set()
        self.sorted = set()

    def display(self):
        beliefs_str = "\n".join(str(belief) for belief in self.beliefs)
        return beliefs_str

    def get_beliefs(self):
        """
        Get beliefs from BeliefBase.
        """
        return {belief.belief for belief in self.beliefs}

    def find_belief(self, belief_str):
        for belief_obj in self.beliefs:
            if belief_obj.belief == belief_str:
                return belief_obj
        return None

    def get_beliefs_with_priorities(self):
        """
        Get beliefs with priorities from BeliefBase.
        """
        beliefs_with_priorities = [(belief.belief, belief.priority) for belief in self.beliefs]
        return beliefs_with_priorities

    def sort(self):
        # Create a list of tuples (belief, priority)
        beliefs_with_priorities = self.get_beliefs_with_priorities()

        # Sort the list of tuples based on priority
        beliefs_with_priorities.sort(key=lambda x: x[1])

        # Update beliefs with sorted list of beliefs
        self.sorted = beliefs_with_priorities


        return self.sorted

    def group_beliefs_by_priority(self):
        """
        Group beliefs by priority.
        returns a list with a list of beliefs that have the priority = index
        """
        grouped_beliefs = {}
        for belief, priority in self.sorted:
            if priority not in grouped_beliefs:
                grouped_beliefs[priority] = []
            grouped_beliefs[priority].append(belief)
        return grouped_beliefs


    def get_combinations(self,grouped_beliefs,order):
        '''
        returns a list of all possible combinations with the correct order to test for entailment
        '''
        comb = []
        for i in range(len(grouped_beliefs),order+1):
            comb.extend(grouped_beliefs[i])
            for num in range(2,len(grouped_beliefs[i])+1):
                c = combinations(grouped_beliefs[i],num)
                comb.extend(c)

    def checkOrder(self,b):
        self.sort()
        base = BeliefBase()
        #check if the order is more than the least important belief
        if b.priority<self.sorted[0][1]:
            return False
        else:
            #check if the base that includes beliefs with higher order entails the negation of the statement
                #if yes we cannot continue, otherwise we can
            base.beliefs =self.beliefs.copy()
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

    def find_combinations(self,order):
        comb = []  # all the combinations
        self.sort()
        beliefs = [item[0] for item in self.sorted if item[1] <= order]
        priority = [item[1] for item in self.sorted if item[1] <= order]


        comb_priority = []
        comb.extend(beliefs)
        for num in range(2, len(beliefs) + 1):
            c = combinations(beliefs, num)
            comb.extend(c)

        for c in comb:  # for each combination
            max_p = 0  # initialize priority for combination
            sum_p = 0
            if isinstance(c, tuple):  # Check if c is a tuple
                for l in range(len(c)):  # for each element in the tuple
                    place = beliefs.index(c[l])
                    p = priority[place]
                    if p > max_p:
                        max_p = p
                    sum_p += p
            else:  # If c is not a tuple, treat it as a single belief
                place = beliefs.index(c)
                p = priority[place]
                max_p = p
                sum_p = p
            comb_priority.append((max_p, sum_p))

        zipped_comb = list(zip(comb, comb_priority))
        zipped_comb = list(set(zipped_comb))
        zipped_comb.sort(key=lambda x: x[1])
        sorted_comb = [item[0] for item in zipped_comb]

        return sorted_comb

    def revision(self,belief):
        # 1.check entailment for degrees>=order
            # if the base that includes degrees more or equal to the order that the statement has then we can continue
            # otherwise it cannot be added
        p = self.checkOrder(belief)

        if p:
            # check for the maximal base subset that doesn't entail the negation of the statement
            comb = self.find_combinations(belief.priority)
            #these are the different combinations that I can try in order to see what I need to remove
            for c in comb:
                #Use a test belief base to try removing the different combinations
                test_base = BeliefBase()
                test_base.beliefs = self.beliefs.copy()
                test_base.sort()
                if isinstance(c, tuple):  # Check if c is a tuple
                    for l in range(len(c)):  # for each element in the tuple
                        b = self.find_belief(c[l])
                        test_base.contraction(b)
                else:  # If c is not a tuple, treat it as a single belief
                    b = self.find_belief(c)
                    test_base.contraction(b)

                entails = test_base.check_entailment(Not(sympify(belief.belief)))
                # if entails=True then I cannot add it
                if not entails:
                    return True,c
            return False, []
        else:
            print('Cannot be added due to low priority')
            return False,[]


    def expansion(self, belief):
        old_belief = self.find_belief(belief.belief)
        if old_belief:
            self.contraction(old_belief)
            self.beliefs.add(belief)
        else:
            self.beliefs.add(belief)
        #####!!!!! an balw me allo priority na to allaksw


    def contraction(self, belief):
        if belief in self.beliefs:
            self.beliefs.remove(belief)

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


