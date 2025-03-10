from collections import defaultdict
from itertools import product

class Vertex(object):
    def __init__(self, letter, number):
        self.letter = letter
        self.number = number
        self.neighbors = dict()

    def add_neighbor(self, neighbor):
        self.neighbors[neighbor.number] = neighbor

    def is_neighbor(self, number):
        return number in self.neighbors

    def get_neighbor(self, number):
        return self.neighbors[number]



T9_MAPPING = {
    2: "ABC", 3: "DEF",
    4: "GHI", 5: "JKL", 6: "MNO",
    7: "PQRS", 8: "TUV", 9: "WXYZ"
}

T9_REVERSE_MAPPING = {
    'A': 2, 'B': 2, 'C': 2,
    'D': 3, 'E': 3, 'F': 3,
    'G': 4, 'H': 4, 'I': 4,
    'J': 5, 'K': 5, 'L': 5,
    'M': 6, 'N': 6, 'O': 6,
    'P': 7, 'Q': 7, 'R': 7, 'S': 7,
    'T': 8, 'U': 8, 'V': 8,
    'W': 9, 'X': 9, 'Y': 9, 'Z': 9
}

def build_t9_decoder(word_list):
    head = Vertex(" ", 1)
    for word in word_list:
        current = head
        for letter in word:
            number = T9_REVERSE_MAPPING[letter]
            amount = T9_MAPPING[number].find(letter)
            for i in range(amount):
                if current.is_neighbor(number):
                    current = current.get_neighbor(number)
                else:
                    if i == amount - 1:
                        v = Vertex(letter, number)
                    else:
                        v = Vertex("", number)
                    current.add_neighbor(v)
                    current = v
        current.add_neighbor(head)
    return head


def dfs(s, n, current, phrase):
    if n == len(s):
        return phrase
    else:
        number = int(s[n])
        if current.is_neighbor(number):
            neighbor = current.get_neighbor(number)
            res = dfs(s, n + 1, neighbor, phrase + neighbor.letter)
            # if res is not None:
        else:
            return None



s = input()
n = int(input())
decoder = build_t9_decoder([input() for _ in range(n)])


# print(" ".join(dp[-1]) if dp[-1] else "")