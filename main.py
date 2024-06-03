from typing import Union
from fastapi import FastAPI, Request, HTTPException
from typing import Dict
import pickle
import json
import numpy as np
import base64
import scipy.sparse as sp
from services.data_preprocessing import custom_tokenizer,custom_preprocessor
from services.data_representation import get_corpus,get_documents
from services.indexing import create_document_term_matrix , get_dtm ,get_tfidf_vectorizer,create_query_vector,get_indexing_terms
from services.query_processing import create_query_vectorizer
from services.matching_and_ranking import matching_and_ranking
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

#=========================== ADD MIDDLEWARE TO ALLOW CORS ===============================#
# Add a middleware to allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
#=========================== DATA REPRESENTATION API ===============================#
@app.get("/corpus")
async def read_corpus(dataset:str):
    try:

        # call function from service file
        result_dict =  get_corpus(dataset)
        return result_dict

    except Exception as e:
        return {"error":str(e)}

#============================== TEXT PREPORCESSING API ===============================#
@app.post("/process_text")
async def process_text(request: Request):
    try:

        body = await request.json()
        text = body.get("text", "")

        preprocessed_text = custom_preprocessor(text)
        tokenized_text = custom_tokenizer(preprocessed_text)
        
        return {"message":"Success","data": tokenized_text}

    except Exception as e:
        return {"error": str(e)}

#================================= INDEXING API ===========================================#

@app.post("/create_index")
async def build_index(request: Request):

    try:

        body = await request.json()
        dataset = body.get("dataset", "") 

        # call function from service
        await create_document_term_matrix(dataset)

        return {"message": "End Creating Index" ,"data":""}

    except Exception as e:
        return {"error": str(e) }
#------------------------------------------------------------------------#
@app.get("/get_dtm")
async def get_document_term_matrix(dataset:str):
    try:
        
        # call function from service
        tfidf_matrix = get_dtm(dataset)
        #print("DTM BEFORE BASE64",tfidf_matrix)

        # serialize csr_matrix & encode to Base64 so i can send it in json
        serialized_matrix = pickle.dumps(tfidf_matrix)
        base64_encoded_dtm = base64.b64encode(serialized_matrix).decode('utf-8')

        return {"message": "Success " , "data": base64_encoded_dtm}

    except Exception as e:
        return {"error": str(e)}
#------------------------------------------------------------------------#
@app.get("/get_terms")
async def get_vocabularies(dataset:str):
    print("test")
    try:

        # call function from service
        terms = get_indexing_terms(dataset)

        # dict:{ "software": 2, "engineering": 0, "index": 1}
        return terms

    except Exception as e:
        
        return {"error": str(e)}
#------------------------------------------------------------------------#
@app.post("/vectorize_query")
async def build_query_vector(request:Request):
    try:

        body = await request.json()
        dataset = body.get("dataset", "")
        query_term = body.get("query_term", "") 

        # call function from service
        vector = create_query_vector(dataset,query_term)
        
        print("QUERY VECTORE BEFORE BASE64",vector)

        # serialize csr_matrix & encode to Base64 so i can send it in json
        serialized_query_vector = pickle.dumps(vector)
        base64_encoded_vector = base64.b64encode(serialized_query_vector).decode('utf-8')

        return {"message":"success","data":base64_encoded_vector}

    except Exception as e:
        return {"error": str(e)}


#================================== Query Processing API ========================================#
@app.get('/process_query')
async def get_processed_query(dataset:str,query:str,online:bool):

    print("form api")
    try:
        # call function from service
        vector , processed_query = await create_query_vectorizer(query,dataset,online)
    
        return {"message": "Success" , "vector": vector ,"processed_query_term": processed_query }

    except Exception as e:
        return {"error": str(e)}

#============================== Matching & Ranking API ========================================#
@app.get('/ranking')
async def get_ranked_doc(dataset:str,query:str):

    print("from rank")
    try:
        # call function from service
        docs_ids = await matching_and_ranking(query,dataset,False)
        print("doc id: ", docs_ids)
        return {"message": "Success" ,"data": docs_ids }

    except Exception as e:
        return {"error": str(e)}

#================================ SEARCH : ONLINE QUERY  ===================================#
@app.get('/search')
async def online_query(dataset:str,query:str):

    try:
        #call functions from services
        docs_ids = await matching_and_ranking(query,dataset,online=True)

        docs_content= get_documents(dataset,docs_ids)
        print("docs: ", docs_content)
        return {"message": "نتائج البحث" ,"data": docs_content }

    except Exception as e:
        return {"error": str(e)}


