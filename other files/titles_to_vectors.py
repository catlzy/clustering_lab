import re
from stopwords import *

# Returns dictionary of word counts for a text
def get_word_counts(text, all_words):
    wc={}
    words = get_words(text)
    # Loop over all the entries

    for word in words:
        if (word not in stopwords) and (word in all_words):
            wc[word] = wc.get(word,0)+1

    return wc


# splits text into words
def get_words(txt):
    # Split words by all non-alpha characters
    words=re.compile(r'[^A-Z^a-z]+').split(txt)

    # Convert to lowercase
    return [word.lower() for word in words if word!='']


# converts counts into a vector
def get_word_vector(word_list, wc):
    v = [0]*len(word_list)
    for i in range(len(word_list)):
        if word_list[i] in wc:
            v[i] = wc[word_list[i]]
    return v


# prints matrix
def print_word_matrix(docs):
    for d in docs:
        print (d[0], d[1])


if __name__ == '__main__':
    file_name = "titles.txt"
    f = open(file_name, "r", encoding="utf-8")
    out = open(file_name.split('.')[0] + "_vectors.txt", "w")

    # load all docs into in-mem list
    # where each element is a list of [doc_id,line]
    docs = []
    doc_id = 1
    all_words = {}

    # transfer content of a file into a list of lines
    lines = [line for line in f]

    # create a dictionary of all words and their total counts
    for line in lines:
        doc_words = get_words(line)
        for w in doc_words :
            if w not in stopwords:
                all_words[w] = all_words.get(w,0)+1

    all_words_clean = set()
    for w, count in all_words.items():
        if all_words[w] > 1 :
            all_words_clean.add(w)


    for line in lines:
        docs.append(["d"+str(doc_id), get_word_counts(line,all_words_clean)])
        doc_id += 1
    print_word_matrix(docs)

    all_words = list(all_words_clean)
    print(all_words)

    for w in all_words:
        out.write('\t' + w)
    out.write('\n')

    # print_word_matrix(docs)
    for i in range(len(docs)):
        docs[i][1] = get_word_vector(all_words, docs[i][1])
        out.write(docs[i][0])
        for x in docs[i][1]:
            out.write('\t' + str(x))
        out.write('\n')

    # print_word_matrix(docs)





