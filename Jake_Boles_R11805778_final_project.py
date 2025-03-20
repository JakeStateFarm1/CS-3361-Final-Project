#Jake_Boles
#Reads through a user provided file, runs 100 rounds of a cellular life simulator with a user provided number of processes, then outputs to a user provided file.
#Jake Boles R11805778
#12/2/24
#Version 1.00
#-i required- The path to your input file
#-o required- The path to your output file
#-p- The number of processes you would like to run, if no number is provided, runs with a default of 1 processes
import argparse
import os #used to check if file paths exist
import multiprocessing #used for multiprocessing
import time #used to calculate run time

# Initialize the dictionaries to switch the matrix values and the sets for checking if numbers are prime or a power of 2
twodmatrix = []
switcher = {"O": 2, "o": 1, ".": 0, "x": -1, "X": -2}
switcher2 = {2: "O", 1: "o", 0: ".", -1: "x", -2: "X"}
primes = {2, 3, 5, 7, 11, 13}
power2 = {1, 2, 4, 8, 16}

# Initialize global row and column variables
rows = 0
columns = 0
#reads in the matrix and converts the text into number values
def matrixMaker():
    global rows, columns
    with open(args.i, "r") as i:
        matrix = i.read()

    tempmatrix = []
    for x in matrix:
        if x == "\n":
            twodmatrix.append(tempmatrix)
            tempmatrix = []
            continue
        tempmatrix.append(switcher[x])
    if tempmatrix:
        twodmatrix.append(tempmatrix)
    rows = len(twodmatrix)
    columns = len(twodmatrix[0])
#calculates all the neighbor values for a single row of the matrix
def calcNeighborRow(inputs):
    rows_above_and_below, columns = inputs
    row_result = [0] * columns

    above, current, below = rows_above_and_below
    for c in range(columns):
        nval=0
        nval += current[c - 1] if c - 1 >= 0 else 0
        nval += current[c + 1] if c + 1 < columns else 0
        if above: #checks if a row above the current value exists
            nval += above[c] + (above[c - 1] if c - 1 >= 0 else 0) + (above[c + 1] if c + 1 < columns else 0)
        if below: #checks if a row below the current value exists
            nval += below[c] + (below[c - 1] if c - 1 >= 0 else 0) + (below[c + 1] if c + 1 < columns else 0)
        row_result[c] = nval
    return row_result
#runs instances of calcneigborrow in parallel, then merges them together to create a matrix storing all the neighbor values
def calcNeighborVals():
    inputs = []
    for r in range(rows): #creates the inputs for each instance of calcNeighborRow
        above = twodmatrix[r - 1] if r > 0 else []
        current = twodmatrix[r]
        below = twodmatrix[r + 1] if r + 1 < rows else []
        inputs.append(((above, current, below), columns))
    with multiprocessing.Pool(processes=args.p) as pool: #runs args.p processes
        neighbor_matrix = pool.map(calcNeighborRow, inputs)
    return neighbor_matrix
#processes a single row of the matrix
def processRow(inputs):
    currentrow, neighborrow, columns = inputs
    temprow = [0] * columns #creates an empty row
    for colCount, y in enumerate(currentrow):
        nval = neighborrow[colCount]
        match y:
            case 2: #case O
                if nval in power2:
                    temprow[colCount] = 0
                elif nval < 10:
                    temprow[colCount] = 1
                else:
                    temprow[colCount] = 2
            case 1: #case o
                if nval <= 0:
                    temprow[colCount] = 0
                elif nval >= 8:
                    temprow[colCount] = 2
                else:
                    temprow[colCount] = 1
            case 0: #case .
                if nval in primes:
                    temprow[colCount] = 1
                elif (abs(nval)) in primes:
                    temprow[colCount] = -1
                else:
                    temprow[colCount] = 0
            case -1: #case x
                if nval >= 1:
                    temprow[colCount] = 0
                elif nval <= -8:
                    temprow[colCount] = -2
                else:
                    temprow[colCount] = -1
            case -2: #case X
                if (abs(nval)) in power2:
                    temprow[colCount] = 0
                elif nval > -10:
                    temprow[colCount] = -1
                else:
                    temprow[colCount] = -2
            case _: #fall through case if some weird error happens
                temprow[colCount]=y
    return temprow
#runs instances of processRow in parallel, then merges them together to create the next step for the matrix
def nextStep():
    global twodmatrix 
    neighbor_matrix = calcNeighborVals() #calculates the new neighbor value matrix
    inputs = [(twodmatrix[r], neighbor_matrix[r], columns) for r in range(rows)] #prepares the inputs for each iteration row of the twodmatrix
    next_matrix = []
    with multiprocessing.Pool(processes=args.p) as pool: #runs processRow with args.p processes
        result = pool.map(processRow, inputs)
    next_matrix = result
    twodmatrix = next_matrix
def output(): #Converts the numbers back into text for output
    """Write the output matrix to a file."""
    with open(args.o, "w+") as o:
        for x in twodmatrix:
            for y in x:
                o.write(switcher2[y])
            o.write("\n")

if __name__ == "__main__": #ensures each process doesn't try to rerun the main function
    parser = argparse.ArgumentParser() 
    parser.add_argument('-i', required=True, type=str, help='input file path') #reads in the user console inputs
    parser.add_argument('-o', required=True, type=str, help='output file path')
    parser.add_argument('-p', type=int, help='number of processes', default=1)
    args = parser.parse_args()

    if os.path.exists(args.i): #checks that the input file exists
        if args.p > 0: #checks that processes is greater then 0
            start_time = time.time()  # Record the start time
            matrixMaker()
            print("Project :: R11805778")
            print("You are running", args.p, "processes")
            for _ in range(100): #Updates the matrix 100 times
                nextStep()
            print("Finished")
            output()
            end_time = time.time()
            print("Elapsed time:", end_time - start_time)
        else:
            print("Args must be greater than 0.")
    else:
        print("Input not found")