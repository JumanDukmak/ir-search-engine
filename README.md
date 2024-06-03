# Information Retrieval System

***

A university project that uses two datasets from [ir-datasets](https://ir-datasets.com/) and build a search engine on them using Python and FastApi.

## Datasets

- [**Lifestyle**](https://ir-datasets.com/lotte.html#lotte/lifestyle/dev).

- [**Wikir**](https://ir-datasets.com/wikir.html#wikir/en1k/training).
## Branches

In this project, we juse use the main branch and represents the main and stable features of our code.

The purpose of each branch is as follows:

- [**main branch**](https://github.com/Rana-Aldahhan/ir-search-engine): This branch represents the main stable requirements of the search engine system.


## How to run the project?

Install required packages. 

Run indexing.py file for the first time to set the database on your device.

Run main.py file then you can access any service by you localhost:YOUR-PORT/SERVICE-ENDPOINT


## Services


- **Search**:

Performs search query and get full documnents results based on passed query and dataset passed.

the following APIs runs the search service on our project:

    - GET: //search?dataset="lifestyle_corpus/wikir"&query="YOUR-QUERY"

- **Text Processing**:

The implemented text processing steps are tow main steps:

- **Preprocessor**:
  
1. **Lowerization**


2. **Expand Contractions**


3. **Remove Html and Links**

- **Tokenizer**:

1. **Tokenizing**


2. **Cleaning**


3. **Filtration**


4. **Normalize dates**


5. **Normalize countries**


6. **Lemmatization**


the following API runs the text processing service:

    - POST: /process_text"

          body : {text : "YOUR-TEXT"}

- **Maching and Ranking**:

In this step, the existing terms resulting from processed query are matched with the indexing terms in order to obtain the docs that contain the terms found in the query, then performs a query search and returns ranked documents. 

the following API runs the Ranking service:

    - GET: /ranking?dataset="lifestyle-copus/wikir"&query="YOUR-QUERY"

- **Get Indexing Terms**:

Gets the terms. 

the following API runs the Get Inverted Index service:

    - GET: /get_terms?dataset="lifestyle_corpus/wikir"

- **Create Index**:

Creates the inverted index for the given dataset. 

the following API runs the Create Inverted Index service:

    - POST: /create_index

        body : {dataset : "lifestyle-copus/wikir"}

- **Get Document Vector**:

Gets the document vector matrix for the given document and dataset. 

the following API runs the Get Document Vector service:

    - GET: /get_dtm?dataset="lifestyle-copus/wikir"

- **Get Query TF-IDF**:

Calculates the query TF-Idf for the given query and dataset. 

the following API runs the Get Documents Vector service:

    - GET: /query-tfidf?query_term="LIST-QUERY-TERMS"&dataset="lifestyle-copus/wikir"

- **Get Proccessed Query**:

Gets the query after proccessing. 

the following API runs the Get Documents Vector service:

    - GET: /process_query?dataset="lifestyle-copus/wikir"&query="YOUR-QUERY"

- ## Evaluation:

The implemented evaluation metrics are **Precision@10**, **Recall**, **MRR** and **MAP**.

to run the evaluation just go to system_evaluation.py file and run it.


## Students

- [**Juman Dukmak**]((https://github.com/JumanDukmak))
- [**Hala Ali**](https://github.com/HALA-7)
- [**Bnan Balbaki**](https://github.com/BananBalbaki2002)
- [**Roaa Alaou**]
