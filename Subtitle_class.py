from collections import defaultdict, Counter
import random
import json
from numpy import array, argsort, unique
# This class stores a single subtitle with start and end time. 
# Methods can change time format.
class sub():
    def __init__(self, words = [], start = 0, end = 0):
        self.words = words
        self.length = len(words)
        self.start = start
        self.end = end
        self.duration = end - start

    def add(self, word):
        self.words.append(word)
        self.length = len(self.words)

    def frameToSec(self, fps = 25):
        self.start = self.start/fps
        self.end = self.end/fps
        self.duration = self.end - self.start

    def secToFrame(self, fps = 25):
        self.start = self.start*fps
        self.end = self.end*fps
        self.duration = self.end - self.start

# This class stores a set of subtitles. Methods:
# readUT reads in a subtitle from an .srt file.
# make_sigMatrix makes the sigMatrix (from learned subtitles)
# make_folMatrix makes the folMatrix (from new subtitles and the sigMatrix)
class Subtitles:
    def __init__(self, name = ""):
        self.name = name
        self.subtitle = []
        self.length = len(self.subtitle)

    def readUT(self, path): # subtitle aus .srt Datei einlesen
        with open(path) as file:
            UT_raw = file.read()
        UT = [] # Liste fuer formatierten Untertiteln
        lines = []
        countwords = []
        for i in UT_raw.split("\n"):
            if i != '': lines.append(i) # Untertitel sammeln
            elif lines == []: continue
            else: # Untertitel formatieren und in UT einfügen
                t_start_ = lines[1].replace(",",".").split(" --> ")[0].split(":")
                t_start = 60*60*int(t_start_[0])+60*int(t_start_[1])+float(t_start_[2])
                t_end = lines[1].replace(",",".").split(" --> ")[1].split(":")
                t_end = 60*60*int(t_end[0])+60*int(t_end[1])+float(t_end[2])
                words = ' '.join(lines[2:]).lower()
                for s in ',;":.!?-&':
                    words = words.replace(s, "")
                words = words.lower().split(" ")
                countwords.extend(words)
                UT.append(sub(words, t_start, t_end))
                lines = []
        self.countlist = countwords
        #countlist = Counter(countwords).most_common(10)
        #print(countlist)
        
        # Einsetzen
        self.name = path.split("/")[-1].replace(".srt","")
        self.subtitle = UT
        self.length = len(UT)
        
    def word_follow_significance(self, word1, word2, else_value = 0, very_important_value = 0, important_value = 0, unimportant_value = 0, very_important_words = "", important_words = "", unimportant_words = ""):
        y = else_value
        very_important = very_important_words
        important = important_words
        unimportant = unimportant_words
        if word1 in very_important or word2 in very_important: y = very_important_value
        if word1 in important or word2 in important: y = important_value
        if word1 in unimportant or word2 in unimportant: y = unimportant_value
        return(y)

    def make_sigMatrix(self, else_value = 0, very_important_value = 0, important_value = 0, unimportant_value = 0, very_important_words = [""], important_words = [""], unimportant_words = [""]):
        sigMatrix = defaultdict(Counter)
        last = sub()
        for current in self.subtitle:
            for word1 in last.words:
                for word2 in current.words:
                    sigMatrix[word1][word2] += self.word_follow_significance(word1, word2, else_value, very_important_value, important_value, unimportant_value, very_important_words, important_words, unimportant_words)
            last = current
        return [sigMatrix, self.name]

    def make_folMatrix(self, sigMatrix, write = 1):
        filename = "folMatrix_{}-{}.txt".format(self.name, sigMatrix[1])
        #try:
        #    with open(filename, 'r') as in_file:
        #        folMatrix = json.load(in_file)
        #    print("\nUsing saved follow Matrix", filename)
        #except:
        #    def follow_sign(ut1, ut2):
        #        return(sum([sigMatrix[0][word1][word2] for word1 in ut1.words for word2 in ut2.words]))
        #    print("\nstart making folmatrix")
        #    folMatrix = [[follow_sign(ut1, ut2)/(ut1.length+ut2.length)
        #                  for ut2 in self.subtitle] for ut1 in self.subtitle]
        #    print("end making folmatrix")
        #    for i,j in enumerate(folMatrix): folMatrix[i][i] = -1
        #    if write == 1:
        #        with open(filename, 'w') as out_file:
        #            json.dump(folMatrix, out_file)
        if write == 0:
            with open(filename, 'r') as in_file:
                folMatrix = json.load(in_file)
            print("\nUsing saved follow Matrix", filename)
        if write == 1:
            def follow_sign(ut1, ut2):
                return(sum([sigMatrix[0][word1][word2] for word1 in ut1.words for word2 in ut2.words]))
            print("\nstart making folmatrix")
            folMatrix = [[follow_sign(ut1, ut2)/(ut1.length+ut2.length)
                          for ut2 in self.subtitle] for ut1 in self.subtitle]
            print("end making folmatrix")
            for i,j in enumerate(folMatrix): folMatrix[i][i] = -1
            with open(filename, 'w') as out_file:
                json.dump(folMatrix, out_file)
        return folMatrix

# Nachfolger-Funktion
def findfollowers(x, folMatrix):
    sig = max(folMatrix[x])
    best_uts = [i for i,j in enumerate(folMatrix[x]) if j == sig]
    new_x = random.choice(best_uts)
    folMatrix[x] = [-1 for i in range(len(folMatrix))]
    for r,s in enumerate(folMatrix[x]):
        folMatrix[r][x] = -1
    return([sig, new_x])

# Funktion zum Erstellen der neuen Filmabfolge
def make_seq(newname, learnname, write = 1, else_value = 0, very_important_value = 0, important_value = 0, unimportant_value = 0, very_important_words = [""], important_words = [""], unimportant_words = [""]):
    learn = Subtitles()
    learn.readUT(learnname)
    sigMatrix = learn.make_sigMatrix(else_value, very_important_value, important_value, unimportant_value, very_important_words, important_words, unimportant_words)
    new = Subtitles()
    new.readUT(newname)
    folMatrix = new.make_folMatrix(sigMatrix, write)
    # Filmabfolge
    x = 0 # start
    sequenz = [x]
    sig = []
    # for i in range(10):
    while True:
        ff = findfollowers(x, folMatrix)
        if ff[0]<0: break
        sig.append(ff[0])
        sequenz.append(ff[1])
        x = ff[1]
    # Output
    print("Neues Material: {}".format(new.name) +
    "\nLernmaterial: {}".format(learn.name) +
    "\nDie Filmabfolge besteht aus {} von {} Szenen.".format(str(len(sequenz)),new.length))
    return(sequenz, sig)
