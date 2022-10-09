from re import A
import string
import unicodedata
from textwrap import wrap
import numpy as np


matrix = np.empty((5,5), dtype=str)


def encoding(text):
    text = unicodedata.normalize('NFD', text)
    text = u"".join([c for c in text if not unicodedata.combining(c)])
    return text


def lowerAndPunctuation(text):
    text.translate(str.maketrans('', '', string.punctuation))
    text = str.lower(text)
    return text


def normalizeText(text):
    text = lowerAndPunctuation(text)
    text = encoding(text)
    text = text.replace(" ", "")
    text = text.replace("i", "y")
    return text


def checkDuplicates(text):
    p=""
    for i in text:
        if i not in p:
            p += i
    return p


def storeStringInMatrix(text):
    alphabet = string.ascii_lowercase
    alphabet = alphabet.replace("i", "y")
    for i in alphabet:
        if i not in text:
            text += i
    # print(text)
    # print(len(text))
    list(text)

    k = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] = text[k]
            k += 1
    return matrix


def encode():
    OT = "Dneska je venku chladno"
    ST = list()
    OT = normalizeText(OT)
    ot = [OT[i:i + 2] for i in range(0, len(OT), 2)]
    klic = "Anakondí ocas"
    klic = normalizeText(klic)
    klic = checkDuplicates(klic)
    storeStringInMatrix(klic)
    n = len(ot)
    for k in ot:
        if n%2 == 0:
            a = k[0:n//2]
            b = k[n//2:]
    for i in range(len(matrix)):
            for j in range(len(matrix)):
                print(i, j, end=" ")
                if a[i] == b[i]:
                    ST = ST.append(a[i, (j+1)%5])
                elif a[j] == b[j]:
                    ST = ST.append(a[(i+1)%5, j])
                elif a[i] != b[i] and a[j] != b[j]:
                    ST = ST.append(a[i, b[j]])
                    ST = ST.append(b[i, a[j]])

    print(ST)

            
   


# text = "Anakondí ocas"
# text = normalizeText(text)
# print(text)
# upravenyText = checkDuplicates(text)
# print(upravenyText)
# storeStringInMatrix(upravenyText)

encode()

print(matrix)