from typing import List
import string
import pandas as pd
import re
import numpy as np
from scipy.sparse import csr_matrix
from dependencies import call_external_service
import pickle
from fastapi import Request, HTTPException
from typing import Dict
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from services.data_preprocessing import custom_tokenizer,custom_preprocessor

async def create_document_term_matrix(dataset:str):
    
    #print(">> IN Indexing Service")
        
    try:
        # CALL API TO GET DATA FROM DATABASE
        corpus = await call_external_service("corpus",{"dataset":dataset})
        

        # #we have to tell this function the way that we want to clean our data to not use the its default
        print("start createing TfidfVectorizer")
        tfidf_vectorizer = TfidfVectorizer(tokenizer=custom_tokenizer, preprocessor=custom_preprocessor)
        print("end createing TfidfVectorizer")

        print("start createing DTM")
        # # the output will be sparse matrix
        tfidf_matrix = tfidf_vectorizer.fit_transform(corpus.values())
        print("end creating DTM")

        print("end creating file1")

        with open('index_store/'f'{dataset}_tfidf_vectorizer_object.pkl', 'wb') as file:
            pickle.dump(tfidf_vectorizer, file)

        print("end creating file1")

        # start save dtm to file
        print("end creating file2")

        with open('index_store/'f'{dataset}_dtm.pkl', 'wb') as file:
            pickle.dump(tfidf_matrix, file)

        print("end creating file2")
        

    except Exception as e:
            return {"error": str(e) }

#------------------------------------------------------------------------#
def get_tfidf_vectorizer(dataset:str):

    print("From service function TO LOAD FILE")
    try:
        
        with open('index_store/'f'{dataset}_tfidf_vectorizer_object.pkl', 'rb') as file:
            tfidf_vectorizer = pickle.load(file)

    
        return tfidf_vectorizer
    
    except Exception as e:
            return {"error": str(e)}

#------------------------------------------------------------------------#

def get_dtm(dataset:str):

    #print(">> LOAD DTM")
    # load the DTM object from the file
    with open('index_store/'f'{dataset}_dtm.pkl', 'rb') as file:
            tfidf_matrix = pickle.load(file)

    #print("DTM FROM SERVICE",tfidf_matrix)
    return tfidf_matrix

#---------------------------------------------------------------------#
def create_query_vector(dataset:str,query_terms:list):
    

    vectorizer= get_tfidf_vectorizer(dataset)

    vector=vectorizer.transform([' '.join(query_terms)])

    return vector
#-------------------------------------------------------------------------#
def get_indexing_terms(dataset:str):

    vectorizer= get_tfidf_vectorizer(dataset)
    terms = vectorizer.vocabulary_

    return terms
#------------------------------------------------------------------------#
