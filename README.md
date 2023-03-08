# CLI Finite State Space Time Homogenous Markov Chain Calculator
(Wow what an *amazing* name right? Totally not extremely niche)

Do you for some reason really need a fast way to do computations on finite state space time homogenous Markov Chains for an open laptop exam that is coming up?

Well this is certainly the python script for you!

## Features
* Solve Unique Stationary Distribution for irreducible Markov Chains
* Obtain recurrent and transient classes from an arbitrary Markov Chain
* Turn specified chains in a given Markov Chain into absorbing states
* Computes hitting time matrices (M and MS), and provides interperetation for those matrices
* Computes formatted matrix [[I 0],[S, Q]] for arbitrary Markov Chains
* Extract recurrent classes from reducbile Markov Chains

## Dependencies
* Python 3.10.10
* numpy 1.24.2
* pandas 1.5.3 
* (You know when you see this that there was no chance I was using an actual build tool, your milage may vary)

# Setting Up
* Ensure that the above dependencies are installed. The listed versions will work, but newer update should still be supported
* Clone the repository using running `git clone https://github.com/ravijay301/MarkovChainCalculator.git`
* Enter the directory `cd MarkovChainCalculator`
* Run `python ./src/Main.py <PATH TO EXCEL FILE>` and perform whatever computations you want!

# Example Usecase
I provided a few simple examples of valid markov chains in the Test Matrices Folder: (TPM1.xlsx, TPM2.xlsx, TPM3.xlsx, MultiRecClasses.xlsx). 

We can go through a simple example use using MultiRecCLasses.xlsx to show the capabilities of the program

* We can intialize the calculator by running `python ./src/Main.py '.\Test Matrices\MultiRecClasses.xlsx'`

![Calculator Initialization](https://github.com/ravijay301/MarkovChainCalculator/blob/71e3b93be88438d70e951017041a3d5511f76650/assets/Initializaiton.png?raw=true)

* Perhaps we want to see the communication classes so we type `2` and press enter to indicate our choice

![Displaying Recurrent and Transient Classes](https://github.com/ravijay301/MarkovChainCalculator/blob/71e3b93be88438d70e951017041a3d5511f76650/assets/DisplayingClasses.png?raw=true)

* We see that there are two different recurrent classes *R0* and *R1*. If we want to investigate *R0* more closely we can indicate that py pressing `6` then enter, followed by `0` and enter to indicate we want to switch to *R0*

![Switching to Recurrent Subchain](https://github.com/ravijay301/MarkovChainCalculator/blob/71e3b93be88438d70e951017041a3d5511f76650/assets/SwitchingToRecurrent.png?raw=true)

* Perhaps we now want to see the long run expected proportion of time we spend in either state, so we indicate we want to solve for the unique stationary distribution by pressing `1` and enter

![Solving For Unique Stationary](https://github.com/ravijay301/MarkovChainCalculator/blob/71e3b93be88438d70e951017041a3d5511f76650/assets/SolvingStationary.png?raw=true)


# About
* When I was told I could use my laptop on my stochastic processes exam, I simply had to find a way to automate my math. I then proceeded to spend way more time building this when I could have just studied for way less time (I couldn't even finish it before the exam)
* On the bright side, I finished it, and if anyone else is put in this exact specific situation that I was, they have a prebuilt solution (I still got this for the final too)
p
# Future Additions (Potential)
* Could add better labeling for the states and different classes in the matrices, instead of making the user do it, probably through the use of a simply gui, though it may end up becoming an information dump
* Could also make my strongly connected components algorithm more readable because I wrote it based on sudocode from my algorithm notes, that were transcribed from my professors slide 6 months ago from one class where I was half-asleep while doing no additional algorithm research when writing my algorithm. Yeah that's not happening