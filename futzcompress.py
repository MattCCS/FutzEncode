#!/usr/local/bin/python3

import collections
import re


ACP_WORDS = "the,a,an,and,not,for,but,or,to,of,in,on,with,at,by,from".split(',')
TO_ACP_MAP = dict(zip(ACP_WORDS, range(16)))
FROM_ACP_MAP = {v: k for (k, v) in TO_ACP_MAP.items()}

PUNCTUATION = [
    '. ', ', ', '," ', '\'ll ', '\'s ', '\'re ', '.\n', ',\n',
]

RESERVED_WORDS = [
    'that', 'have', 'you', 'his', 'they', 'say', 'her', 'she',
]

RESERVED = set()
RESERVED.update([' {} '.format(w) for w in ACP_WORDS])
RESERVED.update(PUNCTUATION)
for RWORD in RESERVED_WORDS:
    RESERVED.add(" {} ".format(RWORD))


NONASCII = 0b10000000
SB       = 0b00100000
SA       = 0b00010000


def to_ACP(acp_word, sb=False, sa=False):
    return NONASCII + \
        (SB * sb) + \
        (SA * sa) + \
        TO_ACP_MAP[acp_word]


def from_ACP(acp):
    sb = ' ' if acp & SB else ''
    sa = ' ' if acp & SA else ''
    word = FROM_ACP_MAP[acp & 0b1111]
    return "{}{}{}".format(sb, word, sa)


def rank(ranked):
    return sorted(ranked, key=lambda p: p[1], reverse=True)


print("Loading...")
ALL_TEXT = open("shakespeare.txt").read() + open("big.txt").read()


UNIGRAMS = (
    'e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'l', 'd', 'c', 'u',
    'm', 'f', 'p', 'g', 'w', 'y', 'b', 'v', 'k', 'x', 'j', 'q', 'z',
)

DIGRAMS = (
    'th', 'he', 'in', 'er', 'an', 're', 'on', 'at', 'en', 'nd',
    'ti', 'es', 'or', 'te', 'of', 'ed', 'is', 'it', 'al', 'ar',
    'st', 'to', 'nt', 'ng', 'se', 'ha', 'as', 'ou', 'io', 'le',
    've', 'co', 'me', 'de', 'hi', 'ri', 'ro', 'ic', 'ne', 'ea',
    'ra', 'ce', 'li', 'ch', 'll', 'be', 'ma', 'si', 'om', 'ur',
)


def pairwise(sliceable, n):
    return zip(*(sliceable[i:] for i in range(n)))


UNIGRAMS = collections.defaultdict(int)
DIGRAMS = collections.defaultdict(int)
TRIGRAMS = collections.defaultdict(int)
# QUADGRAMS = collections.defaultdict(int)

# UNIWORDS = collections.defaultdict(lambda: collections.defaultdict(int))
UNIWORDS = collections.defaultdict(int)
DIWORDS = collections.defaultdict(int)

NPUNCT = collections.defaultdict(int)

# enum
COUNT = 0


# print("Counting unigrams...")
# for c in ALL_TEXT:
#     UNIGRAMS[c] += 1

# print("Counting N-puncts...")
# NPUNCT_RE = re.findall(r"(\W+)", ALL_TEXT)
# for npunct in NPUNCT_RE:
#     NPUNCT[npunct] += 1

print("Counting digrams...")
# for (chars) in pairwise(ALL_TEXT, 2):
DIGRAM_RE = re.findall(r"(?=(\w\w))", ALL_TEXT)
for digram in DIGRAM_RE:
    DIGRAMS[digram] += 1

print("Counting trigrams...")
TRIGRAM_RE = re.findall(r"(?=(\w\w\w))", ALL_TEXT)
for trigram in TRIGRAM_RE:
    TRIGRAMS[trigram] += 1

# print("Counting quadgrams...")
# for (c1, c2, c3, c4) in pairwise(ALL_TEXT, 4):
#     QUADGRAMS[c1 + c2 + c3 + c4] += 1

# print("Finding all separated words...")
# WORDS = re.split(r"(\W+)", ALL_TEXT)

print("Finding all words...")
WORDS = re.findall(r"(\w+)", ALL_TEXT)

print("Counting uniwords...")
for word in WORDS:
    UNIWORDS[word] += 1

# print("Counting separated uniwords...")
# for (pre, word, post) in list(pairwise(WORDS, 3))[1::2]:
#     # print(repr(word))
#     UNIWORDS[word][COUNT] += 1
#     UNIWORDS[word][pre] += 1
#     UNIWORDS[word][post] += 1

print("Finding spaced diwords...")
WORDS_SPACED = re.findall(r"(?=\W(\w+) (\w+)\W)", ALL_TEXT)  # http://stackoverflow.com/questions/5616822/python-regex-find-all-overlapping-matches
for pair in WORDS_SPACED:
    DIWORDS[' '.join(pair)] += 1

ALLGRAMS = {}
# ALLGRAMS.update(UNIGRAMS)
# ALLGRAMS.update(NPUNCT)
ALLGRAMS.update(DIGRAMS)
ALLGRAMS.update(TRIGRAMS)
# ALLGRAMS.update(QUADGRAMS)
ALLGRAMS.update(DIWORDS)

for gram in list(ALLGRAMS.keys()):
    for reserved in RESERVED:
        if gram in reserved:
            print("Removing {} from ALLGRAMS -- present in RESERVED!".format(repr(gram)))
            del ALLGRAMS[gram]
            break

print("Calculating best N-grams...")
pairs = ALLGRAMS.items()
scored = ((gram, count, (len(gram) - 1) * count) for (gram, count) in pairs)
final = sorted(scored, key=lambda p: p[2], reverse=True)[:128]

for each in final:
    print(each)
