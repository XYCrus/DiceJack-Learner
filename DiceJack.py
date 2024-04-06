#%%
import numpy as np
import random
import argparse

parser = argparse.ArgumentParser(description = "Dice Blackjack Simulation with Reinforcement Learning")

parser.add_argument('--NSides', 
                    type = int, 
                    default = 6, 
                    help = "Number of sides on each die.")

parser.add_argument('--LTarget', 
                    type = int, 
                    default = 15, 
                    help = "The lower target value players aim to reach or exceed.")

parser.add_argument('--UTarget', 
                    type = int, 
                    default = 17, 
                    help = "The upper target value players must not exceed.")

parser.add_argument('--NDice', 
                    type = int, 
                    default = 2, 
                    help = "The maximum number of dice a player can roll in a turn.")

parser.add_argument('--NGames', 
                    type = int, 
                    default = 10000, 
                    help = "The number of games to simulate.")

args = parser.parse_args()



#%%
# Simulates NGames of dice Blackjack, returning win/loss counts
def PlayNGames(NSides, LTarget, UTarget, NDice, NGames):
    # Initialize Count Matrices
    WinCount = np.zeros((LTarget, LTarget, NDice + 1))
    LoseCount = np.zeros((LTarget, LTarget, NDice + 1))

    # Call Gameplay Function iteratively
    for _ in range(NGames):
        PlayGame(NSides, LTarget, UTarget, NDice, WinCount, LoseCount)
    
    # Initialize matrices for output
    OptimalDice = np.zeros((LTarget, LTarget), dtype = int)
    WinningProb = np.zeros((LTarget, LTarget))

    # Calculate for each state
    for X in range(LTarget):
        for Y in range(LTarget):
            best_k = 0
            best_prob = 0

            for k in range(1, NDice + 1):
                total = WinCount[X, Y, k] + LoseCount[X, Y, k]
                if total > 0: 
                    prob = WinCount[X, Y, k] / total
                    if prob > best_prob:
                        best_prob = prob
                        best_k = k

            OptimalDice[X, Y] = best_k 
            WinningProb[X, Y] = best_prob


    return OptimalDice, WinningProb

# Manages turn-taking in the game, updating scores based on dice rolls
def TakeTurns(Player, NSides, Score1, Score2, NDice, WinCount, LoseCount, RollTrace):
    diceToRoll, ProbDict = NumDiceRoll(Score1, Score2, WinCount, LoseCount, NDice)

    # Add GamePlay History Tracker
    RollTrace.append((Score1, Score2, diceToRoll))

    for _ in range(diceToRoll):
        Score1 += random.randint(1, NSides)

    print(f'Player {Player} rolls {diceToRoll} dice. {Player} total: {Score1}.')

    return Score1, RollTrace, ProbDict

# Updates win/loss counts based on the game's outcome
def UpdateCounts(Winner, RollTrace, WinCount, LoseCount):
    # Add 1 to Count Matrices based on winner and trace
    for i, trace in enumerate(RollTrace):
        if (Winner == 'A' and i % 2 == 0) or (Winner == 'B' and i % 2 == 1):
            WinCount[trace] += 1
            print(f'Win: {trace}, Count: {WinCount[trace]}')

        else:
            LoseCount[trace] += 1
            print(f'Lose: {trace}, Count: {WinCount[trace]}')

# Core game logic for a single game iteration
def PlayGame(NSides, LTarget, UTarget, NDice, WinCount, LoseCount):
    RollTrace = []
    X, Y = 0, 0

    while True:
        # Player A
        X, RollTrace, ProbDict = TakeTurns('A', NSides, X, Y, NDice, WinCount, LoseCount, RollTrace)
        print(f'Probabilities: {ProbDict}')
        
        if LTarget <= X <= UTarget or X > UTarget:
            Winner = 'A' if X <= UTarget else 'B'
            break

        # Player B
        Y, RollTrace, ProbDict = TakeTurns('B', NSides, Y, X, NDice, WinCount, LoseCount, RollTrace)
        print(f'Probabilities: {ProbDict}')
        
        if LTarget <= Y <= UTarget or Y > UTarget:
            Winner = 'B' if Y <= UTarget else 'A'
            break
    
    if Winner == 'A': print('A wins.')
    else: print('A loses.')

    print(RollTrace)

    UpdateCounts(Winner, RollTrace, WinCount, LoseCount)

# Determines the optimal number of dice to roll based on historical performance
def NumDiceRoll(Score1, Score2, WinCount, LoseCount, NDice, M = 100):
    fDict = {}
    T = sum(WinCount[Score1, Score2, 1:] + LoseCount[Score1, Score2, 1:])
    
    # Calculate f_k
    for k in range(1, NDice + 1):
        denominator = WinCount[Score1, Score2, k] + LoseCount[Score1, Score2, k]
        f_k = WinCount[Score1, Score2, k] / denominator if denominator != 0 else 0.5
        fDict[k] = f_k
    
    # Find k_opt That Maximizes f_k
    k_opt = max(fDict, key = fDict.get)
    f_k_opt = fDict[k_opt]

    s = sum(f_k for k, f_k in fDict.items() if k != k_opt)
    
    # Calculate Probabilities
    p_k_opt = (T * f_k_opt + M) / (T * f_k_opt + NDice * M)
    ProbDict = {k_opt: p_k_opt}
    
    for k in range(1, NDice + 1):
        if k != k_opt:
            p_k = (1 - p_k_opt) * (T * fDict[k] + M) / (s * T + (NDice - 1) * M)
            ProbDict[k] = p_k
    
    # Choose a dice to roll based on calculated probabilities
    diceToRoll = random.choices(list(ProbDict.keys()), 
                                weights = list(ProbDict.values()), 
                                k = 1)[0]

    return diceToRoll, ProbDict

#%%
if __name__ == '__main__':
    OptimalDice, WinningProb = PlayNGames(args.NSides, 
                                          args.LTarget, 
                                          args.UTarget, 
                                          args.NDice, 
                                          args.NGames)
    
    print(OptimalDice)
    print(WinningProb)

