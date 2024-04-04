import numpy as np
import random

def PlayNGames(NSides, LTarget, UTarget, NDice, NGames):
    WinCount = np.zeros((LTarget, LTarget, NDice + 1))
    LoseCount = np.zeros((LTarget, LTarget, NDice + 1))

    for _ in range(NGames):
        PlayGame(NSides, LTarget, UTarget, NDice, WinCount, LoseCount)
    
    return WinCount, LoseCount

def TakeTurns(Player, NSides, Score1, Score2, NDice, WinCount, LoseCount, RollTrace):
    diceToRoll = NumDiceRoll(Score1, Score2, WinCount, LoseCount, NDice)

    RollTrace.append((Score1, Score2, diceToRoll))

    for _ in range(diceToRoll):
        Score1 += random.randint(1, NSides)

    print(f'Player {Player} rolls {diceToRoll} dice. {Player} total: {Score1}.')

    return Score1, RollTrace

def UpdateCounts(Winner, RollTrace, WinCount, LoseCount):
    for i, trace in enumerate(RollTrace):
        if (Winner == 'A' and i % 2 == 0) or (Winner == 'B' and i % 2 == 1):
            WinCount[trace] += 1
            print('Win:', trace)

        else:
            LoseCount[trace] += 1
            print('Lose:', trace)

def PlayGame(NSides, LTarget, UTarget, NDice, WinCount, LoseCount):
    RollTrace = []
    X, Y = 0, 0

    while True:
        # Player A
        X, RollTrace = TakeTurns('A', NSides, X, Y, NDice, WinCount, LoseCount, RollTrace)
        
        if LTarget <= X <= UTarget or X > UTarget:
            Winner = 'A' if X <= UTarget else 'B'
            break

        # Player B
        Y, RollTrace = TakeTurns('B', NSides, Y, X, NDice, WinCount, LoseCount, RollTrace)
        
        if LTarget <= Y <= UTarget or Y > UTarget:
            Winner = 'B' if Y <= UTarget else 'A'
            break
    
    if Winner == 'A': print('A wins.')
    else: print('A loses.')

    print(RollTrace)

    UpdateCounts(Winner, RollTrace, WinCount, LoseCount)



def NumDiceRoll(X, Y, Win, Lose, M = 100):
    return 2


NSides, LTarget, UTarget, NDice, NGames = 6, 15, 17, 2, 3
PlayNGames(NSides, LTarget, UTarget, NDice, NGames)




'''# X is the current point count for the player about to play
# Y is the point count for the opponent
# k is the number of dice the current player rolls
np.zeros
WinCount[X,Y,k] = LTarget × LTarget × [NDice + 1]
LoseCount[X,Y,k] = LTarget × LTarget × [NDice + 1]


def PlayGame()
for i in range(diceToRoll):
    playerValue += (1 to NSides)

update()


NGames = 1e5


def NumDiceRoll(X, Y, Win, Lose, M = 100):
    f_k = win[X,Y,k]/(win + lose)
        if win + lose = 0 then fk = 0.5
    k_opt = k that maximize f_k
        
    s = sum(fk) where k != k_opt
    T = win[X,Y,?] + lose[X,Y,?] where ? <= K
                        
    # for best k
    p_k_opt = (T * f_k_opt + M) / (T * f_k_opt)
    # for all other k 
    p_k = (1 - p_k_opt) * (T * f_k + M) / (s * T + (K - 1) * M)

    return diceToRoll'''