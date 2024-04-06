# DiceJack-Learner

DiceJack-Learner is a simulation program that applies reinforcement learning techniques to a dice-based variant of the traditional card game, Blackjack. Utilizing a self-play methodology, this program simulates thousands of games between two automated players, refining their strategies over time based on the outcomes of each game. The objective is to explore how machine learning principles can be applied to simple games of chance and strategy.

## Overview

In this simulated environment, two players alternately roll dice, aiming to reach a score within a specified target range without exceeding it. The game is designed to test and improve decision-making algorithms, with the focus on dynamically adjusting the number of dice rolled based on the current state of play. Through continuous play, the algorithm seeks to identify optimal strategies for any given situation, enhancing its play quality as it learns from each game's outcome.

## Gameplay Rules

- **Objective**: Players compete to reach a total score within a defined target range.
- **Turns**: Players take turns rolling a specified number of dice, accumulating their total score across turns.
- **Winning Condition**: A player wins by achieving a total score within the target range (inclusive of both lower and upper bounds).
- **Losing Condition**: Exceeding the upper target score results in an immediate loss.
- **Strategic Decision**: Players decide the number of dice to roll each turn, from one up to a maximum limit, to strategically influence their total score.

## Running the Simulation

The game simulation is highly customizable through five key parameters:

- `NSides`: Number of sides on each die.
- `LTarget`: The lowest score within the winning range.
- `UTarget`: The highest score within the winning range, beyond which a player loses.
- `NDice`: The maximum number of dice a player is allowed to roll in a single turn.
- `NGames`: The total number of games to be played in the simulation.

### Command Line Execution

To execute the simulation, use the following command:

```
python DiceJack.py --NSides 6 --LTarget 15 --UTarget 17 --NDice 2 --NGames 10000
```

## Simulation Output

Upon completion, the program outputs two matrices based on the `LTarget` dimension:

- **Optimal Dice Matrix**: Indicates the optimal number of dice to roll in any state ⟨X,Y⟩, where X is the current player's score and Y is the opponent's score.
- **Winning Probability Matrix**: Provides the estimated probability of winning if the optimal number of dice is rolled in state ⟨X,Y⟩.

These outputs offer valuable insights into strategic decision-making and the dynamics of risk and reward in game play.

