alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
import random
import math
random.seed()

#############################################################
# The following code doesn't need to be edited. It allows
# you to read a text file and store it in a single string, 
# and also to write a single string to a text file. This is
# not an ideal way to work with files, but it will suffice
# for this assignment.
#############################################################

def file_to_string(filename):
    with open(filename, "r") as f:
        x = f.read()
    return x

def string_to_file(filename, s):
    with open(filename, "w") as f:
        f.write(s)

#############################################################
# A working Caesar cipher
#############################################################

def simplify_string(s):
    s = s.upper()
    simplified = ""
    for letter in s:
        if letter in alpha:
            simplified += letter
    return simplified

def num_to_let(x):
    return alpha[x]

def let_to_num(a):
    return alpha.index(a)

def shift_char(char, shift):
    charnum = let_to_num(char)
    shiftnum = let_to_num(shift)
    outputnum = (charnum + shiftnum) % 26
    return num_to_let(outputnum)

def unshift_char(char, shift): #Reverses the shift_char operation; useful as a helper function to the Caesar and Vigenere decryption operations.
    charnum = let_to_num(char)
    shiftnum = let_to_num(shift)
    outputnum = (charnum - shiftnum) % 26
    return num_to_let(outputnum)

def caesar_enc(plain, key):
    encrypted = ""
    for letter in plain:
        encrypted += shift_char(letter, key)
    return encrypted

def caesar_dec(cipher, key):
    decrypted = ""
    for letter in cipher:
        decrypted += unshift_char(letter, key)
    return decrypted

#############################################################
# Breaking the Caesar cipher
#############################################################

def letter_counts(s):
    counts = {}
    for letter in alpha:
        counts[letter] = 0
    for letter in s:
        counts[letter] += 1
    return counts

def normalize(counts):
    total = 0
    for item in counts:
        total += counts[item]
    for item in counts:
        counts[item] = (counts[item] / total)

english_freqs = letter_counts(simplify_string(file_to_string("twocities_full.txt")))
normalize(english_freqs)

def distance(observed, expected):
    distsum = 0
    for letter in alpha:
        lettdist = ((observed[letter] - expected[letter]) ** 2) / expected[letter]
        distsum += lettdist
    return distsum

def caesar_break(cipher, frequencies):
    acounts = letter_counts(caesar_dec(cipher, 'A'))
    normalize(acounts)
    bestmatchdistance = distance(acounts, frequencies)
    bestmatch = 'A'
    for letter in alpha:
        counts = letter_counts(caesar_dec(cipher, letter))
        normalize(counts)
        if distance(counts, frequencies) < bestmatchdistance:
            bestmatchdistance = distance(counts, frequencies)
            bestmatch = letter
    return [bestmatch, caesar_dec(cipher, bestmatch)]

#############################################################
# A working Vigenere cipher
#############################################################

def vigenere_enc(plain, key):
    encrypted = ""
    i = 0
    length = len(key)
    while i < len(plain):
        encrypted += shift_char(plain[i], key[i % length])
        i += 1
    return encrypted

def vigenere_dec(cipher, key):
    decrypted = ""
    i = 0
    length = len(key)
    while i < len(cipher):
        decrypted += unshift_char(cipher[i], key[i % length])
        i += 1
    return decrypted

#############################################################
# Breaking the Vigenere cipher
#############################################################

def split_string(s, parts):
    split = []
    i1 = 0
    while i1 < parts:
        i2 = i1
        i1string = ""
        while i2 < len(s):
            i1string += s[i2]
            i2 += parts
        split.append(i1string)
        i1 += 1
    return split

def vig_break_for_length(cipher, klen, frequencies):
    key = ""
    split = split_string(cipher, klen)
    for s in split:
        key += caesar_break(s, frequencies)[0]
    return [key, vigenere_dec(cipher, key)]

def vig_break(c, maxlen, frequencies):
    if maxlen > len(c):
        maxlen = len(c)
    onecounts = letter_counts(vig_break_for_length(c, 1, frequencies)[1])
    normalize(onecounts)
    bestmatchdistance = distance(onecounts, frequencies)
    bestmatch = vig_break_for_length(c, 1, frequencies)[0]
    i = 2
    while i <= maxlen:
        counts = letter_counts(vig_break_for_length(c, i, frequencies)[1])
        normalize(counts)
        if distance(counts, frequencies) < bestmatchdistance:
            bestmatchdistance = distance(counts, frequencies)
            bestmatch = vig_break_for_length(c, i, frequencies)[0]
        i += 1
    return [bestmatch, vigenere_dec(c, bestmatch)]

#############################################################
# A working substitution cipher
#############################################################

def sub_gen_key():
    key = ""
    while len(key) < 26:
        nextletter = alpha[random.randint(0,25)]
        if nextletter not in key:
            key += nextletter
    return key

def sub_enc(s, k):
    map = {}
    encrypted = ""
    i = 0
    while i < 26:
        map[alpha[i]] = k[i]
        i += 1
    for letter in s:
        encrypted += map[letter]
    return encrypted

def sub_dec(s, k):
    map = {}
    decrypted = ""
    i = 0
    while i < 26:
        map[k[i]] = alpha[i]
        i += 1
    for letter in s:
        decrypted += map[letter]
    return decrypted

#############################################################
# Breaking the substitution cipher
#############################################################

def count_trigrams(s):
    counts = {}
    i = 0
    while i < (len(s) - 2):
        trigram = s[i]+s[i+1]+s[i+2]
        if trigram in counts:
            counts[trigram] += 1
        else:
            counts[trigram] = 1
        i += 1
    return counts

english_trigrams = count_trigrams(simplify_string(file_to_string("twocities_full.txt")))
normalize(english_trigrams)

def map_log(d):
    for trigram in d:
        d[trigram] = math.log(d[trigram])

map_log(english_trigrams)

def trigram_score(s, english_trigrams):
    score = 0
    strigrams = count_trigrams(s)
    for trigram in strigrams:
        if trigram in english_trigrams:
            score += (english_trigrams[trigram] * strigrams[trigram])
        else:
            score -= (15 * strigrams[trigram])
    return score

def sub_break(cipher, english_trigrams):
    def keyswap(k):
        swap1 = random.randint(0,25)
        swap2 = random.randint(0,25)
        while swap2 == swap1:
            swap2 = random.randint(0,25)
        newkey = ""
        i = 0
        while len(newkey) < 26:
            if i == swap1:
                newkey += k[swap2]
            elif i == swap2:
                newkey += k[swap1]
            else:
                newkey += k[i]
            i += 1
        return newkey
    bestkey = sub_gen_key()
    initdec = sub_dec(cipher, bestkey)
    bestscore = trigram_score(initdec, english_trigrams)
    i = 0
    while i < 1000:
        i += 1
        testkey = keyswap(bestkey)
        newdec = sub_dec(cipher, testkey)
        if trigram_score(newdec, english_trigrams) > bestscore:
            bestscore = trigram_score(newdec, english_trigrams)
            bestkey = testkey
            i = 0
    return [bestkey, sub_dec(cipher, bestkey)]