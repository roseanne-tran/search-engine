import nltk
import os
import pickle
import re
import gui
import json
#nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords,wordnet
from math import log
import file_extractor
import math
from collections import defaultdict


def tokenize_files(dir,index,corpus):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    end = dir.split("/")[-1]
    for filename in os.listdir(dir):
        text, title, h1, h2, h3, bold = file_extractor.get_clean_text(dir + "/" +filename) #Gets the cleaned text from the html file
        matrixvector = defaultdict(int) #How we are going to create our tfidf vector for each document
        #store the title tags and bolded words so we can give a score later
        titlewords = {lemmatizer.lemmatize(lemmatizer.lemmatize(lemmatizer.lemmatize(lemmatizer.lemmatize(t,wordnet.VERB),wordnet.NOUN),wordnet.ADV),wordnet.ADJ) for t in re.split(r"[^a-zA-Z0-9]",title) if len(t) >0}
        tags = {lemmatizer.lemmatize(lemmatizer.lemmatize(lemmatizer.lemmatize(lemmatizer.lemmatize(t,wordnet.VERB),wordnet.NOUN),wordnet.ADV),wordnet.ADJ) for t in re.split(r"[^a-zA-Z0-9]",h1) if len(t) >0}
        for h in re.split(r"[^a-zA-Z0-9]",h2):
            if(len(h) > 0):
                tags.add(lemmatizer.lemmatize(lemmatizer.lemmatize(lemmatizer.lemmatize(lemmatizer.lemmatize(h,wordnet.VERB),wordnet.NOUN),wordnet.ADV),wordnet.ADJ)) 
        for h in re.split(r"[^a-zA-Z0-9]",h3):
            if(len(h) > 0):
                tags.add(lemmatizer.lemmatize(lemmatizer.lemmatize(lemmatizer.lemmatize(lemmatizer.lemmatize(h,wordnet.VERB),wordnet.NOUN),wordnet.ADV),wordnet.ADJ)) 
        bolded = {lemmatizer.lemmatize(lemmatizer.lemmatize(lemmatizer.lemmatize(lemmatizer.lemmatize(t,wordnet.VERB),wordnet.NOUN),wordnet.ADV),wordnet.ADJ) for t in re.split(r"[^a-zA-Z0-9]",bold) if len(t) >0}
        for w in re.split(r"[^a-zA-Z0-9]",text):  
            if(len(w) > 0 and w not in stop_words):
                w = lemmatizer.lemmatize(lemmatizer.lemmatize(lemmatizer.lemmatize(lemmatizer.lemmatize(w,wordnet.VERB),wordnet.NOUN),wordnet.ADV),wordnet.ADJ)
                matrixvector[w] += 1 #incrementing the count in the term frequency matrix
                if(w in index):
                    index[w].add(end+"/"+filename)#add the docID to the posting list in the index
                else:
                    index.update({w:{end+"/"+filename}})
        corpus.update({end+"/"+filename: {"matrix":matrixvector,"title":titlewords, "tags":tags,"bold":bolded}})#adds the document id and the tokenized text so that we have the info for index construction
        


def tf_idf(index,corpus):
    for word in index:
        idf = math.log10(len(corpus)/len(index[word]))#idf is the same for each posting of a word so its outside the for loop
        for doc in index[word]:
            corpus[doc]["matrix"][word] = 1+math.log10(corpus[doc]["matrix"][word])*idf#we calculate the tfidf score and change the tf matrix to a tfidf matrix
    #normalizing the tfidf scores, so that we don't need to do that at query time
    for doc in corpus:
        sum = 0
        for word in corpus[doc]["matrix"]:
            sum += corpus[doc]["matrix"][word]**2#sum to normalize
        for word in corpus[doc]["matrix"]:
            corpus[doc]["matrix"][word] = corpus[doc]["matrix"][word]/math.sqrt(sum)


    
def build_index():
    file_counter = 0
    corpus = {}
    index = {}
    for dir in os.listdir(os.getcwd() + "/WEBPAGES_RAW/"):#lets us get through the entire corpus
        cleandir = os.getcwd() + "/WEBPAGES_RAW/"+ dir
        if(os.path.isdir(cleandir)): 
            tokenize_files(cleandir,index,corpus)
#            print("hi")
#    print("calculating tf-idf")
    tf_idf(index,corpus)#now that we have combined all the indexes we can find the tf-idf for each page
    with open('final.p','wb') as file:
        pickle.dump(index,file)#save our final database in a file
    with open("matrix.p",'wb') as file:
        pickle.dump(corpus,file)#save our matrix in a file
        

if __name__ == "__main__":
    if("final.p" not in os.listdir(os.getcwd())):#if we have already built the database we don't need to do it again so we load it up
        build_index()
    with open('final.p','rb') as file:
        final_index = pickle.load(file)
    with open('matrix.p','rb') as file:
        matrix = pickle.load(file)
    with open(os.getcwd()+"/WEBPAGES_RAW/bookkeeping.json",'r') as file:
        translator = json.load(file)
    print(len(final_index))
    gui.maingui(final_index,matrix,translator)
    
    













