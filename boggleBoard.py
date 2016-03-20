import random
from boggleWords import boggleWords

all_words = boggleWords

def getBoggleBoard(size=4):
    """creates a boggle board then returns it 
    and all solutions to that board"""

    global board, words, ncols, nrows, prefixes

    # all possible dice
    dice = ['AACIOT', 'ABILTY', 'ABJMOQ', 
    'ACDEMP', 'ACELRS', 'ADENVZ', 'AHMORS', 
    'BIFORX', 'DENOSW', 'DKNOTU', 'EEFHIY', 
    'EGKLUY', 'EGINTV', 'EHINPS', 'ELPSTU', 
    'GILRUW']

    board_size = size

    # loop until the board is produced with length >= 4
    while True:
        random.shuffle(dice)

        grid = ""
        for x in range(board_size):
            for i in range(board_size):
                grid +=random.choice(dice[i+x])
            grid+=" "
        
        # set board to be number of columns
        board = grid.lower().split()
        nrows, ncols = len(board), len(board[0])

        # gets words that can be found in boggle board
        words = findwords()

        # caches beginnings of words for easier searching
        prefixes = set(word[:i] for word in words
                       for i in range(2, len(word)+1))

        # get a list of all solutions using prefixes and words
        all_solutions = list(solve())

        # keep doing this unitl the number of solutions for the board is 4 or more
        if len(all_solutions)>=4:
            return (board, all_solutions)           

def findwords():
    """finds length of words which are 3 or more 
    letters long and in the current board options"""
    
    global board, all_words

    # a list of all letters available
    alphabet = ''.join(set(''.join(board))) 

    words = set()
    
    for word in all_words.split():
        checkWord = any(letter in alphabet for letter in word)
        if len(word)>3 and checkWord:
            words.add(word.rstrip('\n'))
    return words

            
def solve():
    """generator that goes through each row and letter 
    and finds a path to the given word"""
    for y, row in enumerate(board):
        for x, letter in enumerate(row):
            for result in extending(letter, ((x, y),)):
                yield result

def extending(prefix, path):
    """uses recursive call to find all neighbors in path 
    leading to given prefix where prefix will eventually 
    be a word in all possbile solutions to the board"""
    
    global words

    if prefix in words:
        yield (prefix, path)
    for (nx, ny) in neighbors(path[-1]):
        if (nx, ny) not in path:
            prefix1 = prefix + board[ny][nx]
            if prefix1 in prefixes:
                for result in extending(prefix1, path + ((nx, ny),)):
                    yield result

def neighbors((x, y)):
    """finds all neighbors in boggle board"""
    for nx in range(max(0, x-1), min(x+2, ncols)):
        for ny in range(max(0, y-1), min(y+2, nrows)):
            yield (nx, ny)

if __name__ == '__main__':
    """TESTING PURPOSES make new board, check that it sends back required info"""
    x, y = getBoggleBoard()
    print x, y
    myDict = []
    myDict.append({'Username':'tim', 'Move':'(0, 3)', 'Points Scored':2})
    print myDict