# Connect 4 game AI

## Objective:

- Make a Connect 4 game in python from scratch. 
- Build an AI made out of min-max algorithms
- Build an AI made out of Reinforcement Machine Learning neural networks
- Make both AI play to determine which algorithm is stronger

## Current state:

☑️ Game done  
☑️ Min-max AI done  
⬛   ML AI done  
⬛   Competition done

## Improvements:

- Alpha-Beta pruning: Upgraded min-max algorithm with alpha-beta pruning to 'prune' branches that are can not be
stronger that the already analyzed ones.  
 This feature avoid analyzing bad positions and improves time spent by the algorithm when search depth is large.  


- Rearranged search in order to maximize Alpha-Beta pruning (center values are known to be stronger, so is good have 
them analyzed first by the algorithm).


- Added 'Dynamic Depth' feature: It adapts the search depth to always last more o less the same amount. This allows the 
algorithm to continuously increase depth as long as the board's complexity is reduced.