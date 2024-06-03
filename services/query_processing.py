from typing import List
import string
import pandas as pd
import re
import aiohttp
from typing import Dict
import pickle
import base64
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from services.data_preprocessing import custom_tokenizer,custom_preprocessor
from dependencies import call_post_external_service



def query_preprocessor(query:str,online:bool):
    x=custom_preprocessor(query)
    query_term =custom_tokenizer(x,online)
    return query_term

#-----------------------------------------------------------------#

async def create_query_vectorizer(query:str,dataset:str,online:bool):
    
    # print("IN SERVICE QUERY PREPROCESSING")
    processed_query = query_preprocessor(query,online)
    # print("QUERY AFTER PROCESSING",processed_query)

    # API CALL  TO  GET QUERY VECTORE
    response = await call_post_external_service(endpoint="vectorize_query",data={ "dataset": dataset,"query_term":processed_query})
    vector  =   response['data']

    #print("RESULT INSIDE SERVICE vector",vector)

    return vector , processed_query

