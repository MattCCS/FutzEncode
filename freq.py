
import collections
import json
import re
import time


LONG_STRING = "When in the Course of human events, it becomes necessary for one people to dissolve the political bands which have connected them with another, and to assume among the powers of the earth, the separate and equal station to which the Laws of Nature and of Nature's God entitle them, a decent respect to the opinions of mankind requires that they should declare the causes which impel them to the separation."
# LONG_STRING = LONG_STRING.replace('the', chr(128))
# LONG_STRING = LONG_STRING.replace(' of Nature', chr(129))
# LONG_STRING = LONG_STRING.replace('\x00 separat', chr(130))
# LONG_STRING = LONG_STRING.replace(' which', chr(131))
# LONG_STRING = LONG_STRING.replace(' to', chr(132))
# LONG_STRING = LONG_STRING.replace(' and', chr(133))

# LONG_STRING = open("big.txt").read()
# LONG_STRING = open("shakespeare.txt").read()
LONG_STRING = "sYmZCYmIYlZcYlMYmZgYlTYlZqYmFYlZAYlZtYlZtYlZsYmOYlZthYmZbYlJYlFYlNYmZtYlFYlZkYmZqYlZEYlZgYlZGYlZhYlZDKYmQYmZBYlPYmZvYlZjYlHYmFYmZcYlZHYmZiYmZfYlZuYmOYlZOaYlRYmZEYmTYmKYmKYmOYmZfvYlZUYlIYlZdYlUYmZsYmHYlOYlZeYlZIYlZhhYlLYmQYmZtYlPYmZgYmIYmZoYmZlYlZfYlZibYmRYmZCYlSYlVYlIYmZbYmNYmZeYlZEYlZDYlZiYlZsYmZcnYlZUYlPYlMYmZnYmZiYmZdYlZPYmMYlZgYlZGaYmZyYmZyYmZaYlQYlFYmZDYmZuYmZvYlPYlZNYlZtYmZcYlZnYlZGYlZAZCYlLYlPYmPYrOYrOYlZpYlZGYlZvYlZyYmZefYlQYlKYmZEYlZxYlZoYlZOYmNYlZPYlZOtYlGYmQYmZhYlZqYlZhYlZOYlZQYlZyYlZyIYmZgYmZBYmZbYlZzYmZjhYlZdYmQYmPYlZcYlZrYlZfYmMYlZBYmSYmMYmZcaYmHYmZsYlUYlZUYmVYmHYmZEYlZrYmZpYmNYmZidYmZtYlNYmZsYlZkYmZmYmZcYlZfYlZQYlZHbYmQYlJYmZBYlZSYmZlYrOYmZjYlZCYmMYmKZjYlRYmZtYlZcYlHYmIYmVYmVYlGYmQYmZqYmTYlZBYlZpYmMdYlJYlRYlFYmZwYmZyYlZeYmZrYlZvYlZgYlZOYlZmaYlZTYlZDYlZgYlZyYlZIYlZGKYlJYmZgYmZCYlIYmZgYmZDYlVYmTYlZCYlZtYmSYmMYlZFhYlZTYmZsYmZBYlZSYlZdYlSYmZoYlZrYlZEYlZQYlZFYmKYlZRYmZepYlFYlZrYmKYlZzYmZiYmSYlZpUYlRYmZzYlGYlZKYlZLYlZgYlZDYlZDZFYmZtYlRYmZgYmZyYlZeYmZqYlZiYmOYlZuYlZBYmZiYlZoYlZDYmZe"
LONG_STRING = bytearray(LONG_STRING.encode('ascii'))

HARD_CAP = 100


def score(gram, indices):
    return (len(gram) - 1) * len(indices)


def process(data_barr):
    ngrams = collections.defaultdict(lambda: collections.defaultdict(list))
    # print("Finding 2-grams...")

    for i in range(len(data_barr)):
        seq = bytes(data_barr[i:i + 2])
        if len(seq) != 2:
            continue
        ngrams[2][seq].append(i)

    i = 2
    more = True
    best = (None, 0, [])

    while more:
        # print("Finding {}-grams...".format(i + 1))
        more = False
        moved = 0

        for ngram in list(ngrams[i].keys()):
            indices = ngrams[i][ngram]
            if best[1] / len(indices) > HARD_CAP:
                continue
            if len(indices) > 1:
                more = True
                for index in indices:
                    try:
                        char = data_barr[index + i]
                        seq = ngram + bytes([char])
                        ngrams[i + 1][seq].append(index)
                        moved += 1
                    except IndexError:
                        continue
                # del ngrams[i][ngram]

        if len(ngrams[i]) == 0:
            del ngrams[i]

        best = find_best_substitution(ngrams)

        # print("Moved {} sequences".format(moved))
        i += 1

    return ngrams


def find_best_substitution(ngrams):
    # print("Flattening...")
    flattened = {k: v for block in ngrams.values() for (k, v) in block.items()}

    # print("Ranking...")
    ranked = sorted(((gram, score(gram, indices), indices) for (gram, indices) in flattened.items()), key=lambda e: e[1])

    best = ranked[-1]
    if best[1] == 1:
        raise RuntimeError("No good substitution left!")
    return best


CURRENT_BYTE = 127


def next_byte():
    global CURRENT_BYTE
    CURRENT_BYTE += 1
    return CURRENT_BYTE


def replace(data_barr, ngram):
    l = len(ngram[0])
    replacement_byte = [next_byte()]
    for index in reversed(ngram[2]):
        data_barr[index:index + l] = replacement_byte
    return replacement_byte[0]


def run_round():
    # print("Processing...")
    ngrams = process(LONG_STRING)

    # print("Finding substitution...")
    ngram = find_best_substitution(ngrams)
    (gram, score, indices) = ngram
    # print("Best substitution: {}".format((ngram, score)))

    # print("Replacing...")
    new_byte = replace(LONG_STRING, ngram)

    return (ngram, new_byte)

    # print("New string: {}".format(LONG_STRING))


try:
    SUBS = []
    for i in range(1, 128 + 1):
        t0 = time.time()
        out = run_round()
        (ngram, new_byte) = out
        SUBS.append( (ngram[0], new_byte) )
        t1 = time.time()
        print("Substitution {}:  {} -> {} (appears {} times; saves {} bytes; took {} seconds)".format(
            i, repr(ngram[0]), repr(new_byte), len(ngram[2]), ngram[1], t1 - t0)
    )
except RuntimeError as err:
    pass


for r in SUBS:
    print("    {},".format(r))
exit()


# def Table():
#     d = collections.defaultdict(Table)
#     d[''] = 0
#     return d


# class FrequencyCounterFlat(object):

#     def __init__(self):
#         self.counts = Table()

#     def add(self, strng):
#         counts = self.counts

#         counts[''] += 1
#         for char in strng:
#             counts = counts[char]
#             counts[''] += 1

#     def score(self, key):
#         return self[key][''] * len(key)

#     def show(self):
#         print(json.dumps(self.counts, indent=4))

#     def __getitem__(self, key):
#         counts = self.counts
#         for char in key:
#             counts = counts[char]
#         return counts


class FrequencyCounter(object):

    def __init__(self, depth=0):
        self.depth = depth
        self.count = 0
        self.children = {}

    def add(self, strng):
        if not strng:
            self.count += 1
            return

        if strng:
            (first, *rest) = strng
            if first not in self.children:
                self.children[first] = FrequencyCounter(depth=self.depth + 1)
            self.children[first].add(strng[1:])

    def clear(self, strng):
        cleared = 0

        if not strng:
            cleared = self.count
        if strng:
            (first, *rest) = strng
            cleared = self.children[first].clear(rest)
            if not self.children[first]:
                del self.children[first]

        self.count -= cleared
        return cleared

    def score(self):
        return self.count * (self.depth - 1)

    def to_dict(self):
        return {
            "({}) {}/{}".format(repr(k), v.count, v.score()): v.to_dict()
            for (k, v) in self.children.items()
        }

    def show(self):
        for val in sorted(self, key=lambda p: (p[2], p[1])):
            print(val)

    def __iter__(self):
        yield ('', self.count, self.score())

        for (char, child) in self.children.items():
            for (rest, count, score) in child:
                yield (char + rest, count, score)

    def __getitem__(self, key):
        for char in key:
            self = self.children[char]
        return self

    def __bool__(self):
        return bool(self.count or self.children)


tree = FrequencyCounter()

# t0 = time.time()
# for _ in range(5):
#     tree.add('abc')
# for _ in range(3):
#     tree.add('abcdefg')
# t1 = time.time()
# print(t1 - t0)

FORM = r"(?=(.{{{n}}}))"


def findall_up_to(strng, n):
    print("Finding all n-grams up to {}...".format(n))
    for i in range(2, n + 1):
        print("Finding all {}-grams...".format(i))
        grams = re.findall(FORM.format(n=i), strng)
        for gram in grams:
            yield gram

g = findall_up_to(LONG_STRING, 5)

print("Loading tree...")
for (i, s) in enumerate(g):
    if not i % 100000:
        print("{}...".format(i))
    tree.add(s)

tree.show()

# tree.clear('separa')
# tree.show()

# print(tree['abcdefg'].score())
# print(tree.clear('abcdefg'))
# tree.show()

# anothereafternoon
# an
# another
#  no
#  not
#   other
#    the
#    there
#    thereafter
#     here
#     hereafter
#      ere
#         aft
#         after
#         afternoon
#              noon
# ^ how to greedily match??
# another|e|afternoon
# an|o|thereafter|noon


# critsits should expire after 3 hours
# cr
#  ri
#   it
#    ts
#     si
#      it
#       ts
#        s_
