from collections import defaultdict
import sys
import time
import random


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
    # Basically, we map it in reverse so it's student: hospital
    student_to_hospital = {s: h for h, s in matching.items()}
    for h in hospital_ranks:
        current_student = matching[h]
        for s in hospital_ranks[h]:
            if s == current_student:
                break

            # Check if student prefers h over current match
            hh = student_to_hospital[s]
            if student_ranks[s].index(h) < student_ranks[s].index(hh):
                return False, (h, s)

    return True, None

def verify_matching(matching, hospital_ranks, student_ranks, verbose=True):
    # Check validity
    valid, reason = check_validity(matching, hospital_ranks, student_ranks)
    if not valid:
        if verbose:
            print(f"INVALID: ({reason})")
        return False

    # Check stability
    stable, blocking_pair = check_stability(matching, hospital_ranks, student_ranks)
    if not stable:
        if verbose:
            h, s = blocking_pair
            print(f"UNSTABLE: (blocking pair: hospital {h}, student {s})")
        return False

    if verbose:
        print("VALID STABLE")

    return True



# Task C
# Generates random preference lists for n hospitals and n students.
def generate_random_preferences(n):
    hospital_ranks = {}
    for h in range(1, n + 1):
        temp = list(range(1, n + 1))
        random.shuffle(temp)
        hospital_ranks[h] = temp

    student_ranks = {}
    for s in range(1, n + 1):
        temp = list(range(1, n + 1))
        random.shuffle(temp)
        student_ranks[s] = temp

    return hospital_ranks, student_ranks

def task_c():
    print("n, match_time_sec, verify_time_sec")

    sizes = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
    for n in sizes:
        hospital_ranks, student_ranks = generate_random_preferences(n)

        # Matching
        start_match = time.time()
        matching = stableMatching(hospital_ranks, student_ranks)
        end_match = time.time()

        # Verification
        start_verify = time.time()
        verify_matching(matching, hospital_ranks, student_ranks, verbose=False)
        end_verify = time.time()

        # Output
        match_time = end_match - start_match
        verify_time = end_verify - start_verify
        print(f"{n}, {match_time:.6f}, {verify_time:.6f}")


def main():
    args = sys.argv[1:]

    # Task C first because we don't need to parse file
    if args == ["--C"]:
        task_c()
        return

    # Output if wrong input
    if len(args) < 1 or len(args) > 2:
        print("Usage:")
        print("  python main.py <input_file>        (Tasks A + B + C)")
        print("  python main.py <input_file> --A    (Task A only)")
        print("  python main.py <input_file> --B    (Task B only)")
        print("  python main.py --C                 (Task C only)")
        sys.exit(1)

    # Set up vars
    input_file = args[0]
    flag = args[1] if len(args) == 2 else None
    hospital_ranks, student_ranks = parseFile(input_file)
    matching = stableMatching(hospital_ranks, student_ranks)

    # Task A only
    if flag == "--A":
        for h in sorted(matching):
            print(h, matching[h])
        return

    # Task B only
    if flag == "--B":
        verify_matching(matching, hospital_ranks, student_ranks)
        return

    # Default: Task A + B + C
    print("TASK A:")
    for h in sorted(matching):
        print(h, matching[h])
    print("\nTASK B:")
    verify_matching(matching, hospital_ranks, student_ranks)
    print("\nTASK C:")
    task_c()

if __name__=="__main__":
    main()
