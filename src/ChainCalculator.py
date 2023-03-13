import numpy as np
from MarkovChain import MarkovChain
from MarkovChainException import MarkovChainException

"""
Given a markovChainSolves for the unique stationary distribution if it is possible, raises a MarkovChainException if
it is not possible (IE chain not being irreducible).
"""
def getStationaryDistribution(markovChain: MarkovChain) -> np.ndarray:
    if len(markovChain.recurrentClasses) != 1 or len(markovChain.transientClasses) > 0:
        raise MarkovChainException("Chain is not irreducible, unique stationary distribution does not exist")     
       
    n = len(markovChain.tpm)
    """
    I can't really explain this code, but it solves for left eigenvector with eigenvalue 1
    where the rowise sum of the eigenvector is 1.
    """
    A = np.append(np.transpose(markovChain.tpm) - np.identity(n), np.full((1, n), 1), axis=0)
    x = np.full(n + 1, 0)
    x[n] = 1
    b = np.transpose(x)
    return np.linalg.solve(np.transpose(A).dot(A), np.transpose(A).dot(b))

"""
Given a Markov Chain and a specified state, turns the state into a recurrent one, returns the new chain, leaving the
original unchanged. Raises MarkovChainException, if  the state is not valid
"""
def makeAbsorbingState(markovChain: MarkovChain, state: int) -> MarkovChain:
    if state < 0 or state >= len(markovChain.tpm):
        raise MarkovChainException("Please provide a valid state")
    newTPM = markovChain.tpm.copy()
    for i, x in enumerate(newTPM[state]):
        if(i == state):
            newTPM[state, i] = 1
        else:
            newTPM[state, i] = 0

    newMC = MarkovChain(newTPM)
    return newMC

"""
Given a MC and Recurrent Class, returns a MarkovChain with just the specified recurrent class. Raises MarkovChainException
if the recurrent class is invalid
"""
def getChainOfRecurrentClass(markovChain: MarkovChain, classNum: int) -> MarkovChain:
    recurrentClasses = markovChain.recurrentClasses
    
    if classNum < 0 or classNum >= len(recurrentClasses):
        raise MarkovChainException("Invalid Recurrent Class")

    recurrentClass = recurrentClasses[classNum]
    sliceOne = []
    for x in recurrentClass:
        sliceOne.append([x])
    return MarkovChain(np.array(markovChain.tpm[sliceOne, recurrentClass]))

def getProbOfAbsorbtionIntoRecurrentClass(markovChain: MarkovChain, classNum: int, initialState: int) -> float:
    formattedMatrix = getFormattedMatrix(markovChain)
    (M, MS) = getHittingTimeMatrices(formattedMatrix)
    return MS[markovChain.getTransientStates().index(initialState), classNum]

def getTimeUntilAbsorbtion(markovChain: MarkovChain, initialState) -> float:
    formattedMatrix = getFormattedMatrix(markovChain)
    (M, MS) = getHittingTimeMatrices(formattedMatrix)
    return sum(M[markovChain.getTransientStates().index(initialState)])

"""
Given a MC, returns modified chain with new TPM with condensed recurrent classes.
"""
def getFormattedMatrix(markovChain: MarkovChain) -> np.ndarray:
    numRecStates = 0
    numAbsorbingStates = len(markovChain.recurrentClasses)
    for x in markovChain.recurrentClasses:      # Sums for the number of recurrent states
        numRecStates += len(x)      

    # Calculates the n x n size of the formatted matrix based on the number of recurrent classes
    n = len(markovChain.tpm) + numAbsorbingStates - numRecStates 
    newProbMatrix = np.zeros((n, n))

    transientStates = markovChain.getTransientStates()
    for j in range(numAbsorbingStates):
        newProbMatrix[j,j] = 1                  # Designates top left corner of matrix to be absorbing classes
        for i, x in enumerate(transientStates):
            transitionProb = 0
            # Sums the probability for transient state to transition to a specific recurrent class 
            for y in markovChain.recurrentClasses[j]:
                transitionProb += markovChain.tpm[x, y]

            # Fills bottom left of matrix with the transient state -> recurrent class probabilities
            newProbMatrix[i + numAbsorbingStates, j] = transitionProb
    
    # Finishes by filling bottom right of matrix transient state -> transient state probabilies
    for i in range(len(transientStates)):
        for j in range(len(transientStates)):
            newProbMatrix[i + numAbsorbingStates, j + numAbsorbingStates] = markovChain.tpm[transientStates[i], transientStates[j]]

    return newProbMatrix

"""
Given a properly formatted matrix, returns M = (I - Q)^(-1) and MS
"""
def getHittingTimeMatrices(formattedMatrix: np.ndarray):
    numAbsStates = 0
    for i in range(len(formattedMatrix)):
        if(formattedMatrix[i, i] == 1):
            numAbsStates += 1
        else:
            break

    Q = formattedMatrix[numAbsStates:, numAbsStates:]
    S = formattedMatrix[numAbsStates:, 0:numAbsStates]
    M = np.linalg.inv((np.eye(len(formattedMatrix) - numAbsStates) - Q))
    return (M, np.matmul(M, S))