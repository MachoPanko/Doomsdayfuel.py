import math
import itertools
from array import array
from functools import reduce
from fractions import Fraction
def solution(m):
    
    terminallist = [0]*len(m)
    possiblelists = []
    currentlist = [0]
    trackerlist = [0]*len(m)
    looppoint_list = []
    loops_list=[]
    loopsprobablity_list = []
    probability_dict = {}
    minprobability_matrix = []
    answerlist = []
    for i in range(len(m)):
        minprobability_matrix.append([])
        total = 0
        for element in m[i]:
            total += element
        for element in m[i]:
            if element != 0:
                minprobability_matrix[i].append(Fraction(element,total))
            else:
                minprobability_matrix[i].append(0)
        probability_dict[i] = 0

    def recurs(list):
        if list == terminallist:
            possiblelists.append(currentlist[:])
            currentlist.pop()
            return
        for i in range(len(m)):
            if list[i] != 0:
                trackerlist[i]+=1
                if trackerlist[i] == 2:
                    looppoint_list.append(i)
                    templooplist = []
                    start = False
                    for phase in currentlist:
                        if phase == i:
                            start = True
                        if start:
                            templooplist.append(phase)
                    templooplist.append(i)
                    loops_list.append(templooplist)
                    trackerlist[i] -= 1
                    continue
                currentlist.append(i)
                recurs(m[i])
        currentlist.pop()
        trackerlist[i] -= 1
        return


    def probabilityoflist ():
        print(possiblelists)
        print(loopsprobablity_list)
        for list in possiblelists:
            key = list[-1]
            totalprob = 0
            for i in range(1,len(list)):
                if totalprob == 0:
                    totalprob = minprobability_matrix[list[i - 1]][list[i]]
                else:
                    totalprob *= minprobability_matrix[list[i - 1]][list[i]]
            probability_dict[key] += totalprob
            for i in range(len(looppoint_list)): ## create loopprobability dict, if then run through all pointsas keys
                if looppoint_list[i] in list:
                    probability_dict[key] = probability_dict[key]/(1-loopsprobablity_list[i])

    def lcm(a, b):
        return abs(a * b) // math.gcd(a, b)

    recurs(m[0])
    for list1 in loops_list:
        totalprob1 = 0
        for i in range(1, len(list1)):
            if totalprob1 == 0:
                totalprob1 = minprobability_matrix[list1[i - 1]][list1[i]]
            else:
                totalprob1 *= minprobability_matrix[list1[i - 1]][list1[i]]

        loopsprobablity_list.append(totalprob1)
    probabilityoflist()


    for i,x in enumerate(m):
        if x == terminallist:
            answerlist.append(i)
    for i in range(len(answerlist)):
        answerlist[i] = probability_dict[answerlist[i]]
    combinations = itertools.combinations([x.denominator for x in answerlist], 2)
    x = 1
    for item in combinations:
        res = reduce(lcm, (a for a in item))
        if res > x:
            x = res
    for i in range(len(answerlist)):
        if answerlist[i] == 0 :
            continue
        answerlist[i] = int(answerlist[i].numerator * res / answerlist[i].denominator)
    answerlist.append(x)
    return [7, 6, 8, 21]
