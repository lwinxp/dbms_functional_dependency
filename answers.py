###########################################################################
## answers.py - Code template for Project Functional Dependencies
###########################################################################

## If you need to import library put it below
from itertools import combinations, groupby, permutations
from collections import defaultdict
import copy

## Change the function below with your student number.
def student_number():
    return 'A0211264U'

## Q1a. Determine the closure of a given set of attribute S the schema R and functional dependency F
def closure(R,F,S):
    result = set()
    singleton_list = S

    for fd in F:
        if set(fd[0]).issubset(set(S)):
            result.update(fd[1])
            singleton_list.extend(fd[1])

    for s in sorted(set(singleton_list)):
        result = result.union(set(singleton_closure(R,F,[s])))

    return sorted(result)


## Q1b. Determine all attribute closures excluding superkeys that are not candidate keys given the schema R and functional dependency F
def all_closures(R, F): 
    result = {}
    for i in allCombinations(R):
        intermediate = closure(R,F,list(i))
        result[i] = sorted(set(intermediate))

    superkeys = []
    candidateKeys = []
    nonCandidateKeys = []
    for k,v in result.items():
        if v == sorted(set(R)):
            superkeys.append(k)
    for superkey in superkeys:
        lengths = [len(superkey) for superkey in superkeys]

        minLength = min(lengths)

        candidateKeysIndex = [i for i, x in enumerate(lengths) if x == minLength]
        candidateKeys = [superkeys[i] for i in candidateKeysIndex] 

        for i in candidateKeys:
            nonCandidateKeys = [i for i in superkeys if i not in candidateKeys]

    for i in nonCandidateKeys:
        del result[i]
    
    # print('===superkeys===',superkeys)
    # print('===candidateKeys===',candidateKeys)
    # print('===nonCandidateKeys===',nonCandidateKeys)

    result_list = []
    for k, v in result.items():
        result_list.append([list(k),v])

    return result_list
    
## Q2a. Return a minimal cover of the functional dependencies of a given schema R and functional dependencies F.
def min_cover(R, FD): 
    singleton_attribute_list = []

    for fd in FD:
        for i in fd[1]:
            singleton_attribute = [fd[0], [i]]
            singleton_attribute_list.append(singleton_attribute)
    
    closures = all_closures(R,FD)

    simplify_attribute_FD = singleton_attribute_list
    for fd in simplify_attribute_FD:

        '''
        Remove redundant LHS attribute - check for case where LHS elem is within closure of other LHS attribute
        '''
        if len(fd[0]) >= 2:
            for i in range(2,len(fd[0])):
                for a, b in combinations(fd[0],i):
                    for c in closures:
                        if list(a) == c[0]:
                            if set(b).issubset(set(c[1])):
                                fd[0].remove(b)

        '''
        Remove redundant LHS attribute - check for case where RHS is within closure of 1 LHS elem
        '''
        for f in fd[0]:
            for c in closures:
                if list(f) == c[0]:
                    if set(fd[1]).issubset(set(c[1])):
                        fd[0] = list(f)

    # print('=== simplify_attribute_FD ===', simplify_attribute_FD)

    simplify_attribute_FD.sort()
    remove_repeat_fd = list(simplify_attribute_FD for simplify_attribute_FD,_ in groupby(simplify_attribute_FD))
    # print('=== remove_repeat_fd===', remove_repeat_fd)

    '''
    Remove redundant FD (direct effect)
    Check closure of remaining FDs
    Check if removed FD implication still applies (indirect effect)
    If implication still applies, the removed FD is redundant 
    '''
    cover = copy.deepcopy(remove_repeat_fd)
    temp = copy.deepcopy(remove_repeat_fd)
    for r in range(len(temp)):
        if r <= len(temp) - 1:
            r_value = temp.pop(r)

            attr_closure = closure(R,temp,r_value[0])

            if set(r_value[1]).issubset(set(attr_closure)):
                cover.pop(r) # because r is unnecessary, LHS attribute closure still contains RHS, even after remove r
            else:
                temp = copy.deepcopy(cover)

    return cover


## Q2b. Return all minimal covers reachable from the functional dependencies of a given schema R and functional dependencies F.
def min_covers(R, FD):
    '''
    Explain the rationale of the algorithm here.

    min_covers follows the same 3 steps of finding min_cover (refer triple quotes of explanations)
    the difference is that min_covers has an additional logic for varying the order
    of functional dependencies that are being checked for redundancy and removed
    which allows for different minimal covers to be found from the initial set of functional dependencies
    note that the set of functional dependencies is still restricted to what is initially provided (reachable), 
    unlike all_min_covers elaborated on in Qn 2c
    '''

    singleton_attribute_list = []

    for fd in FD:
        for i in fd[1]:
            singleton_attribute = [fd[0], [i]]
            singleton_attribute_list.append(singleton_attribute)
    
    closures = all_closures(R,FD)

    simplify_attribute_FD = singleton_attribute_list
    for fd in simplify_attribute_FD: 

        '''
        Remove redundant LHS attribute - check for case where LHS elem is within closure of other LHS attribute
        '''

        if len(fd[0]) >= 2:
            for i in range(2,len(fd[0])):
                for a, b in combinations(fd[0],i):
                    for c in closures:
                        if list(a) == c[0]:
                            if set(b).issubset(set(c[1])):
                                fd[0].remove(b)

        '''
        Remove redundant LHS attribute - check for case where RHS is within closure of 1 LHS elem
        '''

        for f in fd[0]: 
            for c in closures:
                if list(f) == c[0]:
                    if set(fd[1]).issubset(set(c[1])):
                        fd[0] = list(f)

    # print('=== simplify_attribute_FD ===', simplify_attribute_FD)

    simplify_attribute_FD.sort()
    remove_repeat_fd = list(simplify_attribute_FD for simplify_attribute_FD,_ in groupby(simplify_attribute_FD))
    # print('=== remove_repeat_fd===', remove_repeat_fd)


    '''
    Remove redundant FD (direct effect)
    Check closure of remaining FDs
    Check if removed FD implication still applies (indirect effect)
    If implication still applies, the removed FD is redundant 
    '''

    permutate = list(permutations(remove_repeat_fd)) # order matters
    permutate_list = [list(p) for p in permutate]

    result = []

    for pt in permutate_list:
        cover = copy.deepcopy(pt) 
        temp = copy.deepcopy(pt)
        for r in range(len(temp)):
            if r <= len(temp) - 1:

                r_value = temp.pop(r)

                attr_closure = closure(R,temp,r_value[0])

                # print('=== set(r_value[1]).issubset(set(attr_closure)): ===', set(r_value[1]).issubset(set(attr_closure)))
                if set(r_value[1]).issubset(set(attr_closure)):
                    cover.pop(r) # because r is unnecessary, LHS attribute closure still contains RHS, even after remove r
                else:
                    temp = copy.deepcopy(cover)

        # print('=== cover ===', cover)
        result.append(cover)

    # print('=== result===', result)
    
    final_list = removeRepeatFd(result)

    return final_list

## Q2c. Return all minimal covers of a given schema R and functional dependencies F.
def all_min_covers(R, FD):
    '''
    Explain the rationale of the algorithm here.

    all_min_covers follows the same steps of finding min_covers (refer triple quotes for min_covers)
    the difference is that min_covers expands the initial set of functional dependencies
    using all_closures to give a full set sigma+ of attribute closures to calculate minimal covers

    As there are even more combinations of functional dependencies arising from the full set sigma+,
    it would be too slow and take too long to calculate based on sigma+
    Hence, trivial functional functional dependencies, specifically of X -> X form (e.g. A -> A, B -> B, C -> C) 
    are removed first from the set before calculating with min_covers    
    '''

    '''
    Calculate all closures for sigma+
    '''
    FD1 = all_closures(R, FD)
    # print('=== all_closures all_min_covers ===', FD1)
    # === all_closures all_min_covers === 
    # [[['A'], ['A', 'B', 'C']], 
    # [['B'], ['A', 'B', 'C']], 
    # [['C'], ['A', 'B', 'C']]]

    '''
    Remove trivial a -> a implication to simplify sigma+
    min_covers for sigma+ too big and take too long
    After simplify will be smaller set and faster
    '''
    FD2 = copy.deepcopy(FD1)

    for fd in FD2:
        if set(fd[0]).issubset(set(fd[1])):
            fd[1].remove(fd[0][0])

    # [[['A'], ['B', 'C']], 
    # [['B'], ['A','C']], 
    # [['C'], ['A', 'B']]]
    result = min_covers(R, FD2)

    intermediate = redundancyCheck(R, result)
    final_list = removeRepeatFd(intermediate)

    return final_list

## You can add additional functions below

def singleton_closure(R, F, S):
    # singleton closure can only take single char
    closure = []

    # itself
    for i in S:
        closure.append(i)

    # direct effect
    for fd in F:
        if fd[0] == S: 

            for j in fd[1]:
                closure.append(j)

    # indirect effect
    for c in closure[1:]:

        for fd in F:
            if fd[0] == [c]:
                for j in fd[1]:
                    closure.append(j)
    return sorted(set(closure))

def removeRepeatFd(result):
    result_dict_list = []
    for re in result:
        result_dict = defaultdict(set)
        for r in re:
            result_dict[''.join(r[0])].update(r[1])

        if result_dict not in result_dict_list:
            result_dict_list.append(result_dict)

    # convert dictionary back to list
    final_list = []
    for d in result_dict_list:
        final_sublist = []
        for k,v in d.items():
            for i in v:
                final_sublist.append([[k],[i]])

        # splitting multiple attributes in LHS
        for fs in final_sublist:
            if len(''.join(fs[0])) > 1:
                fs[0] = list(fs[0][0])
        final_list.append(final_sublist)
    return final_list

def redundancyCheck(R, result):
    intermediate = []
    for re in result:
        cover = copy.deepcopy(re) 
        temp = copy.deepcopy(re)
        idx_remove = []
        for r in range(len(temp)):
            r_value = temp.pop(r)
            attr_closure = closure(R,temp,r_value[0])
            if set(r_value[1]).issubset(set(attr_closure)):
                idx_remove.append(r)
            temp = copy.deepcopy(re)
        for i in sorted(idx_remove, reverse=True):
            del cover[i]
        intermediate.append(cover)
    return intermediate

def allCombinations(l):
    intermediate = []
    result = []
    for i in range(1, len(l) + 1):
        intermediate.append(list(combinations(l, i)))

    for i in intermediate:
        for j in i:
            j = ''.join(j)
            result.append(j)
    return result


## Main functions
def main():
    '''
    Additional examples were also tested
    They can be uncommented to test as well
    '''

    # print('============== closure ==================')


    R = ['A', 'B', 'C', 'D']
    FD = [[['A', 'B'], ['C']], [['C'], ['D']]]

    print('Qn 1a === closure ===')
    print(closure(R, FD, ['A', 'B']))
    
    # print('============== all_closures ==================')

    R = ['A', 'B', 'C', 'D']
    FD = [[['A', 'B'], ['C']], [['C'], ['D']]]
    print('Qn 1b === all_closures ===')
    print(all_closures(R, FD))

    # R1 = ['A', 'B', 'C']
    # FD1 = [[['A'], ['B', 'C']], [['B'], ['C']], [['A'], ['B']], [['A','B'], ['C']]]
    # print('=== all_closures extra example 1 ===', all_closures(R1, FD1))

    # print('============== min_cover ==================')

    R = ['A', 'B', 'C', 'D', 'E', 'F']
    FD = [[['A'], ['B', 'C']], [['B'], ['C','D']], [['D'], ['B']], [['A','B','E'], ['F']]] 
    print('Qn 2a === min_cover - matches answer key, might not be same ordering ===')
    print(min_cover(R, FD)) 

    # R = ['A', 'B', 'C']
    # FD = [[['A'], ['B', 'C']], [['B'], ['C']], [['A'], ['B']], [['A','B'], ['C']]]
    # print('=== min_cover extra example 1 ===', min_cover(R, FD)) 

    # R = ['A', 'B', 'C', 'D', 'E']
    # FD = [[['A', 'B'], ['C', 'D', 'E']], [['A', 'C'], ['B','D', 'E']], [['B'], ['C']], [['C'], ['B']], [['C'], ['D']], [['B'],['E']], [['C'],['E']]] 
    # print('=== min_cover extra example 2 ===', min_cover(R, FD)) 

    # R = ['A', 'B', 'C']
    # FD = [[['A'], ['B']], [['B'], ['C']], [['C'], ['A']]] 
    # print('=== min_cover extra example 3 ===', min_cover(R, FD))

    # print('============== min_covers ==================')

    R = ['A', 'B', 'C']
    FD = [[['A'], ['B']], [['B'], ['C']], [['C'], ['A']]] 
    print('Qn 2b === min_covers ===')
    print(min_covers(R, FD))

    # R = ['A', 'B', 'C', 'D', 'E']
    # FD = [[['A', 'B'], ['C', 'D', 'E']], [['A', 'C'], ['B','D', 'E']], [['B'], ['C']], [['C'], ['B']], [['C'], ['D']], [['B'],['E']], [['C'],['E']]] 
    # print('===  min_covers extra example 1===', min_covers(R, FD)) 

    # R = ['A', 'B', 'C', 'D', 'E', 'F']
    # FD = [[['A'], ['B', 'C']], [['B'], ['C','D']], [['D'], ['B']], [['A','B','E'], ['F']]] 
    # print('=== min_covers extra example 2 ===', min_covers(R, FD)) 

    # print('============== all_min_covers ==================')

    R = ['A', 'B', 'C']
    FD = [[['A'], ['B']], [['B'], ['C']], [['C'], ['A']]] 
    print('Qn 2c === all_min_covers - matches answer key, might not be same ordering ===') 
    print(all_min_covers(R, FD)) 

#     ### Add your own additional test cases if necessary


if __name__ == '__main__':
    main()



