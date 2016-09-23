
import base64
import math


CHARS = '''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'''
# CHARS = ''.join(map(chr, range(256)))
# CHARS = ''.join(map(chr, range(128)))
CODE = CHARS[:-4]
SINGLE_ESCAPE = CHARS[-1]
DOUBLE_ESCAPE = CHARS[-2]
TRIPLE_ESCAPE = CHARS[-3]
MULTIPLE_ESCAPE = CHARS[-4]


LONG_STRING = "When in the Course of human events, it becomes necessary for one people to dissolve the political bands which have connected them with another, and to assume among the powers of the earth, the separate and equal station to which the Laws of Nature and of Nature's God entitle them, a decent respect to the opinions of mankind requires that they should declare the causes which impel them to the separation."
TERRIBLE = '''H̡̫̤̤̣͉̤ͭ̓̓̇͗̎̀ơ̯̗̱̘̮͒̄̀̈ͤ̀͡w͓̲͙͖̥͉̹͋ͬ̊ͦ̂̀̚ ͎͉͖̌ͯͅͅd̳̘̿̃̔̏ͣ͂̉̕ŏ̖̙͋ͤ̊͗̓͟͜e͈͕̯̮̙̣͓͌ͭ̍̐̃͒s͙͔̺͇̗̱̿̊̇͞ ̸̤͓̞̱̫ͩͩ͑̋̀ͮͥͦ̊Z̆̊͊҉҉̠̱̦̩͕ą̟̹͈̺̹̋̅ͯĺ̡̘̹̻̩̩͋͘g̪͚͗ͬ͒o̢̖͇̬͍͇͓̔͋͊̓ ̢͈͙͂ͣ̏̿͐͂ͯ͠t̛͓̖̻̲ͤ̈ͣ͝e͋̄ͬ̽͜҉͚̭͇ͅx͎̬̠͇̌ͤ̓̂̓͐͐́͋͡ț̗̹̝̄̌̀ͧͩ̕͢ ̮̗̩̳̱̾w͎̭̤͍͇̰̄͗ͭ̃͗ͮ̐o̢̯̻̰̼͕̾ͣͬ̽̔̍͟ͅr̢̪͙͍̠̀ͅǩ̵̶̗̮̮ͪ́?̙͉̥̬͙̟̮͕ͤ̌͗ͩ̕͡'''

TO_MAP = set(range(256))
AVAILABLE = set(range(256))
PREFERENCE = ''' eEtTaAoOiInNsSrRhHlLdDcCuU\nmMfFpPgGwWyYbB,.vVkK()_;"='-\txX/0$*1jJ:{}>qQ[]2zZ!<?3+5\\4#@|6&987%^~`'''  # http://letterfrequency.org/
REMAP = {}


for (i, char) in enumerate(PREFERENCE):
    REMAP[ord(char)] = i
    TO_MAP.remove(ord(char))

for _ in range(len(TO_MAP)):
    low_to_map = min(TO_MAP)
    low_available = min(AVAILABLE)

    TO_MAP.remove(low_to_map)
    AVAILABLE.remove(low_available)

    REMAP[low_to_map] = low_available


def remap256(nums):
    return (REMAP.get(num, num) for num in nums)


def futzencodenum(num):
    (zs, rem) = divmod(num, len(CODE))
    return SINGLE_ESCAPE * zs + CODE[rem]


def futzencodenum2(num):
    (zs, rem) = divmod(num, len(CODE))
    if zs == 0:
        return CODE[rem]
    elif zs == 1:
        return SINGLE_ESCAPE + CODE[rem]
    elif zs == 2:
        return DOUBLE_ESCAPE + CODE[rem]
    elif zs == 3:
        return TRIPLE_ESCAPE + CODE[rem]
    else:
        return MULTIPLE_ESCAPE + CODE[zs] + CODE[rem]


def futzencode(unicode_string):
    return ''.join(futzencodenum2(c) for c in remap256(unicode_string.encode('utf-8')))


def test(strng):
    enc = futzencode(strng)
    benc = base64.b64encode(strng.encode('utf-8'))
    print()
    print(repr(strng), repr(enc), repr(benc))
    print(len(strng), len(enc), len(benc))

test('test!')
test("tést!")
test(LONG_STRING)
test(TERRIBLE)


########################################

def binifychar(chr):
    n = ord(chr)
    assert 0 <= n < 256
    return "{:>08b}".format(n)


def binify(strng):
    return ''.join(binifychar(c) for c in strng)


def numify(strng):
    return int(binify(strng), 2)


# val = numify('hello')
# print(val)
# print(math.log(val, 2))

# print(numify(LONG_STRING))
