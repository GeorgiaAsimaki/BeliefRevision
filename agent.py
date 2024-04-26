import  beliefRevision
from beliefRevision import BeliefBase


from sympy.logic.boolalg import to_cnf


if __name__ == '__main__':
    base = BeliefBase()
    print("my Belief base is: ", base.display())
    print("Input the statement to be revisioned")
    statement=input()
    statement = statement.lower()
    base.expansion(statement)

    #print(statement)
    print("my Belief base is: ", base.display())
    print("Input the statement to be revisioned")
    statement2 = input()
    statement2 = statement2.lower()
    #base.expansion(statement2)

    # print(statement)
    print("my Belief base is: ", base.display())
    print(base.check_entailment(statement2))

    #print(type(statement))
    #print(to_cnf(belief))
