# Implementation of the game Nim (Open Sourced on GitHub - Snehasish Ghosh(optimisticexquisite))
# This is a demonstration for IISc Open Day 2024 - Department of Mathematics

def nim_sum(piles):
    xor = 0
    for pile in piles:
        xor ^= pile
    return xor


def next_move(piles):
    binary = []
    for pile in piles:
        binary.append(bin(pile)[2:])
    max_len = max([len(b) for b in binary])
    for i in range(len(binary)):
        binary[i] = binary[i].zfill(max_len)
    nim = nim_sum(piles)
    if nim != 0:
        nim = bin(nim)[2:].zfill(max_len)
        for i in range(len(binary)):
            if int(binary[i], 2) ^ int(nim, 2) < int(binary[i], 2):
                piles[i] = int(binary[i], 2) ^ int(nim, 2)
                break
        print(f"Computer removes {int(binary[i], 2) - piles[i]} coins from pile {i+1}")
    else:
        # Remove one coin from the largest pile
        max_pile = max(piles)
        for i in range(len(piles)):
            if piles[i] == max_pile:
                piles[i] -= 1
                print(f"Computer removes 1 coin from pile {i+1}")
                break



    
        
if __name__ == "__main__":
    print("Welcome to IISc Open Day 2024 - Department of Mathematics")
    print("---------------------------------------------")
    print("This is a game called Nim - a mathematical game of strategy")
    print("The game starts with a number of piles of coins")
    print("Players take turns removing coins from the piles")
    print("A player must remove at least one coin and can remove any number of coins from STRICTLY a single pile")
    print("The player who removes the last coin wins")
    print("---------------------------------------------")
    print("Let's play!")
    piles = []
    print("Enter the number of coins in each pile")
    inputval = input()
    piles = list(map(int, inputval.split()))
    n_piles = len(piles)
    print("The game begins!")
    print("The piles are:")
    print(piles)
    print("You are player 1")
    last_piles = [piles.copy()]
    while True:
        print("Your move")
        print("Enter the pile number and the number of coins to remove")
        inputval = input()
        revertcount = 0
        if (inputval == "revert"):
            piles = last_piles[revertcount - 1].copy()
            revertcount -= 1
            print("Your move has been reverted!")
            print("The piles are:")
            print(piles)
            continue
        else: 
            revertcount = 0
            last_piles.append(piles.copy())
            pile, coins = map(int, inputval.split())
            if coins > piles[pile-1]:
                print("Invalid move! Try again")
                continue
            if coins == 0:
                print("Invalid move! Try again")
                continue
            piles[pile-1] -= coins
            print("The piles are:")
            print(piles)
            if sum(piles) == 0:
                print("You win!")
                break
            print("Computer's move")
            next_move(piles)
            print("The piles are:")
            print(piles)
            if sum(piles) == 0:
                print("Computer wins!")
                break


