class Problem:
    def __init__(self,objective,startState):
        self.objective=objective
        self.startState=startState
        self.taboo=[]
        self.candidates=None
    def getNeighbors(self):
        pass
    def getCandidate(self):
        pass
    def updateTaboo(self):
        pass

