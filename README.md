# Connect 4 game AI

## Objectives:

- [X] Make a Connect 4 game in python from scratch. 
- [X] Build an AI made out of min-max algorithms
- [X] Build an AI made out of NEAT algorithm
- [ ] Build an AI made out of Reinforcement Machine Learning neural networks
- [ ] Make the AIs play to determine which algorithm is stronger


## Improvements and journey:

### Min-Max algorithm:

- Alpha-Beta pruning: Upgraded min-max algorithm with alpha-beta pruning to 'prune' branches that are can not be
stronger that the already analyzed ones.  
 This feature avoid analyzing bad positions and improves time spent by the algorithm when search depth is large.  


- Rearranged search in order to maximize Alpha-Beta pruning (center values are known to be stronger, so is good have 
them analyzed first by the algorithm).


- Added 'Dynamic Depth' feature: It adapts the search depth to always last more o less the same amount. This allows the 
algorithm to continuously increase depth as long as the board's complexity is reduced.

### NEAT algorithm:

- Added NEAT algorithm to the game, which is a genetic algorithm that evolves neural networks to play the game.


- Implemented a tournament system to evaluate each generation and select the best performers to seed the next generation.


- Find out major problems:
  - Generations are not evolving, they are just repeating the same moves, which in most of the cases is just play a single line until winning/losing or until the line is full
  - Fitness design: The current fitness primarily ranks individuals within the current generation and does not reflect progress across generations. Introducing an Elo system and/or a “hall of fame” to evaluate against champions from previous generations could provide a more stable, comparative signal.
  - Insufficient network complexity: Final networks are too simple to capture the board patterns required for strong play.


- Conclusion: Pausing NEAT work here and proceeding to the next goal.