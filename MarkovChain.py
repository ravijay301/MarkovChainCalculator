import numpy as np
import copy
import StronglyConnectedComponents as sc
from MarkovChainException import MarkovChainException
import math

"""
Class that stores the most important pieces of information about a Markov Chain. Contains the transitions probability
matrix, as well as lists of the recurrent and transient classes as well as the transient states.
"""
class MarkovChain:

    """
    Constructs MarkovChain with the given transition probability matrix. Computes communications classes, and classification
    of each as either recurrent or transient. Raises MarkovChainException if rows are not valid probability vectors, 
    """
    def __init__(self, tpm: np.ndarray):
        (n, m) = np.shape(tpm)
        if n == 0:
            raise MarkovChainException("No chain detected")
        if n != m:
            raise MarkovChainException("Square matrix required for valid MarkovChain.")
        for row in tpm:
            sum = 0
            for val in row:
                sum += val
            if not math.isclose(1, sum, abs_tol = 1e-9):
                raise MarkovChainException("Invalid chain. Rows not valid probability vectors.")

        self.tpm = tpm
        self.commClasses = self.getCommunicationClasses()
        self.recurrentClasses = self.getRecurrentClasses()
        self.transientClasses = self.getTransientClasses()

    """
    Given the communication classes of the MC obtains the recurrent classes as part of the 
    group of function calls to classify all of the communication classes
    """
    def getRecurrentClasses(self) -> list:
        recurrentClasses = copy.deepcopy(self.commClasses)
        for group in self.commClasses:
            toDel = 0
            for s in group:
                for i, p in enumerate(self.tpm[s]):
                    if p != 0 and group.count(i) == 0:
                        toDel = 1
                        break
                if toDel == 1:
                    recurrentClasses.remove(group)
                    break

        return sorted(recurrentClasses)

    def getTransientClasses(self) -> list:
        transientClasses = copy.deepcopy(self.commClasses)
        for group in self.recurrentClasses:
            transientClasses.remove(group)

        return transientClasses
    """
    Returns a list of all of the transient states in the MC
    """
    def getTransientStates(self) -> list:
        transientStates = []
        for x in self.transientClasses:
            for state in x:
                transientStates.append(state)

        return sorted(transientStates)

    def showClasses(self) -> None:
        print("--------------------\nRecurrent Classes:\n--------------------")
        for i, r in enumerate(self.recurrentClasses):
            print("R", i, ": ", r, sep='')
        print("--------------------\nTransient Classes:\n--------------------")
        for i, t in enumerate(self.transientClasses):
            print("T", i, ": ", t, sep='')

    def getCommunicationClasses(self) -> list:
        return sc.scc(self.tpm)

    """
    If the value of the TPM has been modified, updates the chain's communication classes to fix it
    """
    def updateChain(self) -> None:
        self.commClasses = self.getCommunicationClasses()
        self.recurrentClasses = self.getRecurrentClasses()
        self.transientClasses = self.getTransientClasses()