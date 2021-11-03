class Problem:
    def __init__(self,objective,startState):
        self.objective=objective
        self.startState=startState
        self.frequencies=[]
    def getNeighbors(self,state):
        neighbors=[]
        for i in range(len(state[2])):
            for j in range(i+1,len(state[2])):
                copyState = state[2][:]
                copyState[i],copyState[j] = state[2][j],state[2][i]
                move=None
                if(copyState[i]>copyState[j]):
                    move=(copyState[j],copyState[i])
                else:
                    move=(copyState[i],copyState[j])
                total=0
                
                count = [1 for i in range(len(self.frequencies)) if copyState == self.frequencies[i][2]]
                total = sum(count)    
                value = self.objective((move,0,copyState),total)
                neighbors.append((move,value,copyState))
        return neighbors
    def getInitialState(self):
        return self.startState
    def getAspiration(self,state):
        return self.objective(state)

def objective(state,penalty=0):
    actual = state[2]
    global V, W
    s = [(actual[i], actual[i+1]) for i in range(len(actual)-1)]
    f=0
    for i,j in s:
        f+=W[(i,j)]*(V[i]-V[j])
    return f-penalty




def tabuSearch(problem,holding):
    aspiration = problem.getAspiration(problem.getInitialState())
    tabuList=[]
    actual = problem.getInitialState()
    bestSolution=(actual,aspiration)
    it=1000
    i=0
    while(i<it):
        neighbors = problem.getNeighbors(actual)
        candidate = findBestNeighbor(neighbors)
        isInTabu= isCandidateInTabu(candidate,tabuList)
        while isInTabu:
            if(problem.getAspiration(candidate)<=bestSolution[1]):
                neighbors.remove(candidate)
                candidate = findBestNeighbor(neighbors)
                isInTabu= isCandidateInTabu(candidate,tabuList)
        actual=candidate
        aspiration=problem.getAspiration(candidate)
        tabuList=updateTabuList(tabuList,candidate,holding)
        problem.frequencies.append(candidate)
        if(aspiration>bestSolution[1]):
            bestSolution=(actual,aspiration)
            print(bestSolution)
        i+=1   
    return bestSolution
def findBestNeighbor(neighbors):
    bestNeighbor=neighbors[0]
    for neighbor in neighbors:
        if(neighbor[1]>bestNeighbor[1]):
            bestNeighbor=neighbor
    return bestNeighbor

def isCandidateInTabu(candidate,tabuList):
    for el in tabuList:
        if(el[0][0]==candidate[0]):
            return True
    return False

def updateTabuList(tabuList,candidate,holding):
    copyTabuList=tabuList[:]
    for el in copyTabuList:
        el[1]-=1
        if(el[1]==0):
            copyTabuList.remove(el)
    copyTabuList.append([candidate,holding])
    return copyTabuList
W={}
V={}
def run():
    global V,W
    f = open("C:/Users/santi/Documents/Universidad/Semestre VIII/Inteligencia Artificial/Corte 3/Tabu-Search/data.txt", "r")
    lines = f.readlines()
    
    i=0
    for line in lines:
        j=0
        weights = line.split()
        for weight in weights:
            W[(i,j)]=int(weight)
            j+=1
        i+=1
    V={0:3,1: 1,2: 4,3:3,4:9,5:1,6:5}
    s0=[i for i in range(7)]
    problem = Problem(objective,([],objective(([],0,s0)),s0))
    solution=tabuSearch(problem,3)
    print(solution)

if __name__ == "__main__":
    run()