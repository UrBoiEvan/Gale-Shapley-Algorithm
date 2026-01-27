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

def stableMatching(hospitals,students):
    #init all hospitals to free
    free_hospitals = list(hospitals.keys())
    print(free_hospitals)
    # TODO implement algorithm
    return

if __name__=="__main__":
    hospitals, students = {}, {}
    hospitals, students = parseFile("example.in")
    print(hospitals)
    print(students)
    stableMatching(hospitals,students)