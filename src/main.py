from collections import defaultdict
import sys


def parseFile(file):
    with open(file, "r") as f:
        line = f.readline()
        if not line:
            raise ValueError("Empty input file")

        n = int(line.strip())
        hospital_ranks = {}
        student_ranks = {}

        for i in range(1, n + 1):
            prefs = list(map(int, f.readline().split()))
            hospital_ranks[i] = prefs
        for i in range(1, n + 1):
            prefs = list(map(int, f.readline().split()))
            student_ranks[i] = prefs

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
    if len(sys.argv) != 2:
        print("Usage: python matcher.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    hospital_ranks, student_ranks = parseFile(input_file)
    res = stableMatching(hospital_ranks, student_ranks)
    for h in sorted(res): print(h, res[h])

    #TODO verify stable match
    #TODO time complexity

if __name__=="__main__":
    main()
