import random

from hashlib import sha256
from itertools import zip_longest

def gen_sudoku_puzzle():
    puzzle = [
        0,0,0,0,0,0,6,8,0, \
        0,0,0,0,7,3,0,0,9, \
        3,0,9,0,0,0,0,4,5, \
        4,9,0,0,0,0,0,0,0, \
        8,0,3,0,5,0,9,0,2, \
        0,0,0,0,0,0,0,3,6, \
        9,6,0,0,0,0,3,0,8, \
        7,0,0,6,8,0,0,0,0, \
        0,2,8,0,0,0,0,0,0 
    ]
    # Indices of given values
    presets = [6,7,13,14,17,18,20,25,26,27,28,36,38,40,42,44,52,53,54,55,60,62,63,66,67,73,74]
    return puzzle, presets

def solve_sudoku_puzzle(puzzle):
    solution = [
        1,7,2,5,4,9,6,8,3, \
        6,4,5,8,7,3,2,1,9, \
        3,8,9,2,6,1,7,4,5, \
        4,9,6,3,2,7,8,5,1, \
        8,1,3,4,5,6,9,7,2, \
        2,5,7,1,9,8,4,3,6, \
        9,6,4,7,1,5,3,2,8, \
        7,3,1,6,8,2,5,9,4, \
        5,2,8,9,3,4,1,6,7
    ]
    return solution

def chunk(iterable, size):
    return [iterable[i:i+size] for i in range(0, len(iterable), size)]

def flatten(iterable):
    return [item for sublist in iterable for item in sublist]

def puzzle_rows(puzzle):
    return chunk(puzzle, 9)

def puzzle_columns(puzzle):
    return list(zip(*puzzle_rows(puzzle)))

def puzzle_subgrids(puzzle, size=3, n=9):
    subgrids = []
    rows = puzzle_rows(puzzle)
    for i in range(0,n,size):
        for j in range(0,n,size):
            subgrids.append(flatten([rows[j+k][i:i+size] for k in range(size)]))
    return subgrids

def puzzle_subgrids_column(puzzle, size=3, n=9):
    subgrids = []
    columns = puzzle_columns(puzzle)
    for i in range(0,n,size):
        for j in range(0,n,size):
            subgrids.append(flatten([columns[j+k][i:i+size] for k in range(size)]))
    return subgrids

def create_permutations():
    permutations = list(range(1,10))
    random.shuffle(permutations)
    permutations = [0] + permutations
    return permutations

def puzzle_permute(puzzle, permutations):
    return [permutations[x] for x in puzzle]
    
def gen_nonces():
    nonces = [
        random.SystemRandom().getrandbits(8) for _ in range(9**2)
    ]
    return nonces

def puzzle_commitment(puzzle, nonces):
    return [sha256((str(nonce)+str(val)).encode('utf-8')).hexdigest() for nonce, val in zip(nonces, puzzle)]

def all_digits_exist_once(iterable):
    digit_mask = [0 for i in range(9)]
    for x in iterable:
        digit_mask[x-1]=1
    return all(digit_mask)

if __name__ == "__main__":

    random_nonce = random.randint(1,999)
    print("random:",random_nonce)
    print("random:",len(str(random_nonce)))

    puzzle, presets = gen_sudoku_puzzle()
    solution = solve_sudoku_puzzle(puzzle)

    permutations = create_permutations()
    permuted_solution = puzzle_permute(solution, permutations)
    nonces = gen_nonces()
    commitment = puzzle_commitment(permuted_solution, nonces)

    sender_solution = []
    sender_solution_nonce = []
    sender_solution_commitment = []

    if random_nonce % 2 == 0:
        tag = random_nonce
        for a in range(len(str(random_nonce))):
            if random_nonce % 10 != 9:
                sender_solution_column = puzzle_columns(permuted_solution)[random_nonce % 10]
                sender_solution.append(sender_solution_column)
                sender_solution_nonce_column = puzzle_columns(nonces)[random_nonce % 10]
                sender_solution_nonce.append(sender_solution_nonce_column)
                sender_solution_commitment_column = puzzle_columns(commitment)[random_nonce % 10]
                sender_solution_commitment.append(sender_solution_commitment_column)
            else:
                sender_solution_column = puzzle_columns(permuted_solution)[0]
                sender_solution.append(sender_solution_column)
                sender_solution_nonce_column = puzzle_columns(nonces)[0]
                sender_solution_nonce.append(sender_solution_nonce_column)
                sender_solution_commitment_column = puzzle_columns(commitment)[0]
                sender_solution_commitment.append(sender_solution_commitment_column)
            random_nonce = random_nonce // 10
    else:
        tag = random_nonce
        for a in range(len(str(random_nonce))):
            if random_nonce % 10 != 9:
                sender_solution_row = puzzle_rows(permuted_solution)[random_nonce % 10]
                sender_solution.append(sender_solution_row)
                sender_solution_nonce_row = puzzle_rows(nonces)[random_nonce % 10]
                sender_solution_nonce.append(sender_solution_nonce_row)
                sender_solution_commitment_row = puzzle_rows(commitment)[random_nonce % 10]
                sender_solution_commitment.append(sender_solution_commitment_row)
            else:
                sender_solution_row = puzzle_rows(permuted_solution)[0]
                sender_solution.append(sender_solution_row)
                sender_solution_nonce_row = puzzle_rows(nonces)[0]
                sender_solution_nonce.append(sender_solution_nonce_row)
                sender_solution_commitment_row = puzzle_rows(commitment)[0]
                sender_solution_commitment.append(sender_solution_commitment_row)
            random_nonce = random_nonce // 10

    #print("test_2",type(sender_solution[0][0]))
    #print("test_3",type(sender_solution_nonce[0][0]))
    print("test_1",sender_solution)
    print("test_2",sender_solution_nonce)
    print("test_3",sender_solution_commitment)

    for a in range(len(str(tag))):
        sudoku_verification = all_digits_exist_once(sender_solution[a])
        assert sudoku_verification == True
        receiver_verification_commitment = puzzle_commitment(sender_solution[a], sender_solution_nonce[a])
        for b in range(9):
            if sender_solution_commitment[a][b] != receiver_verification_commitment[b]:
                raise AssertionError
            else:
                pass
            
            """
            if tag % 10 != 9:
                sender_solution_commitment_column = puzzle_columns(commitment)[tag % 10]
            else:
                sender_solution_commitment_column = puzzle_columns(commitment)[0]
            """

