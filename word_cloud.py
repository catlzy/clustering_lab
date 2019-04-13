from __future__ import print_function
import csv
from nltk.corpus import stopwords
import pygame
import simplejson
from pytagcloud import create_tag_image, make_tags

warned_of_error = False

def create_cloud (oname, words,maxsize=60, fontname='Lobster'):
    '''Creates a word cloud (when pytagcloud is installed)
    Parameters
    ----------
    oname : output filename
    words : list of (value,str)
    maxsize : int, optional
        Size of maximum word. The best setting for this parameter will often
        require some manual tuning for each input.
    fontname : str, optional
        Font to use.
    '''

    # gensim returns a weight between 0 and 1 for each word, while pytagcloud
    # expects an integer word count. So, we multiply by a large number and
    # round. For a visualization this is an adequate approximation.


    #words = [(w,int(v*10000)) for w,v in words]
    tags = make_tags(words, maxsize=maxsize)
    create_tag_image(tags, oname, size=(1800, 1800), fontname=fontname)


def count_words(vector, name):
    word_counts = {}
    with open('dimensions_keywords.csv') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        index = -1
        for row in csvreader:
            if index != -1:
                high = row[1]
                low = row[2]
                high_words = high.split()
                low_words = low.split()

                for w in high_words:
                    if w not in word_counts:
                        word_counts[w] = [0,0]
                    word_counts[w][1] += 1
                    word_counts[w][0] += vector[index]
                for w in low_words:
                    if w not in word_counts:
                        word_counts[w] = [0,0]
                    word_counts[w][1] += 1
                    word_counts[w][0] += 100-vector[index]
            index += 1

    word_counts = [(w,count[0]/count[1]) for w,count in word_counts.items()]
    create_cloud(name + '.png', word_counts)
