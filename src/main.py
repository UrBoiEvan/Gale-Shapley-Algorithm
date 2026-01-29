from collections import defaultdict
import sys


# Helper function to open input files
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


# Task A
def stableMatching(hospital_ranks,student_ranks):
    # init all hospitals to free
    free_hospitals = list(hospital_ranks.keys())
    proposal_idx = defaultdict(int) # track which student a particular hospital is iterating with the list
    student_assignments = {} # {Student: Hospital}

    while len(free_hospitals) > 0:
        h = free_hospitals[0] # choose front of queue
        if proposal_idx[h] >= len(hospital_ranks[h]):   # If hospital exhausted its list, remove it
            free_hospitals.pop(0)
            continue

        a = hospital_ranks[h][proposal_idx[h]] # student next for proposal
        proposal_idx[h] += 1  # advance proposal pointer

        if a not in student_assignments:    # student is free
            student_assignments[a] = h
            free_hospitals.pop(0)
        else:
            h_old = student_assignments[a]
            if student_ranks[a].index(h) < student_ranks[a].index(h_old):   # else: student rejects h next i, hospital stays free
                student_assignments[a] = h
                free_hospitals.pop(0)
                free_hospitals.append(h_old)

    return {h: a for a, h in student_assignments.items()} # flip to {Hospital: Student}


# Task B: three helper functions, verify_matching is the one to be called
def check_validity(matching, hospital_ranks, student_ranks):
    # First, it's clear something is wrong if we don't have correct # of matches
    n = len(hospital_ranks)
    if len(matching) != n:
        return False, "Incorrect # of matches"

    # Can't have weird id's not in sets, can't appear in a match more than once
    matched_students = set()
    for h, s in matching.items():
        if h not in hospital_ranks:
            return False, f"Bad hospital ID {h}"
        if s not in student_ranks:
            return False, f"Bad student ID {s}"
        if s in matched_students:
            return False, f"{s} matched more than once"
        matched_students.add(s)

    # Last, can't not appear in a match
    if len(matched_students) != n:
        return False, "There exist unmatched students"

    return True, None

def check_stability(matching, hospital_ranks, student_ranks):
    # TODO: stability
    # Search for blocking pairs where hospital h prefers student s over its current match and student s prefers hospital h over its current match

def verify_matching(matching, hospital_ranks, student_ranks):
    # Check validity
    valid, reason = check_validity(matching, hospital_ranks, student_ranks)
    if not valid:
        print(f"INVALID: ({reason})")
        return

    # Check stability
    stable, blocking_pair = check_stability(matching, hospital_ranks, student_ranks)
    if not stable:
        h, s = blocking_pair
        print(f"UNSTABLE: (blocking pair: hospital {h}, student {s})")
        return

    print("VALID & STABLE")


def main():
    if len(sys.argv) != 2:
        print('Incorrect args, use: "python matcher.py <input_file>"')
        sys.exit(1)

    input_file = sys.argv[1]
    hospital_ranks, student_ranks = parseFile(input_file)

    # Task A
    res = stableMatching(hospital_ranks, student_ranks)
    for h in sorted(res): print(h, res[h])

    # Task B


    #TODO time complexity

if __name__=="__main__":
    main()
