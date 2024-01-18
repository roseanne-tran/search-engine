from collections import defaultdict
import nltk
import re
import math
import lxml.html
from lxml.html.clean import clean_html
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords,wordnet
def get_clean_text(file):
    
    #strings of important html tags
    title = ""
    h1 = ""
    h2 = ""
    h3 = ""
    bold = ""
    
    try:
        with open(file, 'r', encoding="utf-8") as f:
            textcont = f.read()
            html = lxml.html.fromstring(textcont)
            
    except:
        return ("", "", "", "", "", "")
    words = html.text_content()
    
    #get the content in important tags
    for tag in html.xpath("//title"):
        title += tag.text_content()
        title += ""
    for tag in html.xpath("//h1"):
        h1 += tag.text_content()
        h1 += ""
    for tag in html.xpath("//h2"):
        h2 += tag.text_content()
        h2 += ""
    for tag in html.xpath("//h3"):
        h3 += tag.text_content()
        h3 += ""
    for tag in html.xpath("//bold"):
        bold += tag.text_content()
        bold += ""
     
    #return a tuple
    return (words.lower(), title.lower(), h1.lower(), h2.lower(), h3.lower(), bold.lower())


def rank(query,index,matrix):
    dist_dict = {"query":{}}
    query_dict = defaultdict(int)
    docIDs = set()
    cosines = defaultdict(int)
    lemmatizer = WordNetLemmatizer()
    filtered_tokens = [lemmatizer.lemmatize(lemmatizer.lemmatize(lemmatizer.lemmatize(lemmatizer.lemmatize(w,wordnet.VERB),wordnet.NOUN),wordnet.ADV),wordnet.ADJ) for w in re.split(r"[^a-zA-Z0-9]",query) if len(w) > 0]
    #normalizing the query terms
    for word in filtered_tokens:
        query_dict[word] += 1
    sum = 0
    for word in query_dict:
        if(word in index):
            weight = (1+math.log10(query_dict[word]))*math.log10(len(matrix)/len(index[word]))
            sum += weight**2
            dist_dict["query"].update({word: weight})
    for word in dist_dict["query"]:
        dist_dict["query"][word] = dist_dict["query"][word]/math.sqrt(sum)
        docIDs |= index[word]#add the documents we should score   
    #do the dot product
    for doc in docIDs:
        for word in dist_dict["query"]:
            cosines[doc] += (dist_dict["query"][word])*(matrix[doc]["matrix"][word])
            #add a static quality score to the cosine value based on whether the word is in a tag, tile, or bolded
            if(word in matrix[doc]["tags"]):
                cosines[doc] += .1 
            if(word in matrix[doc]["title"]):
                cosines[doc] += .2
            if(word in matrix[doc]["bold"]):
                cosines[doc] += .05 
    if(len(cosines) == 0):
        return []
    return sorted(cosines.keys(), key = (lambda t: -cosines[t]))
    
