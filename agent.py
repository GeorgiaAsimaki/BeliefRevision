import  beliefRevision
from beliefRevision import BeliefBase,Belief
from sympy import sympify
from sympy.logic.boolalg import  Not


from sympy.logic.boolalg import to_cnf


def checkForRevision(base,new_belief):
    # if base entails the negation of the statement then I do revision, if it returns False I add it to the base
    isEntailed = base.check_entailment(Not(sympify(new_belief.belief)))
    if isEntailed:
        flag,remove = base.revision(new_belief)
        #flag=True means that the belief can be added if we remove the combination remove
        if flag:
            if isinstance(remove, tuple):  # Check if c is a tuple
                for l in range(len(remove)):  # for each element in the tuple
                    b = base.find_belief(remove[l])
                    base.contraction(b)
            else:  # If c is not a tuple, treat it as a single belief
                b = base.find_belief(remove)
                base.contraction(b)
            base.expansion(new_belief)
        else:
            print('Cannot be added')

    else:
        base.expansion(new_belief)

def make_belief(statement,order):
    cnf = to_cnf(statement)
    cnf = str(cnf)
    b = Belief()
    b.belief = cnf
    b.priority = order
    return b


if __name__ == '__main__':
    base = BeliefBase()
    '''
    #Belief 1
    print("my Belief base is: ", base.display())
    print("Input the statement to be revisioned")
    statement=input()
    print("Input the priority (integer from 0-10)")
    p = input()
    statement = statement.lower()
    belief1 = make_belief(statement,int(p))
    base.expansion(belief1)
    '''
    belief1 = make_belief('~a',1)
    base.expansion(belief1)
    belief1 = make_belief('a|b', 3)
    base.expansion(belief1)
    belief1 = make_belief('a&b', 4)
    base.expansion(belief1)
    belief1 = make_belief('~a', 4)
    base.expansion(belief1)

    #Belief 2
    print("my Belief base is: ", base.display())
    print("Input the statement to be revisioned")
    statement2 = input()
    statement2 = statement2.lower()
    print("Input the priority (integer from 0-10)")
    p2 = input()
    belief2 = make_belief(statement2, int(p2))
    #base.expansion(belief2)
    print("my Belief base is: ", base.display())
    #print(base.check_entailment(statement2))

    print("sorted: ", base.sort())
    checkForRevision(base, belief2)
    print("my Belief base is: ", base.display())

    '''
    # Belief 3
    print("my Belief base is: ", base.display())
    print("Input the statement to be revisioned")
    statement3 = input()
    statement3 = statement3.lower()
    print("Input the priority (integer from 0-10)")
    p3 = input()
    #base.expansion(statement3, int(p3))
    checkForRevision(base, statement3, int(p3))

    # print(statement)
    print("my Belief base is: ", base.display())
    print("sorted: ", base.sort())
    #print(base.check_entailment(Not(sympify(statement2))))
    #print(base.check_entailment(statement2))

    #print(type(statement))
    #print(to_cnf(belief))
'''