###########################################################################
## answers.py - Code template for Project Functional Dependencies
###########################################################################

## If you need to import library put it below
from itertools import combinations, groupby
from collections import defaultdict
import copy

## Change the function below with your student number.
def student_number():
    return 'A0211264U'

def closure(R,F,S):
    # closure function can take multiple char
    # result = []
    result = set()
    singleton_list = S

    # print('=== closure F ===', F)
    for fd in F:
        # print('===fd===', fd)
        # print('===S===', S)

        # print('===fd[0]===', fd[0])
        # print('=== set(fd[0]) in set(S) ===',set(fd[0]).issubset(S))
        if set(fd[0]).issubset(set(S)):
            # print('===fd===', fd)
            # print('===fd1===', fd[1])
            result.update(fd[1])
            singleton_list.extend(fd[1])
        
        # print('=== checking double attr result ===', result) 
        # print('=== checking double attr singleton_list ===', singleton_list) 
    # print('=== sorted(set(singleton_list)) ===', sorted(set(singleton_list)))
    for s in sorted(set(singleton_list)):
        # print('===s===',s)
        # result.append(singleton_closure(R,F,[s]))
        # print('=== result before union ===', result)
        result = result.union(set(singleton_closure(R,F,[s])))
        # print('===result after union ===',result)
    # print('===closure result===',result)
    # print('=== is F modified? ===', F)
    return sorted(result)


## Q1a. Determine the closure of a given set of attribute S the schema R and functional dependency F
def singleton_closure(R, F, S):
    # singleton closure can only take single char
    closure = []
    # print('=== singleton_closure S ===', S)

    # itself
    # closure.append(S)
    for i in S:
        closure.append(i)
    # print('===closure1===', closure)

    # direct
    for fd in F:
        # print('===fd===', fd)
        # print('===fd[0]===', fd[0])
        # print('===S===', S)

        if fd[0] == S: 

            for j in fd[1]:
                # print('===j===', j)
                closure.append(j)
    # print('===closure2===', closure)

    # indirect
    for c in closure[1:]:
        # if c != S cannot work
        # print('===c===', c)

        for fd in F:
            # print('===fd===', fd)
            # print('===fd[0]===', fd[0])
            # print('===c-type===', type(c))
            # print('===fd-type===', type(fd))

            if fd[0] == [c]:
                # print('=== fd[0] ===', fd[0])
                # print('=== c ===', c)


                for j in fd[1]:
                    # print('=== j ===', j)
                    # print('=== fd[1] ===', fd[1])

                    closure.append(j)
                    # print('===singleton_closure result ===', closure)
    # return closure
    # print('===singleton_closure final result ===', sorted(set(closure)))
    return sorted(set(closure))

## Q1b. Determine all attribute closures excluding superkeys that are not candidate keys given the schema R and functional dependency F
def all_closures(R, F): 
    result = {}
    for i in allCombinations(R):
        # print('=== i ===', i)
        # print('=== [i] ===', list(i))
        intermediate = closure(R,F,list(i))
        # print('=== intermediate ===', intermediate)

        result[i] = sorted(set(intermediate))
    # print('=== intermediate_result ===', result)
    # exclude superkeys that are not candidate keys
    superkeys = []
    candidateKeys = []
    nonCandidateKeys = []
    for k,v in result.items():
        if v == sorted(set(R)):
            superkeys.append(k)
    # print('===superkeys===',superkeys)
    for superkey in superkeys:
        lengths = [len(superkey) for superkey in superkeys]
        # print('===lengths===',lengths)

        minLength = min(lengths)
        # print('===minLength===',minLength)

        candidateKeysIndex = [i for i, x in enumerate(lengths) if x == minLength]
        # print('===candidateKeysIndex===',candidateKeysIndex)
        candidateKeys = [superkeys[i] for i in candidateKeysIndex] 
        # candidateKeys = []
        # for i in candidateKeysIndex:
        #     candidateKeys.append(superkeys[i])
        # print('===candidateKeys===',candidateKeys)
        for i in candidateKeys:
            nonCandidateKeys = [i for i in superkeys if i not in candidateKeys]

        # print('===nonCandidateKeys===',nonCandidateKeys)
    for i in nonCandidateKeys:
        del result[i]
    
    print('===superkeys===',superkeys)
    print('===candidateKeys===',candidateKeys)
    print('===nonCandidateKeys===',nonCandidateKeys)

    result_list = []
    for k, v in result.items():
        result_list.append([list(k),v])

    return result_list
    
## Q2a. Return a minimal cover of the functional dependencies of a given schema R and functional dependencies F.
def min_cover(R, FD): 
    # convert RHS to singleton expression
    print('=== FD ===', FD)
    singleton_attribute_list = []
    # closure_list = []

    # intermediate = {}
    for fd in FD:
        for i in fd[1]:
            singleton_attribute = [fd[0], [i]]
            singleton_attribute_list.append(singleton_attribute)
    #     for i in fd[0]:
    #         print('=== i ===', i)
    #         intermediate[i] = closure(R, FD, [i])
    #         # closure_list.append(intermediate)
    # print('=== intermediate ===', intermediate)
    
    print('=== singleton_attribute_list ===', singleton_attribute_list)

    closures = all_closures(R,FD)

    # convert dictionary faster access than iteration later
    # closures_dict = {}
    # for c in closures:
    #     closures_dict[closures[c][0]] = closures[c][1] 

    # print('=== all closures ===', closures)

    simplify_attribute_FD = singleton_attribute_list
    for fd in simplify_attribute_FD:
        # lhs_simplify = set()
        # print('===fd ===', fd)

        # logic should be to check closure of each attribute in LHS
        # see which of it contains the RHS attribute
        # that LHS attribute can be kept and others discarded
        # the choice of which LHS attribute is kept can lead to different outcomes

        # but my way of checking which LHS attribute includes other LHS attribute is also not bad

        # maybe both logic need to be in

        # TODO
        # where LHS have multiple attributes
        # easy: implement candidatekey check, if candidatekey is subset of LHS, replace LHS with candidatekey
        # should implement candidatekey check first as if case, then else check all others, speed up by elminate superkey cases
        # middle: implement combination LHS check, where not just check if LHS singleton attribute contain RHS, but also check if minimal LHS combination contain LHS

        # NOT DO ABOVE
        # we did check for RHS is within closure of LHS
        # now add 


        '''
        check for case where LHS elem is within closure of other LHS elem or all combinations of LHS elem
        '''


        if len(fd[0]) >= 2:
            for i in range(2,len(fd[0])-1):
                for a, b in combinations(fd[0],i):
                    for c in closures:
                        if list(a) == c[0]:
                            if set(b).issubset(set(c[1])):
                                fd[0].remove(b)


            # for i in range(len(fd[0])-1):
            #     for c in closures:
            #         print('=== fd ===', fd)
            #         print('=== fd[0] ===', fd[0])
            #         print('=== fd[1] ===', fd[1])
            #         print('===fd[0][i] ===', fd[0][i])
            #         # print('===closures[fd[0][i]] ===', closures[fd[0][i]])
            #         print('===fd[0][i+1] ===', fd[0][i+1])
            #         if list(fd[0][i]) == c[0]:

            #             if set(fd[0][i+1]).issubset(set(c[1])):

            #         # if fd[0][i+1] in closures[fd[0][i]]:
            #                 print('===before popped fd ===', fd)
            #                 fd[0].pop(i+1)
            #                 print('===popped fd[0][i+1] ===', fd[0][i+1])
            #                 print('===after popped fd ===', fd)

        '''
        check for case where RHS is within closure of 1 LHS elem
        actually should check within all combinations of LHS elems
        '''

        for f in fd[0]:
            for c in closures:
                # print('=== fd ===', fd)
                # print('=== fd[0] ===', fd[0])
                # print('=== fd[1] ===', fd[1])
                # print('=== f ===', f)
                # print('=== c ===', c)
                # print('=== c[0] ===', c[0])
                # print('=== f == c[0] ===', f == c[0])
                if list(f) == c[0]:
                    # print('=== set(fd[1]).issubset(set(c[1]])) ===', set(fd[1]).issubset(set(c[1])))
                    if set(fd[1]).issubset(set(c[1])):
                        fd[0] = list(f)
                        # print('===new fd[0] ===', fd[0])

    print('=== simplify_attribute_FD ===', simplify_attribute_FD)



    # remove_repeat_fd = {}
    # for fd in simplify_attribute_FD:
    #     remove_repeat_fd[fd] = 1

    # print('=== remove_repeat_fd ===', remove_repeat_fd)

    # remove_repeat_fd = simplify_attribute_FD
    # for i in range(len(simplify_attribute_FD)-1):
    #     for j in range(len(simplify_attribute_FD)-2):
    #         print('===simplify_attribute_FD[i] ===', simplify_attribute_FD[i])
    #         print('===simplify_attribute_FD[j] ===', simplify_attribute_FD[j])

    #         if simplify_attribute_FD[i] == simplify_attribute_FD[j]:
    #             remove_repeat_fd.pop(j)

    # # remove_repeat_fd = set(tuple(i) for i in simplify_attribute_FD)
    # simplify_attribute_FD_tuples = [tuple(i) for i in simplify_attribute_FD]
    # print('===simplify_attribute_FD_tuples ===', simplify_attribute_FD_tuples)
    simplify_attribute_FD.sort()
    # print('=== simplify_attribute_FD.sort() ===', simplify_attribute_FD)
    remove_repeat_fd = list(simplify_attribute_FD for simplify_attribute_FD,_ in groupby(simplify_attribute_FD))
    print('=== remove_repeat_fd===', remove_repeat_fd)

    # # remove_repeat_fd = list(simplify_attribute_FD_tuples for simplify_attribute_FD_tuples,_ in groupby(simplify_attribute_FD_tuples))
    # remove_repeat_fd = [t for t in (set(tuple(i) for i in set(simplify_attribute_FD_tuples)))]
    # print('===remove_repeat_fd ===', remove_repeat_fd)

            # print('===lhs_simplify start===', lhs_simplify)
            # print('===closures[i]===', closures[i])

        #     if lhs_simplify.issubset(closures[i]): 
        #         lhs_simplify = set(closures[i])
        #         print('===lhs_simplify===', lhs_simplify)

        # fd_new = fd
        # fd_new[0] = list(lhs_simplify)
        # print('===fd_new===', fd_new)

    # print('=== closure_list ===', closure_list)

    # final = []
    # for i in range(len(remove_repeat_fd)-1):
    #     if remove_repeat_fd[i][0] == remove_repeat_fd[i+1][0]:
    #         result = zip(remove_repeat_fd[i],remove_repeat_fd[i+1])
    #         final.append(list(result))
    #     final.append(remove_repeat_fd[i])

    # ### Recombining implications with same LHS, not necessary based on notes
    # final = defaultdict(list)
    # for i in remove_repeat_fd:
    #     # print('=== i[0] ===', i[0])
    #     i[0] = ''.join(i[0])
    #     i[1] = ''.join(i[1])

    #     final[i[0]].extend([i[1]])

    # finalList = list(map(list, final.items()))
    # for f in finalList:
    #     f[0] = list(f[0]) 

    # TODO: simplify the complex LHS (into singleton) if possible

    # if a RHS of expression 1 (C of B -> C)
    # is also a LHS of expression 2 (C of C -> D)
    # and there is expression 3 where LHS 1 -> RHS 2 (B -> D) should be cancelled

    '''
    remove redundant fd, to check
    remove direct effect for an attribute
    check if indirect effect exists for an attribute
    if indirect effect exists, remove the direct effect fd 
    '''
    cover = copy.deepcopy(remove_repeat_fd)
    temp = copy.deepcopy(remove_repeat_fd)
    for r in range(len(temp)):
        if r <= len(temp) - 1:
            # print('=== cover 1 ===', cover)
            # print('=== r ===', r)
            # print('=== temp before pop ===', temp)
            r_value = temp.pop(r)
            # print('=== temp after pop ===', temp)
            # print('=== r_value ===', r_value)
            # print('=== r_value[0] ===', r_value[0])
            # print('=== r_value[1] ===', r_value[1])

            # print('=== cover 1 ===', cover)
            # print('=== closure(R,temp,r_value[0]) ===', closure(R,temp,r_value[0]))
            # print('=== cover 2 ===', cover)

            # print('=== R ===', R)

            # print('=== set(r_value[1]).issubset(set(closure(R,temp,r_value[0])))===', set(r_value[1]).issubset(set(closure(R,temp,r_value[0]))))
            # print('=== cover 2 ===', cover)

            attr_closure = closure(R,temp,r_value[0])
            # print('=== attr_closure ===', attr_closure)

            # print('=== set(r_value[1]) ===', set(r_value[1]))
            # print('=== set(attr_closure) ===', set(attr_closure))

            if set(r_value[1]).issubset(set(attr_closure)):
                cover.pop(r) # because r is unnecessary, LHS attribute closure still contains RHS, even after remove r
                # print('=== cover pop r ===', cover)
                # print('=== cover length after pop r ===', len(cover))
            else:
                # print('=== cover to reset temp===', cover)
                temp = copy.deepcopy(cover)
                # temp.insert(r, r_value)
                # print('=== temp reset r ===', temp)
                # print('=== temp length after reset r ===', len(temp))




    # return finalList
    # return remove_repeat_fd
    return cover


## Q2b. Return all minimal covers reachable from the functional dependencies of a given schema R and functional dependencies F.
def min_covers(R, FD):
    '''
    Explain the rationale of the algorithm here.

    Assignment question:
    Find all minimal cover that can reach from sigma?
    because can make different choices, so want to find all the possible outcomes

    qn 2a code
    simplify step, use attribute closure to simplify
    B -> B, C, D, E
    so 
    A, B -> D 
    simplify to 
    B -> D

    use min_cover
    vary step 2
    '''
    

    # call min_cover multiple times
    # but how to decide how many times?
    # google!

    return []

## Q2c. Return all minimal covers of a given schema R and functional dependencies F.
def all_min_covers(R, FD):
    '''
    Explain the rationale of the algorithm here.

    Explanation:
    All minimal cover can be found by the min_cover algorithm applied on Σ+

    to guarantee to reach all minimal cover
    go back to sigma+
    apply minimal cover algo, will reach everything
    only if u implement this
    but u don't want to go to sigma+ because its slow
    just need to go high enough to reach all the minimal cover
    the hint is need to think about the attribute closures u have, all the info u want is there, info inside
    similarly to find the keys, no need to calc all attribute closures, maybe some enough

    use min_covers
    vary step 2 and step 3

    '''
    closures = all_closures(R, FD)
    # print('=== all_closures all_min_covers ===', closures)
    # === all_closures all_min_covers === 
    # [[['A'], ['A', 'B', 'C']], 
    # [['B'], ['A', 'B', 'C']], 
    # [['C'], ['A', 'B', 'C']]]

    # R = [[['A'], ['B']],[['B'], ['C']], [['C'], ['A']]]

    # [
    # [[['A'], ['B']], [['A'], ['C']], [['B'], ['A']], [['C'], ['A']]], 
    # [[['A'], ['B']], [['B'], ['C']], [['B'], ['A']], [['C'], ['B']]] 
    # [[['A'], ['C']], [['B'], ['C']], [['C'], ['A']],[['C'], ['B']]], 
    # [[['A'], ['B']], [['B'], ['C']], [['C'], ['A']]], # this and below are reverse LHS, RHS
    # [[['B'], ['A']], [['C'], ['B']], [['A'], ['C']]],
    # ]
    return []

## You can add additional functions below

# def reflexivity(lhs, rhsList):
#     result = []
#     for rhs in rhsList:
#         if rhs in lhs:
#             result.append([lhs,rhs])
#     return result

def augmentation(iter):
    return []

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

def reflexivity(x):
    result = []
    # chars = [char for char in l]
    chars = [''.join(l) for i in range(len(x)) for l in combinations(x, i+1)]
    for char in chars:
        result.append([x,char])
    return result
    
def calcReflexivity(allCombinations):
    result = []
    for ac in allCombinations:
        result.append(reflexivity(ac))
        flatten_result = [item for sublist in result for item in sublist]
    return flatten_result

# def transitivity(allCombinations):


## Main functions
def main():
    ### Test case from the project
    R = ['A', 'B', 'C', 'D']
    FD = [[['A', 'B'], ['C']], [['C'], ['D']]]

    print(closure(R, FD, ['A']))
    print(closure(R, FD, ['A', 'B']))

    print(closure(['A','B','C'], [[['A'], ['B']], [['A'], ['C']], [['B'], ['C']]], ['A']))
    print(closure(['A','B','C'], [[['A'], ['C']], [['B'], ['C']]], ['A']))

    print(all_closures(R, FD))

    R1 = ['A', 'B', 'C']
    FD1 = [[['A'], ['B', 'C']], [['B'], ['C']], [['A'], ['B']], [['A','B'], ['C']]] # example from https://www.tutorialspoint.com/what-is-the-minimal-set-of-functional-dependencies-or-canonical-cover-of-fd

    print(all_closures(R1, FD1))

    print('============== min_cover ==================')

    # R = ['A', 'B', 'C', 'D', 'E', 'F']
    # FD = [[['A'], ['B', 'C']], [['B'], ['C','D']], [['D'], ['B']], [['A','B','E'], ['F']]] 
    # print('=== 1st example min_cover ===', min_cover(R, FD)) 

    R = ['A', 'B', 'C']
    FD = [[['A'], ['B', 'C']], [['B'], ['C']], [['A'], ['B']], [['A','B'], ['C']]] # example from https://www.tutorialspoint.com/what-is-the-minimal-set-of-functional-dependencies-or-canonical-cover-of-fd
    print('=== base example min_cover ===', min_cover(R, FD)) 

    R = ['A', 'B', 'C', 'D', 'E']
    FD = [[['A', 'B'], ['C', 'D', 'E']], [['A', 'C'], ['B','D', 'E']], [['B'], ['C']], [['C'], ['B']], [['C'], ['D']], [['B'],['E']], [['C'],['E']]] 
    print('=== 2nd example min_cover ===', min_cover(R, FD)) 

    R = ['A', 'B', 'C', 'D', 'E', 'F']
    FD = [[['A'], ['B', 'C']], [['B'], ['C','D']], [['D'], ['B']], [['A','B','E'], ['F']]] 
    print('=== 3rd complex min_cover ===', min_cover(R, FD)) 


    R = ['A', 'B', 'C']
    FD = [[['A'], ['B']], [['B'], ['C']], [['C'], ['A']]] 
    print('=== 1st reachable min_cover ===', min_covers(R, FD))

    print(all_min_covers(R, FD)) 

    R = ['A','B','C','D','E','F','G']
    FD = [[['A','C'],['G']], [['D'],['E','G']], [['B','C'],['D']], [['C','G'],['B','D']], [['A','C','D'],['B']], [['C','E'],['A','G']]]

    print('=== example all_closures ===',all_closures(R,FD))
    print('=== example min_cover ===',min_cover(R,FD))


#     # print('========= calcReflexivity ============', calcReflexivity(allCombinations(['A','B'])))

#     R1 = ['A', 'B', 'C', 'D', 'E']
#     print('========= allCombinations ============', allCombinations(R1))

#     FD1 = [[['A', 'B'], ['C', 'D', 'E']], [['A', 'C'], ['B','D','E']], [['B'],['C']], [['C'],['B']], [['C'],['D']], [['B'],['E']], [['C'],['E']]]

#     """
#     B case

#     Itself
#     closure add B
#     closure = B

#     Direct
#     LHS == B
#     closure add C
#     closure add E
#     closure = B, C, E


#     Indirect
#     closure = B, C, E


#     """


#     print('=== closure A ===', closure(R1, FD1, ['A']))
#     print('=== closure B ===', closure(R1, FD1, ['B']))
#     print('=== closure C ===', closure(R1, FD1, ['C']))
#     print('=== closure D ===', closure(R1, FD1, ['D']))
#     print('=== closure E ===', closure(R1, FD1, ['E']))

#     print('=== closure AB ===', closure(R1, FD1, ['A','B']))
#     print('=== closure AC ===', closure(R1, FD1, ['A','C']))
#     print('=== closure AD ===', closure(R1, FD1, ['A','D']))
#     print('=== closure AE ===', closure(R1, FD1, ['A','E']))
#     print('=== closure BC ===', closure(R1, FD1, ['B','C']))
#     print('=== closure BD ===', closure(R1, FD1, ['B','D'])) 
#     ### REALISATION, the PAIR COVERS need to INCLUDE the SINGLETON COVERS!!!
#     ### BD closure need to include B closure and D closure as well!!!
#     ### WRONG!!! call closure on all constituents individually, and merge the result back into set
#     ### closure function can only be used to calculate singleton cover!!!
#     ### CORRECT!!! pair cover must call closure function separately on each constituent and merge their closures into set!!!

#     ### def singleton_closure
#     ### def closure calls singleton_closure on each constituent, merges results into set

#     print('=== closure BE ===', closure(R1, FD1, ['B','E']))
#     print('=== closure CD ===', closure(R1, FD1, ['C','D']))
#     print('=== closure CE ===', closure(R1, FD1, ['C','E']))
#     print('=== closure DE ===', closure(R1, FD1, ['D','E']))

#     print('=== closure ADE ===', closure(R1, FD1, ['A', 'D', 'E']))
#     print('=== closure BDE ===', closure(R1, FD1, ['B', 'D','E']))
#     print('=== closure CDE ===', closure(R1, FD1, ['C','D','E']))
#     print('=== closure BCE ===', closure(R1, FD1, ['B','C','E']))
#     print('=== closure BCD ===', closure(R1, FD1, ['B','C','D']))

#     print('=== closure BCDE ===', closure(R1, FD1, ['B','C','D','E']))


#     print(all_closures(R1, FD1)) ### all_closures function needs to call closure function on allcombinations

#     # TODO: all_closures still not correct answer!!!

#     # print('=== all_closures ===', all_closures(R1, FD1))



#     ### Add your own additional test cases if necessary


if __name__ == '__main__':
    main()



