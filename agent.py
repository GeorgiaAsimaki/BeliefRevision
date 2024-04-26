import  beliefRevision
from beliefRevision import BeliefBase

from sympy.logic.boolalg import to_cnf


if __name__ == '__main__':
    base = BeliefBase()
    print("my Belief base is: ", base.display())
    print("Input the statement to be revisioned")
    statement=input()
    base.expansion(statement)
    statement = statement.lower()
    #print(statement)
    print("my Belief base is: ", base.display())
    print(base.check_entailment(statement))

    #print(type(statement))
    #print(to_cnf(belief))
