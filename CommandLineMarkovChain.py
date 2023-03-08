import pandas as pd
import numpy as np
import ChainCalculator as cc
from MarkovChain import MarkovChain
from MarkovChainException import MarkovChainException
import sys

def main():
    global baseTPM, modifiedChain
    np.set_printoptions(precision = 3)
    tpmPanda = pd.read_excel(sys.argv[1], header = None)
    baseTPM = np.array(tpmPanda)
    modTPM = baseTPM.copy()
    try: 
        modifiedChain = MarkovChain(modTPM)
        menu()
    except MarkovChainException as e:
        print(e.message)

def menu():
    global modifiedChain
    while(True):
        print("\nTPM = \n", modifiedChain.tpm, sep = '', end = " ")
        print("\nWelcome to a basic finite state space MC calculator, what would you like to know about this TPM?")
        print(" 1) Solve For Unique Stationary Distribution")
        print(" 2) Show Communication Classes")
        print(" 3) Make States Absorbing")
        print(" 4) Show Hitting Time Matrices")
        print(" 5) Condense Recurrent Classes")
        print(" 6) Switch to Recurrent Chain")
        print(" 7) Return to Base Chain")
        print(" 8) Exit")
        numChoice = getInputRange(1, 8)
        if numChoice == 1:
            solveUniqueStationary()
        elif numChoice == 2:
            showClasses()
        elif numChoice == 3:
            while(True):                #Idea is that usually you want to make more than one class absorbing
                makeAbsorbingState()
                yn = input("Would you like to make another state absorbing? (y/n) ")
                if yn.lower() == "y":
                    continue
                else:
                    break
        elif numChoice == 4:
            showHittingTimeMatrices()
        elif numChoice == 5:
            condenseRecurrent()
        elif numChoice == 6:
            switchToRecurrentClass()
        elif numChoice == 7:
            resetChain()
        elif numChoice == 8:
            break
    
"""
Given an input range of int, will prompt CLI for input, and only will accept
the numbers in the range. Raises attribute error if start > end
"""
def getInputRange(start: int, end: int) -> int:
    if end < start:
        raise AttributeError
    while(True):
        try: 
            numChoice = int(input("Enter num 1-6 to indicate choice: "))
            if numChoice < start or numChoice > end:
                raise ValueError
            else:
                break

        except ValueError:
            print("Please enter a valid input")
    return numChoice

def solveUniqueStationary() -> None:
    global modifiedChain
    try:
        piBar = cc.getStationaryDistribution(modifiedChain)
        print("PIBAR =", piBar)
    except MarkovChainException as e:
        print(e.message)

def showClasses() -> None:
    global modifiedChain
    print("--------------------\nRecurrent Classes:\n--------------------")
    for i, r in enumerate(modifiedChain.recurrentClasses):
        print("R", i, ": ", r, sep='')

    print("--------------------\nTransient Classes:\n--------------------")
    if len(modifiedChain.transientClasses) == 0:
        print("No Transient Classes")

    for i, t in enumerate(modifiedChain.transientClasses):
        print("T", i, ": ", t, sep='')

def makeAbsorbingState():
    global modifiedChain
    while(True):
        try:
            toAbsorb = int(input("Which state would you like to make absorbing? "))
            modifiedChain = cc.makeAbsorbingState(modifiedChain, toAbsorb)
            break
        except MarkovChainException as e:
            print(e.message)
        except ValueError:
            print("Please provide a valid input")
        
    print("New TPM =\n", modifiedChain.tpm, sep = '')  

"""
Resets chain back to original input (from excel or csv)
"""
def resetChain():
    global modifiedChain, baseTPM
    tpm = baseTPM.copy()
    modifiedChain = MarkovChain(tpm)

def showHittingTimeMatrices() -> None:
    global modifiedChain
    formattedMatrix = cc.getFormattedMatrix(modifiedChain)          # Obtains formatted matrix
    (M, MS) = cc.getHittingTimeMatrices(formattedMatrix, 0)         # Obtains M and MS Matrices from formatted matrix
    print("Formatted Matrix =\n", formattedMatrix, sep = '')
    print("M =\n", M, sep = '')
    print("MS =\n", MS, sep = '')
    
    printRecurrentClasses()

    print("Transient States: ")                                     #Prints Transient States
    transientStates = modifiedChain.getTransientStates()
    for i, x in enumerate(transientStates):
        if i < len(transientStates) - 1:
            print("T", i, ": ", x, sep = '', end = ", ")
        else:
            print("T", i, ": ", x, sep = '')

    yn = input("Would you like to know how to interperet these matrices? (y/n) ") #Prompts user if they want additional information
    if yn.lower() == "y":
        print("M[i, j] represents the expected number of visits to transient state j, given starting in transient state i")
        print("MS[i, j] represents the probability of being absorbed into recurrent class j, given that you started in transient state i")
        print("Additionally you can find the expected time until absorbtion given starting in transient state i, by performing the row sum M[i]")

"""
Condenses recurrent classes and formats matrix, and returns to main menu to continue for additional calculations to be performed
"""
def condenseRecurrent():
    global modifiedChain
    print("Now condensing recurrent classes into absorbing states and formatting matrix")
    formattedMatrix = cc.getFormattedMatrix(modifiedChain)
    print("Formatted Matrix =\n", formattedMatrix, sep = '')

    printRecurrentClasses()

    transientStates = modifiedChain.getTransientStates()
    for i, x in enumerate(transientStates):
        if i < len(transientStates) - 1:
            print("T", i, ": ", x, sep = '', end = ", ")
        else:
            print("T", i, ": ", x, sep = '')
    
    modifiedChain = MarkovChain(formattedMatrix)            # Changed modified chain to the new formatted matrix

#Prints the recurrent classes of the Modified Chain
def printRecurrentClasses():
    global modifiedChain
    print("Recurrent Classes: ")  
    for i, x in enumerate(modifiedChain.recurrentClasses):
        if i < len(modifiedChain.recurrentClasses) - 1:
            print("R", i, ": ", x, sep = '', end = ", ")
        else:
            print("R", i, ": ", x, sep = '')

def switchToRecurrentClass():
    global modifiedChain
    printRecurrentClasses()
    while(True):
        try:
            recClass = int(input("Which recurrent class would you like to switch to? "))
            modifiedChain = cc.getChainOfRecurrentClass(modifiedChain, recClass)
            break
        # except ValueError:
        #     print("Please provide a valid input")
        except MarkovChainException as e:
            print(e.message)