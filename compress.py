
import collections
import sys

TO_BYTE = collections.OrderedDict()
TO_ARRAY = collections.OrderedDict()


def expand_rule(s):
    return bytes(bytearray(c for b in s for c in TO_ARRAY.get(b, [b])))

MAPPINGS = [
    (b'               ', 128),
    (b'   ', 129),
    (b' th', 130),
    (b'e ', 131),
    (b'\n\x81', 132),
    (b'\n  ', 133),
    (b't ', 134),
    (b's ', 135),
    (b', ', 136),
    (b'd ', 137),
    (b'ou', 138),
    (b'er', 139),
    (b'in', 140),
    (b'an', 141),
    (b'. ', 142),
    (b'y ', 143),
    (b'or', 144),
    (b'll ', 145),
    (b'en', 146),
    (b'o ', 147),
    (b'ar', 148),
    (b'on', 149),
    (b'th', 150),
    (b'of ', 151),
    (b'ha', 152),
    (b'es', 153),
    (b'\x82\x83', 154),
    (b'\x8ar ', 156),
    (b'i\x87', 157),
    (b',\x84', 159),
    (b'.\x85', 161),
    (b'ea', 162),
    (b'\x8d\x89', 163),
    (b'\x8cg ', 164),
    (b'y\x8a ', 166),
    (b'I ', 167),
    (b'ow', 168),
    (b'wi\x96 ', 169),
    (b'st', 170),
    (b'om', 171),
    (b'\x8b ', 172),
    (b'no\x86', 173),
    (b't\x93', 174),
    (b'\x82a\x86', 175),
    (b'el', 176),
    (b'ch', 177),
    (b'a ', 178),
    (b'hi', 180),
    (b'f\x90', 181),
    (b'is', 182),
    (b'al', 183),
    (b'm\x8f', 184),
    (b'ir', 185),
    (b'v\x83', 186),
    (b'h\x83', 187),
    (b'ee', 188),
    (b'at', 189),
    (b'it', 190),
    (b'; ', 191),
    (b'igh', 192),
    (b'e\x88', 193),
    (b'oo', 194),
    (b'e\x94', 195),
    (b'wi', 196),
    (b'\x8c ', 197),
    (b'\x82e', 198),
    (b'\x8al\x89', 199),
    (b'.\x84', 200),
    (b're', 201),
    (b'\x82\x8a ', 202),
    (b'ra', 203),
    (b'\x92 ', 204),
    (b'le', 205),
    (b'us', 206),
    (b'h\x9d', 207),
    (b'n\x89', 208),
    (b'ur', 209),
    (b'li', 210),
    (b'm ', 211),
    (b'ma', 212),
    (b'\x8cg', 213),
    (b'la', 214),
    (b';\x84', 215),
    (b"'\x87", 216),
    (b'me', 217),
    (b'ri', 218),
    (b'ol', 219),
    (b'\x95 ', 220),
    (b'US\x8e', 221),
    (b'be', 222),
    (b'\x96 ', 223),
    (b'\x8d ', 224),
    (b'h\x8b', 225),
    (b'\x8dd', 226),
    (b'm\x83', 227),
    (b'bu\x86', 228),
    (b'\x98\x86', 229),
    (b'il', 230),
    (b'a\x87', 231),
    (b'ce', 232),
    (b'i\x86', 233),
    (b'y\x9c', 234),
    (b'un', 235),
    (b's\x98\x91', 236),
    (b'\xb1 ', 237),
    (b'os', 238),
    (b'\xa8 ', 239),
    (b'k ', 240),
    (b"'\x89", 241),
    (b'b\x83', 242),
    (b'of', 243),
    (b'y\x8a', 244),
    (b'\x8agh', 245),
    (b'f ', 246),
    (b'e\x87', 247),
    (b'to', 248),
    (b'\x90 ', 249),
    (b'ti', 250),
    (b'ro', 251),
    (b'?\x85', 252),
    (b'k\x83', 253),
    (b'\x92t', 254),
    (b'fr\xab ', 255),
]

MAPPINGS = [
    (b'YlZ', 128),
    (b'YmZ', 129),
    (b'Yl', 130),
    (b'Ym', 131),
    (b'\x80g\x80', 132),
    (b'\x82G\x83Q\x81', 133),
    (b'\x82R\x81', 134),
    (b'\x81y\x80e\x81', 135),
    (b'O\x80', 136),
    (b'\x81c\x80', 137),
    (b'\x81B\x80S', 138),
    (b'I\x81g\x81', 139),
    (b'\x83M', 140),
    (b'\x81t\x82', 141),
    (b'\x83K', 142),
    (b'\x80D', 143),
    (b'\x81i', 144),
    (b'\x82F', 145),
    (b'\x80c\x82', 146),
    (b'\x80U\x82', 147),
    (b'\x80G\x80', 148),
    (b'\x81s', 149),
    (b'\x81e', 150),
    (b'\x81C\x82', 151),
    (b'h\x80', 152),
    (b'\x83T\x80', 153),
    (b'\x80t', 154),
    (b'\x81E\x80', 155),
    (b'\x83V\x83', 156),
    (b'\x80I\x80', 157),
    (b'\x83Q', 158),
    (b'\x80r\x80', 159),
    (b'\x83S\x8c', 160),
    (b'\x80d\x82', 161),
    (b'\x82J', 162),
    (b'\x80k\x81', 163),
    (b'\x80Q\x80', 164),
    (b'YrO', 165),
    (b'\x81y\x81', 166),
    (b'\x83I', 167),
    (b'\x83\x88', 168),
    (b'P\x80', 169),
    (b'\x83N', 170),
    (b'q\x80', 171),
    (b'\x81b', 172),
    (b'\x81g', 173),
    (b'\x80y', 174),
    (b'\x80pU', 175),
    (b'\x8e\x80z', 176),
    (b'\x91\x81', 177),
    (b'\x80s\x81', 178),
    (b'\x82Q\x82', 179),
    (b'\x80B\x90', 180),
    (b'\x81v', 181),
    (b'\x81o', 182),
    (b'\x82P', 183),
    (b'\x82L\xb7', 184),
    (b'\x81j\x80', 185),
    (b'G\x80h', 186),
    (b'\x80ib', 187),
    (b'\x80o', 188),
    (b'\x83H\x82', 189),
    (b'\x81f', 190),
    (b'\x83F\x89', 191),
    (b'\x82V\x82', 192),
    (b'\x81l\x80', 193),
]

for (barr, byt) in MAPPINGS:
    rule = expand_rule(barr)
    # print("Was {}, now {}".format(repr(barr), repr(rule)))
    TO_ARRAY[byt] = rule
    TO_BYTE[rule] = byt


import re


def replace_with_byte(mo):
    # print(mo)

    (s, start, end) = mo.string, mo.start(), mo.end()
    # print(s)
    # print(start)
    # print(end)

    s = s[start:end]
    # print(s)

    return bytes([TO_BYTE[bytes(s)]])



def many_to_one(text):
    """
    Source:
    http://stackoverflow.com/questions/15175142/how-can-i-do-multiple-substitutions-using-regex-in-python
    """

    # Create a regular expression from the dictionary keys
    regex_string = b'(' + b"|".join(map(lambda s: re.escape(s), TO_BYTE.keys())) + b')'
    # print(regex_string)
    regex = re.compile(regex_string)

    # For each match, look-up corresponding value in dictionary
    return regex.sub(replace_with_byte, text) 

if __name__ == "__main__": 
    # text = "Larry Wall is the creator of Perl".encode('ascii')
    # text = "When in the Course of human events, it becomes necessary for one people to dissolve the political bands which have connected them with another, and to assume among the powers of the earth, the separate and equal station to which the Laws of Nature and of Nature's God entitle them, a decent respect to the opinions of mankind requires that they should declare the causes which impel them to the separation."

    text = "sYmZCYmIYlZcYlMYmZgYlTYlZqYmFYlZAYlZtYlZtYlZsYmOYlZthYmZbYlJYlFYlNYmZtYlFYlZkYmZqYlZEYlZgYlZGYlZhYlZDKYmQYmZBYlPYmZvYlZjYlHYmFYmZcYlZHYmZiYmZfYlZuYmOYlZOaYlRYmZEYmTYmKYmKYmOYmZfvYlZUYlIYlZdYlUYmZsYmHYlOYlZeYlZIYlZhhYlLYmQYmZtYlPYmZgYmIYmZoYmZlYlZfYlZibYmRYmZCYlSYlVYlIYmZbYmNYmZeYlZEYlZDYlZiYlZsYmZcnYlZUYlPYlMYmZnYmZiYmZdYlZPYmMYlZgYlZGaYmZyYmZyYmZaYlQYlFYmZDYmZuYmZvYlPYlZNYlZtYmZcYlZnYlZGYlZAZCYlLYlPYmPYrOYrOYlZpYlZGYlZvYlZyYmZefYlQYlKYmZEYlZxYlZoYlZOYmNYlZPYlZOtYlGYmQYmZhYlZqYlZhYlZOYlZQYlZyYlZyIYmZgYmZBYmZbYlZzYmZjhYlZdYmQYmPYlZcYlZrYlZfYmMYlZBYmSYmMYmZcaYmHYmZsYlUYlZUYmVYmHYmZEYlZrYmZpYmNYmZidYmZtYlNYmZsYlZkYmZmYmZcYlZfYlZQYlZHbYmQYlJYmZBYlZSYmZlYrOYmZjYlZCYmMYmKZjYlRYmZtYlZcYlHYmIYmVYmVYlGYmQYmZqYmTYlZBYlZpYmMdYlJYlRYlFYmZwYmZyYlZeYmZrYlZvYlZgYlZOYlZmaYlZTYlZDYlZgYlZyYlZIYlZGKYlJYmZgYmZCYlIYmZgYmZDYlVYmTYlZCYlZtYmSYmMYlZFhYlZTYmZsYmZBYlZSYlZdYlSYmZoYlZrYlZEYlZQYlZFYmKYlZRYmZepYlFYlZrYmKYlZzYmZiYmSYlZpUYlRYmZzYlGYlZKYlZLYlZgYlZDYlZDZFYmZtYlRYmZgYmZyYlZeYmZqYlZiYmOYlZuYlZBYmZiYlZoYlZDYmZe".encode('ascii')
    # text = open(sys.argv[1]).read().encode('ascii')
    # text = open("uniwords.txt").read().encode('ascii')
    # text = open("big.txt").read().encode('ascii')

    before = len(text)
    print(repr(text[:30]))
    print(before)

    out = many_to_one(text)
    after = len(out)
    # print(repr(out[:30]))
    print(repr(out))
    print(after)

    diff = before - after
    perc = diff / before
    print("Compressed by {:.2%} ({} bytes saved)".format(perc, diff))

    with open("out.txt", 'wb') as outfile:
        outfile.write(out)
        outfile.flush()
