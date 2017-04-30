'''
Author: Abhishek Mishra
'''

import random
from itertools import permutations
import os
import tabulate

DICTIONARY = {}

SCOWL_WORD_LIST = os.path.join(os.path.dirname(__file__), 'SCOWL-wl/words.txt')
DICTIONARY_FILE = open(SCOWL_WORD_LIST, 'r')

for line in DICTIONARY_FILE:
    w = line.rstrip()
    if not '\'' in w and len(w) < 10:
        if len(w) in DICTIONARY:
            DICTIONARY[len(w)].append(w)
        else:
            DICTIONARY[len(w)] = [w]

class NSpellathon:
    '''
    Defines a spellathon puzzle.
    Includes the letters of the word in the puzzle,
    and the index of the letter in the array of letters
    to use as the central letter in the puzzle.
    '''

    central_index = -1
    letters = ''

    def __init__(self, word, central):
        self.letters = word
        self.central_index = central

    def get_puzzle(self):
        '''
        Returns the list of letters in the puzzle.
        '''
        return self.letters

    def get_central_char(self):
        '''
        Returns the central letter/character in the puzzle.
        '''
        return self.letters[self.central_index]

    def print_puzzle(self):
        '''
        Prints a dot and dash representation of the puzzle.
        Each dot or dash represents a letter in the word to be guessed.
        There is one and only one dash which represents the letter shown in the
        central portion of the puzzle.
        '''
        print(self.letters)
        puzzle_line = ''
        for i in range(0, 7):
            if i == self.central_index:
                puzzle_line += '-'
            else:
                puzzle_line += '.'
        print(puzzle_line)

    def __str__(self):
        upper_letters = self.letters.upper()
        central_letter = upper_letters[self.central_index]
        upper_letters = upper_letters[:self.central_index] + upper_letters[self.central_index+1:]
        out = '    ________\n'
        out += '   /\  ' + upper_letters[0] + '   /\\\n'
        out += '  /  \____/  \\\n'
        out += ' / ' + upper_letters[1] + ' /    \\ ' + upper_letters[2] + ' \\\n'
        out += '/___/  ' + central_letter + '   \\___\\\n'
        out += '\   \      /   /\n'
        out += ' \ ' + upper_letters[3] + ' \____/ ' + upper_letters[4] + ' /\n'
        out += '  \  /  ' + upper_letters[5] + ' \  /\n'
        out += '   \/______\/\n'

        return out

class NSpellathonSolution:
    '''
    Represents a solution of the spellathon puzzle.
    Includes the puzzle object and all the discovered
    solution words.
    '''
    puzzle = None
    solution_words = None

    def __init__(self, ns):
        self.puzzle = ns
        self.solution_words = {
            4: [],
            5: [],
            6: [],
            7: []
        }

    def is_valid_word(self, word):
        if len(word) < 4:
            return False

        if not self.puzzle.get_central_char() in word:
            return False

        check_letters = self.puzzle.get_puzzle()
        for c in word:
            if c in check_letters:
                idx = check_letters.index(c)
                check_letters = check_letters[:idx] + check_letters[idx+1:]
                #print check_letters
            else:
                return False

        return self.is_in_dictionary(word)

    def is_in_dictionary(self, word):
        return word in DICTIONARY[len(word)]

    def add_word(self, word):
        if self.is_valid_word(word=word):
            if word in self.solution_words[len(word)]:
                return 'Already added - ' + word
            else:
                self.solution_words[len(word)].append(word)
                return 'Added - ' + word
        else:
            return 'Not Valid - ' + word

    def get_score(self):
        score = [['words', 'score']]
        total = 0
        for i in range(4, 8):
            s = len(self.solution_words[i]) * (i - 3)
            score.append(['words of length ' + str(i), s])
            total += s
        score.append(['total', total])
        return score

    def __str__(self):
        return str(self.solution_words) \
               + '\n' \
               + tabulate.tabulate(self.get_score(), headers='firstrow', tablefmt="grid")

def create_spellathon():
    '''
    This method creates and returns a spellathon game object.

    1. To create the spellathon object it first looks up the dictinoary
    for a random word with length 7.

    2. It then creates a random permutation of the word and creates
    an NSPellathon object with it, and a random number between 0 and 6
    to use as the central character in the spellathon puzzle.

    '''
    random_word = DICTIONARY[7][random.randint(0, len(DICTIONARY[7])-1)]
    idx = random.randint(0, 6)
    print('random word is - ', random_word)
    perms = [''.join(p) for p in permutations(random_word)]
    word = perms[random.randint(0, len(perms))]

    return NSpellathon(word=word, central=idx)

def solve_spellathon(ns):
    soln = NSpellathonSolution(ns)
    for i in range(4, 8):
        for w in DICTIONARY[i]:
            soln.add_word(w)
    print(ns)
    print(soln)

if __name__ == "__main__":
    ns = NSpellathon(word = 'install', central = 4)
    print(ns.get_central_char())
    print(ns.get_puzzle())

    solution = NSpellathonSolution(ns = ns)
    print(solution.is_valid_word('ins'))
    print(solution.is_valid_word('tall'))

    print(solution.add_word('tall'))
    print(solution.add_word('tall'))
    print(solution.add_word('stall'))
    print(solution.add_word('stalin'))
    print(solution.solution_words)

    print(solution)

    ns1 = create_spellathon()
    print(ns1)
    ns1.print_puzzle()

    solve_spellathon(ns1)