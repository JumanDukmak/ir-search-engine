from collections import defaultdict


def calculate_precision_at_10(retrieved, relevant, k=10):
    #retrieved= retrieved[:k]
    relevant_set = set(relevant)
    true_positives = len([doc for doc in retrieved if doc in relevant_set])
    return true_positives / k


def calculate_recall_at_10(retrieved, relevant, k=10):
    retrieved_at_k = retrieved
    relevant_set = set(relevant)
    true_positives = len([doc for doc in retrieved_at_k if doc in relevant_set])
    return true_positives / len(relevant_set)


def calculate_reciprocal_rank(retrieved, relevant):
    relevant_set = set(relevant)
    for index, doc in enumerate(retrieved):
        if doc in relevant_set:
            return 1 / (index + 1)
    return 0

def calculate_average_precision_at_10(retrieved, relevant, k=10):

    relevant_set = set(relevant)
    precision_at_i = 0.0
    num_of_relevant_found = 0.0

    for i, doc in enumerate(retrieved):
        if doc in relevant and doc not in retrieved[:i]:
            num_of_relevant_found += 1.0
            precision_at_i += num_of_relevant_found / (i + 1.0)

    return precision_at_i / min(10, len(relevant_set))

#-------------------------------------------------------------------------------#



################## this function to calculate metrices #########################3 
def all_metrices(tfidf_matrix,tifidfObj,corpus,queries,qrel):

    queries = queries

    actual_relevant_docs = qrel # this is from qrels  
    
    sum_of_rr = 0.0
    sum_of_aps = 0.0
    query_precision={}
    query_recall={}
    
    i=0
    for query_id in queries.keys():
        
            print(i)
            predicted_result=matching_and_ranking(queries[query_id],tfidf_matrix,tifidfObj,corpus)
            relevant_docs = actual_relevant_docs[query_id]   

            # print("Q",queries[query_id])
            # print("__________________________________________")
            # print("retrieved FROM EVAL ",predicted_result)
            # print("relevant_set FROM EVAL",relevant_docs)
            # print("========================================")
       
            # precision = calculate_precision_at_10(predicted_result, relevant_docs)
            # query_precision[query_id]=precision

            # # #------------------------------------------------------------------------------------------#

            # recall = calculate_recall_at_10(predicted_result, relevant_docs)
            # query_recall[query_id]=recall

            # #------------------------------------------------------------------------------------------#

            rr = calculate_reciprocal_rank(predicted_result,relevant_docs)
            sum_of_rr  += rr

            # #------------------------------------------------------------------------------------------#
            ap = calculate_average_precision_at_10(predicted_result,relevant_docs)
            sum_of_aps += ap
            i+=1
        # print("queryID",query_id)
        # print("rr",rr,"mrr",sum_of_rr)
    
    mrr = sum_of_rr / len(queries)
    map=sum_of_aps / len(queries)
    print(f"Mean Reciprocal Rank at 10: {mrr:.2f}")
    print(f"Mean Average Precision at 10: {map:.2f}")
    print("precision at 10:", query_precision)
    print("recall at 10",query_recall)
    


    
