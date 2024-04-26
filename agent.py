import  beliefRevision
from beliefRevision import BeliefBase


from sympy.logic.boolalg import to_cnf


if __name__ == '__main__':
    base = BeliefBase()
    print("my Belief base is: ", base.display())
    print("Input the statement to be revisioned")
    statement=input()
    print("Input the priority (integer from 0-10)")
    p = input()
    statement = statement.lower()
    base.expansion(statement, int(p))

    #print(statement)
    print("my Belief base is: ", base.display())
    print("Input the statement to be revisioned")
    statement2 = input()
    statement2 = statement2.lower()
    print("Input the priority (integer from 0-10)")
    p2 = input()
    base.expansion(statement2, int(p2))

    # print(statement)
    print("my Belief base is: ", base.display())
    print("sorted: ", base.sort())
    #print(base.check_entailment(statement2))

    #print(type(statement))
    #print(to_cnf(belief))
