import numpy as np

class graphNode:
    def __init__(self, val):
        self.path = -1
        self.color = 0
        self.f = 0
        self.d = 0
        self.val = val

nodesByFinishTime = []
"""
Performs a SCC algorithm on the given adjacency matrix as input
Returns list of list, each being vertexes of strongly connected components
"""
def scc(G: np.ndarray) -> list:
    global nodesByFinishTime
    nodesByFinishTime = []
    nodeInfo = DFS(G)

    nodesByFinishTime = sorted(nodeInfo, key=lambda x: x.f, reverse=True)
    Gtrans = np.transpose(G)
    
    for u in nodesByFinishTime:
        u.color = 0

    indexMap: dict[int, int] = {}
    for i, u in enumerate(nodesByFinishTime):
        indexMap[u.val] = i

    components = []
    for u in nodesByFinishTime:
        if u.color == 0:
            component = [u.val]
            DFSVisitMapped(Gtrans, u.val, indexMap, component)
            components.append(sorted(component))

    return components

"""
Recursive DFS algorithm, but performs search based on a specified compon
"""
def DFSVisitMapped(G: np.ndarray, u, iMap, component: list):
    global nodesByFinishTime
    nodesByFinishTime[iMap.get(u)].color = 1
    for v, x in enumerate(G[u]):
        if x > 0 and nodesByFinishTime[iMap.get(v)].color == 0:
            component.append(v)
            DFSVisitMapped(G, v, iMap, component)

nodeInfo = []
time: int = 0
"""
Standard recursive DFS to compute finish times
"""
def DFS(G: np.ndarray) -> list:
    global time, nodeInfo
    time = 0
    nodeInfo = []
    for u, x in enumerate(G):
        nodeInfo.append(graphNode(u))
    time = 0
    for u, x in enumerate(G):
        if nodeInfo[u].color == 0:
            DFSVisit(G, u)

    return nodeInfo

def DFSVisit(G: np.ndarray, u: int) -> None:
    global time, nodeInfo
    time += 1
    nodeInfo[u].d = time
    nodeInfo[u].color = 1
    for v, x in enumerate(G[u]):
        if x > 0 and nodeInfo[v].color == 0:
            nodeInfo[v].path = u
            DFSVisit(G, v)
    time += 1
    nodeInfo[u].f = time
    return