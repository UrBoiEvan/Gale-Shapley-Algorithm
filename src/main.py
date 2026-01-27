def parseFile(file):
    targetFile = open(file,"r")
    line = targetFile.readline()
    n = int(line.strip())
    hospital_ranks, student_ranks = {}, {}
    i = 0
    while line and i < 2*n:
        line = targetFile.readline().split()
        if i < n:
            hospital_ranks[i] = list(line)
        else:
            student_ranks[i-n] = list(line)
        i += 1
    targetFile.close()
    return hospital_ranks, student_ranks

def stableMatching(hospital_ranks,student_ranks):
    # init all hospitals to free
    free_hospitals = list(hospitals.keys())
    print(free_hospitals)
    # TODO implement algorithm
    return

if __name__=="__main__":
    hospital_ranks, student_ranks = parseFile("example.in")
    print(hospital_ranks)
    print(student_ranks)
    stableMatching(hospital_ranks,student_ranks)