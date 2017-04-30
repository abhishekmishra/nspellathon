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

#print dictionary

class NSpellathon:
    '''

    '''

    central_index = -1
    letters = ''

    def __init__(self, word, central):
        self.letters = word
        self.central_index = central

    def get_puzzle(self):
        return self.letters

    def get_central_char(self):
        return self.letters[self.central_index]

    def print_puzzle(self):
        print(self.letters)
        ul = ''
        for i in range(0, 7):
            if i == self.central_index:
                ul += '-'
            else:
                ul += '.'
        print(ul)

    def __str__(self):
        le = self.letters.upper()
        ci = self.central_index
        cc = le[ci]
        le = le[:ci] + le[ci+1:]
        out =  '    ________\n'
        out += '   /\  ' + le[0] + '   /\\\n'
        out += '  /  \____/  \\\n'
        out += ' / ' + le[1] + ' /    \\ ' + le[2] + ' \\\n'
        out += '/___/  ' + cc + '   \\___\\\n'
        out += '\   \      /   /\n'
        out += ' \ ' + le[3] + ' \____/ ' + le[4] + ' /\n'
        out += '  \  /  ' + le[5] + ' \  /\n'
        out += '   \/______\/\n'

        return out

class NSpellathonSolution:
    '''

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
    r = DICTIONARY[7][random.randint(0, len(DICTIONARY[7])-1)]
    idx = random.randint(0, 6)
    print('random word is - ', r)
    perms = [''.join(p) for p in permutations(r)]
    word = perms[random.randint(0, len(perms))]

    return NSpellathon(word = word, central=idx)

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