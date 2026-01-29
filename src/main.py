from collections import defaultdict
def parseFile(file):
    targetFile = open(file,"r")
    line = targetFile.readline()
    n = int(line.strip())
    hospital_ranks, student_ranks = {}, {}
    i = 1
    while line and i <= 2*n:
        line = targetFile.readline().split()
        line = [int(char) for char in line]
        if i < n+1:
            hospital_ranks[i] = line
        else:
            student_ranks[i-n] = line
        i += 1
    targetFile.close()
    return hospital_ranks, student_ranks

def stableMatching(hospital_ranks,student_ranks):
    # init all hospitals to free
    free_hospitals = list(hospital_ranks.keys())
    proposal_idx = defaultdict(int) # track which student a particular hospital is iterating with the list
    student_assignments = {} # {Student: Hospital}
    while len(free_hospitals) > 0:
        h = free_hospitals[0] # choose front of queue
        a = hospital_ranks[h][proposal_idx[h]] # student next for proposal
        if a not in student_assignments: # student is free
            student_assignments[a] = h
            free_hospitals.pop(0)
        elif student_ranks[a].index(h) < student_ranks[a].index(student_assignments[a]): # student may trade up
            # dump current match
            h_old = student_assignments[a]
            free_hospitals.append(student_assignments[a])
            proposal_idx[h_old] += 1 # move old hospital proposal to the next entry
            # new hospital
            student_assignments[a] = h
            free_hospitals.pop(0)
        else: # a rejects h, increment h proposal for next student
            proposal_idx[h] += 1
    return {h: a for a, h in student_assignments.items()} # flip to {Hospital: Student}

def main():
    hospital_ranks, student_ranks = parseFile("example.in")
    res = stableMatching(hospital_ranks, student_ranks)
    print("Hospital Match: ",res)
    #TODO verify stable match

if __name__=="__main__":
    main()