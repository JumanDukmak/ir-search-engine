from dependencies import call_external_service,call_post_external_service
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from services.indexing import get_tfidf_vectorizer , get_dtm
import pickle
import base64
import shelve
import time

async def dtm_matched_doc(query_terms,dataset):
    # CALL API TO GET INDEX TERMS & GET DTM 
    terms= await call_external_service("get_terms",params= {"dataset":dataset})
    print("TERMS_________",terms)

    response = await call_external_service("get_dtm",{"dataset":dataset})

    # decode to get the sparse matrix
    tfidf_matrix= pickle.loads(base64.b64decode(response['data'])) 

    
    # this will give index of term (that i get from query) in dtm 
    term_indices = [terms[term] for term in query_terms if term in terms]


    # this will give me the docs(index of docs in dtm) that contains this terms 
    matching_docs = set()
    for term_index in term_indices:
        matching_docs.update(tfidf_matrix[:, term_index].nonzero()[0])
            

    # this will give the index of docs inside the dtm
    matching_docs = list(matching_docs)

    # extract from dtm only the docs vectores that contain same term that appear in query
    submatrix = tfidf_matrix[matching_docs, :]

    # link between doc-id and doc-index in dtm
    index_mapping = {i: matching_docs[i] for i in range(submatrix.shape[0])}

    # this will retrun sub dtm 
    return submatrix , index_mapping

#-----------------------------------------------------------------------------------------------#

async def matching_and_ranking(query:str,dataset:str,online:bool):
    

    #print("FROM RANKING AND MATCHING SERVICE",type(online))
    online_str = str(online).lower()

    # API CALLS TO QUERY PREPROCESSOR 
    response1 = await call_external_service("process_query",params= {"dataset":dataset ,"query":query,"online":online_str})

    # decode to get the sparse matrix
    query_vector =pickle.loads(base64.b64decode(response1['vector']))

    processed_query =  response1['processed_query_term']

    print("Response1 query_vector",query_vector)
    print("Response1 processed_query_term",processed_query)

    corpus = await call_external_service("corpus", params={"dataset":dataset})

    # print("Response2 corpus",corpus)
    # print("Response2 corpus KEY",corpus.keys())
    # print("Response2 corpus VALUE",corpus.values())

    docs_tfidf_matrix ,index_mapping = await dtm_matched_doc(processed_query,dataset)
    
    #Calculate cosine similarity between the query vector and the matched doc where there are terms
    top_K_documents = []
    if docs_tfidf_matrix.nnz > 0:
                
        cosine_similarities = cosine_similarity(query_vector, docs_tfidf_matrix)

        top_ten_indices = np.argsort(-cosine_similarities[0])[:10]
            
        top_ten_doc_ids = [index_mapping[index] for index in top_ten_indices]
                    
        top_K_documents = [list(corpus.keys())[i] for i in top_ten_doc_ids]

        
    return top_K_documents