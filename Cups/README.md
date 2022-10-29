## Problem: We have two containers of capacity m liters and n liters respectively and an unlimited amount of water. Determine a sequence of filling the containers and pouring from one container into the other (until it is full) or on the ground, so that k liters remain in one of the containers. We have no other method of measuring a quantity of water.

Requirements:

(0.2) Choose a representation of a state of the problem. The representation must be explicit enough to contain all the necessary information to continue finding a solution, but it must also be formalized enough to be easy to process/store.

(0.2) Identify the special states (initial and final) and implement the initialization function (gets as parameters the instance m, n and k, returns the initial state) and the boolean function that checks whether a state received as a parameter is final.

(0.2) Implement transitions as functions that get as parameters a state (and additional ones, if needed)  and return the state resulting from applying the transition. Validation of transitions is done in one or more boolean functions with the same parameters.

(0.2) Implement the Backtracking strategy.

(0.2) Implement the BFS strategy.

(0.2) Implement the Hillclimbing strategy.

(0.2) Implement strategy A*

(0.2) Implement a menu that allows, after entering the instance, to select the strategy to be tried.
(Bonus: 0.1) Implement a boolean function that checks for an instance received as parameter whether or not we can find a solution.
