from tesserocr import PyTessBaseAPI
import pickle
import sys
import numpy as np


image = sys.argv[1]

with PyTessBaseAPI() as api:
    api.SetImageFile(image)
    text = api.GetUTF8Text()

# print(text)

ingredients = pickle.load(open("./static/data/ingredients", "rb"))

def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    return (matrix[size_x - 1, size_y - 1])

def get_items(text):
    def match(word, ingredient):
        i = 0
        j = 0
        while i!=len(word) and j!=len(ingredient):
            if word[i]==ingredient[j]:
                i+=1
                j+=1
            elif ingredient[j] in 'aeiou ':
                j+=1
            else:
                return False
        if i==(len(word)-1) and word[i]=='s':
            i+=1
        if j==(len(ingredient)-1) and ingredient[j]=='s':
            j+=1
        if i==len(word) and j==len(ingredient):
            return True
    def check_words(line):
        return "total" not in line and "card" not in line and "change" not in line
    def convert(line):
        line = line.lower()
        for a in ".,-$'%:[]()*&^#@!":
            line = line.replace(a, '')
        return line
    text = [convert(line) for line in text.split("\n") if line!=""]
    text = [line for line in text if line.isdigit()==False and check_words(line)==True]
    
    items = []
    for line in text:
        words = [word for word in line.split(" ") if len(word)>3]
        combos = []
        for a in range(len(words)):
            for b in range(a, len(words)):
                temp = " ".join(words[b-a:b+1])
                combos.insert(0, temp)
        answer = False
        for combo in combos:
            if answer!=False:
                break
            for ingredient in ingredients:
                if match(combo, ingredient):
                    answer = ingredient
                    break
        if answer==False:
            min_dist = 3
            for combo in combos:
                for ingredient in ingredients:
                    dist = levenshtein(combo, ingredient)
                    if dist<min_dist:
                        min_dist = dist
                        answer = ingredient
        if answer!=False:
            items.append(answer)
    return items       
                    
items = [item for item in get_items(text) if item!=""]
# print("-"*30)
for item in items:
    print(item)
